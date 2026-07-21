from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from generator.layout.ghost_placement import build_ghost_placement_baseline

OUT = ROOT / "out" / "layout" / "ghost_placement_baseline.json"


def main() -> int:
    model = build_ghost_placement_baseline()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(model.to_dict(), indent=2) + "\n", encoding="utf-8")
    print("Project Shellac G3-011 ghost placement: PASS")
    print(f"Board: {model.board_width_mm:.1f} x {model.board_depth_mm:.1f} mm")
    print(f"Ghost clusters: {len(model.clusters)}")
    print(f"Status: {model.status}")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
