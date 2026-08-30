from generator.layout.sr041_routing_release import build_sr041_routing_release

def test_sr041_releases_routing_without_mounting_collisions():
    gate=build_sr041_routing_release()
    assert gate.status=="ROUTING_RELEASED"
    assert gate.board_width_mm==220.0
    assert gate.board_depth_mm==140.0
    assert gate.mounting_hole_count==4
    assert gate.mounting_collision_count==0

def test_sr041_accepts_every_manual_cluster_as_controlled_baseline():
    gate=build_sr041_routing_release()
    assert gate.manual_cluster_count>0
    assert len(gate.accepted_clusters)==gate.manual_cluster_count
    assert all(item.status=="ACCEPTED_AS_ROUTING_BASELINE" for item in gate.accepted_clusters)
    assert all("LOCAL_REFINEMENT" in item.movement_authority for item in gate.accepted_clusters)

def test_sr041_retains_manual_critical_net_authority():
    gate=build_sr041_routing_release()
    assert gate.manual_only_net_count>=7
    joined=" ".join(gate.routing_rules)
    assert "LT5400" in joined
    assert "THAT1646" in joined
    assert "autorouter" in joined
