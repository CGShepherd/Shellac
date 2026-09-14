from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
SIM = ROOT / "simulation"


class ToolchainError(RuntimeError):
    pass


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ToolchainError(f"{path} did not contain a mapping")
    return data


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return "UNKNOWN"


def find_ltspice() -> Path | None:
    cfg = load_yaml(SIM / "config" / "toolchain.yaml")
    env_name = cfg["executable_environment_variable"]
    env_value = os.environ.get(env_name)
    if env_value:
        path = Path(env_value).expanduser()
        if path.is_file():
            return path.resolve()
        raise ToolchainError(f"{env_name} points to a missing file: {path}")

    for candidate in cfg.get("windows_candidates", []):
        path = Path(candidate)
        if path.is_file():
            return path.resolve()

    for name in ("LTspice", "LTspice.exe", "XVIIx64.exe", "XVIIx86.exe"):
        found = shutil.which(name)
        if found:
            return Path(found).resolve()
    return None


def ltspice_version(exe: Path) -> str:
    # LTspice generations do not expose a single stable CLI version flag.
    # File metadata would require platform-specific APIs; record executable
    # identity/hash here and allow the operator to capture GUI version separately.
    try:
        return f"{exe.name}; sha256={sha256_file(exe)}"
    except OSError:
        return exe.name


def render_template(template: str, parameters: dict[str, Any]) -> str:
    rendered = template
    for key, value in parameters.items():
        token = "{{" + key + "}}"
        if token not in rendered:
            raise ToolchainError(f"RUN configuration parameter {key} is unused by template")
        rendered = rendered.replace(token, str(value))
    leftovers = re.findall(r"\{\{[A-Za-z0-9_]+\}\}", rendered)
    if leftovers:
        raise ToolchainError(f"Unresolved template parameters: {sorted(set(leftovers))}")
    return rendered


def run_config(run_id: str) -> dict[str, Any]:
    if run_id.upper() != "RUN00":
        raise ToolchainError("Stage 1 implements RUN00 only")
    return load_yaml(SIM / "config" / "run00.yaml")


def prepare(run_id: str) -> Path:
    cfg = run_config(run_id)
    template_path = ROOT / cfg["netlist_template"]
    output_path = ROOT / cfg["generated_netlist"]
    text = template_path.read_text(encoding="utf-8")
    rendered = render_template(text, cfg.get("parameters", {}))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8", newline="\n")
    return output_path


def build_command(exe: Path, netlist: Path) -> list[str]:
    cfg = load_yaml(SIM / "config" / "toolchain.yaml")
    args = [str(x).replace("{netlist}", str(netlist)) for x in cfg["batch_arguments"]]
    return [str(exe), *args]


_MEAS_RE = re.compile(
    r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*(?::|=)\s*"
    r"([-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)",
    re.MULTILINE,
)


def parse_measurements(text: str) -> dict[str, float]:
    return {name.upper(): float(value) for name, value in _MEAS_RE.findall(text)}


def evaluate(value: float, criterion: dict[str, Any]) -> tuple[bool, str]:
    kind = criterion["kind"]
    if kind == "range":
        lo, hi = float(criterion["minimum"]), float(criterion["maximum"])
        return lo <= value <= hi, f"{lo} <= x <= {hi}"
    if kind == "absolute_max":
        limit = float(criterion["maximum_abs"])
        return abs(value) <= limit, f"|x| <= {limit}"
    raise ToolchainError(f"Unsupported acceptance criterion kind: {kind}")


def write_measurement_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "RUN_ID", "MODEL_REV", "SIMULATOR", "SIM_VERSION", "DATE",
        "MEASURED_METRIC", "MEASURED_VALUE", "UNIT",
        "ACCEPTANCE_LIMIT", "PASS_FAIL", "NOTES",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def manifest() -> Path:
    sources = load_yaml(SIM / "manifests" / "model_sources.yaml")
    paths: list[Path] = []
    for section in ("reference_models", "project_models"):
        for item in sources.get(section, []):
            paths.append(ROOT / item["path"])
    # Templates/config are also execution inputs.
    paths.extend([
        SIM / "runs" / "run00_sanity" / "run00_sanity.cir.in",
        SIM / "config" / "run00.yaml",
        SIM / "config" / "acceptance.yaml",
        SIM / "config" / "toolchain.yaml",
    ])
    entries = []
    for path in paths:
        if not path.is_file():
            raise ToolchainError(f"Manifest input missing: {path.relative_to(ROOT)}")
        entries.append({
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": sha256_file(path),
            "bytes": path.stat().st_size,
        })
    payload = {
        "schema_version": 1,
        "authority": "AE-053",
        "repository_commit": _git_commit(),
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "files": sorted(entries, key=lambda x: x["path"]),
    }
    out = SIM / "manifests" / "model_manifest.json"
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return out


