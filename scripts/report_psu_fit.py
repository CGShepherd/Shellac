#!/usr/bin/env python3
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from generator.mechanical.psu_fit import build_psu_fit_closure, validate_psu_fit_closure


def main() -> int:
    model = build_psu_fit_closure()
    issues = validate_psu_fit_closure(model)
    print(f"{model.identifier} {model.revision}")
    print(f"PSU: {model.enclosure_order_code} {model.state.value}")
    print(f"Validation issues: {len(issues)}")
    print(f"Release blockers: {len(model.release_blockers)}")
    print(f"Internal envelope: {model.floor.width_mm:g} x {model.floor.depth_mm:g} x {model.floor.usable_height_mm:g} mm")
    print(f"Known overlay: {model.side_by_side_fit.occupied_width_mm:g} x {model.side_by_side_fit.occupied_depth_mm:g} mm")
    for finding in model.findings:
        print(f"- {finding}")
    for blocker in model.release_blockers:
        print(f"OPEN: {blocker}")
    out = ROOT / "out/mechanical/psu_fit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(model.to_dict(), indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
