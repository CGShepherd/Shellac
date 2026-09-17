import pytest
from generator.model.balanced_input import (
    AE037_FIXED_RF_SANITY_CARTRIDGES,AT_VM95SP,BalancedInputStatus,
    CABLE_CAP_MAX_PF,CABLE_CAP_MIN_PF,DESIGN_STATUS,DIFF_CONVERTER_GAIN,
    GAIN_FIXED_RF_OHM,GAIN_HIGH_PARALLEL_RG_OHM,GAIN_LOW_PARALLEL_RF_OHM,
    GAIN_RG_OHM,GAIN_SETTINGS,GRADO_78C,GRADO_GOLD,
    INPUT_DIFFERENTIAL_LOAD_OHM,INPUT_FIXED_BOARD_DIFF_EQUIV_PF,
    MAX_BOARD_ADDED_RESPONSE_DB_20K,SERVICE_CAPACITANCE_PF,
    board_added_response_db,bookkeeping_total_cap_pf,default_setting,
    simultaneous_low_high_gain_db,validate_balanced_input,
)

def test_sch101_ae042_live_implementation_is_qualification_open():
    assert DESIGN_STATUS is BalancedInputStatus.AE042_IMPLEMENTED_QUALIFICATION_OPEN
    validate_balanced_input()

def test_ae042_gain_programming_values_are_live():
    assert GAIN_FIXED_RF_OHM == 999.0
    assert GAIN_RG_OHM == 1000.0
    assert GAIN_LOW_PARALLEL_RF_OHM == 332.0
    assert GAIN_HIGH_PARALLEL_RG_OHM == 866.0
    assert [x.name for x in GAIN_SETTINGS] == ["LOW","DEFAULT","HIGH"]
    assert [x.target_total_db for x in GAIN_SETTINGS] == [14.0,18.0,22.0]
    assert DIFF_CONVERTER_GAIN == pytest.approx(4.0)

def test_default_is_fail_safe_no_active_program_branch():
    d=default_setting()
    assert d.rf_program_ohm is None
    assert d.rg_program_ohm is None
    assert d.realised_total_db == pytest.approx(18.05746,abs=0.001)

def test_all_ae042_settings_are_close_to_targets_and_invalid_both_is_benign():
    assert all(abs(item.error_db)<0.08 for item in GAIN_SETTINGS)
    assert simultaneous_low_high_gain_db() == pytest.approx(15.77429,abs=0.001)

def test_balanced_load_and_service_cap_states():
    assert INPUT_DIFFERENTIAL_LOAD_OHM == pytest.approx(47400.0)
    assert INPUT_FIXED_BOARD_DIFF_EQUIV_PF == pytest.approx(23.5)
    assert SERVICE_CAPACITANCE_PF == {"BASE":0.0,"PLUS_47":47.0,"PLUS_100":100.0}

def test_ae064_cartridge_identity_is_retained_and_at_is_present():
    assert GRADO_78C.name == "Grado Prestige 78C"
    assert AT_VM95SP.resistance_ohm == 485.0
    assert AT_VM95SP.inductance_h == pytest.approx(0.55)
    assert GRADO_GOLD.name.startswith("Grado Gold")
    assert bookkeeping_total_cap_pf(100.0,"BASE") == pytest.approx(123.5)

@pytest.mark.parametrize("cartridge",AE037_FIXED_RF_SANITY_CARTRIDGES)
@pytest.mark.parametrize("cable_pf",[CABLE_CAP_MIN_PF,100.0,150.0,200.0,CABLE_CAP_MAX_PF])
def test_legacy_fixed_rf_board_capacitance_sanity_remains_for_ae037_cases(cartridge,cable_pf):
    delta=abs(board_added_response_db(cartridge,20000.0,cable_pf))
    assert delta < MAX_BOARD_ADDED_RESPONSE_DB_20K
