from generator.model.rotary_switch_procurement_gate import (
    FAMILY, BASE_SWITCH_MPN, BASS_MPN, TREBLE_MPN,
    ELECTRICAL, MECHANICAL, BASS_KNOB_COLOUR, TREBLE_KNOB_COLOUR,
    VERTICAL_STACK_STATUS, FOOTPRINT_STATUS, validate_procurement_gate,
)

def test_ae075c_procurement_gate():
    validate_procurement_gate()

def test_current_gate_is_nkk_not_historical_lorlin():
    assert FAMILY == "NKK NR01"
    assert BASE_SWITCH_MPN == "NR01105ANG13"
    assert BASS_MPN == "NR01105ANG13-2C"
    assert TREBLE_MPN == "NR01105ANG13-2A"

def test_nkk_electrical_contract():
    assert ELECTRICAL["positions"] == 5
    assert ELECTRICAL["poles"] == 1
    assert ELECTRICAL["action"] == "BBM_NON_SHORTING"
    assert ELECTRICAL["contact_finish"] == "gold"

def test_nkk_mechanical_contract_is_not_threaded_bushing():
    assert MECHANICAL["threaded_bushing"] is False
    assert MECHANICAL["knob_family"] == "AT3009"
    assert MECHANICAL["knob_mount"] == "FLANGE_BENEATH_PANEL"
    assert BASS_KNOB_COLOUR == "RED"
    assert TREBLE_KNOB_COLOUR == "BLACK"
    assert VERTICAL_STACK_STATUS.startswith("OPEN")
    assert FOOTPRINT_STATUS.startswith("OPEN")
