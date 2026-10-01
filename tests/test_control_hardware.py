from generator.mechanical.control_hardware import (
    CK_A30403RNCB, CK_7201SYCBE, NKK_NR01, ROTARY_PLATFORM_AUTHORITY,
    TE_MRJE3404, validate_control_mechanical_evidence,
)

def test_control_hardware_validates():
    validate_control_mechanical_evidence()

def test_nkk_exact_current_geometry_is_reconciled():
    assert NKK_NR01.installed_panel_to_pcb_mm==12.3
    assert "no threaded mounting bushing" in NKK_NR01.mounting
    assert ROTARY_PLATFORM_AUTHORITY["eq_mpns"]==("NR01105ANG13-2C","NR01105ANG13-2A")
    assert ROTARY_PLATFORM_AUTHORITY["eq_exact_mpn_status"]=="FROZEN_AE075C"

def test_ck_installed_planes_are_not_invented():
    assert CK_A30403RNCB.installed_panel_to_pcb_mm is None
    assert CK_7201SYCBE.installed_panel_to_pcb_mm is None
    assert CK_7201SYCBE.bushing_length_mm==8.89

def test_fallback_is_recorded_not_primary():
    assert TE_MRJE3404.mpn=="MRJE3404"
    assert ROTARY_PLATFORM_AUTHORITY["matrix_mpn"]=="A30403RNCB"
