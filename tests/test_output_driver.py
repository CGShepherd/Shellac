import pytest
from generator.model.output_driver import (
    DESIGN_STATUS, DIFFERENTIAL_GAIN_DB, DIFFERENTIAL_GAIN_LINEAR,
    NOMINAL_INPUT_RMS_V, OutputDriverStatus, SEVERE_INPUT_RMS_V,
    output_budget, validate_output_driver,
)

def test_output_driver_is_electrically_closed():
    assert DESIGN_STATUS is OutputDriverStatus.ELECTRICALLY_CLOSED
    validate_output_driver()

def test_that1646_gain_is_frozen():
    assert DIFFERENTIAL_GAIN_LINEAR == pytest.approx(2.0)
    assert DIFFERENTIAL_GAIN_DB == pytest.approx(6.020599913, rel=1e-9)

def test_nominal_balanced_output_is_642_mv():
    assert output_budget(NOMINAL_INPUT_RMS_V).differential_output_rms_v == pytest.approx(0.642)

def test_severe_balanced_output_retains_margin():
    result=output_budget(SEVERE_INPUT_RMS_V)
    assert result.differential_output_rms_v == pytest.approx(6.42)
    assert result.margin_to_design_ceiling_db > 3.8

def test_negative_input_is_rejected():
    with pytest.raises(ValueError):
        output_budget(-0.1)
