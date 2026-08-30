"""SR-039 schematic-to-layout release gate."""
from __future__ import annotations
from dataclasses import asdict, dataclass, field

from generator.layout.constraints import build_layout_baseline
from generator.layout.detailed_placement_readiness import build_detailed_placement_readiness
from generator.mechanical.board_outline import OutlineStatus, build_provisional_outline_contract
from generator.model.balanced_input import LT5400_FOOTPRINT, validate_balanced_input
from generator.model.post_eq_dc_block import cutoff_hz, validate_post_eq_dc_block

@dataclass(frozen=True, slots=True)
class ReleaseDisposition:
    schematic_release: str
    placement_release: str
    routing_release: str
    manufacturing_release: str

@dataclass(slots=True)
class SchematicToLayoutReleaseGate:
    identifier: str
    revision: str
    status: str
    disposition: ReleaseDisposition
    electrical_invariants: list[str] = field(default_factory=list)
    layout_invariants: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    next_actions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

def build_schematic_to_layout_release_gate() -> SchematicToLayoutReleaseGate:
    validate_balanced_input()
    validate_post_eq_dc_block()
    layout = build_layout_baseline()
    placement = build_detailed_placement_readiness()
    outline = build_provisional_outline_contract(
        width_mm=layout.envelope.preferred_usable_width_mm,
        depth_mm=layout.envelope.preferred_usable_depth_mm,
    )
    blockers=[]
    if outline.status is not OutlineStatus.FROZEN:
        blockers.append("Final PCB routing/manufacture blocked: board outline, mounting holes and enclosure keep-outs are not frozen from verified mechanical datums.")
    if placement.blocker_count:
        blockers.append(f"Placement candidate contains {placement.blocker_count} deterministic blocker(s) that must be cleared before routing.")
    blockers.append("Manufacturing release blocked until the controlled BOM is expanded from the partial high-level baseline to the full schematic population with exact purchasable identities.")
    return SchematicToLayoutReleaseGate(
        identifier="SR-039",
        revision="Rev A0",
        status="SCHEMATIC_RELEASED — PLACEMENT_ALLOWED — ROUTING/MANUFACTURE_GATED",
        disposition=ReleaseDisposition(
            schematic_release="RELEASED",
            placement_release="ALLOWED_WITH_PROVISIONAL_MECHANICAL_KEEP_IN",
            routing_release="BLOCKED_PENDING_MECHANICAL_DATUM_FREEZE",
            manufacturing_release="BLOCKED_PENDING_MECHANICAL_AND_FULL_BOM_CLOSURE",
        ),
        electrical_invariants=[
            f"SCH101 precision front end is implemented DR-038; LT5400 footprint = {LT5400_FOOTPRINT}.",
            f"DR-039 common post-EQ DC block is implemented at 1.0 uF / 330 kOhm; calculated corner = {cutoff_hz():.4f} Hz.",
            "Validated baseline evidence: 374/374 Python tests and native KiCad ERC 0 errors / 0 warnings on 30 August 2026.",
            "No further signal-chain architecture changes are authorised during layout unless a new defect is demonstrated and controlled.",
        ],
        layout_invariants=[
            "Four-layer board architecture retained: top critical analogue, inner-1 continuous 0VA, inner-2 rails, bottom supporting routing.",
            "Cartridge, LT5400 summing, replay-EQ timing, frequency-setting and THAT1646 sense loops remain manual-routing authority.",
            "Critical-cluster placement may proceed inside the provisional 220 x 140 mm keep-in.",
            "Mounting holes, enclosure intrusion zones and final harness corridors remain provisional until mechanical datum freeze.",
        ],
        blockers=blockers,
        next_actions=[
            "Reconcile/freeze authoritative audio-enclosure and carrier-plate mechanical datums.",
            "Close full component-level schematic/BOM/footprint/procurement identities.",
            "Perform human placement of SCH101, SCH103, SCH107 and SCH108 critical analogue clusters.",
            "Freeze board outline/mounting holes/keep-outs, then release routing.",
            "After routing: DRC, ERC regression, fabrication outputs and PCBWay manufacturing pack.",
        ],
    )
