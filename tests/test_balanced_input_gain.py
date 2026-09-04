import pytest
from generator.model.balanced_input import (
    CABLE_CAP_MAX_PF,CABLE_CAP_MIN_PF,DESIGN_STATUS,BalancedInputStatus,
    DIFF_CONVERTER_GAIN,GAIN_SETTINGS,GRADO_78C,GRADO_GOLD,
    INPUT_DEFAULT_BOARD_DIFF_CAP_PF,INPUT_DIFFERENTIAL_LOAD_OHM,
    INPUT_DIFF_SHUNT_FITTED,MAX_BOARD_ADDED_RESPONSE_DB_20K,
    board_added_response_db,default_setting,validate_balanced_input,
)

def test_sch101_is_electrically_closed():
    assert DESIGN_STATUS is BalancedInputStatus.ELECTRICALLY_CLOSED
    validate_balanced_input()

def test_three_gain_settings_are_frozen():
    assert [item.target_total_db for item in GAIN_SETTINGS] == [14.0,18.0,22.0]
    assert DIFF_CONVERTER_GAIN == pytest.approx(4.0)

def test_default_gain_matches_downstream_budget():
    assert default_setting().realised_total_db == pytest.approx(18.0,abs=0.06)
    assert default_setting().total_gain == pytest.approx(7.94,rel=0.01)

def test_all_settings_are_close_to_targets():
    assert all(abs(item.error_db)<0.08 for item in GAIN_SETTINGS)

def test_balanced_load_and_default_rf_state():
    assert INPUT_DIFFERENTIAL_LOAD_OHM == pytest.approx(47400.0)
    assert INPUT_DEFAULT_BOARD_DIFF_CAP_PF == pytest.approx(23.5)
    assert INPUT_DIFF_SHUNT_FITTED is False

@pytest.mark.parametrize("cartridge",[GRADO_78C,GRADO_GOLD])
@pytest.mark.parametrize("cable_pf",[CABLE_CAP_MIN_PF,100.0,150.0,200.0,CABLE_CAP_MAX_PF])
def test_board_added_capacitance_stays_below_02db_at_20khz(cartridge,cable_pf):
    delta=abs(board_added_response_db(cartridge,20000.0,cable_pf))
    assert delta < MAX_BOARD_ADDED_RESPONSE_DB_20K
