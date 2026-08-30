from generator.model.precision_cad_contract import (
    LT5400_A_CMRR_MATCHING_MAX_PERCENT,
    LT5400_A_MATCHING_MAX_PERCENT,
    LT5400_CAD_FOOTPRINT_STATUS,
    LT5400_EXPOSED_PAD_ELECTRICAL,
    LT5400_EXPOSED_PAD_PIN,
    LT5400_RATIO,
    LT5400_RESISTOR_PINS,
    SERVICE_LINK_INVALID_PATTERN,
    SERVICE_LINK_PATTERNS,
    validate_precision_cad_contract,
)


def test_ae018_precision_cad_contract():
    validate_precision_cad_contract()


def test_lt5400_7_pin_pairs_are_complete_and_disjoint():
    pins = [p for pair in LT5400_RESISTOR_PINS.values() for p in pair]
    assert len(pins) == 8
    assert len(set(pins)) == 8
    assert set(pins) == {str(i) for i in range(1, 9)}


def test_lt5400_exposed_pad_is_not_an_electrical_resistor_terminal():
    assert LT5400_EXPOSED_PAD_PIN == "9"
    assert LT5400_EXPOSED_PAD_ELECTRICAL == "FLOATING"
    assert all("9" not in pair for pair in LT5400_RESISTOR_PINS.values())


def test_lt5400_7_precision_contract():
    assert LT5400_RATIO == 4.0
    assert LT5400_A_MATCHING_MAX_PERCENT == 0.010
    assert LT5400_A_CMRR_MATCHING_MAX_PERCENT == 0.005


def test_footprint_is_deliberately_not_guessed():
    assert LT5400_CAD_FOOTPRINT_STATUS == "VERIFY_EP_GEOMETRY_BEFORE_BINDING"


def test_service_link_states_are_three_valid_plus_one_prohibited():
    assert SERVICE_LINK_PATTERNS == {"LOW": "00", "DEFAULT": "01", "HIGH": "10"}
    assert SERVICE_LINK_INVALID_PATTERN == "11"
