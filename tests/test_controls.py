import pytest

from generator.model.controls import (
    CONTROLS,
    DESIGN_STATUS,
    INDICATORS,
    LED_CURRENT_A,
    LED_SERIES_RESISTANCE_OHM,
    ControlsStatus,
    validate_controls,
)


def test_controls_are_electrically_closed():
    assert DESIGN_STATUS is ControlsStatus.ELECTRICALLY_CLOSED
    validate_controls()


def test_external_control_inventory_is_frozen():
    assert [control.identifier for control in CONTROLS] == [
        "SW901", "SW902", "SW903", "SW904", "SW905"
    ]
    assert [len(control.positions) for control in CONTROLS] == [5, 5, 4, 2, 2]


def test_bass_and_treble_are_independent_linked_stereo_controls():
    assert CONTROLS[0].control_type == "2P5 rotary"
    assert CONTROLS[1].control_type == "2P5 rotary"
    assert "TRUE RIAA" in CONTROLS[0].positions
    assert "2121 Hz RIAA" in CONTROLS[1].positions


def test_rail_indicators_are_independent():
    assert [indicator.rail for indicator in INDICATORS] == ["+18V", "-18V"]
    assert all(indicator.resistor_ohm == pytest.approx(8200.0) for indicator in INDICATORS)


def test_led_current_is_about_two_milliamps():
    assert LED_SERIES_RESISTANCE_OHM == pytest.approx(8200.0)
    assert LED_CURRENT_A * 1000 == pytest.approx(1.9512, rel=1e-3)
