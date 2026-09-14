from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import time
from pathlib import Path
from typing import Any

import yaml

from simulation.scripts.analytical_correlation import build_report
from simulation.scripts.shellac_spice import (
    ROOT,
    SIM,
    ToolchainError,
    build_command,
    find_ltspice,
    ltspice_version,
    render_template,
    sha256_file,
)


class LTCorrelationError(RuntimeError):
    pass


_NUMBER = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?"
_SCALAR_RESULT_RE = re.compile(
    rf"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*[^\r\n]*?=\s*({_NUMBER})\s*$",
    re.IGNORECASE | re.MULTILINE,
)
_COMPLEX_DB_RE = re.compile(
    rf"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*[^\r\n]*?=\(\s*({_NUMBER})\s*dB\s*,[^\r\n]*\)\s+at\s+{_NUMBER}\s*$",
    re.IGNORECASE | re.MULTILINE,
)
_WHEN_AT_RE = re.compile(
    rf"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*[^\r\n]*?\bAT\s+({_NUMBER})\s*$",
    re.IGNORECASE | re.MULTILINE,
)


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise LTCorrelationError(f"{path} did not contain a mapping")
    return data


def read_ltspice_text(path: Path) -> str:
    raw = path.read_bytes()
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        return raw.decode("utf-16")
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw.decode("utf-8-sig")
    if len(raw) >= 4 and raw[1::2].count(0) > max(2, len(raw) // 8):
        return raw.decode("utf-16-le")
    return raw.decode("utf-8", errors="replace")


def parse_correlation_measurements(text: str) -> dict[str, float]:
    values: dict[str, float] = {}
    for name, value in _SCALAR_RESULT_RE.findall(text):
        values[name.upper()] = float(value)
    return values


def extract_measurement(text: str, name: str, spec: dict[str, Any]) -> float:
    key = name.upper()
    extraction = spec.get("extraction", "scalar")
    if extraction == "scalar":
        values = parse_correlation_measurements(text)
        if key not in values:
            raise LTCorrelationError(f"{name}: scalar measurement not found")
        return values[key]
    if extraction == "when_at":
        for found_name, value in _WHEN_AT_RE.findall(text):
            if found_name.upper() == key:
                return float(value)
        raise LTCorrelationError(f"{name}: WHEN/AT measurement not found")
    if extraction == "complex_db":
        for found_name, value in _COMPLEX_DB_RE.findall(text):
            if found_name.upper() == key:
                return float(value)
        raise LTCorrelationError(f"{name}: LTspice complex dB measurement not found")
    raise LTCorrelationError(f"{name}: unsupported extraction mode {extraction!r}")


def _lookup_path(data: dict[str, Any], dotted: str) -> Any:
    cur: Any = data
    for part in dotted.split("."):
        cur = cur[part]
    return cur


def _analytical_value(spec: dict[str, Any], analytical: dict[str, Any]) -> float:
    if "analytical_path" in spec:
        return float(_lookup_path(analytical, spec["analytical_path"]))
    if "analytical_checkpoint_hz" in spec:
        target = float(spec["analytical_checkpoint_hz"])
        pts = analytical["cases"]["dr039_direct_rc"]["checkpoints"]
        for p in pts:
            if math.isclose(float(p["frequency_hz"]), target, abs_tol=1e-12):
                return float(p["magnitude_db"])
        raise LTCorrelationError(f"No analytical checkpoint for {target} Hz")
    if "analytical_stimulus" in spec:
        stimulus = spec["analytical_stimulus"]
        for s in analytical["cases"]["matrix_mono_average"]["stimuli"]:
            if s["name"] == stimulus:
                return float(s["output_v"])
        raise LTCorrelationError(f"No analytical matrix stimulus {stimulus}")
    raise LTCorrelationError(f"Measurement lacks analytical mapping: {spec}")


def _transform_actual(value: float, spec: dict[str, Any]) -> float:
    transform = spec.get("transform")
    if transform is None:
        return value
    if transform == "magnitude_to_db":
        if value <= 0.0:
            raise LTCorrelationError(f"Cannot convert non-positive magnitude {value} to dB")
        return 20.0 * math.log10(value)
    raise LTCorrelationError(f"Unsupported measurement transform: {transform}")


def prepare_case(case_id: str, spec: dict[str, Any]) -> Path:
    template_path = ROOT / spec["template"]
    generated = ROOT / spec["generated"]
    rendered = render_template(template_path.read_text(encoding="utf-8"), spec.get("parameters", {}))
    generated.parent.mkdir(parents=True, exist_ok=True)
    generated.write_text(rendered, encoding="utf-8", newline="\n")
    return generated


def _native_log_matches_netlist(native_text: str, netlist: Path) -> bool:
    normalized = native_text.replace("\\", "/").lower()
    target = str(netlist).replace("\\", "/").lower()
    return f"circuit: {target}" in normalized


def run_case(case_id: str, spec: dict[str, Any], exe: Path) -> dict[str, Any]:
    netlist = prepare_case(case_id, spec)
    log_path = ROOT / spec["log"]
    log_path.parent.mkdir(parents=True, exist_ok=True)
    command = build_command(exe, netlist)
    native_log = netlist.with_suffix(".log")

    attempts: list[dict[str, Any]] = []
    native_text = ""
    proc = None
    for attempt in (1, 2):
        if native_log.exists():
            native_log.unlink()
        proc = subprocess.run(command, cwd=netlist.parent, text=True, capture_output=True, check=False)
        time.sleep(0.15)
        native_text = read_ltspice_text(native_log) if native_log.is_file() else ""
        matches = _native_log_matches_netlist(native_text, netlist)
        transient_wrong_deck = "Could not open input deck for reading:" in native_text
        attempts.append({
            "attempt": attempt,
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "native_log_matches_netlist": matches,
            "transient_wrong_deck": transient_wrong_deck,
        })
        if proc.returncode == 0 and matches and not transient_wrong_deck:
            break
        if attempt == 1:
            time.sleep(0.35)

    assert proc is not None
    captured = f"COMMAND: {command!r}\nATTEMPTS: {attempts!r}\n"
    log_path.write_text(captured, encoding="utf-8")
    if native_text:
        with log_path.open("a", encoding="utf-8") as f:
            f.write("\nLTSPICE_NATIVE_LOG:\n")
            f.write(native_text)

    if proc.returncode != 0:
        raise LTCorrelationError(f"{case_id}: LTspice returned {proc.returncode}; see {log_path.relative_to(ROOT)}")
    if not _native_log_matches_netlist(native_text, netlist):
        raise LTCorrelationError(f"{case_id}: LTspice native log does not identify the requested netlist; see {log_path.relative_to(ROOT)}")
    if "Could not open input deck for reading:" in native_text:
        raise LTCorrelationError(f"{case_id}: LTspice failed to open the requested input deck; see {log_path.relative_to(ROOT)}")

    text = log_path.read_text(encoding="utf-8", errors="replace")
    measurements: dict[str, float] = {}
    missing: list[str] = []
    for metric, metric_spec in spec["measurements"].items():
        try:
            measurements[metric] = extract_measurement(text, metric, metric_spec)
        except LTCorrelationError:
            missing.append(metric)
    if missing:
        raise LTCorrelationError(f"{case_id}: missing measurements {missing}; see {log_path.relative_to(ROOT)}")
    return {"case_id": case_id, "netlist": netlist.relative_to(ROOT).as_posix(), "netlist_sha256": sha256_file(netlist), "measurements": measurements}


def compare_all() -> dict[str, Any]:
    cfg = load_yaml(SIM / "config" / "correlation_ltspice.yaml")
    analytical = build_report()
    exe = find_ltspice()
    if exe is None:
        raise LTCorrelationError("LTspice not found; set LTSPICE_EXE")
    result: dict[str, Any] = {"schema_version": 1, "authority": cfg["authority"], "simulator": "LTspice", "simulator_identity": ltspice_version(exe), "cases": {}, "pass": True}
    for case_id, spec in cfg["cases"].items():
        run = run_case(case_id, spec, exe)
        comparisons = {}
        case_pass = True
        for metric, metric_spec in spec["measurements"].items():
            raw_actual = float(run["measurements"][metric])
            actual = _transform_actual(raw_actual, metric_spec)
            expected = _analytical_value(metric_spec, analytical)
            delta = abs(actual - expected)
            tol = float(metric_spec["abs_tolerance"])
            passed = delta <= tol
            case_pass &= passed
            comparisons[metric] = {"ltspice_raw": raw_actual, "ltspice": actual, "analytical": expected, "absolute_delta": delta, "absolute_tolerance": tol, "pass": passed}
        run["comparisons"] = comparisons
        run["pass"] = case_pass
        result["cases"][case_id] = run
        result["pass"] &= case_pass
    out = SIM / "results" / "correlation" / "ltspice_vs_analytical.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def main(argv=None) -> int:
    argparse.ArgumentParser(description="Project Shellac LTspice versus analytical correlation").parse_args(argv)
    try:
        result = compare_all()
    except (LTCorrelationError, ToolchainError) as exc:
        print(f"ERROR: {exc}")
        return 2
    for case_id, case in result["cases"].items():
        print(f"{case_id}: {'PASS' if case['pass'] else 'FAIL'}")
        for metric, comp in case["comparisons"].items():
            print(f"  {metric}: LTspice={comp['ltspice']:.12g} analytical={comp['analytical']:.12g} delta={comp['absolute_delta']:.3g} tol={comp['absolute_tolerance']:.3g}")
    print(f"overall: {'PASS' if result['pass'] else 'FAIL'}")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
