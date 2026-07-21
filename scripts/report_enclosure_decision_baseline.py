from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from generator.mechanical.freeze import build_enclosure_decision_baseline

OUT = ROOT / "out" / "layout"


def main() -> int:
    decisions = build_enclosure_decision_baseline()
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "enclosure_decision_baseline.json"
    path.write_text(json.dumps([item.to_dict() for item in decisions], indent=2) + "\n", encoding="utf-8")
    print("G3-006 enclosure decision and carrier-plate freeze audit")
    for item in decisions:
        print(f"{item.role.value}: {item.status}; leading candidate={item.candidate_id}")
        for finding in item.gate_findings:
            print(f"  - {finding}")
    print("Wrote out/layout/enclosure_decision_baseline.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
