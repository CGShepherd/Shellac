import pytest

from generator.model.controls import (
    ASSUMED_LED_FORWARD_V,
    CONTROLS,
    DESIGN_STATUS,
    INDICATORS,
    LED_BEZEL_MPN,
    LED_CURRENT_A,
    LED_MPN,
    LED_SERIES_RESISTANCE_OHM,
    ROTARY_BASS_TREBLE_MPN,
    ROTARY_MODE_MPN,
    TOGGLE_MPN,
    ControlsStatus,
    validate_controls,
)


def test_controls_are_physically_selected():
    assert DESIGN_STATUS is ControlsStatus.PHYSICAL_HARDWARE_SELECTED
    validate_controls()


def test_external_control_inventory_is_frozen():
    assert [control.identifier for control in CONTROLS] == [
        "SW901",
        "SW902",
        "SW903",
        "SW904",
        "SW905",
    ]
    assert [len(control.positions) for control in CONTROLS] == [5, 5, 4, 2, 2]


def test_bass_and_treble_electrical_functions_are_preserved():
    assert "TRUE RIAA" in CONTROLS[0].positions
    assert "2121 Hz RIAA" in CONTROLS[1].positions
    assert "Linked stereo" in CONTROLS[0].electrical_function
    assert "Linked stereo" in CONTROLS[1].electrical_function
    assert CONTROLS[0].switching == "Break-before-make"
    assert CONTROLS[1].switching == "Break-before-make"


def test_mode_electrical_requirement_is_preserved():
    assert CONTROLS[2].positions == (
        "STEREO",
        "DUAL LEFT",
        "DUAL RIGHT",
        "L+R MONO",
    )
    assert "passive routing and mono-averaging matrix" in CONTROLS[2].electrical_function
    assert CONTROLS[2].switching == "Break-before-make"


def test_selected_rotary_hardware_is_overcapable_but_configured_to_required_states():
    assert CONTROLS[0].control_type == "2P6 rotary configured to 5 positions"
    assert CONTROLS[1].control_type == "2P6 rotary configured to 5 positions"
    assert CONTROLS[2].control_type == "4P6 rotary configured to 4 positions"
    assert CONTROLS[0].mpn == CONTROLS[1].mpn == ROTARY_BASS_TREBLE_MPN
    assert CONTROLS[2].mpn == ROTARY_MODE_MPN
    assert all(control.manufacturer == "Grayhill" for control in CONTROLS[:3])


def test_toggle_hardware_is_common_and_retains_two_state_functions():
    assert CONTROLS[3].positions == ("FILTER", "BYPASS")
    assert CONTROLS[4].positions == ("PLAY", "MUTE")
    assert CONTROLS[3].mpn == CONTROLS[4].mpn == TOGGLE_MPN
    assert CONTROLS[3].manufacturer == CONTROLS[4].manufacturer == "C&K"
    assert CONTROLS[3].switching == "Break-before-make"
    assert CONTROLS[4].switching == "Break-before-make"


def test_external_controls_are_secondary_structural_connections():
    assert all("PCB through-hole" in control.mounting for control in CONTROLS)
    assert all("secondary structural connection" in control.mounting for control in CONTROLS)


def test_rail_indicators_are_independent_and_common():
    assert [indicator.rail for indicator in INDICATORS] == ["+18V", "-18V"]
    assert all(
        indicator.resistor_ohm == pytest.approx(8200.0)
        for indicator in INDICATORS
    )
    assert all(indicator.mpn == LED_MPN for indicator in INDICATORS)
    assert all(indicator.bezel_mpn == LED_BEZEL_MPN for indicator in INDICATORS)
    assert all(
        "central longitudinal spine" in indicator.mounting
        for indicator in INDICATORS
    )


def test_selected_led_current_is_low():
    assert LED_SERIES_RESISTANCE_OHM == pytest.approx(8200.0)
    assert ASSUMED_LED_FORWARD_V == pytest.approx(2.4)
    assert LED_CURRENT_A * 1000 == pytest.approx(1.9024, rel=1e-3)
