from pathlib import Path
from generator.layout.sr043_native_board_audit import audit_native_board

def test_sr043_audit_module_targets_native_board():
    assert Path("out/kicad/ProjectShellac.kicad_pcb").exists()

def test_sr043_audit_never_calls_two_layer_board_routing_ready():
    result=audit_native_board()
    if not result.four_layer_ok:
        assert not result.routing_ready
