from generator.core.sheet import Sheet
from generator.dispatch import shellac_builder_registry
from generator.layout.placement_clusters import (
    EdgeAffinity,
    PlacementAuthority,
    build_cluster_placement_baseline,
)


def _on_board_refs():
    registry = shellac_builder_registry()
    refs = set()
    for block_id in registry.registered_ids():
        registration = registry.resolve(block_id)
        sheet = Sheet(registration.title, f"{block_id}.kicad_sch")
        registration.builder(sheet)
        refs.update(component.ref for component in sheet.components if component.on_board)
    return refs


def test_every_on_board_reference_has_exactly_one_cluster_owner():
    model = build_cluster_placement_baseline()
    clustered = [ref for cluster in model.clusters for ref in cluster.member_refs]
    interfaces = [ref for cluster in model.clusters for ref in cluster.interface_refs]
    assert len(clustered + interfaces) == len(set(clustered + interfaces))
    assert set(clustered) == _on_board_refs()
    assert {"SW3001", "SW501", "SW801", "SW901", "J8001", "J9001"} <= set(interfaces)


def test_manual_clusters_dominate_sensitive_signal_path():
    model = build_cluster_placement_baseline()
    manual = [c for c in model.clusters if c.authority is PlacementAuthority.MANUAL]
    assert len(manual) >= 14
    assert all(c.authority is PlacementAuthority.MANUAL for c in model.clusters if c.sheet_id in {"SCH101", "SCH103", "SCH107", "SCH108"})


def test_input_output_and_power_edge_affinities_are_preserved():
    model = build_cluster_placement_baseline()
    right = {c.identifier for c in model.clusters if c.edge_affinity is EdgeAffinity.RIGHT}
    left = {c.identifier for c in model.clusters if c.edge_affinity is EdgeAffinity.LEFT}
    assert {"CLU-101-A", "CLU-101-C"} <= right
    assert {"CLU-108-L", "CLU-108-R", "CLU-106"} <= left


def test_critical_loop_limits_are_no_larger_than_architecture_rules():
    model = build_cluster_placement_baseline()
    by_id = {c.identifier: c for c in model.clusters}
    assert by_id["CLU-101-B"].maximum_cluster_span_mm <= 32.0
    assert by_id["CLU-103-LF-L"].routing_handoff.startswith("Manual")
    assert "5 mm" in by_id["CLU-108-L"].adjacency_rule


def test_cluster_precedence_is_acyclic_and_resolvable():
    model = build_cluster_placement_baseline()
    ids = {c.identifier for c in model.clusters}
    assert all(set(c.precedence_after) <= ids for c in model.clusters)


def test_exact_xy_export_is_explicitly_deferred():
    model = build_cluster_placement_baseline()
    assert "PROVISIONAL" in model.status
    assert any("Exact XY" in rule for rule in model.export_rules)
