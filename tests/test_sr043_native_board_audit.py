from pathlib import Path

from generator.layout.sr043_native_board_audit import audit_native_board


def test_sr043_audit_module_targets_native_board():
    assert Path("out/kicad/ProjectShellac.kicad_pcb").exists()


def test_sr043_two_layer_board_cannot_have_native_board_integrity():
    result = audit_native_board()
    if not result.four_layer_ok:
        assert not result.native_board_integrity_ok


def test_ae071b_board_owned_mounting_holes_are_persistently_protected():
    result = audit_native_board()
    assert result.mounting_holes_ok
    assert result.mounting_holes_pose_ok
    assert result.mounting_holes_board_only_ok
    assert result.mounting_holes_locked_ok
    assert result.mounting_holes_output_excluded_ok


def test_ae071b_distinguishes_board_integrity_from_routing_authority():
    result = audit_native_board()
    assert result.native_board_integrity_ok
    assert result.routing_authorized is False
