"""G3-018 detailed-placement readiness audit.

The audit closes what can be checked deterministically before KiCad human
review: board-edge clearance, conservative footprint-body overlap, courtyard
proximity, and the explicit manual-authority cluster gate.  It does not invent
mounting-hole or enclosure keep-outs while those mechanical datums remain
unfrozen.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum

from generator.layout.footprint_contract import build_footprint_contract
from generator.layout.preliminary_placement import (
    PlacementProposal,
    build_preliminary_placement_baseline,
    footprint_envelope,
)
from generator.mechanical.board_outline import build_provisional_outline_contract


class FindingSeverity(str, Enum):
    BLOCKER = "blocker"
    REVIEW = "review"


class FindingKind(str, Enum):
    BOARD_EDGE = "board_edge"
    BODY_OVERLAP = "body_overlap"
    COURTYARD_PROXIMITY = "courtyard_proximity"
    MANUAL_CLUSTER = "manual_cluster"
    MECHANICAL_DATUM = "mechanical_datum"


@dataclass(frozen=True, slots=True)
class PlacementFinding:
    severity: FindingSeverity
    kind: FindingKind
    refs: tuple[str, ...]
    cluster_ids: tuple[str, ...]
    detail: str


@dataclass(slots=True)
class DetailedPlacementReadiness:
    identifier: str
    revision: str
    status: str
    proposal_count: int
    accepted_proposal_count: int
    manual_review_cluster_count: int
    blocker_count: int
    review_count: int
    findings: list[PlacementFinding] = field(default_factory=list)
    unresolved_mechanical_inputs: list[str] = field(default_factory=list)
    invariants: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        payload = asdict(self)
        for finding in payload["findings"]:
            finding["severity"] = finding["severity"].value
            finding["kind"] = finding["kind"].value
        return payload


def _overlap(a: PlacementProposal, b: PlacementProposal, extra_a: float = 0.0, extra_b: float = 0.0) -> bool:
    return (
        abs(a.x_mm - b.x_mm) < (a.width_mm + b.width_mm) / 2.0 + extra_a + extra_b - 1e-9
        and abs(a.y_mm - b.y_mm) < (a.depth_mm + b.depth_mm) / 2.0 + extra_a + extra_b - 1e-9
    )


def build_detailed_placement_readiness(edge_clearance_mm: float = 5.0) -> DetailedPlacementReadiness:
    placement = build_preliminary_placement_baseline()
    contract = build_footprint_contract()
    outline = build_provisional_outline_contract(
        width_mm=placement.board_width_mm,
        depth_mm=placement.board_depth_mm,
    )
    entries = {entry.ref: entry for entry in contract.entries}
    findings: list[PlacementFinding] = []

    # KO-001 can be checked now because the provisional board outline and the
    # board-edge clearance are already part of the accepted layout contract.
    for proposal in placement.proposals:
        margin = footprint_envelope(entries[proposal.ref]).courtyard_margin_mm
        left = proposal.x_mm - proposal.width_mm / 2.0 - margin
        right = proposal.x_mm + proposal.width_mm / 2.0 + margin
        top = proposal.y_mm - proposal.depth_mm / 2.0 - margin
        bottom = proposal.y_mm + proposal.depth_mm / 2.0 + margin
        if (
            left < edge_clearance_mm
            or top < edge_clearance_mm
            or right > placement.board_width_mm - edge_clearance_mm
            or bottom > placement.board_depth_mm - edge_clearance_mm
        ):
            findings.append(PlacementFinding(
                FindingSeverity.BLOCKER,
                FindingKind.BOARD_EDGE,
                (proposal.ref,),
                (proposal.cluster_id,),
                f"Conservative envelope violates {edge_clearance_mm:.1f} mm board-edge clearance.",
            ))

    # Component bodies must never overlap. Courtyard proximity is kept as a
    # review finding because these dimensions are conservative approximations,
    # not parsed KiCad courtyard polygons.
    proposals = placement.proposals
    for index, a in enumerate(proposals):
        margin_a = footprint_envelope(entries[a.ref]).courtyard_margin_mm
        for b in proposals[index + 1:]:
            if _overlap(a, b):
                findings.append(PlacementFinding(
                    FindingSeverity.BLOCKER,
                    FindingKind.BODY_OVERLAP,
                    (a.ref, b.ref),
                    tuple(sorted({a.cluster_id, b.cluster_id})),
                    "Conservative footprint bodies overlap in the placement candidate.",
                ))
            elif _overlap(a, b, margin_a, footprint_envelope(entries[b.ref]).courtyard_margin_mm):
                findings.append(PlacementFinding(
                    FindingSeverity.REVIEW,
                    FindingKind.COURTYARD_PROXIMITY,
                    (a.ref, b.ref),
                    tuple(sorted({a.cluster_id, b.cluster_id})),
                    "Conservative courtyard envelopes touch or overlap; inspect in KiCad.",
                ))

    for cluster_id in placement.manual_review_clusters:
        refs = tuple(sorted(p.ref for p in proposals if p.cluster_id == cluster_id))
        findings.append(PlacementFinding(
            FindingSeverity.REVIEW,
            FindingKind.MANUAL_CLUSTER,
            refs,
            (cluster_id,),
            "Critical analogue/power cluster requires explicit human placement acceptance before routing.",
        ))

    # Mounting-hole and enclosure intrusion geometry is deliberately not
    # guessed. Surface the unresolved datum as one review item instead.
    if outline.unresolved_inputs:
        findings.append(PlacementFinding(
            FindingSeverity.REVIEW,
            FindingKind.MECHANICAL_DATUM,
            (),
            (),
            "Mounting-hole and enclosure keep-out checks remain unavailable until mechanical datums are frozen.",
        ))

    blocker_count = sum(f.severity is FindingSeverity.BLOCKER for f in findings)
    review_count = sum(f.severity is FindingSeverity.REVIEW for f in findings)
    status = "BLOCKED" if blocker_count else "HUMAN_REVIEW_REQUIRED" if review_count else "READY_FOR_ROUTING"
    return DetailedPlacementReadiness(
        identifier="G3-PLC-018",
        revision="Rev A0",
        status=status,
        proposal_count=len(proposals),
        accepted_proposal_count=sum(p.accepted for p in proposals),
        manual_review_cluster_count=len(placement.manual_review_clusters),
        blocker_count=blocker_count,
        review_count=review_count,
        findings=findings,
        unresolved_mechanical_inputs=list(outline.unresolved_inputs),
        invariants=[
            "Every PCB-owned component has exactly one deterministic placement proposal.",
            "No conservative footprint body overlap is permitted before routing review.",
            "KO-001 board-edge clearance is checked against conservative footprint envelopes.",
            "Critical analogue and power clusters retain explicit human placement authority.",
            "Unfrozen mounting-hole or enclosure geometry is reported, never guessed.",
        ],
    )
