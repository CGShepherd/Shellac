from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from generator.mechanical.board_skeleton import write_board_skeleton


OUT = ROOT / "out" / "pcb" / "ProjectShellac_Provisional.kicad_pcb"


def main() -> int:
    result = write_board_skeleton(OUT)
    print("Project Shellac provisional KiCad PCB skeleton")
    print(f"State: {result.state}")
    print(f"Outline: {result.outline_width_mm:.1f} x {result.outline_depth_mm:.1f} mm")
    print(f"Placement regions: {result.region_count}")
    print(f"Manufacturing mounting holes: {result.mounting_hole_count}")
    print(f"Wrote {result.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
