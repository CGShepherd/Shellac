from generator.mechanical.top_cover_stack import (
    CK_MATRIX_STACK, CK_TOGGLE_STACK, DIRECT_MAIN_PCB_SELECTED,
    MAIN_PCB_SUPPORT_COUNT, MCAD_STACK_PROOF_REQUIRED, NKK_EQ_STACK,
    SUPPORT_XY_FROZEN, SUPPORT_Z_TOLERANCE_STACK_FROZEN,
    TOP_COVER_NOMINAL_MM, TOP_COVER_TOLERANCE_MM, validate_top_cover_stack,
)

def test_top_cover_stack_remains_unreleased():
    validate_top_cover_stack()
    assert TOP_COVER_NOMINAL_MM==2.0
    assert TOP_COVER_TOLERANCE_MM is None
    assert DIRECT_MAIN_PCB_SELECTED is True
    assert MAIN_PCB_SUPPORT_COUNT==6
    assert SUPPORT_XY_FROZEN is False
    assert SUPPORT_Z_TOLERANCE_STACK_FROZEN is False
    assert MCAD_STACK_PROOF_REQUIRED is True

def test_nkk_plane_is_controlled_but_ck_planes_are_not_invented():
    assert NKK_EQ_STACK.installed_panel_to_pcb_mm==12.3
    assert CK_MATRIX_STACK.installed_panel_to_pcb_mm is None
    assert CK_TOGGLE_STACK.installed_panel_to_pcb_mm is None
