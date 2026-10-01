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
    assert "  AE-075E:" in text
    assert "  AE-075F:" in text
    assert "  AE-075G:" in text
    assert "  AE-076A:" in text
    assert "  AE-076B:" in text
    assert "  AE-076B2A:" in text

def test_live_routing_hold_authority_is_registered_and_fail_closed():
    decisions=yaml.safe_load(INDEX.read_text(encoding="utf-8"))
    hold=yaml.safe_load(HOLD.read_text(encoding="utf-8"))
    assert hold["authority"] in decisions["pre_spice_assurance"]
    assert hold["previous_authority"] in decisions["pre_spice_assurance"]
    blockers={item["id"]:item for item in hold["routing_blockers"]}
    assert set(blockers)=={"AE071-B03","AE071-B04","AE071-B08"}
    b03=blockers["AE071-B03"]
    assert b03["architecture_authority"]=="AE-076B"
    assert b03["direct_main_pcb_control_mounting"]=="SELECTED_CURRENT_ARCHITECTURE"
    assert b03["control_module_partition"]=="NONE_SINGLE_MAIN_AUDIO_PCB"
    assert b03["interconnect_architecture"]=="NO_CONTROL_INTERBOARD_HARNESSES"
    assert b03["aluminium_carrier_selected"] is False
    assert b03["main_pcb_support_count"]==6
    assert b03["support_xy_frozen"] is False
    assert b03["support_z_tolerance_stack_frozen"] is False
    assert "INTERIM_SR040_AE071B_MH1_MH4" in b03["physical_cad_state"]
    assert hold["permissions"]["final_routing"] is False
    assert hold["permissions"]["layout_freeze"] is False
    assert hold["permissions"]["bom_freeze"] is False
    assert hold["permissions"]["manufacturing_release"] is False

def test_current_control_hardware_and_b03_architecture_are_coherent():
    from generator.mechanical.control_stack import (
        CARRIER_PRESENT_IN_SELECTED_ARCHITECTURE, CONTROL_BOARD_OWNERSHIP,
        CONTROL_INTERCONNECT_ARCHITECTURE, CONTROL_MODULE_PARTITION,
        DIRECT_MAIN_PCB_CONTROL_MOUNTING_ALLOWED, MAIN_PCB_SUPPORT_COUNT,
        NKK_INSTALLED_PANEL_TO_PCB_MM, PHYSICAL_CAD_MIGRATION_COMPLETE,
        SUPPORT_XY_FROZEN, SUPPORT_Z_TOLERANCE_STACK_FROZEN, validate_control_stack,
    )
    validate_control_stack()
    assert NKK_INSTALLED_PANEL_TO_PCB_MM==12.3
    assert CARRIER_PRESENT_IN_SELECTED_ARCHITECTURE is False
    assert CONTROL_BOARD_OWNERSHIP=="ONE_MAIN_AUDIO_PCB_ALL_SEVEN_CONTROLS_DIRECT_SELECTED_PHYSICAL_MIGRATION_PENDING"
    assert CONTROL_MODULE_PARTITION==("MAIN_AUDIO_PCB",)
    assert CONTROL_INTERCONNECT_ARCHITECTURE=="NO_CONTROL_INTERBOARD_HARNESSES"
    assert DIRECT_MAIN_PCB_CONTROL_MOUNTING_ALLOWED is True
    assert MAIN_PCB_SUPPORT_COUNT==6
    assert SUPPORT_XY_FROZEN is False
    assert SUPPORT_Z_TOLERANCE_STACK_FROZEN is False
    assert PHYSICAL_CAD_MIGRATION_COMPLETE is False

    hold=yaml.safe_load(HOLD.read_text(encoding="utf-8"))
    assert hold["authority"]=="AE-076B2A"
    assert hold["previous_authority"]=="AE-076B"
    assert hold["baseline_commit"]=="e9b47d1b7edbe42f76410dbafc918c9b52b25120"
    b03=next(item for item in hold["routing_blockers"] if item["id"]=="AE071-B03")
    assert b03["architecture_authority"]=="AE-076B"
    assert b03["pcb_face_strategy"]=="F_CU_DOWN_ELECTRONICS_B_CU_UP_CONTROLS_SELECTED"
    assert b03["native_population_audit"]=="261_FCU_0_BCU"
    assert b03["control_footprint_side"]=="B_CU_SELECTED_EXACT_FOOTPRINT_MIGRATION_OPEN"
    assert b03["native_pcb_mechanical_migration"]=="NOT_AUTHORIZED"

    bom=yaml.safe_load(Path("config/bom/shellac_bom.yaml").read_text(encoding="utf-8"))
    ids={x["id"] for x in bom["items"]}
    assert "BOM-CTRL-INTERCONNECT-FAMILY" not in ids
    for item_id in ("BOM-CTRL-BASS","BOM-CTRL-TREBLE","BOM-CTRL-CHANNEL","BOM-CTRL-RUMBLE","BOM-CTRL-MUTE"):
        item=next(x for x in bom["items"] if x["id"]==item_id)
        assert item["physical_ownership"]=="MAIN_AUDIO_PCB_DIRECT_SELECTED_PHYSICAL_MIGRATION_PENDING"
        assert item["physical_architecture_reconciled_by"]=="AE-076B"
        assert item["interconnect_family"]=="NONE_SINGLE_MAIN_PCB"
