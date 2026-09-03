from generator.model.rotary_switch_procurement_gate import (
    STANDARD_BASS_TREBLE_MPN,
    STANDARD_BASS_TREBLE,
    PRODUCTION_BASS_TREBLE_MPN,
    CHANNEL,
    CONTACT_RESISTANCE_INITIAL_MAX_MOHM,
    validate_procurement_gate,
)

def test_ae027_procurement_gate():
    validate_procurement_gate()

def test_standard_pt6004_is_not_misrepresented_as_gold():
    assert STANDARD_BASS_TREBLE_MPN == "PT6004"
    assert STANDARD_BASS_TREBLE["contact_finish"] == "standard silver"

def test_gold_production_mpn_remains_open_until_manufacturer_confirmation():
    assert PRODUCTION_BASS_TREBLE_MPN.startswith("OPEN")
    assert CHANNEL["mpn"].startswith("OPEN")

def test_pt_datasheet_contact_resistance_limit():
    assert CONTACT_RESISTANCE_INITIAL_MAX_MOHM == 20.0
