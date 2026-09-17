from generator.model.precision_cad_contract import (
    GAIN_SERVICE_HEADER_REFS,GAIN_SERVICE_PAIRING_STATUS,
    LOAD_SERVICE_HEADER_REFS,LOAD_SERVICE_PAIRING_STATUS,
    LT5400_CAD_FOOTPRINT_STATUS,LT5400_EXPOSED_PAD_ELECTRICAL,
    LT5400_EXPOSED_PAD_PIN,LT5400_GRADE,LT5400_RATIO,
    LT5400_RESISTOR_PINS,LT5400_TOLERANCE_CMRR_AUTHORITY,
    validate_precision_cad_contract,
)

def test_ae071a_precision_cad_contract():
    validate_precision_cad_contract()

def test_lt5400_7_pin_pairs_are_complete_and_disjoint():
    pins=[p for pair in LT5400_RESISTOR_PINS.values() for p in pair]
    assert len(pins)==8
    assert len(set(pins))==8
    assert set(pins)=={str(i) for i in range(1,9)}

def test_lt5400_current_contract_is_b_grade_run10_open_not_stale_a_grade():
    assert LT5400_RATIO==4.0
    assert LT5400_GRADE=="B_CANDIDATE"
    assert LT5400_TOLERANCE_CMRR_AUTHORITY=="RUN10_OPEN"
    assert LT5400_EXPOSED_PAD_PIN=="9"
    assert LT5400_EXPOSED_PAD_ELECTRICAL=="FLOATING"
    assert LT5400_CAD_FOOTPRINT_STATUS=="FOOTPRINT_BOUND_EP_DISPOSITION_OPEN"

def test_service_headers_encode_park_states_but_keep_pairing_verification_open():
    assert GAIN_SERVICE_HEADER_REFS=={"LOW":"H110","HIGH":"H111","DEFAULT_PARK":"H112"}
    assert LOAD_SERVICE_HEADER_REFS=={"PLUS_47":"H120","BASE_PARK":"H121","PLUS_100":"H122"}
    assert GAIN_SERVICE_PAIRING_STATUS.endswith("_OPEN")
    assert LOAD_SERVICE_PAIRING_STATUS.endswith("_OPEN")
