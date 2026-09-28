from pathlib import Path
import re
import yaml

INDEX = Path("config/decisions/current_decision_index.yaml")
HOLD = Path("config/release/ae071_prerouting_hold.yaml")

def _text():
    return INDEX.read_text(encoding="utf-8")

def _decision_block(decision_id, next_id=None):
    text = _text()
    start = f"  {decision_id}:"
    assert start in text, f"Missing decision {decision_id}"
    block = text.split(start, 1)[1]
    if next_id is not None:
        block = block.split(f"  {next_id}:", 1)[0]
    elif "historical_implementation_events:" in block:
        block = block.split("historical_implementation_events:", 1)[0]
    return block

def _decision_status(decision_id, next_id=None):
    block = _decision_block(decision_id, next_id)
    m = re.search(r"(?m)^    status:\s*([^\n]+)$", block)
    assert m, f"Missing status for {decision_id}"
    return m.group(1).strip()

def test_authoritative_decision_index_is_well_formed():
    text = _text()
    assert re.search(r"(?m)^  branch:\s*main\s*$", text)
    assert "commit: dce5c0ec36e12f979338d8c46106c44a79c7a023" in text
    assert _decision_status("DR-037", "DR-038") == "CURRENT_IMPLEMENTED"
    assert _decision_status("DR-038", "DR-039") == "CURRENT_ARCHITECTURE_QUALIFICATION_OPEN"
    assert _decision_status("DR-039", "DR-040") == "CURRENT_ARCHITECTURE_QUALIFICATION_OPEN"
    assert _decision_status("DR-040") == "CURRENT_IMPLEMENTED"

def test_dr038_dr039_record_current_pre_spice_disposition():
    dr038 = _decision_block("DR-038", "DR-039")
    assert "    implementation:" in dr038
    assert "      converter_gain: 4.0" in dr038
    assert "LT5400BIMS8E-7#PBF selected" in dr038
    assert "EP9 to quiet 0VA implemented" in dr038
    assert "RUN10 full-stage tolerance/CMRR acceptance remains open" in dr038
    assert "LT5400-7 A-grade retained provisionally" not in dr038
    assert "AE-071A live fail-safe removable gold service-shunt topology" in dr038
    assert "approximately 14/18/22 dB" in dr038
    assert "BASE/+47/+100 pF" in dr038
    assert "Samtec physical pairing/orientation" in dr038
    assert "pre-DR038 implementation" not in dr038

    dr039 = _decision_block("DR-039", "DR-040")
    assert "status: CURRENT_ARCHITECTURE_QUALIFICATION_OPEN" in dr039
    assert "primary_record: docs/decisions/DR-039_Branch_Local_DC_Block_SELECTED.md" in dr039
    assert "historical_record: docs/decisions/DR-039_Common_Post_EQ_DC_Block_SELECTED.md" in dr039
    assert "AE-074 migrates the AE-067 selected branch-local topology" in dr039
    assert "C30060/R30060/C35060/R35060" in dr039
    assert "RUN09, RUN10, RUN12 and bench" in dr039
    assert "correlation remain open" in dr039

def test_design_pack_and_maintenance_structure_exist():
    assert Path("docs/knowledge/DESIGN_PACK_INDEX.md").exists()
    assert Path("docs/maintenance/MAINTENANCE_GUIDE_SKELETON.md").exists()


def test_pre_spice_assurance_chain_contains_required_records():
    text = _text()
    for n in range(42, 72):
        assert f"  AE-{n:03d}:" in text
    assert "  AE-071A:" in text
    assert "  AE-071B:" in text
    assert "  AE-074:" in text
    assert "  AE-075A:" in text
    assert "  AE-075B:" in text
    assert "  AE-075C:" in text
    assert "  AE-075D:" in text

