from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from generator.mechanical import build_mechanical_baseline, build_placement_synthesis, evaluate_candidate

OUT = ROOT / "out" / "layout"


def main() -> int:
    mechanical = build_mechanical_baseline()
    placement = build_placement_synthesis()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "mechanical_baseline.json").write_text(json.dumps(mechanical.to_dict(), indent=2) + "\n", encoding="utf-8")
    (OUT / "placement_synthesis.json").write_text(json.dumps(placement.to_dict(), indent=2) + "\n", encoding="utf-8")

    print(f"{mechanical.identifier} {mechanical.revision}")
    print(mechanical.status)
    print(f"Audio hard gates: {len(mechanical.audio_requirement.hard_gates)}")
    print(f"PSU hard gates: {len(mechanical.psu_requirement.hard_gates)}")
    print("\nCandidate decision matrix")
    print("ID       Role   Status         Score  Gate findings")
    print("-" * 78)
    for candidate in mechanical.candidates:
        requirement = mechanical.audio_requirement if candidate.role.value == "audio" else mechanical.psu_requirement
        failures = evaluate_candidate(candidate, requirement)
        finding = "; ".join(failures) if failures else "passes current dimensional/access gates"
        print(f"{candidate.identifier:<8} {candidate.role.value:<6} {candidate.status.value:<14} {candidate.weighted_score:>5}  {finding}")

    print("\nPreliminary placement")
    for region in sorted(placement.regions, key=lambda item: item.sequence):
        print(f"{region.identifier} {region.name}: x={region.x_mm:.1f}, y={region.y_mm:.1f}, w={region.width_mm:.1f}, d={region.depth_mm:.1f} mm")
    print("\nWrote out/layout/mechanical_baseline.json")
    print("Wrote out/layout/placement_synthesis.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
