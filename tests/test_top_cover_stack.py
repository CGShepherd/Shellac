import pytest
from generator.mechanical.top_cover_stack import (
    CK_STACK,
    GRAYHILL_STACK,
    TOP_COVER_NOMINAL_MM,
    TOP_COVER_TOLERANCE_MM,
    validate_top_cover_stack,
)


def test_nominal_cover_thickness_is_controlled_but_tolerance_is_not_invented():
    assert TOP_COVER_NOMINAL_MM == 2.0
    assert TOP_COVER_TOLERANCE_MM is None


def test_selected_switch_bushings_protrude_through_nominal_cover():
    validate_top_cover_stack()
    assert GRAYHILL_STACK.thread_available_above_cover_mm == pytest.approx(5.92)
    assert CK_STACK.thread_available_above_cover_mm == pytest.approx(6.89)


def test_machining_remains_gated():
    assert GRAYHILL_STACK.machining_released is False
    assert CK_STACK.machining_released is False
    assert GRAYHILL_STACK.final_hardware_stack_verified is False
    assert CK_STACK.final_hardware_stack_verified is False
