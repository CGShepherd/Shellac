from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from generator.layout.preliminary_placement import build_preliminary_placement_baseline


def main() -> int:
    model = build_preliminary_placement_baseline()
    out = ROOT / "out" / "layout" / "preliminary_placement_baseline.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(model.to_dict(), indent=2), encoding="utf-8")
    accepted = sum(1 for item in model.proposals if item.accepted)
    print("Project Shellac preliminary real-footprint placement")
    print(f"Status: {model.status}")
    print(f"Board: {model.board_width_mm:.1f} x {model.board_depth_mm:.1f} mm")
    print(f"Coordinate proposals: {len(model.proposals)}")
    print(f"Auto-accepted proposals: {accepted}")
    print(f"Manual-review clusters: {len(model.manual_review_clusters)}")
    print(f"Panel/virtual exclusions: {len(model.excluded_refs)}")
    print(f"Wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
