from generator.layout.ghost_placement import (
    SensitivityClass,
    build_ghost_placement_baseline,
    validate_ghost_placement,
)


def test_ghost_placement_contains_all_sixteen_clusters():
    model = build_ghost_placement_baseline()
    assert len(model.clusters) == 16
    assert len({cluster.identifier for cluster in model.clusters}) == 16


def test_ghost_placement_respects_board_and_architecture_invariants():
    model = build_ghost_placement_baseline()
    assert validate_ghost_placement(model) == []
    micro = [c for c in model.clusters if c.sensitivity == SensitivityClass.MICROVOLT]
    assert {c.identifier for c in micro} == {"CLU-101-A", "CLU-101-C"}
    assert all(c.harness_edge == "front" for c in micro)


def test_power_cluster_is_rear_edge_and_thermally_identified():
    model = build_ghost_placement_baseline()
    power = next(c for c in model.clusters if c.identifier == "CLU-106")
    assert power.harness_edge == "rear"
    assert power.thermal.value == "moderate"


def test_ghost_export_is_explicitly_non_manufacturing():
    model = build_ghost_placement_baseline()
    assert "not for manufacture" in model.status.lower()
    assert all(cluster.member_count > 0 for cluster in model.clusters)
