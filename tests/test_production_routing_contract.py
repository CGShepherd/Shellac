from generator.layout.production_routing_contract import (
    CRITICAL_MANUAL_NET_GROUPS,
    LAYERS,
    ROUTING_HOLDS,
    RULES,
    validate_production_routing_contract,
)

def test_ae032_routing_contract_is_valid():
    validate_production_routing_contract()

def test_in1_is_the_only_continuous_reference_plane():
    refs = [x.layer for x in LAYERS if x.continuous_reference]
    assert refs == ["In1.Cu"]

def test_rotary_geometry_is_explicitly_held():
    assert any("Bass" in x for x in ROUTING_HOLDS)
    assert any("Treble" in x for x in ROUTING_HOLDS)
    assert any("Channel" in x for x in ROUTING_HOLDS)

def test_critical_nets_remain_manual():
    assert len(CRITICAL_MANUAL_NET_GROUPS) >= 7
    assert any("Autorouting is prohibited" in x for x in RULES)
