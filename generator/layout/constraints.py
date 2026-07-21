"""Gate 3 PCB architecture baseline.

This model records physical-design intent without depending on KiCad board
syntax or final enclosure coordinates.  It is deliberately provisional until
the audio enclosure and board outline are frozen.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum


class NetClass(str, Enum):
    CARTRIDGE = "cartridge_level"
    FEEDBACK = "feedback_or_frequency_setting"
    ANALOG = "ordinary_analog"
    BALANCED_OUTPUT = "balanced_output"
    POWER = "power_distribution"
    GROUND = "reference_or_chassis"
    CONTROL = "panel_control"


class PlacementPolicy(str, Enum):
    MANUAL = "manual"
    CONSTRAINED_ASSISTED = "constrained_assisted"


class RoutingPolicy(str, Enum):
    MANUAL_ONLY = "manual_only"
    ASSISTED_REVIEW_REQUIRED = "assisted_review_required"
    CONSTRAINED_AUTOMATION = "constrained_automation"


@dataclass(frozen=True, slots=True)
class BoardStackup:
    layer_count: int
    top_role: str
    inner_1_role: str
    inner_2_role: str
    bottom_role: str
    copper_oz: float = 1.0
    finished_thickness_mm: float = 1.6
    rationale: str = ""


@dataclass(frozen=True, slots=True)
class FunctionalRegion:
    identifier: str
    name: str
    sequence: int
    preferred_edge: str
    placement_policy: PlacementPolicy
    isolation_rule: str
    notes: str = ""


@dataclass(frozen=True, slots=True)
class CriticalNet:
    identifier: str
    pattern: str
    net_class: NetClass
    routing_policy: RoutingPolicy
    max_signal_vias: int
    reference_domain: str
    placement_rule: str
    routing_rule: str
    verification: str


@dataclass(frozen=True, slots=True)
class MechanicalEnvelope:
    minimum_usable_width_mm: float
    minimum_usable_depth_mm: float
    preferred_usable_width_mm: float
    preferred_usable_depth_mm: float
    board_edge_clearance_mm: float
    mounting_hole_keepout_mm: float
    access_rule: str
    status: str


@dataclass(slots=True)
class LayoutBaseline:
    identifier: str
    revision: str
    status: str
    stackup: BoardStackup
    envelope: MechanicalEnvelope
    regions: list[FunctionalRegion] = field(default_factory=list)
    critical_nets: list[CriticalNet] = field(default_factory=list)
    global_rules: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def build_layout_baseline() -> LayoutBaseline:
    regions = [
        FunctionalRegion("REG-01", "Balanced input and RF protection", 10, "input/right", PlacementPolicy.MANUAL, "No unrelated trace may cross the cartridge-input island."),
        FunctionalRegion("REG-02", "Replay EQ left", 20, "central/input side", PlacementPolicy.MANUAL, "Keep all left EQ feedback and selector components local."),
        FunctionalRegion("REG-03", "Replay EQ right", 30, "central/input side", PlacementPolicy.MANUAL, "Keep all right EQ feedback and selector components local."),
        FunctionalRegion("REG-04", "Rumble filter", 40, "central", PlacementPolicy.MANUAL, "Frequency-setting components remain adjacent to their amplifiers."),
        FunctionalRegion("REG-05", "Final gain and mode matrix", 50, "central/output side", PlacementPolicy.MANUAL, "Maintain recognisable channel structure and short summing paths."),
        FunctionalRegion("REG-06", "Mute and balanced output", 60, "output/left", PlacementPolicy.MANUAL, "Keep THAT1646 OUT/SNS loops local and output protection near the harness connector."),
        FunctionalRegion("REG-07", "DC entry and local bulk decoupling", 70, "output/high-level end", PlacementPolicy.MANUAL, "DC entry must be remote from cartridge inputs and feed a controlled rail spine."),
        FunctionalRegion("REG-08", "Panel-control harness interfaces", 80, "control edge", PlacementPolicy.CONSTRAINED_ASSISTED, "Control harnesses may not traverse the cartridge-input island."),
    ]

    critical_nets = [
        CriticalNet("NET-001", "INPUT_[LR]_(POS|NEG)", NetClass.CARTRIDGE, RoutingPolicy.MANUAL_ONLY, 0, "0VA continuous reference", "Place RF and input components immediately behind the input harness connector.", "Route channel pairs together, avoid stubs, and prohibit unrelated copper beneath or between the pair.", "Visual review plus continuity and pair-symmetry report."),
        CriticalNet("NET-002", "U*.IN-/feedback nodes", NetClass.FEEDBACK, RoutingPolicy.MANUAL_ONLY, 0, "local 0VA return", "Feedback parts adjacent to the associated amplifier pins.", "Minimise enclosed loop area; no test-point or connector branch inside the loop.", "Loop-area and component-distance audit."),
        CriticalNet("NET-003", "SCH103 selector RC branches", NetClass.FEEDBACK, RoutingPolicy.MANUAL_ONLY, 0, "local 0VA return", "Keep each selector branch within its EQ island.", "No branch sharing or endpoint-on-segment junctions; preserve channel separation.", "Topology regression and visual branch audit."),
        CriticalNet("NET-004", "SCH107 frequency-setting nets", NetClass.FEEDBACK, RoutingPolicy.MANUAL_ONLY, 0, "local 0VA return", "Frequency-setting passives adjacent to OPA1656 pins.", "Shortest practical traces with no unrelated vias or crossings.", "Distance and via-count audit."),
        CriticalNet("NET-005", "THAT1646 OUT*/SNS*", NetClass.BALANCED_OUTPUT, RoutingPolicy.MANUAL_ONLY, 0, "local driver return", "Sense capacitors and output isolation parts adjacent to each driver.", "Direct OUT-to-capacitor and SNS-to-capacitor conductors; matched channel geometry where practical.", "Direct-edge and symmetry regression."),
        CriticalNet("NET-006", "+18V|-18V", NetClass.POWER, RoutingPolicy.ASSISTED_REVIEW_REQUIRED, 2, "0VA plane", "Use a controlled rail spine with local branches and block-level bulk capacitance.", "Avoid routing rail current through low-level return regions; use paired supply/return vias where needed.", "Voltage-drop and current-return review."),
        CriticalNet("NET-007", "0VA", NetClass.GROUND, RoutingPolicy.MANUAL_ONLY, 0, "self", "Continuous inner reference plane; no arbitrary splits beneath signals.", "Control high-current return entry points and preserve separation from CHASSIS except at the defined bond.", "Plane continuity and return-path review."),
        CriticalNet("NET-008", "CHASSIS", NetClass.GROUND, RoutingPolicy.MANUAL_ONLY, 0, "chassis", "Bond connector shells at entry and localise the 0VA/CHASSIS network.", "No signal-current use of chassis copper; keep bond components serviceable.", "Continuity/isolation test."),
        CriticalNet("NET-009", "*_SELECT|MUTE_CONTROL|RUMBLE_BYPASS", NetClass.CONTROL, RoutingPolicy.CONSTRAINED_AUTOMATION, 3, "0VA plane", "Group at the control-harness edge.", "Do not run parallel to cartridge inputs; add separation from EQ high-impedance nodes.", "Clearance and coupling review."),
        CriticalNet("NET-010", "OUTPUT_[LR]_(POS|NEG)", NetClass.BALANCED_OUTPUT, RoutingPolicy.ASSISTED_REVIEW_REQUIRED, 1, "0VA plane", "Route from output protection directly to the output harness region.", "Maintain pair adjacency and avoid the input region.", "Pair geometry and output-continuity audit."),
    ]

    return LayoutBaseline(
        identifier="G3-LYT-001",
        revision="Rev A0",
        status="PROVISIONAL — enclosure and board outline not frozen",
        stackup=BoardStackup(
            layer_count=4,
            top_role="Components and critical analogue routing",
            inner_1_role="Continuous 0VA reference plane",
            inner_2_role="+18V/-18V distribution with limited non-critical routing",
            bottom_role="Supporting analogue and control routing",
            rationale="Four layers reduce reference discontinuity and first-pass analogue-layout risk while preserving affordable manufacture.",
        ),
        envelope=MechanicalEnvelope(
            minimum_usable_width_mm=190.0,
            minimum_usable_depth_mm=125.0,
            preferred_usable_width_mm=220.0,
            preferred_usable_depth_mm=140.0,
            board_edge_clearance_mm=5.0,
            mounting_hole_keepout_mm=10.0,
            access_rule="Audio enclosure requires vertically removable lid or base after all controls are fitted.",
            status="Provisional until audio enclosure trade study closes.",
        ),
        regions=regions,
        critical_nets=critical_nets,
        global_rules=[
            "Physical signal flow shall progress from input region to output region without avoidable reversals.",
            "Component placement shall be accepted before routing begins.",
            "No unrelated route may pass through a low-level input, feedback, or replay-EQ island.",
            "All defined test points and nearby ground probe points shall remain accessible from the component side.",
            "Panel harnesses shall use locking connectors and remain removable without soldering.",
            "Strategic whitespace is permitted for probing, separation, readable silkscreen, and Revision B flexibility.",
            "A generic autorouter shall not route any manual-only net.",
        ],
    )
