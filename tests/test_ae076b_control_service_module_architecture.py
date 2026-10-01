from pathlib import Path
import re
import yaml

ROOT=Path(__file__).resolve().parents[1]

def test_ae076b_selected_architecture_contract():
    from generator.mechanical.control_stack import (
        CARRIER_PRESENT_IN_SELECTED_ARCHITECTURE,
        CONTROL_BOARD_OWNERSHIP,
        CONTROL_INTERCONNECT_ARCHITECTURE,
        DIRECT_MAIN_PCB_CONTROL_MOUNTING_ALLOWED,
        MAIN_PCB_SUPPORT_COUNT,
        PHYSICAL_CAD_MIGRATION_COMPLETE,
        SUPPORT_XY_FROZEN,
        SUPPORT_Z_TOLERANCE_STACK_FROZEN,
        validate_control_stack,
    )
    validate_control_stack()
    assert CARRIER_PRESENT_IN_SELECTED_ARCHITECTURE is False
    assert CONTROL_BOARD_OWNERSHIP=="ONE_MAIN_AUDIO_PCB_ALL_SEVEN_CONTROLS_DIRECT_SELECTED_PHYSICAL_MIGRATION_PENDING"
    assert CONTROL_INTERCONNECT_ARCHITECTURE=="NO_CONTROL_INTERBOARD_HARNESSES"
    assert DIRECT_MAIN_PCB_CONTROL_MOUNTING_ALLOWED is True
    assert MAIN_PCB_SUPPORT_COUNT==6
    assert SUPPORT_XY_FROZEN is False
    assert SUPPORT_Z_TOLERANCE_STACK_FROZEN is False
    assert PHYSICAL_CAD_MIGRATION_COMPLETE is False

def test_ae076b_config_is_fail_closed():
    cfg=yaml.safe_load((ROOT/"config/mechanical/ae076b_control_service_module.yaml").read_text(encoding="utf-8"))
    assert cfg["authority"]=="AE-076B"
    assert cfg["selected_architecture"]["audio_pcb_count"]==1
    assert cfg["selected_architecture"]["aluminium_carrier"]=="NOT_SELECTED"
    assert cfg["selected_architecture"]["primary_pcb_support"]["count"]==6
    assert cfg["physical_cad_boundary"]["sr040_carrier_and_mh1_mh4_state"]=="INTERIM_IMPLEMENTATION_PRESERVED"
    assert cfg["permissions"]["native_pcb_mechanical_migration"] is False
    assert cfg["permissions"]["final_routing"] is False

def test_native_pcb_remains_interim_mh1_mh4_only():
    pcb=(ROOT/"out/kicad/ProjectShellac.kicad_pcb").read_text(encoding="utf-8")
    refs=set(re.findall(r"\bMH[1-9]\b",pcb))
    assert {"MH1","MH2","MH3","MH4"}.issubset(refs)
    assert "MH5" not in refs and "MH6" not in refs

def test_sr040_geometry_is_preserved_as_interim():
    sr=yaml.safe_load((ROOT/"config/mechanical/sr040_audio_mechanical_freeze.yaml").read_text(encoding="utf-8"))
    assert sr["carrier"]["plate_mm"]==[231.0,219.0,2.0]
    assert sr["pcb"]["mounting_holes"]["inset_mm"]==[5.0,8.0]

def test_historical_ae075_architecture_records_are_preserved():
    checks=(
        ("docs/design_pack/AE-075D_B03_Control_Z_Stack_and_EQ_Mezzanine_Discriminator_Rev_A0.md","two channel-local EQ mezzanine PCBs"),
        ("docs/design_pack/AE-075E_B03_Shared_CK_Local_Control_PCB_Ownership_Rev_A0.md","distributed local control PCB(s)"),
        ("docs/design_pack/AE-075F_B03_Control_Module_Partition_and_Serviceable_Harness_Architecture_Rev_A0.md","four local control PCBs"),
    )
    for rel,token in checks:
        assert token in (ROOT/rel).read_text(encoding="utf-8")
