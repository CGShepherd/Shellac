from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from generator.build_provenance import verify_generated_project

OUT = Path("out/kicad")


def main() -> int:
    provenance = verify_generated_project(OUT)
    print("Generated KiCad project provenance: PASS")
    print(f"Build ID: {provenance['build_id']}")
    print(f"Verified immutable files: {len(provenance['files'])}")
    mutable_changes = provenance.get('mutable_changes', [])
    if mutable_changes:
        print('Mutable KiCad project files changed after generation: ' + ', '.join(mutable_changes))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
