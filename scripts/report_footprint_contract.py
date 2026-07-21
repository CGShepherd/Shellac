from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from generator.layout.footprint_contract import build_footprint_contract, validate_footprint_contract

OUT = Path("out/layout/footprint_contract.json")


def main() -> int:
    contract = build_footprint_contract()
    issues = validate_footprint_contract(contract)
    if issues:
        print("Footprint contract: FAIL")
        for issue in issues:
            print(f"- {issue}")
        return 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(contract.to_dict(), indent=2) + "\n", encoding="utf-8")
    print("Project Shellac G3-009 footprint contract")
    print(f"Status: {contract.status}")
    print(f"Approved PCB population: {len(contract.board_population_refs)}")
    print(f"Panel/virtual exclusions: {len(contract.panel_interface_refs)}")
    print(f"Mechanical ECO blockers: {len(contract.mechanical_eco_refs)}")
    for blocker in contract.freeze_blockers:
        print(f"- {blocker}")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
