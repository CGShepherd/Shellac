from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from generator.layout.detailed_placement_readiness import build_detailed_placement_readiness


def main() -> int:
    model = build_detailed_placement_readiness()
    out = ROOT / "out" / "layout" / "detailed_placement_readiness.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(model.to_dict(), indent=2), encoding="utf-8")
    print("Project Shellac detailed-placement readiness")
    print(f"Status: {model.status}")
    print(f"Placement proposals: {model.proposal_count}")
    print(f"Auto-accepted proposals: {model.accepted_proposal_count}")
    print(f"Manual-review clusters: {model.manual_review_cluster_count}")
    print(f"Blockers: {model.blocker_count}")
    print(f"Review findings: {model.review_count}")
    print(f"Unresolved mechanical inputs: {len(model.unresolved_mechanical_inputs)}")
    print(f"Wrote {out.relative_to(ROOT)}")
    return 1 if model.blocker_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
