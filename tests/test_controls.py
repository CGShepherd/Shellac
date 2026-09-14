import pytest
from generator.model.controls import (
    ASSUMED_LED_FORWARD_V, CONTROLS, DESIGN_STATUS, INDICATORS,
    EQ_ROTARY_FAMILY, EQ_ROTARY_MANUFACTURER, EQ_ROTARY_MPN,
    MATRIX_MPN, TOGGLE_MPN, LED_CURRENT_A, LED_MPN, LED_BEZEL_MPN,
    LED_SERIES_RESISTANCE_OHM, ControlsStatus, validate_controls,
)

def test_controls_architecture_is_ae041():
    assert DESIGN_STATUS is ControlsStatus.ARCHITECTURE_SELECTED_PROCUREMENT_PARTIAL
    validate_controls()

def test_control_inventory_is_dual_mono_plus_shared_controls():
    assert [c.identifier for c in CONTROLS] == [
        "SW901L","SW901R","SW902L","SW902R","SW903","SW904","SW905"
    ]
    assert [len(c.positions) for c in CONTROLS] == [5,5,5,5,4,2,2]

def test_eq_controls_are_four_independent_nkk_nr01_family_controls():
    assert all(c.manufacturer == EQ_ROTARY_MANUFACTURER == "NKK" for c in CONTROLS[:4])
    assert all(c.mpn == EQ_ROTARY_MPN for c in CONTROLS[:4])
    assert EQ_ROTARY_FAMILY == "NR01"
    assert [c.channel for c in CONTROLS[:4]] == ["L","R","L","R"]
    assert "TRUE RIAA" in CONTROLS[0].positions
    assert "2121 Hz RIAA" in CONTROLS[2].positions

def test_matrix_and_toggle_authority():
    assert CONTROLS[4].mpn == MATRIX_MPN == "A30403RNCB"
    assert CONTROLS[4].positions == ("DUAL LEFT","STEREO","L+R MONO","DUAL RIGHT")
    assert CONTROLS[5].positions == ("BYPASS","IN")
    assert CONTROLS[6].positions == ("RUN","MUTE")
    assert CONTROLS[5].mpn == CONTROLS[6].mpn == TOGGLE_MPN == "7201SYCBE"

def test_rail_indicators_unchanged():
    assert [i.rail for i in INDICATORS] == ["+18V","-18V"]
    assert all(i.mpn == LED_MPN and i.bezel_mpn == LED_BEZEL_MPN for i in INDICATORS)
    assert LED_SERIES_RESISTANCE_OHM == pytest.approx(8200.0)
    assert ASSUMED_LED_FORWARD_V == pytest.approx(2.4)
    assert LED_CURRENT_A * 1000 == pytest.approx(1.9024, rel=1e-3)
