from generator.model.precision_cad_contract import *

def test_ae076c_precision_contract():
    validate_precision_cad_contract()

def test_lt5400_contract_matches_live_ae075b():
    assert LT5400_MPN=="LT5400BIMS8E-7#PBF"
    assert LT5400_GRADE=="B_SELECTED"
    assert LT5400_EXPOSED_PAD_PIN=="9"
    assert LT5400_EXPOSED_PAD_ELECTRICAL=="QUIET_0VA"
    assert LT5400_CAD_FOOTPRINT_STATUS=="EXACT_MPN_SELECTED_EP9_IMPLEMENTED"
    assert LT5400_TOLERANCE_CMRR_AUTHORITY=="RUN10_OPEN"

def test_gain_hardware_retained():
    assert GAIN_SERVICE_HEADER_REFS=={"LOW":"H110","HIGH":"H111","DEFAULT_PARK":"H112"}
    assert GAIN_SERVICE_PAIRING_STATUS.endswith("_OPEN")

def test_personality_interface_selected_next_not_falsely_live():
    assert LOAD_PERSONALITY_ARCHITECTURE=="TWO_IDENTICAL_PER_CHANNEL_PASSIVE_CARDS"
    assert LOAD_PERSONALITY_IMPLEMENTATION_STATUS=="SELECTED_NEXT_PENDING_LIVE_MIGRATION"
    assert LOAD_PERSONALITY_MAIN_SOCKET_MPN=="Samtec SLW-102-01-G-D"
    assert LOAD_PERSONALITY_CARD_HEADER_MPN=="Samtec TSW-102-07-G-D"
    assert LOAD_PERSONALITY_SELECTED_REFS=={"L":"H120","R":"H220"}
    assert LOAD_PERSONALITY_PIN_NODES=={1:"POS",2:"NEG",3:"NEG",4:"POS"}
    assert "BASE_NO_CARD" in LOAD_PERSONALITY_STATES
    assert LOAD_PERSONALITY_PARASITIC_AUTHORITY=="RUN10_OPEN"
