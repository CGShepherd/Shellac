from __future__ import annotations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from generator.layout.placement_clusters import build_cluster_placement_baseline

OUT = ROOT / "out" / "layout"

def main() -> int:
    model = build_cluster_placement_baseline()
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / "cluster_placement_baseline.json"
    target.write_text(json.dumps(model.to_dict(), indent=2) + "\n", encoding="utf-8")
    print(f"{model.identifier} {model.revision}")
    print(f"Board envelope: {model.board_width_mm:.1f} x {model.board_depth_mm:.1f} mm")
    print(f"Component clusters: {len(model.clusters)}")
    print(f"Keepouts: {len(model.keepouts)}")
    print(f"Wrote {target}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
