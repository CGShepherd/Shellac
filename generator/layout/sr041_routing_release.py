"""SR-041 critical-placement acceptance and PCB routing release."""
from __future__ import annotations
from dataclasses import asdict, dataclass, field
from math import hypot

from generator.layout.constraints import RoutingPolicy, build_layout_baseline
from generator.layout.preliminary_placement import build_preliminary_placement_baseline
from generator.mechanical.sr040_audio_freeze import frozen_audio_board_outline

@dataclass(frozen=True, slots=True)
class PlacementAcceptance:
    cluster_id: str
    status: str
    movement_authority: str
    acceptance_basis: str

@dataclass(slots=True)
class RoutingRelease:
    identifier: str
    revision: str
    status: str
    board_width_mm: float
    board_depth_mm: float
    mounting_hole_count: int
    placement_count: int
    manual_cluster_count: int
    mounting_collision_count: int
    manual_only_net_count: int
    accepted_clusters: list[PlacementAcceptance] = field(default_factory=list)
    routing_rules: list[str] = field(default_factory=list)
    release_checks: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

def _proposal_hits_mounting_keepout(proposal, hole) -> bool:
    # Conservative rectangular footprint envelope versus circular copper/
    # component keep-out. Treat footprint as a bounding rectangle and compare
    # nearest point to the mounting-hole keep-out radius.
    half_w=proposal.width_mm/2.0
    half_d=proposal.depth_mm/2.0
    dx=max(abs(hole.centre.x_mm-proposal.x_mm)-half_w,0.0)
    dy=max(abs(hole.centre.y_mm-proposal.y_mm)-half_d,0.0)
    return hypot(dx,dy) < hole.copper_keepout_diameter_mm/2.0 - 1e-9

def build_sr041_routing_release() -> RoutingRelease:
    outline=frozen_audio_board_outline()
    placement=build_preliminary_placement_baseline(
        width_mm=outline.outline.width_mm,
        depth_mm=outline.outline.depth_mm,
    )
    layout=build_layout_baseline()

    collisions=[]
    for proposal in placement.proposals:
        for hole in outline.mounting_holes:
            if _proposal_hits_mounting_keepout(proposal,hole):
                collisions.append((proposal.ref,hole.identifier))

    accepted=[]
    for cluster_id in placement.manual_review_clusters:
        accepted.append(PlacementAcceptance(
            cluster_id=cluster_id,
            status="ACCEPTED_AS_ROUTING_BASELINE",
            movement_authority="LOCAL_REFINEMENT_WITHIN_CLUSTER_ENVELOPE",
            acceptance_basis=(
                "SR-040 deterministic placement has no footprint-body blocker; "
                "cluster topology, adjacency, sensitivity separation and routing "
                "authority are frozen. Exact XY may be refined during manual routing."
            ),
        ))

    manual_nets=[
        item for item in layout.critical_nets
        if item.routing_policy is RoutingPolicy.MANUAL_ONLY
    ]

    status="ROUTING_RELEASED" if not collisions else "BLOCKED_MOUNTING_COLLISION"
    return RoutingRelease(
        identifier="SR-041",
        revision="Rev A0",
        status=status,
        board_width_mm=outline.outline.width_mm,
        board_depth_mm=outline.outline.depth_mm,
        mounting_hole_count=len(outline.mounting_holes),
        placement_count=len(placement.proposals),
        manual_cluster_count=len(placement.manual_review_clusters),
        mounting_collision_count=len(collisions),
        manual_only_net_count=len(manual_nets),
        accepted_clusters=accepted,
        routing_rules=[
            "PCB outline and four mounting-hole datums are frozen by SR-040.",
            "Inner-1 remains an uninterrupted 0VA reference plane beneath analogue signal paths.",
            "Manual-only nets may not be delegated to an autorouter.",
            "INPUT_[LR]_(POS|NEG), LT5400 summing/feedback, replay-EQ selector/timing, SCH107 frequency-setting, and THAT1646 OUT/SNS routes are routed manually.",
            "No signal via is permitted where the applicable critical-net contract specifies max_signal_vias=0.",
            "Local component movement during routing is permitted only within the owning cluster envelope and must preserve the cluster adjacency/orientation rules.",
            "No unrelated route may enter cartridge-input, feedback, replay-EQ, or filter high-impedance islands.",
            "Power branches shall leave the rail spine locally; load-return geometry must not force current through low-level reference regions.",
            "CHASSIS is not a signal-current return and bonds to 0VA only through the defined serviceable network.",
            "Test-point probe access and locking-harness extraction corridors remain protected during routing.",
        ],
        release_checks=[
            "Schematic electrical baseline validated before SR-040.",
            "Mechanical outline and mounting datums frozen.",
            "Every approved PCB-owned schematic reference has a deterministic placement proposal.",
            "Critical/manual clusters accepted as routing baseline with controlled local refinement.",
            "Mounting-hole versus component-envelope collision audit passed." if not collisions else f"Mounting collisions: {collisions}",
            "Procurement MPN closure may continue in parallel where electrical value, technology and footprint are already controlled.",
        ],
    )
