"""G3-011 ghost-PCB placement synthesis.

This model places component clusters as reviewable envelopes rather than real
footprints.  It is intentionally non-manufacturing and exists to validate
signal flow, adjacency, interface access, sensitivity separation and thermal
balance before exact component coordinates are emitted.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum

from generator.layout.placement_clusters import (
    ClusterPlacementBaseline,
    ComponentCluster,
    EdgeAffinity,
    build_cluster_placement_baseline,
)
from generator.mechanical.placement import RegionBox, build_placement_synthesis


class SensitivityClass(str, Enum):
    MICROVOLT = "microvolt"
    HIGH_IMPEDANCE = "high_impedance"
    ANALOGUE = "analogue"
    LINE_LEVEL = "line_level"
    POWER = "power"
    CONTROL = "control"


class ThermalClass(str, Enum):
    NEGLIGIBLE = "negligible"
    LOW = "low"
    MODERATE = "moderate"


@dataclass(frozen=True, slots=True)
class GhostCluster:
    identifier: str
    name: str
    region_id: str
    x_mm: float
    y_mm: float
    width_mm: float
    depth_mm: float
    signal_entry_edge: str
    signal_exit_edge: str
    harness_edge: str
    sensitivity: SensitivityClass
    thermal: ThermalClass
    manual_authority: bool
    keepout_mm: float
    member_count: int
    anchor_refs: tuple[str, ...]
    notes: str

    @property
    def area_mm2(self) -> float:
        return self.width_mm * self.depth_mm


@dataclass(slots=True)
class GhostPlacementBaseline:
    identifier: str
    revision: str
    status: str
    board_width_mm: float
    board_depth_mm: float
    clusters: list[GhostCluster] = field(default_factory=list)
    invariants: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        payload = asdict(self)
        for cluster, raw in zip(self.clusters, payload["clusters"]):
            raw["area_mm2"] = cluster.area_mm2
        return payload


def _sensitivity(cluster: ComponentCluster) -> SensitivityClass:
    if cluster.identifier in {"CLU-101-A", "CLU-101-C"}:
        return SensitivityClass.MICROVOLT
    if cluster.identifier.startswith("CLU-103") or cluster.identifier.startswith("CLU-107"):
        return SensitivityClass.HIGH_IMPEDANCE
    if cluster.identifier in {"CLU-108-L", "CLU-108-R"}:
        return SensitivityClass.LINE_LEVEL
    if cluster.identifier == "CLU-106":
        return SensitivityClass.POWER
    if cluster.identifier == "CLU-109":
        return SensitivityClass.CONTROL
    return SensitivityClass.ANALOGUE


def _thermal(cluster: ComponentCluster) -> ThermalClass:
    if cluster.identifier == "CLU-106":
        return ThermalClass.MODERATE
    if cluster.identifier in {"CLU-108-L", "CLU-108-R"}:
        return ThermalClass.LOW
    return ThermalClass.NEGLIGIBLE


def _entry_exit(cluster: ComponentCluster) -> tuple[str, str]:
    if cluster.identifier in {"CLU-101-A", "CLU-101-C"}:
        return "right", "left"
    if cluster.identifier == "CLU-106":
        return "left", "right"
    if cluster.identifier == "CLU-109":
        return "control", "control"
    return "right", "left"


def _harness_edge(cluster: ComponentCluster) -> str:
    if cluster.edge_affinity == EdgeAffinity.RIGHT:
        return "right"
    if cluster.edge_affinity == EdgeAffinity.LEFT:
        return "left"
    if cluster.edge_affinity == EdgeAffinity.CONTROL:
        return "control"
    return "none"


def _pack_region(region: RegionBox, clusters: list[ComponentCluster]) -> list[GhostCluster]:
    if not clusters:
        return []
    margin = 2.0
    gap = 2.0
    usable_w = region.width_mm - 2 * margin
    usable_d = region.depth_mm - 2 * margin

    # Prefer vertical stacking for full-depth edge regions; horizontal packing
    # elsewhere. This is a review envelope, not final placement.
    vertical = region.identifier in {"REG-01", "REG-04", "REG-05", "REG-06"}
    total_weight = sum(max(c.maximum_cluster_span_mm, 1.0) for c in clusters)
    ghosts: list[GhostCluster] = []
    cursor = margin

    for index, cluster in enumerate(clusters):
        weight = max(cluster.maximum_cluster_span_mm, 1.0) / total_weight
        entry, exit_ = _entry_exit(cluster)
        if vertical:
            height = max(10.0, usable_d * weight - gap * (len(clusters) - 1) / len(clusters))
            width = usable_w
            x = region.x_mm + margin
            y = region.y_mm + cursor
            cursor += height + gap
        else:
            width = max(12.0, usable_w * weight - gap * (len(clusters) - 1) / len(clusters))
            height = usable_d
            x = region.x_mm + cursor
            y = region.y_mm + margin
            cursor += width + gap

        ghosts.append(GhostCluster(
            identifier=cluster.identifier,
            name=cluster.name,
            region_id=cluster.region_id,
            x_mm=round(x, 3),
            y_mm=round(y, 3),
            width_mm=round(width, 3),
            depth_mm=round(height, 3),
            signal_entry_edge=entry,
            signal_exit_edge=exit_,
            harness_edge=_harness_edge(cluster),
            sensitivity=_sensitivity(cluster),
            thermal=_thermal(cluster),
            manual_authority=cluster.authority.value == "manual",
            keepout_mm=round(cluster.minimum_separation_mm, 3),
            member_count=len(cluster.member_refs),
            anchor_refs=cluster.anchor_refs,
            notes=cluster.keepout_rule,
        ))
    return ghosts


def validate_ghost_placement(model: GhostPlacementBaseline) -> list[str]:
    issues: list[str] = []
    ids = [c.identifier for c in model.clusters]
    if len(ids) != len(set(ids)):
        issues.append("duplicate ghost cluster identifiers")
    for cluster in model.clusters:
        if cluster.width_mm <= 0 or cluster.depth_mm <= 0:
            issues.append(f"{cluster.identifier} has invalid envelope")
        if cluster.x_mm < 0 or cluster.y_mm < 0:
            issues.append(f"{cluster.identifier} lies outside board")
        if cluster.x_mm + cluster.width_mm > model.board_width_mm + 1e-6:
            issues.append(f"{cluster.identifier} exceeds board width")
        if cluster.y_mm + cluster.depth_mm > model.board_depth_mm + 1e-6:
            issues.append(f"{cluster.identifier} exceeds board depth")
    micro = [c for c in model.clusters if c.sensitivity == SensitivityClass.MICROVOLT]
    if not micro or any(c.harness_edge != "right" for c in micro):
        issues.append("microvolt clusters must remain on right-side harness edge")
    power = [c for c in model.clusters if c.sensitivity == SensitivityClass.POWER]
    if len(power) != 1 or power[0].harness_edge != "left":
        issues.append("power-entry cluster must remain on left-side harness edge")
    return issues


def build_ghost_placement_baseline(
    width_mm: float = 220.0,
    depth_mm: float = 140.0,
) -> GhostPlacementBaseline:
    regions = build_placement_synthesis(width_mm, depth_mm)
    clusters = build_cluster_placement_baseline(width_mm, depth_mm)
    by_region: dict[str, list[ComponentCluster]] = {}
    for cluster in clusters.clusters:
        by_region.setdefault(cluster.region_id, []).append(cluster)

    ghosts: list[GhostCluster] = []
    for region in regions.regions:
        ghosts.extend(_pack_region(region, by_region.get(region.identifier, [])))

    # REG-08 is the board-edge harness-interface corridor rather than a
    # signal-processing region.  It is represented explicitly along the
    # lower control edge so it cannot be lost merely because the earlier
    # seven-region synthesis omitted panel-interface geometry.
    control_clusters = by_region.get("REG-08", [])
    if control_clusters:
        control_region = RegionBox(
            "REG-08", "Panel-control harness interface",
            65.0, 128.0, 90.0, 7.0, 80, "edge-local",
            "Dedicated control-edge corridor; no cartridge or feedback routing.",
        )
        ghosts.extend(_pack_region(control_region, control_clusters))

    model = GhostPlacementBaseline(
        identifier="G3-GHOST-011",
        revision="Rev A0",
        status="PROVISIONAL — cluster envelopes only; not for manufacture",
        board_width_mm=width_mm,
        board_depth_mm=depth_mm,
        clusters=ghosts,
        invariants=[
            "All sixteen placement clusters appear exactly once.",
            "Microvolt input clusters remain on the right-side harness edge.",
            "Balanced-output and regulated-power interfaces remain on the left side.",
            "Signal direction remains predominantly right-to-left.",
            "Ghost envelopes never imply exact footprint coordinates.",
            "Manual-authority clusters remain subject to human acceptance.",
        ],
    )
    issues = validate_ghost_placement(model)
    if issues:
        raise ValueError("invalid ghost placement: " + "; ".join(issues))
    return model
