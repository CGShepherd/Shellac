from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from generator.kicad_erc import run_hierarchical_erc


def main() -> int:
    schematic = Path("out/kicad/ProjectShellac.kicad_sch")
    report = Path("out/kicad/ProjectShellac-erc.rpt")
    if not schematic.exists():
        raise SystemExit("Generated schematic not found; run build_shellac_from_model.py first.")
    counts = run_hierarchical_erc(schematic, report)
    print("Project Shellac native KiCad hierarchical ERC")
    print(f"Violations: {sum(counts.values())}")
    for name, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        print(f"- {name}: {count}")
    print(f"Wrote {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
