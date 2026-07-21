from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from generator.layout.real_footprint_audit import (
    build_real_footprint_audit,
    validate_real_footprint_audit,
)

OUT = ROOT / "out" / "layout" / "real_footprint_audit.json"


def main() -> int:
    audit = build_real_footprint_audit()
    issues = validate_real_footprint_audit(audit)
    if issues:
        print("Real-footprint audit: FAIL")
        for issue in issues:
            print(f"- {issue}")
        return 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(audit.to_dict(), indent=2) + "\n", encoding="utf-8")
    print("Project Shellac G3-016 real-footprint audit")
    print(f"Status: {audit.status}")
    print(f"PCB-owned references: {audit.board_population_count}")
    print(f"Accepted footprint identities: {audit.accepted_identity_count}")
    print(f"Review required: {audit.review_count}")
    print(f"ECO blockers: {audit.blocker_count}")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
