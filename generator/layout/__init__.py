"""CAD-independent PCB architecture and layout constraints for Project Shellac."""

from .constraints import (
    BoardStackup,
    CriticalNet,
    FunctionalRegion,
    LayoutBaseline,
    NetClass,
    PlacementPolicy,
    RoutingPolicy,
    build_layout_baseline,
)

__all__ = [
    "BoardStackup",
    "CriticalNet",
    "FunctionalRegion",
    "LayoutBaseline",
    "NetClass",
    "PlacementPolicy",
    "RoutingPolicy",
    "build_layout_baseline",
]

from .performance import (
    Criticality, CriticalityRecord, EvidenceStatus, GainSettingBudget,
    MarginRecord, PerformanceBaseline, PlacementConstraint,
    build_performance_baseline,
)

__all__ += [
    "Criticality", "CriticalityRecord", "EvidenceStatus",
    "GainSettingBudget", "MarginRecord", "PerformanceBaseline",
    "PlacementConstraint", "build_performance_baseline",
]
from .placement_clusters import (
    BoardKeepout,
    ClusterPlacementBaseline,
    ComponentCluster,
    EdgeAffinity,
    PlacementAuthority,
    build_cluster_placement_baseline,
    validate_cluster_baseline,
)


def build_footprint_contract():
    from .footprint_contract import build_footprint_contract as _build
    return _build()
