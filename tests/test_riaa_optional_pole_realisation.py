from math import pi

import pytest

from generator.model.riaa_optional_pole_realisation import (
    CAP_33_MPN,
    CAP_68_MPN,
    GAIN,
    REALISATION,
    STATUS,
    SWITCH_MPN,
    RealisationStatus,
    gain_db,
    magnitude,
    max_section_input_rms_v,
    output_noise_proxy_1khz_nv_rt_hz,
    pole_hz,
    reference_error_db,
    reference_gain_bounds_db,
    time_constant_s,
    timing_pole_bounds_hz,
    transfer,
    validate_realisation,
)


def test_realisation_is_electrically_frozen_but_not_manufacturing_released():
    assert STATUS is RealisationStatus.ELECTRICALLY_FROZEN
    validate_realisation()
    assert REALISATION.manufacturing_released is False


def test_nominal_3180us_timing_is_close():
    assert time_constant_s() * 1e6 == pytest.approx(3181.5)
    assert pole_hz() == pytest.approx(50.0251, abs=0.001)


def test_reference_gain_is_effectively_unity():
    assert reference_error_db() == pytest.approx(0.00489, abs=0.0002)
    assert magnitude(1000.0) == pytest.approx(1.00056, rel=2e-4)


def test_selected_transfer_is_non_inverting_first_order_low_pass():
    for frequency_hz in (20.0, 50.0, 1000.0, 20_000.0):
        s = 1j * 2.0 * pi * frequency_hz
        assert transfer(s).real > 0 or transfer(s).imag < 0
    assert gain_db(20.0) > 25.3
    assert gain_db(20_000.0) < -25.9


def test_component_tolerances_remain_controlled():
    low, high = timing_pole_bounds_hz()
    assert low == pytest.approx(49.48, abs=0.05)
    assert high == pytest.approx(50.58, abs=0.05)
    gain_low, gain_high = reference_gain_bounds_db()
    assert gain_low > -0.12
    assert gain_high < 0.13


def test_noise_and_headroom_proxies_are_acceptable():
    assert output_noise_proxy_1khz_nv_rt_hz() < 110.0
    assert max_section_input_rms_v(20.0) > 0.53
    assert max_section_input_rms_v(1000.0) > 9.9


def test_selected_parts_match_foundry_trade():
    assert REALISATION.op_amp_mpn == "OPA1656"
    assert SWITCH_MPN == "ASE2D-2M-10-Z"
    assert CAP_68_MPN == "C1206C683F5GECAUTO7210"
    assert CAP_33_MPN == "C1206C333F5GEC7210"
    assert GAIN == pytest.approx(20.0262172)
