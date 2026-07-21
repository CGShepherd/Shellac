from __future__ import annotations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from generator.layout.performance import build_performance_baseline


def main() -> int:
    baseline = build_performance_baseline()
    print(f"{baseline.identifier} — {baseline.revision}")
    print(baseline.status)
    print("\nSCH101 selectable-gain budget at 5 mV RMS cartridge input")
    print(f"{'Setting':<10} {'Gain/x':>10} {'Gain/dB':>10} {'Output/mV':>12} {'Output/dBV':>12}")
    for row in baseline.gain_settings:
        print(f"{row.name:<10} {row.input_stage_gain_linear:>10.4f} {row.input_stage_gain_db:>10.3f} "
              f"{row.nominal_5mv_output_rms_v*1000:>12.3f} {row.nominal_5mv_output_dbv:>12.3f}")
    print("\nDesign margins")
    for row in baseline.margins:
        db = "n/a" if row.margin_db is None else f"{row.margin_db:.2f} dB"
        print(f"- {row.identifier}: {row.parameter}: x{row.margin_ratio:.3f} ({db}) [{row.status.value}]")
    print(f"\nCriticality records: {len(baseline.criticality)}")
    print(f"Placement constraints: {len(baseline.placement_constraints)}")
    print(f"Open measurements: {len(baseline.open_measurements)}")

    out = ROOT / "out" / "layout"
    out.mkdir(parents=True, exist_ok=True)
    path = out / "performance_baseline.json"
    path.write_text(json.dumps(baseline.to_dict(), indent=2), encoding="utf-8")
    print(f"\nWrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
