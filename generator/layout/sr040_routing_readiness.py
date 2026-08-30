"""SR-040 routing-readiness gate using frozen mechanical datums."""
from __future__ import annotations
from dataclasses import asdict, dataclass, field

from generator.layout.preliminary_placement import build_preliminary_placement_baseline
from generator.mechanical.sr040_audio_freeze import frozen_audio_board_outline
from generator.procurement.full_bom_census import build_full_bom_census

@dataclass(slots=True)
class Sr040RoutingReadiness:
    identifier: str
    revision: str
    status: str
    mechanical_frozen: bool
    board_outline_frozen: bool
    mounting_hole_count: int
    manual_review_clusters: list[str] = field(default_factory=list)
    procurement_pending_count: int = 0
    blockers: list[str] = field(default_factory=list)
    next_actions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

def build_sr040_routing_readiness() -> Sr040RoutingReadiness:
    outline=frozen_audio_board_outline()
    placement=build_preliminary_placement_baseline(
        width_mm=outline.outline.width_mm,
        depth_mm=outline.outline.depth_mm,
    )
    census=build_full_bom_census()
    blockers=[]
    if placement.manual_review_clusters:
        blockers.append(
            "Critical analogue clusters require explicit human placement acceptance before routing."
        )
    if census.procurement_pending_count:
        blockers.append(
            "Full board population is identified, but manufacturer MPN freeze remains open for generic passives and selected standard parts."
        )
    return Sr040RoutingReadiness(
        identifier="SR-040-ROUTING-READINESS",
        revision="Rev A0",
        status="MECHANICAL_FROZEN__CRITICAL_PLACEMENT_REVIEW_REQUIRED",
        mechanical_frozen=True,
        board_outline_frozen=True,
        mounting_hole_count=len(outline.mounting_holes),
        manual_review_clusters=list(placement.manual_review_clusters),
        procurement_pending_count=census.procurement_pending_count,
        blockers=blockers,
        next_actions=[
            "Generate and inspect the critical-cluster placement report in KiCad.",
            "Accept or amend SCH101/SCH103/SCH107/SCH108 manual-authority cluster coordinates.",
            "Freeze generic passive manufacturer series/MPNs as a procurement catalogue, without altering electrical values or footprints.",
            "After critical placement acceptance, release routing immediately.",
        ],
    )
