from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
SIM = ROOT / "simulation"


class CorrelationError(RuntimeError):
    pass


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise CorrelationError(f"{path} did not contain a mapping")
    return data


def high_pass_fc(r_ohm: float, c_f: float) -> float:
    return 1.0 / (2.0 * math.pi * r_ohm * c_f)


def high_pass_mag_db(f_hz: float, r_ohm: float, c_f: float) -> float:
    x = 2.0 * math.pi * f_hz * r_ohm * c_f
    mag = x / math.sqrt(1.0 + x * x)
    return 20.0 * math.log10(mag)


def gain_db(voltage_gain: float) -> float:
    return 20.0 * math.log10(voltage_gain)


def equal_resistor_average(left_v: float, right_v: float, r_left: float, r_right: float) -> float:
    if r_left <= 0 or r_right <= 0:
        raise CorrelationError("Averaging resistors must be positive")
    conductance_sum = 1.0 / r_left + 1.0 / r_right
    return (left_v / r_left + right_v / r_right) / conductance_sum


def build_report() -> dict[str, Any]:
    cfg = load_yaml(SIM / "config" / "correlation.yaml")
    out: dict[str, Any] = {
        "schema_version": 1,
        "authority": cfg["authority"],
        "cases": {},
    }

    for case_id, case in cfg["cases"].items():
        kind = case["kind"]
        if kind == "high_pass_rc":
            r = float(case["resistance_ohm"])
            c = float(case["capacitance_f"])
            out["cases"][case_id] = {
                "description": case["description"],
                "kind": kind,
                "corner_hz": high_pass_fc(r, c),
                "checkpoints": [
                    {"frequency_hz": float(f), "magnitude_db": high_pass_mag_db(float(f), r, c)}
                    for f in case["checkpoints_hz"]
                ],
            }
        elif kind == "fixed_gain_db":
            gain = float(case["voltage_gain"])
            out["cases"][case_id] = {
                "description": case["description"],
                "kind": kind,
                "voltage_gain": gain,
                "gain_db": gain_db(gain),
            }
        elif kind == "equal_resistor_average":
            rl = float(case["resistor_left_ohm"])
            rr = float(case["resistor_right_ohm"])
            out["cases"][case_id] = {
                "description": case["description"],
                "kind": kind,
                "resistor_left_ohm": rl,
                "resistor_right_ohm": rr,
                "stimuli": [
                    {
                        "name": s["name"],
                        "left_v": float(s["left_v"]),
                        "right_v": float(s["right_v"]),
                        "output_v": equal_resistor_average(
                            float(s["left_v"]), float(s["right_v"]), rl, rr
                        ),
                    }
                    for s in case["stimuli"]
                ],
            }
        else:
            raise CorrelationError(f"Unsupported correlation kind: {kind}")

    return out


def write_outputs(report: dict[str, Any]) -> tuple[Path, Path]:
    out_dir = SIM / "results" / "correlation"
    out_dir.mkdir(parents=True, exist_ok=True)

    json_path = out_dir / "analytical_correlation.json"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    csv_path = out_dir / "analytical_correlation.csv"
    rows = []

    rc = report["cases"]["dr039_direct_rc"]
    rows.append({
        "CASE": "dr039_direct_rc",
        "METRIC": "corner_hz",
        "X": "",
        "VALUE": rc["corner_hz"],
        "UNIT": "Hz",
    })
    for p in rc["checkpoints"]:
        rows.append({
            "CASE": "dr039_direct_rc",
            "METRIC": "magnitude_db",
            "X": p["frequency_hz"],
            "VALUE": p["magnitude_db"],
            "UNIT": "dB",
        })

    gain = report["cases"]["sch101_nominal_gain"]
    rows.append({
        "CASE": "sch101_nominal_gain",
        "METRIC": "gain_db",
        "X": gain["voltage_gain"],
        "VALUE": gain["gain_db"],
        "UNIT": "dB",
    })

    matrix = report["cases"]["matrix_mono_average"]
    for s in matrix["stimuli"]:
        rows.append({
            "CASE": "matrix_mono_average",
            "METRIC": s["name"],
            "X": f"{s['left_v']},{s['right_v']}",
            "VALUE": s["output_v"],
            "UNIT": "V/V",
        })

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["CASE", "METRIC", "X", "VALUE", "UNIT"])
        writer.writeheader()
        writer.writerows(rows)

    return json_path, csv_path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Project Shellac analytical correlation generator")
    parser.parse_args(argv)
    report = build_report()
    jp, cp = write_outputs(report)
    print(jp.relative_to(ROOT))
    print(cp.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
