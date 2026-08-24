import pytest

from generator.mechanical.control_hardware import (
    CK_7201SYCBE,
    EXTERNAL_CONTROL_CONTRACTS,
    GRAYHILL_1_DECK,
    GRAYHILL_2_DECK,
    LED_BEZEL,
    validate_control_mechanical_evidence,
)


def test_control_mechanical_evidence_is_coherent():
    validate_control_mechanical_evidence()


def test_grayhill_family_preserves_common_front_interface():
    assert GRAYHILL_1_DECK.shaft_diameter_mm == GRAYHILL_2_DECK.shaft_diameter_mm
    assert GRAYHILL_1_DECK.shaft_projection_mm == GRAYHILL_2_DECK.shaft_projection_mm
    assert GRAYHILL_1_DECK.bushing_thread == GRAYHILL_2_DECK.bushing_thread
    assert (
        GRAYHILL_2_DECK.behind_panel_depth_mm
        - GRAYHILL_1_DECK.behind_panel_depth_mm
    ) == pytest.approx(5.54)


def test_toggle_and_led_panel_cutouts_are_controlled_but_not_released():
    assert CK_7201SYCBE.panel_cutout_mm == 6.35
    assert LED_BEZEL.panel_cutout_mm == 6.30
    assert all(
        item.manufacturing_released is False
        for item in EXTERNAL_CONTROL_CONTRACTS
    )