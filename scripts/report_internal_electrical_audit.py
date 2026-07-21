from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from generator.core.sheet import Sheet
from generator.dispatch import shellac_builder_registry
from generator.electrical_audit import audit_sheet_electrical
from generator.model.shellac import build_shellac_model


def main() -> int:
    model = build_shellac_model()
    registry = shellac_builder_registry()
    failed = 0
    print("Project Shellac internal electrical-integrity audit")
    print()
    print(f"{'Block':<8} {'Grid':>6} {'Pins':>6} {'Nets':>6} {'Zero':>6} {'Result':>8}")
    print("-" * 50)
    for block in model.blocks:
        sheet = Sheet(block.name, f"{block.identifier}.kicad_sch")
        registry.resolve(block.identifier).builder(sheet)
        audit = audit_sheet_electrical(sheet)
        result = "PASS" if audit.passed else "FAIL"
        failed += not audit.passed
        print(
            f"{block.identifier:<8} {len(audit.off_grid_items):>6} "
            f"{len(audit.unterminated_pins):>6} "
            f"{len(audit.net_name_conflicts):>6} "
            f"{audit.zero_length_wires:>6} {result:>8}"
        )
        for issue in audit.off_grid_items:
            print(f"  - off-grid: {issue}")
        for issue in audit.unterminated_pins:
            print(f"  - unterminated: {issue.reference}.{issue.pin_name} at {issue.point}")
        for issue in audit.net_name_conflicts:
            print(f"  - merged labels: {', '.join(issue.names)}")
    print()
    print(f"Internal electrical-integrity gate: {'PASS' if not failed else 'FAIL'}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
