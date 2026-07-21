from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from generator.layout.kicad_native_pipeline import write_kicad_native_pipeline_baseline


def main() -> int:
    out = ROOT / "out" / "layout" / "kicad_native_pipeline.json"
    baseline = write_kicad_native_pipeline_baseline(out)
    print("Project Shellac KiCad-native PCB pipeline")
    print(f"Status: {baseline.status}")
    print(f"PCB owner: {baseline.pcb_owner}")
    print(f"Placement intent items: {baseline.footprint_count}")
    print(f"Accepted / review: {baseline.accepted_count} / {baseline.review_count}")
    print(f"Manufacturing holes frozen: {baseline.manufacturing_holes_frozen}")
    print(f"Wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
