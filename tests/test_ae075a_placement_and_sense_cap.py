from pathlib import Path
import yaml
from generator.component_selection import common_mode_sense_capacitor_requirements
from generator.layout.sr043_native_board_audit import audit_native_board

BOARD = Path("out/kicad/ProjectShellac.kicad_pcb")
FP = "ProjectShellac:Panasonic_ECEA1VN100U_D5.0mm_H11.0mm_P2.00mm"

def test_ae075a_native_product_origins_are_inside_edgecuts():
    result = audit_native_board()
    assert result.footprint_origins_inside_outline_ok
    assert result.native_board_integrity_ok

def test_ae075a_sense_cap_policy_is_exact_panasonic_footprint():
    req = common_mode_sense_capacitor_requirements()
    assert req.selected_footprint == FP
    assert "Panasonic ECEA1VN100U" in req.notes
    assert "H11.0" in req.notes

def test_ae075a_native_board_has_exact_four_panasonic_sense_cap_footprints():
    text = BOARD.read_text(encoding="utf-8")
    assert text.count(f'(footprint "{FP}"') == 4
    for ref in ("C80010","C80011","C90010","C90011"):
        assert f'(property "Reference" "{ref}"' in text

def test_ae075a_b05_is_resolved_and_no_longer_routing_blocker():
    hold = yaml.safe_load(Path("config/release/ae071_prerouting_hold.yaml").read_text(encoding="utf-8"))
    assert "AE071-B05" not in {x["id"] for x in hold["routing_blockers"]}
    resolved = {x["id"]: x for x in hold["resolved_after_ae075"]}
    assert resolved["AE071-B05"]["mpn"] == "ECEA1VN100U"

def test_ae075a_validation_state_is_closed_after_native_qualification():
    hold_text = Path("config/release/ae071_prerouting_hold.yaml").read_text(encoding="utf-8")
    bom_text = Path("config/bom/shellac_bom.yaml").read_text(encoding="utf-8")
    record_text = Path(
        "docs/design_pack/AE-075A_Post_SR043_Placement_and_SCH108_Sense_Cap_Reconciliation_Rev_A0.md"
    ).read_text(encoding="utf-8")
    assert "native_validation: PASS" in hold_text
    assert "SELECTED_IMPLEMENTED_NATIVE_VALIDATED" in bom_text
    assert "**Status:** CLOSED — PRE-ROUTING DESIGN IMPLEMENTATION VALIDATED" in record_text

