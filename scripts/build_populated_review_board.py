from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from generator.mechanical.populated_board import write_populated_board

OUT = ROOT / "out" / "pcb" / "ProjectShellac_Gate3A_Review.kicad_pcb"


def main() -> int:
    result = write_populated_board(OUT)
    print("Project Shellac G3-013 populated review board")
    print(f"Status: {result.status}")
    print(f"Footprints proposed: {result.footprint_count}")
    print(f"Auto-accepted: {result.accepted_count}")
    print(f"Manual review: {result.manual_review_count}")
    print(f"Routed items: {result.routing_count}")
    print(f"Manufacturing holes: {result.mounting_hole_count}")
    print(f"Wrote {result.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
