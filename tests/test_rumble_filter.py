import pytest

from generator.model.rumble_filter import (
    DESIGN_STATUS,
    FILTER_ORDER,
    RumbleFilterStatus,
    SECTIONS,
    TARGET_CUTOFF_HZ,
    magnitude_db,
    validate_rumble_filter,
)
from generator.model.rumble_filter_analysis import (
    approximate_group_delay_seconds,
    response_points,
)


def test_rumble_filter_is_electrically_closed():
    assert DESIGN_STATUS is RumbleFilterStatus.ELECTRICALLY_CLOSED
    validate_rumble_filter()


def test_filter_order_and_section_values_are_frozen():
    assert FILTER_ORDER == 4
    assert TARGET_CUTOFF_HZ == pytest.approx(15.0)
    assert len(SECTIONS) == 2
    assert SECTIONS[0].r1_ohm == pytest.approx(20_800.0)
    assert SECTIONS[0].r2_ohm == pytest.approx(24_300.0)
    assert SECTIONS[1].r1_ohm == pytest.approx(8_660.0)
    assert SECTIONS[1].r2_ohm == pytest.approx(59_000.0)


def test_wanted_band_is_preserved():
    assert magnitude_db(20.0) == pytest.approx(-0.4596, abs=0.01)
    assert magnitude_db(30.0) > -0.05
    assert magnitude_db(50.0) > -0.02


def test_infrasonic_rejection_is_material():
    assert magnitude_db(10.0) < -14.0
    assert magnitude_db(5.0) < -38.0
    assert magnitude_db(1.0) < -94.0
    assert magnitude_db(0.55) < -110.0


def test_response_report_has_expected_points():
    points = response_points()
    frequencies = {point.frequency_hz for point in points}
    assert {0.55, 5.0, 10.0, 20.0, 50.0, 1000.0, 20_000.0}.issubset(frequencies)


def test_group_delay_falls_above_cutoff():
    assert approximate_group_delay_seconds(20.0) > approximate_group_delay_seconds(50.0)
    assert approximate_group_delay_seconds(50.0) > approximate_group_delay_seconds(100.0)
