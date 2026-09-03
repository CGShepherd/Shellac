from generator.model.rotary_switch_platform import (
    BASS_TREBLE, CHANNEL, BUSH_THREAD, PANEL_HOLE_MM,
    SHAFT_DIAMETER_MM, CONTACT_FINISH_REQUIRED,
    validate_pt_platform_contract,
)

def test_pt_platform_contract():
    validate_pt_platform_contract()

def test_all_rotaries_share_front_panel_geometry():
    assert SHAFT_DIAMETER_MM == 6.0
    assert BUSH_THREAD == "M10 x 0.75"
    assert PANEL_HOLE_MM == 10.0

def test_channel_uses_same_platform_but_two_wafers():
    assert BASS_TREBLE["wafer_count"] == 1
    assert CHANNEL["wafer_count"] == 2
    assert CHANNEL["poles"] == 4

def test_gold_contact_requirement_is_not_silently_relaxed():
    assert "gold" in CONTACT_FINISH_REQUIRED.lower()
