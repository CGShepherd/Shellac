from generator.mechanical.control_hardware import CK_A30403RNCB, TE_MRJE3404, ROTARY_PLATFORM_AUTHORITY, validate_control_mechanical_evidence

def test_control_hardware_validates(): validate_control_mechanical_evidence()
def test_preferred_matrix_switch_geometry():
    assert CK_A30403RNCB.mpn=="A30403RNCB"; assert CK_A30403RNCB.shaft_diameter_mm==6.35; assert CK_A30403RNCB.shaft_projection_mm==9.53
def test_fallback_is_recorded_not_primary():
    assert TE_MRJE3404.mpn=="MRJE3404"; assert ROTARY_PLATFORM_AUTHORITY["matrix_mpn"]=="A30403RNCB"