def test_live_routing_hold_authority_is_registered_and_fail_closed():
    decisions = yaml.safe_load(INDEX.read_text(encoding="utf-8"))
    hold = yaml.safe_load(HOLD.read_text(encoding="utf-8"))
    assert hold["authority"] in decisions["pre_spice_assurance"]
    assert hold["previous_authority"] in decisions["pre_spice_assurance"]
    assert re.fullmatch(r"[0-9a-f]{40}", hold["baseline_commit"])
    blockers = {item["id"]: item for item in hold["routing_blockers"]}
    assert set(blockers) == {"AE071-B03", "AE071-B04", "AE071-B08"}
    assert blockers["AE071-B03"]["ownership_status"] == "EQ_LOCAL_MEZZANINES_SELECTED_SHARED_CK_OPEN"
    assert blockers["AE071-B03"]["eq_control_ownership"] == "TWO_CHANNEL_LOCAL_EQ_MEZZANINES_SELECTED"
    assert blockers["AE071-B03"]["shared_ck_ownership"] == "OPEN_DIRECT_MAIN_PCB_OR_LOCAL_CONTROL_PCB"
    assert hold["status"] == "ROUTING_HELD_PENDING_REMAINING_PREROUTING_BLOCKERS"
    assert hold["permissions"]["final_routing"] is False
    assert hold["permissions"]["layout_freeze"] is False
    assert hold["permissions"]["bom_freeze"] is False
    assert hold["permissions"]["manufacturing_release"] is False



def test_current_control_hardware_and_b03_architecture_are_coherent():
    from generator.mechanical.control_stack import (
        B03_STATUS,
        CENTRAL_REMOTE_CONTROL_STRIP_ALLOWED,
        CONTROL_BOARD_OWNERSHIP,
        EQ_CONTROL_OWNERSHIP,
        NKK_INSTALLED_PANEL_TO_PCB_MM,
        PARTS,
        SHARED_CK_CONTROL_OWNERSHIP,
        validate_control_stack,
    )
    from generator.model.controls import CONTROLS

    validate_control_stack()

    assert [c.mpn for c in CONTROLS] == [
        "NR01105ANG13-2C",
        "NR01105ANG13-2C",
        "NR01105ANG13-2A",
        "NR01105ANG13-2A",
        "A30403RNCB",
        "7201SYCBE",
        "7201SYCBE",
    ]

    assert NKK_INSTALLED_PANEL_TO_PCB_MM == 12.3
    assert EQ_CONTROL_OWNERSHIP == "TWO_CHANNEL_LOCAL_EQ_MEZZANINES_SELECTED"
    assert CONTROL_BOARD_OWNERSHIP == "EQ_LOCAL_MEZZANINES_SELECTED_SHARED_CK_OPEN"
    assert SHARED_CK_CONTROL_OWNERSHIP == "OPEN_DIRECT_MAIN_PCB_OR_LOCAL_CONTROL_PCB"
    assert CENTRAL_REMOTE_CONTROL_STRIP_ALLOWED is False
    assert B03_STATUS == "EQ_MEZZANINE_ARCHITECTURE_SELECTED_SHARED_CK_AND_PHYSICAL_DETAIL_OPEN"
    eq_parts = [part for part in PARTS if part.function in {"BASS", "TREBLE"}]
    assert len(eq_parts) == 2
    assert all("REG-08 EQ mezzanine" not in part.pcb_mounting for part in PARTS)
    assert all("REG-08 mechanical registration" in part.pcb_mounting for part in eq_parts)

    hold = yaml.safe_load(HOLD.read_text(encoding="utf-8"))
    assert hold["authority"] == "AE-075D"
    assert hold["previous_authority"] == "AE-075C"
    assert hold["baseline_commit"] == "22f651f78c9448671b9305db70c7fbd0ddf74993"

    b03 = next(x for x in hold["routing_blockers"] if x["id"] == "AE071-B03")
    assert b03["eq_control_ownership"] == "TWO_CHANNEL_LOCAL_EQ_MEZZANINES_SELECTED"
    assert b03["shared_ck_ownership"] == "OPEN_DIRECT_MAIN_PCB_OR_LOCAL_CONTROL_PCB"
    assert b03["central_remote_control_strip"] == "REJECTED_ANALOGUE_LOCALITY"
    assert "EQ_MEZZANINE_INTERCONNECT_STACK_AND_SUPPORT" in b03["remaining_scope"]

    bom = yaml.safe_load(
        Path("config/bom/shellac_bom.yaml").read_text(encoding="utf-8")
    )
    for item_id in ("BOM-CTRL-BASS", "BOM-CTRL-TREBLE"):
        item = next(x for x in bom["items"] if x["id"] == item_id)
        assert item["installed_panel_to_pcb_mm"] == 12.3
        assert item["physical_ownership"] == "CHANNEL_LOCAL_EQ_MEZZANINE_SELECTED"
        assert item["physical_architecture_reconciled_by"] == "AE-075D"