def doctor() -> int:
    print(f"Repository: {ROOT}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"PyYAML: {yaml.__version__}")
    print(f"Git commit: {_git_commit()}")
    exe = find_ltspice()
    if exe is None:
        print("LTspice: NOT FOUND")
        print("Set LTSPICE_EXE to the full LTspice executable path.")
        return 2
    print(f"LTspice: {exe}")
    print(f"LTspice identity: {ltspice_version(exe)}")
    return 0


def run(run_id: str) -> int:
    cfg = run_config(run_id)
    exe = find_ltspice()
    if exe is None:
        raise ToolchainError("LTspice not found; set LTSPICE_EXE")
    netlist = prepare(run_id)
    log_path = ROOT / cfg["log_file"]
    log_path.parent.mkdir(parents=True, exist_ok=True)

    command = build_command(exe, netlist)
    proc = subprocess.run(
        command,
        cwd=netlist.parent,
        text=True,
        capture_output=True,
        check=False,
    )
    captured = (
        f"COMMAND: {command!r}\n"
        f"RETURN_CODE: {proc.returncode}\n"
        f"STDOUT:\n{proc.stdout}\n"
        f"STDERR:\n{proc.stderr}\n"
    )
    log_path.write_text(captured, encoding="utf-8")

    # LTspice commonly writes a sibling .log file. Preserve/copy it into controlled logs.
    native_log = netlist.with_suffix(".log")
    if native_log.is_file():
        native_text = native_log.read_text(encoding="utf-8", errors="replace")
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write("\nLTSPICE_NATIVE_LOG:\n")
            handle.write(native_text)

    if proc.returncode != 0:
        raise ToolchainError(f"LTspice returned {proc.returncode}; see {log_path.relative_to(ROOT)}")

    combined = log_path.read_text(encoding="utf-8", errors="replace")
    measurements = parse_measurements(combined)
    acceptance = load_yaml(SIM / "config" / "acceptance.yaml")["criteria"]
    expected = cfg["expected_measurements"]
    missing = sorted(set(expected) - set(measurements))
    if missing:
        raise ToolchainError(f"Missing RUN00 measurements: {missing}; see {log_path.relative_to(ROOT)}")

    now = datetime.now(timezone.utc).isoformat()
    sim_identity = ltspice_version(exe)
    rows = []
    all_pass = True
    for name, spec in expected.items():
        value = measurements[name]
        criterion_name = spec["criterion"]
        passed, limit_text = evaluate(value, acceptance[criterion_name])
        all_pass &= passed
        rows.append({
            "RUN_ID": cfg["run_id"],
            "MODEL_REV": _git_commit(),
            "SIMULATOR": "LTspice",
            "SIM_VERSION": sim_identity,
            "DATE": now,
            "MEASURED_METRIC": name,
            "MEASURED_VALUE": value,
            "UNIT": spec["unit"],
            "ACCEPTANCE_LIMIT": limit_text,
            "PASS_FAIL": "PASS" if passed else "FAIL",
            "NOTES": f"criterion={criterion_name}",
        })

    csv_path = ROOT / cfg["measurement_csv"]
    write_measurement_csv(csv_path, rows)
    result_path = ROOT / cfg["result_file"]
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result = {
        "schema_version": 1,
        "run_id": cfg["run_id"],
        "authority": cfg["authority"],
        "repository_commit": _git_commit(),
        "simulator": "LTspice",
        "simulator_identity": sim_identity,
        "command": command,
        "netlist_sha256": sha256_file(netlist),
        "model_manifest_sha256": sha256_file(manifest()),
        "measurements": measurements,
        "pass": all_pass,
        "timestamp_utc": now,
    }
    result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"{cfg['run_id']}: {'PASS' if all_pass else 'FAIL'}")
    print(f"Result: {result_path.relative_to(ROOT)}")
    return 0 if all_pass else 1


def verify(run_id: str) -> int:
    cfg = run_config(run_id)
    result_path = ROOT / cfg["result_file"]
    if not result_path.is_file():
        raise ToolchainError(f"No result exists for {run_id}; run it first")
    first = json.loads(result_path.read_text(encoding="utf-8"))
    first_values = first["measurements"]
    rc = run(run_id)
    if rc != 0:
        return rc
    second = json.loads(result_path.read_text(encoding="utf-8"))
    second_values = second["measurements"]
    tol = float(cfg["determinism"]["absolute_tolerance"])
    keys = sorted(set(first_values) | set(second_values))
    deltas = {k: abs(float(first_values[k]) - float(second_values[k])) for k in keys}
    worst = max(deltas.values(), default=0.0)
    print(f"Determinism worst absolute delta: {worst}")
    if worst > tol:
        raise ToolchainError(f"Non-reproducible RUN00: {worst} > {tol}")
    print("Determinism: PASS")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Project Shellac controlled LTspice/Python toolchain")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor")
    sub.add_parser("manifest")
    for name in ("prepare", "run", "verify"):
        p = sub.add_parser(name)
        p.add_argument("run_id")
    args = parser.parse_args(argv)
    try:
        if args.command == "doctor":
            return doctor()
        if args.command == "manifest":
            print(manifest().relative_to(ROOT))
            return 0
        if args.command == "prepare":
            print(prepare(args.run_id).relative_to(ROOT))
            return 0
        if args.command == "run":
            return run(args.run_id)
        if args.command == "verify":
            return verify(args.run_id)
        raise AssertionError(args.command)
    except ToolchainError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
