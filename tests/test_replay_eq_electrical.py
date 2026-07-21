import pytest

from generator.model.replay_eq import (
    DESIGN_STATUS,
    EqValueStatus,
    RECOVERY_GAIN,
    RECOVERY_RF_OHM,
    RECOVERY_RG_OHM,
)
from generator.model.replay_eq_electrical import (
    closure_points,
    johnson_noise_nv_per_rt_hz,
    validate_electrical_closure,
    worst_case_point,
)


def test_sch103_is_electrically_closed():
    assert DESIGN_STATUS is EqValueStatus.ELECTRICALLY_CLOSED
    validate_electrical_closure()


def test_recovery_stage_values_are_frozen():
    assert RECOVERY_RG_OHM == pytest.approx(10_000.0)
    assert RECOVERY_RF_OHM == pytest.approx(11_000.0)
    assert RECOVERY_GAIN == pytest.approx(2.1)


def test_conservative_overload_margin_exceeds_30_mv_at_cartridge():
    assert worst_case_point().max_cartridge_input_rms_v > 0.030


def test_closure_table_covers_historical_and_riaa_modes():
    points = closure_points()
    assert any(point.curve_name == "TRUE RIAA" for point in points)
    assert {point.frequency_hz for point in points} == {20.0, 50.0, 1000.0, 20_000.0}


def test_johnson_noise_reference_values():
    assert johnson_noise_nv_per_rt_hz(100_000.0) == pytest.approx(40.70, rel=0.01)
    assert johnson_noise_nv_per_rt_hz(750.0) == pytest.approx(3.52, rel=0.02)
