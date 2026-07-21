"""Report the Gate 3 board-outline synthesis contract."""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from generator.mechanical.board_outline import build_provisional_outline_contract

OUT = ROOT / "out" / "layout" / "board_outline_baseline.json"


def main() -> int:
    contract = build_provisional_outline_contract()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(contract.to_dict(), indent=2) + "\n", encoding="utf-8")
    print("Project Shellac board-outline synthesis interface")
    print(f"Status: {contract.status.value}")
    print(f"Provisional board: {contract.outline.width_mm:.1f} x {contract.outline.depth_mm:.1f} mm")
    print(f"Manufacturing holes emitted: {len(contract.mounting_holes)}")
    print(f"Unresolved enclosure inputs: {len(contract.unresolved_inputs)}")
    print(f"Wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
