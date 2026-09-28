import pytest
from generator.model.controls import (
    ASSUMED_LED_FORWARD_V, CONTROLS, DESIGN_STATUS, INDICATORS,
    EQ_ROTARY_FAMILY, EQ_ROTARY_MANUFACTURER, EQ_ROTARY_BASE_MPN,
    EQ_BASS_MPN, EQ_TREBLE_MPN, EQ_ROTARY_MOUNTING,
    MATRIX_MPN, TOGGLE_MPN, LED_CURRENT_A, LED_MPN, LED_BEZEL_MPN,
    LED_SERIES_RESISTANCE_OHM, ControlsStatus, validate_controls,
)

def test_controls_architecture_is_ae075c_hardware_selected():
    assert DESIGN_STATUS is ControlsStatus.PHYSICAL_HARDWARE_SELECTED
    validate_controls()

def test_control_inventory_is_dual_mono_plus_shared_controls():
    assert [c.identifier for c in CONTROLS] == [
        "SW901L","SW901R","SW902L","SW902R","SW903","SW904","SW905"
    ]
    assert [len(c.positions) for c in CONTROLS] == [5,5,5,5,4,2,2]

def test_eq_controls_are_exact_nkk_nr01_flanged_knob_variants():
    assert EQ_ROTARY_FAMILY == "NR01"
    assert EQ_ROTARY_BASE_MPN == "NR01105ANG13"
    assert EQ_BASS_MPN == "NR01105ANG13-2C"
    assert EQ_TREBLE_MPN == "NR01105ANG13-2A"
    assert [c.mpn for c in CONTROLS[:4]] == [
        EQ_BASS_MPN, EQ_BASS_MPN, EQ_TREBLE_MPN, EQ_TREBLE_MPN
    ]
    assert all(c.manufacturer == EQ_ROTARY_MANUFACTURER == "NKK" for c in CONTROLS[:4])
    assert [c.channel for c in CONTROLS[:4]] == ["L","R","L","R"]
    assert all(c.mounting == EQ_ROTARY_MOUNTING for c in CONTROLS[:4])
    assert all("no threaded bushing" in c.mounting for c in CONTROLS[:4])
    assert "TRUE RIAA" in CONTROLS[0].positions
    assert "2121 Hz RIAA" in CONTROLS[2].positions

def test_matrix_and_toggle_authority():
    assert CONTROLS[4].mpn == MATRIX_MPN == "A30403RNCB"
    assert "3/8-32" in CONTROLS[4].mounting
    assert CONTROLS[4].positions == ("DUAL LEFT","STEREO","L+R MONO","DUAL RIGHT")
    assert CONTROLS[5].positions == ("BYPASS","IN")
    assert CONTROLS[6].positions == ("RUN","MUTE")
    assert CONTROLS[5].mpn == CONTROLS[6].mpn == TOGGLE_MPN == "7201SYCBE"
    assert all("1/4-40" in c.mounting for c in CONTROLS[5:])

def test_rail_indicators_unchanged():
    assert [i.rail for i in INDICATORS] == ["+18V","-18V"]
    assert all(i.mpn == LED_MPN and i.bezel_mpn == LED_BEZEL_MPN for i in INDICATORS)
    assert LED_SERIES_RESISTANCE_OHM == pytest.approx(8200.0)
    assert ASSUMED_LED_FORWARD_V == pytest.approx(2.4)
    assert LED_CURRENT_A * 1000 == pytest.approx(1.9024, rel=1e-3)

def test_ae059_sw905_selected_mechanical_mute_contract():
    mute = next(control for control in CONTROLS if control.identifier == "SW905")
    assert mute.control_type == "DPDT toggle"
    assert mute.mpn == "7201SYCBE"
    desc = mute.electrical_function.lower()
    assert "that1646" in desc
    assert "0va" in desc
    assert "no relay/timer/comparator" in desc

def test_ae059_balanced_output_source_keeps_mechanical_input_mute():
    from pathlib import Path
    text = Path("generator/blocks/balanced_output.py").read_text(encoding="utf-8")
    assert "Select MODE_L/R or 0VA into each THAT1646 input" in text
    assert "Both line-driver inputs connected to 0VA" in text
