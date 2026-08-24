from math import pi

import pytest

from generator.model.riaa_optional_pole import (
    CONTRACT,
    CURRENT_C_F,
    OptionalPoleStatus,
    STATUS,
    architecture_transfer,
    canonical_riaa_transfer,
    current_single_rc_breaks_hz,
    riaa_core_transfer,
    scaled_single_rc_breaks_hz,
    single_rc_break_ratio,
    validate_optional_pole_contract,
)


def test_optional_pole_architecture_has_advanced_to_component_freeze():
    assert STATUS is OptionalPoleStatus.CIRCUIT_REALISATION_FROZEN
    validate_optional_pole_contract()
    assert CONTRACT.exact_switch_mpn_frozen is True
    assert CONTRACT.exact_rc_realisation_frozen is True


def test_enabled_architecture_exactly_factorises_canonical_riaa():
    for frequency_hz in (10.0, 20.0, 50.0, 500.0, 1000.0, 2122.0, 20_000.0):
        s = 1j * 2.0 * pi * frequency_hz
        assert architecture_transfer(s, pole_enabled=True) == pytest.approx(
            canonical_riaa_transfer(s), rel=1e-12, abs=1e-12
        )


def test_bypass_preserves_318_75_core_exactly():
    for frequency_hz in (20.0, 50.0, 500.0, 1000.0, 20_000.0):
        s = 1j * 2.0 * pi * frequency_hz
        assert architecture_transfer(s, pole_enabled=False) == pytest.approx(
            riaa_core_transfer(s), rel=1e-12, abs=1e-12
        )


def test_current_single_rc_branch_is_about_50_and_500_hz():
    pole, zero = current_single_rc_breaks_hz()
    assert pole == pytest.approx(50.05, abs=0.15)
    assert zero == pytest.approx(500.5, abs=1.5)


def test_changing_single_capacitor_moves_pole_and_zero_together():
    base_ratio = single_rc_break_ratio()
    for factor in (0.5, 2.0, 10.0):
        pole, zero = scaled_single_rc_breaks_hz(CURRENT_C_F * factor)
        assert zero / pole == pytest.approx(base_ratio, rel=1e-12)


def test_stereo_bypass_needs_two_linked_signal_paths():
    assert CONTRACT.channels == 2
    assert CONTRACT.minimum_linked_switch_paths == 2
    assert "straight-through" in CONTRACT.bypass_state
