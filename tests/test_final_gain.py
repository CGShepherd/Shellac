import pytest
from generator.model.final_gain import (
    DESIGN_STATUS, FinalGainStatus, GAIN_DB, GAIN_LINEAR,
    NOMINAL_INPUT_RMS_V, SEVERE_INPUT_RMS_V, gain_budget,
    validate_final_gain_stage,
)

def test_final_gain_stage_is_electrically_closed():
    assert DESIGN_STATUS is FinalGainStatus.ELECTRICALLY_CLOSED
    validate_final_gain_stage()

def test_sch104_is_unity_after_that1646_selection():
    assert GAIN_LINEAR == pytest.approx(1.0)
    assert GAIN_DB == pytest.approx(0.0)

def test_nominal_output_is_unchanged():
    assert gain_budget(NOMINAL_INPUT_RMS_V).output_rms_v == pytest.approx(0.321)

def test_severe_case_retains_more_than_9_8_db_margin():
    b=gain_budget(SEVERE_INPUT_RMS_V)
    assert b.output_rms_v == pytest.approx(3.21)
    assert b.margin_to_design_ceiling_db > 9.8

def test_negative_input_is_rejected():
    with pytest.raises(ValueError):
        gain_budget(-0.1)
