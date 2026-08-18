"""G3-012 preliminary real-footprint placement synthesis.

This module converts the accepted ghost-cluster envelopes and footprint
contract into deterministic, reviewable component-coordinate proposals.  It
is deliberately non-manufacturing: critical analogue clusters remain under
manual authority, enclosure-dependent mounting geometry is unresolved, and no
proposal is accepted merely because it has a coordinate.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import ceil

from generator.layout.footprint_contract import (
    FootprintEntry,
    PopulationStatus,
    build_footprint_contract,
)
from generator.layout.ghost_placement import (
    GhostCluster,
    build_ghost_placement_baseline,
)
from generator.layout.placement_clusters import build_cluster_placement_baseline


@dataclass(frozen=True, slots=True)
class FootprintEnvelope:
    width_mm: float
    depth_mm: float
    courtyard_margin_mm: float


@dataclass(frozen=True, slots=True)
class PlacementProposal:
    ref: str
    sheet_id: str
    cluster_id: str
    footprint: str
    x_mm: float
    y_mm: float
    rotation_deg: float
    width_mm: float
    depth_mm: float
    accepted: bool
    placement_authority: str
    rationale: str


@dataclass(slots=True)
class PreliminaryPlacementBaseline:
    identifier: str
    revision: str
    status: str
    board_width_mm: float
    board_depth_mm: float
    proposals: list[PlacementProposal] = field(default_factory=list)
    excluded_refs: list[str] = field(default_factory=list)
    manual_review_clusters: list[str] = field(default_factory=list)
    invariants: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


# Conservative body/courtyard approximations sufficient for architectural
# placement review. Exact KiCad courtyard geometry is deferred to the board
# population/export stage.
_FOOTPRINT_HINTS: tuple[tuple[str, FootprintEnvelope], ...] = (
    ("SOIC-8_3.9x4.9", FootprintEnvelope(6.0, 7.0, 0.5)),
    ("R_0805", FootprintEnvelope(3.2, 2.4, 0.4)),
    ("CP_Radial_D10.0mm_P5.00mm", FootprintEnvelope(11.0, 11.0, 0.5)),
    ("C_1206", FootprintEnvelope(4.2, 3.2, 0.4)),
    ("C_0805", FootprintEnvelope(3.2, 2.4, 0.4)),
    ("SOD-123", FootprintEnvelope(4.6, 2.8, 0.4)),
    ("SMA", FootprintEnvelope(5.8, 3.8, 0.5)),
    ("TestPoint_Pad_D1.5", FootprintEnvelope(3.0, 3.0, 0.8)),
    ("JST_VH_B3P", FootprintEnvelope(13.0, 9.0, 1.0)),
    ("Mini-Fit_Jr_5566-06A2", FootprintEnvelope(14.0, 12.0, 1.0)),
    ("SW_DIP", FootprintEnvelope(12.0, 10.0, 1.0)),
    ("PinHeader", FootprintEnvelope(10.0, 6.0, 0.8)),
)


def footprint_envelope(entry: FootprintEntry) -> FootprintEnvelope:
    for token, envelope in _FOOTPRINT_HINTS:
        if token in entry.footprint:
            return envelope
    if entry.package_family == "resistor":
        return FootprintEnvelope(3.2, 2.4, 0.4)
    if entry.package_family == "capacitor":
        return FootprintEnvelope(3.2, 2.4, 0.4)
    if entry.package_family == "test_point":
        return FootprintEnvelope(3.0, 3.0, 0.8)
    return FootprintEnvelope(7.0, 7.0, 0.8)



# G3-019 invalidates the former left-edge CLU-106 macro coordinates.
# The rear-centre DC-entry cluster now uses the same deterministic reviewed
# packer as other manual-authority clusters until exact enclosure/connector
# datums are frozen.
def _proposal_rotation(entry: FootprintEntry, cluster: GhostCluster) -> float:
    if entry.ref.startswith("H"):
        return 90.0 if cluster.harness_edge in {"front", "rear"} else 0.0
    if entry.ref.startswith("TP"):
        return 0.0
    # Signal-flow orientation: long passives predominantly horizontal.
    if entry.package_family in {"0805", "resistor", "capacitor"}:
        return 0.0
    return 0.0


def _pack_cluster(
    ghost: GhostCluster,
    entries: list[FootprintEntry],
) -> list[PlacementProposal]:
    if not entries:
        return []

    margin = max(1.5, ghost.keepout_mm / 2.0)
    usable_w = max(ghost.width_mm - 2 * margin, 1.0)
    usable_d = max(ghost.depth_mm - 2 * margin, 1.0)
    max_w = max(footprint_envelope(e).width_mm for e in entries)
    max_d = max(footprint_envelope(e).depth_mm for e in entries)
    pitch_x = max_w + 1.2
    pitch_y = max_d + 1.2
    columns = max(1, min(len(entries), int(usable_w // pitch_x)))
    rows = ceil(len(entries) / columns)
    if rows * pitch_y > usable_d:
        # Architectural placement may be dense; distribute uniformly while
        # retaining deterministic ordering. Overlap is reported by validation.
        pitch_y = usable_d / max(rows, 1)
    if columns * pitch_x > usable_w:
        pitch_x = usable_w / max(columns, 1)

    proposals: list[PlacementProposal] = []
    ordered = sorted(entries, key=lambda item: (
        0 if item.ref in ghost.anchor_refs else 1,
        0 if item.ref.startswith("U") else 1,
        item.ref,
    ))
    for index, entry in enumerate(ordered):
        row, col = divmod(index, columns)
        envelope = footprint_envelope(entry)
        x = ghost.x_mm + margin + (col + 0.5) * pitch_x
        y = ghost.y_mm + margin + (row + 0.5) * pitch_y
        rotation = _proposal_rotation(entry, ghost)
        accepted = not ghost.manual_authority
        proposals.append(PlacementProposal(
            ref=entry.ref,
            sheet_id=entry.sheet_id,
            cluster_id=ghost.identifier,
            footprint=entry.footprint,
            x_mm=round(x, 3),
            y_mm=round(y, 3),
            rotation_deg=rotation,
            width_mm=envelope.width_mm,
            depth_mm=envelope.depth_mm,
            accepted=accepted,
            placement_authority=("manual_review" if ghost.manual_authority else "synthesised_review"),
            rationale=(
                "Coordinate proposal only; critical cluster requires Gate 3A human acceptance."
                if ghost.manual_authority else
                "Constrained proposal eligible for review acceptance."
            ),
        ))
    if _has_body_overlap(proposals):
        return _pack_cluster_shelves(ghost, entries)
    return proposals



def _pack_cluster_shelves(
    ghost: GhostCluster,
    entries: list[FootprintEntry],
) -> list[PlacementProposal]:
    """Fallback deterministic shelf packer for dense mixed-size clusters.

    The preliminary grid is intentionally simple and can compress row pitch
    when a cluster contains one unusually large package.  This fallback is
    used only when that grid would overlap conservative footprint envelopes.
    """
    gap = 1.2
    margin = max(1.5, ghost.keepout_mm / 2.0)
    left = ghost.x_mm + margin
    top = ghost.y_mm + margin
    right = ghost.x_mm + ghost.width_mm - margin
    bottom = ghost.y_mm + ghost.depth_mm - margin

    ordered = sorted(
        entries,
        key=lambda item: (
            0 if item.ref in ghost.anchor_refs else 1,
            -footprint_envelope(item).depth_mm,
            -footprint_envelope(item).width_mm,
            item.ref,
        ),
    )

    rows: list[list[FootprintEntry]] = []
    row_widths: list[float] = []
    row_heights: list[float] = []
    for entry in ordered:
        env = footprint_envelope(entry)
        placed = False
        for index, row in enumerate(rows):
            candidate_width = row_widths[index] + gap + env.width_mm
            if candidate_width <= (right - left) + 1e-9:
                row.append(entry)
                row_widths[index] = candidate_width
                row_heights[index] = max(row_heights[index], env.depth_mm)
                placed = True
                break
        if not placed:
            rows.append([entry])
            row_widths.append(env.width_mm)
            row_heights.append(env.depth_mm)

    total_height = sum(row_heights) + gap * max(0, len(rows) - 1)
    if total_height > (bottom - top) + 1e-9:
        raise ValueError(f"{ghost.identifier} cannot fit conservative footprint envelopes")

    proposals: list[PlacementProposal] = []
    y_cursor = top
    for row, row_height in zip(rows, row_heights):
        x_cursor = left
        for entry in row:
            env = footprint_envelope(entry)
            x = x_cursor + env.width_mm / 2.0
            y = y_cursor + row_height / 2.0
            proposals.append(PlacementProposal(
                ref=entry.ref,
                sheet_id=entry.sheet_id,
                cluster_id=ghost.identifier,
                footprint=entry.footprint,
                x_mm=round(x, 3),
                y_mm=round(y, 3),
                rotation_deg=_proposal_rotation(entry, ghost),
                width_mm=env.width_mm,
                depth_mm=env.depth_mm,
                accepted=not ghost.manual_authority,
                placement_authority=("manual_review" if ghost.manual_authority else "synthesised_review"),
                rationale=(
                    "Coordinate proposal only; critical cluster requires Gate 3A human acceptance."
                    if ghost.manual_authority else
                    "Constrained proposal eligible for review acceptance."
                ),
            ))
            x_cursor += env.width_mm + gap
        y_cursor += row_height + gap
    return proposals


def _has_body_overlap(proposals: list[PlacementProposal]) -> bool:
    for index, a in enumerate(proposals):
        for b in proposals[index + 1:]:
            if (
                abs(a.x_mm - b.x_mm) < (a.width_mm + b.width_mm) / 2.0 - 1e-9
                and abs(a.y_mm - b.y_mm) < (a.depth_mm + b.depth_mm) / 2.0 - 1e-9
            ):
                return True
    return False

def validate_preliminary_placement(model: PreliminaryPlacementBaseline) -> list[str]:
    issues: list[str] = []
    refs = [item.ref for item in model.proposals]
    if len(refs) != len(set(refs)):
        issues.append("duplicate component placement proposal")
    for item in model.proposals:
        if not (0.0 <= item.x_mm <= model.board_width_mm):
            issues.append(f"{item.ref} x coordinate outside board")
        if not (0.0 <= item.y_mm <= model.board_depth_mm):
            issues.append(f"{item.ref} y coordinate outside board")
        if item.width_mm <= 0 or item.depth_mm <= 0:
            issues.append(f"{item.ref} has invalid footprint envelope")
        if item.accepted and item.placement_authority == "manual_review":
            issues.append(f"{item.ref} manual placement was auto-accepted")
    return issues


def build_preliminary_placement_baseline(
    width_mm: float = 220.0,
    depth_mm: float = 140.0,
) -> PreliminaryPlacementBaseline:
    footprint_contract = build_footprint_contract()
    ghost_model = build_ghost_placement_baseline(width_mm, depth_mm)
    cluster_model = build_cluster_placement_baseline(width_mm, depth_mm)

    entries = {
        entry.ref: entry
        for entry in footprint_contract.entries
        if entry.population_status is PopulationStatus.APPROVED
    }
    owner: dict[str, str] = {}
    for cluster in cluster_model.clusters:
        for ref in cluster.member_refs:
            owner[ref] = cluster.identifier

    by_cluster: dict[str, list[FootprintEntry]] = {}
    for ref, entry in entries.items():
        by_cluster.setdefault(owner[ref], []).append(entry)

    proposals: list[PlacementProposal] = []
    for ghost in ghost_model.clusters:
        proposals.extend(_pack_cluster(ghost, by_cluster.get(ghost.identifier, [])))

    model = PreliminaryPlacementBaseline(
        identifier="G3-PLC-012",
        revision="Rev A0",
        status="PROVISIONAL — real footprints proposed; not accepted for manufacture",
        board_width_mm=width_mm,
        board_depth_mm=depth_mm,
        proposals=sorted(proposals, key=lambda item: item.ref),
        excluded_refs=sorted(footprint_contract.panel_interface_refs),
        manual_review_clusters=sorted(
            ghost.identifier for ghost in ghost_model.clusters if ghost.manual_authority
        ),
        invariants=[
            "Every approved PCB-owned reference has exactly one coordinate proposal.",
            "Panel and virtual references receive no PCB coordinate.",
            "Manual-authority clusters are never automatically accepted.",
            "Coordinates remain provisional until enclosure and mounting datums are frozen.",
            "Conservative footprint-envelope collision closure is required before routing review.",
        ],
    )
    issues = validate_preliminary_placement(model)
    if issues:
        raise ValueError("invalid preliminary placement: " + "; ".join(issues))
    return model
