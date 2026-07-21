import pytest

from generator.model.balanced_input import (
    DESIGN_STATUS,
    BalancedInputStatus,
    DIFF_CONVERTER_GAIN,
    GAIN_SETTINGS,
    default_setting,
    validate_balanced_input,
)


def test_sch101_is_electrically_closed():
    assert DESIGN_STATUS is BalancedInputStatus.ELECTRICALLY_CLOSED
    validate_balanced_input()


def test_three_gain_settings_are_frozen():
    assert [item.target_total_db for item in GAIN_SETTINGS] == [14.0, 18.0, 22.0]
    assert DIFF_CONVERTER_GAIN == pytest.approx(3.48)


def test_default_gain_matches_downstream_budget():
    assert default_setting().realised_total_db == pytest.approx(18.0, abs=0.06)
    assert default_setting().total_gain == pytest.approx(7.94, rel=0.01)


def test_all_settings_are_close_to_targets():
    assert all(abs(item.error_db) < 0.08 for item in GAIN_SETTINGS)
