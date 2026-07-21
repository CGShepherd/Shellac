from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from generator.dispatch import shellac_builder_registry
from generator.model.shellac import build_shellac_model
from generator.readiness import audit_project
from generator.kicad_erc import run_hierarchical_erc


def main() -> int:
    project = build_shellac_model()
    schematic = Path("out/kicad/ProjectShellac.kicad_sch")
    if not schematic.exists():
        raise SystemExit("Generated schematic not found; run build_shellac_from_model.py first.")
    erc_counts = run_hierarchical_erc(
        schematic, Path("out/kicad/ProjectShellac-erc.rpt")
    )
    audit = audit_project(
        project,
        shellac_builder_registry(),
        erc_violations=sum(erc_counts.values()),
        human_reviewable_block_ids={"SCH101", "SCH103", "SCH104", "SCH105", "SCH106", "SCH107", "SCH108", "SCH109"},
    )

    print("Project Shellac schematic-generation readiness audit")
    print()
    print(
        f"{'Block':<8} {'Components':>10} {'Wires':>8} {'Labels':>8} "
        f"{'CAD ready':>10} {'Reviewable':>11}"
    )
    print("-" * 64)

    for block in audit.blocks:
        print(
            f"{block.block_id:<8} {block.components:>10} {block.wires:>8} "
            f"{block.labels:>8} {('YES' if block.cad_ready else 'NO'):>10} "
            f"{('YES' if block.human_reviewable else 'NO'):>11}"
        )
        for blocker in block.blockers:
            print(f"  - {blocker}")

    print()
    print(
        "Root hierarchy: "
        f"{audit.hierarchical_sheets} sheets, "
        f"{audit.hierarchical_pins} pins, "
        f"{audit.cross_sheet_signals} cross-sheet signals"
    )
    print(f"Native KiCad ERC violations: {sum(erc_counts.values())}")
    print()
    print("Project-level blockers")
    for blocker in audit.project_blockers:
        print(f"- {blocker}")

    print()
    print(f"CAD-ready blocks: {audit.ready_blocks}/{len(audit.blocks)}")
    print(
        "Human-reviewable blocks: "
        f"{audit.human_reviewable_blocks}/{len(audit.blocks)}"
    )
    print(f"Gate 2A machine readiness: {'PASS' if audit.cad_ready else 'FAIL'}")
    print(
        "Gate 2B human-review readiness: "
        f"{'PASS' if audit.human_review_ready else 'FAIL'}"
    )

    # A failed readiness gate is the expected and useful result until the
    # pin-aware renderer and hierarchy are implemented. Return zero so this
    # report remains usable in the current build workflow.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
