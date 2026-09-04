import pytest

from generator.mechanical.control_hardware import (
    CK_7201SYCBE,
    EXTERNAL_CONTROL_CONTRACTS,
    GRAYHILL_1_DECK,
    GRAYHILL_2_DECK,
    HISTORICAL_ROTARY_EVIDENCE,
    LED_BEZEL,
    ROTARY_PLATFORM_AUTHORITY,
    validate_control_mechanical_evidence,
)


def test_control_mechanical_evidence_is_coherent():
    validate_control_mechanical_evidence()


def test_grayhill_geometry_is_preserved_as_rejected_historical_evidence_only():
    assert GRAYHILL_1_DECK in HISTORICAL_ROTARY_EVIDENCE
    assert GRAYHILL_2_DECK in HISTORICAL_ROTARY_EVIDENCE
    assert GRAYHILL_1_DECK not in EXTERNAL_CONTROL_CONTRACTS
    assert GRAYHILL_2_DECK not in EXTERNAL_CONTROL_CONTRACTS
    assert "REJECTED" in GRAYHILL_1_DECK.notes
    assert "REJECTED" in GRAYHILL_2_DECK.notes
    assert GRAYHILL_1_DECK.shaft_diameter_mm == GRAYHILL_2_DECK.shaft_diameter_mm
    assert GRAYHILL_1_DECK.shaft_projection_mm == GRAYHILL_2_DECK.shaft_projection_mm
    assert GRAYHILL_1_DECK.bushing_thread == GRAYHILL_2_DECK.bushing_thread
    assert (
        GRAYHILL_2_DECK.behind_panel_depth_mm
        - GRAYHILL_1_DECK.behind_panel_depth_mm
    ) == pytest.approx(5.54)


def test_lorlin_pt_is_current_rotary_platform_authority_with_procurement_open():
    assert ROTARY_PLATFORM_AUTHORITY["manufacturer"] == "Lorlin"
    assert ROTARY_PLATFORM_AUTHORITY["family"] == "PT"
    assert "OPEN" in ROTARY_PLATFORM_AUTHORITY["status"]
    assert "AE-026" in ROTARY_PLATFORM_AUTHORITY["authority"]
    assert "AE-027" in ROTARY_PLATFORM_AUTHORITY["authority"]


def test_toggle_and_led_panel_cutouts_are_controlled_but_not_released():
    assert CK_7201SYCBE.panel_cutout_mm == 6.35
    assert LED_BEZEL.panel_cutout_mm == 6.30
    assert all(
        item.manufacturing_released is False
        for item in HISTORICAL_ROTARY_EVIDENCE + EXTERNAL_CONTROL_CONTRACTS
    )
