"""Gate 3 component-cluster placement and board-constraint export.

This model converts the accepted functional-region architecture into bounded
component clusters.  It does not emit a KiCad PCB and does not freeze exact
component coordinates.  Instead it records adjacency, precedence, edge access,
keep-outs and routing authority for later placement synthesis.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum

from generator.mechanical.placement import build_placement_synthesis


class PlacementAuthority(str, Enum):
    MANUAL = "manual"
    SYNTHESISED_REVIEW = "synthesised_review"


class EdgeAffinity(str, Enum):
    NONE = "none"
    LEFT = "left"
    RIGHT = "right"
    CONTROL = "control"


@dataclass(frozen=True, slots=True)
class ComponentCluster:
    identifier: str
    name: str
    sheet_id: str
    region_id: str
    member_refs: tuple[str, ...]
    interface_refs: tuple[str, ...]
    anchor_refs: tuple[str, ...]
    authority: PlacementAuthority
    edge_affinity: EdgeAffinity
    precedence_after: tuple[str, ...]
    maximum_cluster_span_mm: float
    minimum_separation_mm: float
    orientation_rule: str
    adjacency_rule: str
    keepout_rule: str
    routing_handoff: str
    notes: str = ""


@dataclass(frozen=True, slots=True)
class BoardKeepout:
    identifier: str
    name: str
    applies_to: str
    clearance_mm: float
    rule: str


@dataclass(slots=True)
class ClusterPlacementBaseline:
    identifier: str
    revision: str
    status: str
    board_width_mm: float
    board_depth_mm: float
    clusters: list[ComponentCluster] = field(default_factory=list)
    keepouts: list[BoardKeepout] = field(default_factory=list)
    export_rules: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def _cluster(
    identifier: str,
    name: str,
    sheet_id: str,
    region_id: str,
    refs: str,
    anchors: str,
    *,
    interfaces: str = "",
    authority: PlacementAuthority = PlacementAuthority.MANUAL,
    edge: EdgeAffinity = EdgeAffinity.NONE,
    after: tuple[str, ...] = (),
    span: float,
    separation: float = 3.0,
    orientation: str,
    adjacency: str,
    keepout: str,
    routing: str,
    notes: str = "",
) -> ComponentCluster:
    return ComponentCluster(
        identifier, name, sheet_id, region_id,
        tuple(refs.split()), tuple(interfaces.split()), tuple(anchors.split()), authority, edge, after,
        span, separation, orientation, adjacency, keepout, routing, notes,
    )


def build_cluster_placement_baseline(
    width_mm: float = 220.0,
    depth_mm: float = 140.0,
) -> ClusterPlacementBaseline:
    placement = build_placement_synthesis(width_mm, depth_mm)

    clusters = [
        _cluster("CLU-101-A", "Left input RF and connector interface", "SCH101", "REG-01",
                 "H101 R102 R103 C101 C102 C103", "H101",
                 edge=EdgeAffinity.RIGHT, span=18.0, orientation="Connector-facing RF chain flows inward from right board edge.",
                 adjacency="RF resistors and capacitors immediately behind the input-harness termination.",
                 keepout="No control, output or power routing inside the cartridge-input keepout.",
                 routing="Manual differential pair; zero signal vias."),
        _cluster("CLU-101-B", "Left gain and differential conversion", "SCH101", "REG-01",
                 "SW1011 U101 U102 R111 R112 R113 R114 R121 R122 R123 R124 U103 R130 R131 R132 R133", "U101 U102 U103",
                 after=("CLU-101-A",), span=32.0, orientation="Plus/minus gain legs remain visually paired; converter follows them toward EQ.",
                 adjacency="Gain and converter feedback parts within 6 mm of their owning amplifier pins.",
                 keepout="No harness or unrelated trace between paired gain legs.",
                 routing="Manual feedback and differential-converter routes; zero vias."),
        _cluster("CLU-101-C", "Right input RF and connector interface", "SCH101", "REG-01",
                 "H201 R202 R203 C201 C202 C203", "H201",
                 edge=EdgeAffinity.RIGHT, span=18.0, orientation="Connector-facing RF chain flows inward from right board edge.",
                 adjacency="Mirror functional order of left channel without forcing longer loops.",
                 keepout="No control, output or power routing inside the cartridge-input keepout.",
                 routing="Manual differential pair; zero signal vias."),
        _cluster("CLU-101-D", "Right gain and differential conversion", "SCH101", "REG-01",
                 "U201 U202 R211 R212 R213 R214 R221 R222 R223 R224 U203 R230 R231 R232 R233", "U201 U202 U203",
                 after=("CLU-101-C",), span=32.0, orientation="Plus/minus gain legs remain visually paired; converter follows them toward EQ.",
                 adjacency="Gain and converter feedback parts within 6 mm of their owning amplifier pins.",
                 keepout="No harness or unrelated trace between paired gain legs.",
                 routing="Manual feedback and differential-converter routes; zero vias."),
        _cluster("CLU-103-LF-L", "Left active LF replay network", "SCH103", "REG-02",
                 "U3001 R30001 R30002 R30010 C30010 R30011 C30011 R30012 C30012 R30013 C30013 TP3001 TP3002", "U3001", interfaces="SW3001",
                 after=("CLU-101-B",), span=40.0, orientation="Input, amplifier, bass selector and output progress right-to-left.",
                 adjacency="Active feedback within 6 mm; selector RC branches remain grouped by switch position.",
                 keepout="No unrelated copper through selector fan-out or inverting-input region.",
                 routing="Manual only; zero signal vias."),
        _cluster("CLU-103-HF-L", "Left passive treble and recovery", "SCH103", "REG-02",
                 "R30030 C30030 C30031 C30032 C30033 U3002 R30040 R30041 TP3003 TP3004 C30050 C30051 C30052 C30053", "U3002", interfaces="SW3002",
                 after=("CLU-103-LF-L",), span=36.0, orientation="Treble bank precedes recovery amplifier toward output.",
                 adjacency="Recovery feedback within 6 mm; local 100 nF capacitors within 4 mm of supply pins.",
                 keepout="Treble branch fan-out and recovery feedback are protected sub-regions.",
                 routing="Manual selector and feedback; reviewed supply routing."),
        _cluster("CLU-103-LF-R", "Right active LF replay network", "SCH103", "REG-03",
                 "U3501 R35001 R35002 R35010 C35010 R35011 C35011 R35012 C35012 R35013 C35013 TP3501 TP3502", "U3501", interfaces="SW3501",
                 after=("CLU-101-D",), span=40.0, orientation="Input, amplifier, bass selector and output progress right-to-left.",
                 adjacency="Active feedback within 6 mm; selector RC branches remain grouped by switch position.",
                 keepout="No unrelated copper through selector fan-out or inverting-input region.",
                 routing="Manual only; zero signal vias."),
        _cluster("CLU-103-HF-R", "Right passive treble and recovery", "SCH103", "REG-03",
                 "R35030 C35030 C35031 C35032 C35033 U3502 R35040 R35041 TP3503 TP3504 C35050 C35051 C35052 C35053", "U3502", interfaces="SW3502",
                 after=("CLU-103-LF-R",), span=36.0, orientation="Treble bank precedes recovery amplifier toward output.",
                 adjacency="Recovery feedback within 6 mm; local 100 nF capacitors within 4 mm of supply pins.",
                 keepout="Treble branch fan-out and recovery feedback are protected sub-regions.",
                 routing="Manual selector and feedback; reviewed supply routing."),
        _cluster("CLU-107-L", "Left two-section rumble filter", "SCH107", "REG-04",
                 "U700 C7001 C7002 R7001 R7002 U720 C7201 C7202 R7201 R7202 R70090 C70091 C70092 C70093 C70094 TP7001 TP7002 TP7003 TP7004", "U700 U720", interfaces="SW1071",
                 after=("CLU-103-HF-L",), span=38.0, orientation="Two Sallen-Key sections in strict cascade.",
                 adjacency="Each frequency-setting quartet within 6 mm of its amplifier.",
                 keepout="No control harness through high-impedance filter nodes.",
                 routing="Manual frequency-setting nets; zero vias."),
        _cluster("CLU-107-R", "Right two-section rumble filter", "SCH107", "REG-04",
                 "U750 C7501 C7502 R7501 R7502 U770 C7701 C7702 R7701 R7702 R75090 C75091 C75092 C75093 C75094 TP7501 TP7502 TP7503 TP7504", "U750 U770",
                 after=("CLU-103-HF-R",), span=38.0, orientation="Two Sallen-Key sections in strict cascade.",
                 adjacency="Each frequency-setting quartet within 6 mm of its amplifier.",
                 keepout="No control harness through high-impedance filter nodes.",
                 routing="Manual frequency-setting nets; zero vias."),
        _cluster("CLU-104", "Isolation buffers", "SCH104", "REG-05",
                 "U401 U402 R4001 R4501 TP4001 TP4002 TP4501 TP4502 C4091 C4092 C4093 C4094", "U401 U402",
                 after=("CLU-107-L", "CLU-107-R"), span=25.0, orientation="Channels remain parallel with outputs facing mode matrix.",
                 adjacency="Isolation resistors and local decouplers adjacent to buffer pins.",
                 keepout="Preserve clear probing access at buffer input and output test points.",
                 routing="Manual local feedback; assisted ordinary signal routes."),
        _cluster("CLU-105", "Passive mode matrix and buffers", "SCH105", "REG-05",
                 "R501 R502 U501 U502 R510 R511 R520 R521 TP501 TP502 TP503 TP504 TP505 C5091 C5092 C5093 C5094", "U501 U502", interfaces="SW501",
                 after=("CLU-104",), span=36.0, orientation="Selector central; channel buffers face output region.",
                 adjacency="Mono averaging pair adjacent and symmetrical; input-bias resistors local to buffer inputs.",
                 keepout="Control harness approaches from control edge without crossing input or EQ islands.",
                 routing="Manual summing nodes; constrained automation for control contacts."),
        _cluster("CLU-108-L", "Left mute, driver and protection", "SCH108", "REG-06",
                 "U8001 C80010 C80011 FB8001 FB8002 C80020 C80021 D80030 D80031 D80032 D80033 TP8010 TP8001 TP8002 TP8003 C80040 C80041 C80042 C80043", "U8001", interfaces="SW801 J8001",
                 after=("CLU-105",), edge=EdgeAffinity.LEFT, span=34.0, orientation="Mute precedes driver; protected outputs face left harness edge.",
                 adjacency="OUT/SNS capacitors within 5 mm; protection components immediately before harness termination.",
                 keepout="No input or EQ routing in output-current region.",
                 routing="Manual OUT/SNS loops; reviewed balanced-output pair."),
        _cluster("CLU-108-R", "Right mute, driver and protection", "SCH108", "REG-06",
                 "TP8011 U9001 C90010 C90011 FB9001 FB9002 C90020 C90021 D90030 D90031 D90032 D90033 TP9001 TP9002 TP9003 C90040 C90041 C90042 C90043", "U9001", interfaces="J9001",
                 after=("CLU-105",), edge=EdgeAffinity.LEFT, span=34.0, orientation="Mute precedes driver; protected outputs face left harness edge.",
                 adjacency="OUT/SNS capacitors within 5 mm; protection components immediately before harness termination.",
                 keepout="No input or EQ routing in output-current region.",
                 routing="Manual OUT/SNS loops; reviewed balanced-output pair."),
        _cluster("CLU-106", "DC entry, bulk capacitance and chassis bond", "SCH106", "REG-07",
                 "H901 R901 R902 C901 C902 C903 R903 C904 C905 C906 R904 R909 C909 D901 D902 TP901 TP902 TP903 TP904", "H901 R909",
                 edge=EdgeAffinity.LEFT, span=38.0, orientation="DC connector at left edge; rail links and bulk capacitance feed inward.",
                 adjacency="Chassis bond remains local and serviceable; rail bypasses group by polarity.",
                 keepout="Separated from cartridge region; reserve mechanical access to bond and rail test points.",
                 routing="Manual 0VA/chassis bond; reviewed rail-spine handoff."),
        _cluster("CLU-109", "Panel-control harness interface", "SCH109", "REG-08",
                 "R906 R907 TP9901 TP9902", "TP9901 TP9902", interfaces="SW901 SW902 SW903 SW904 SW905 LED901 LED902",
                 authority=PlacementAuthority.SYNTHESISED_REVIEW, edge=EdgeAffinity.CONTROL, span=55.0,
                 orientation="Harness connectors follow front/top panel control order.",
                 adjacency="Related switch poles grouped into one locking harness interface per control family.",
                 keepout="Harness bend and connector extraction zones remain clear of test points.",
                 routing="Constrained automation permitted after harness pinout freeze."),
    ]

    keepouts = [
        BoardKeepout("KO-001", "Board edge", "all components and copper", 5.0, "No component body or ordinary copper inside the board-edge clearance."),
        BoardKeepout("KO-002", "Mounting holes", "components, copper and harnesses", 10.0, "Radial keepout around each enclosure-dependent mounting datum."),
        BoardKeepout("KO-003", "Input magnetic/noise exclusion", "output, DC and control hardware", 15.0, "No high-current or panel-control hardware adjacent to cartridge-input anchors."),
        BoardKeepout("KO-004", "Harness extraction", "tall components and test points", 12.0, "Clear corridor behind every locking board connector."),
        BoardKeepout("KO-005", "Probe access", "tall components and harness crossings", 8.0, "Component-side test points require a local probe-access disc."),
    ]

    model = ClusterPlacementBaseline(
        identifier="G3-PLC-005",
        revision="Rev A0",
        status="PROVISIONAL — exact XY coordinates await enclosure and PCB-outline freeze",
        board_width_mm=placement.board_width_mm,
        board_depth_mm=placement.board_depth_mm,
        clusters=clusters,
        keepouts=keepouts,
        export_rules=[
            "Every schematic on-board reference shall belong to exactly one placement cluster.",
            "Cluster precedence shall be acyclic.",
            "Manual-authority clusters may be synthesised only as a proposal and require explicit acceptance.",
            "Exact XY placement shall not be exported until the enclosure, carrier plate and mounting datums are frozen.",
            "Constraint export shall preserve region, adjacency, span, edge-affinity and keepout metadata.",
        ],
    )
    validate_cluster_baseline(model)
    return model


def validate_cluster_baseline(model: ClusterPlacementBaseline) -> None:
    issues: list[str] = []
    ids = {cluster.identifier for cluster in model.clusters}
    if len(ids) != len(model.clusters):
        issues.append("duplicate cluster identifiers")
    owners: dict[str, str] = {}
    for cluster in model.clusters:
        if not cluster.member_refs:
            issues.append(f"{cluster.identifier} has no component references")
        if cluster.maximum_cluster_span_mm <= 0:
            issues.append(f"{cluster.identifier} has invalid span")
        for dependency in cluster.precedence_after:
            if dependency not in ids:
                issues.append(f"{cluster.identifier} depends on unknown {dependency}")
        for ref in cluster.member_refs + cluster.interface_refs:
            if ref in owners:
                issues.append(f"{ref} owned by both {owners[ref]} and {cluster.identifier}")
            owners[ref] = cluster.identifier

    # Detect precedence cycles.
    graph = {cluster.identifier: set(cluster.precedence_after) for cluster in model.clusters}
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            issues.append(f"precedence cycle at {node}")
            return
        if node in visited:
            return
        visiting.add(node)
        for dependency in graph[node]:
            visit(dependency)
        visiting.remove(node)
        visited.add(node)

    for node in graph:
        visit(node)
    if issues:
        raise ValueError("invalid cluster placement baseline: " + "; ".join(issues))
