from pathlib import Path
import re, yaml
ROOT=Path(__file__).resolve().parents[1]
CFG=ROOT/"config/mechanical/ae076b2b_mcad_sources.yaml"
BOM=ROOT/"config/bom/shellac_bom.yaml"
POWER=ROOT/"generator/blocks/power_entry.py"
HELPER=ROOT/"tools/prepare_ae076b2b_mcad_inputs.py"

def cfg(): return yaml.safe_load(CFG.read_text(encoding="utf-8"))

def test_metcase_auth_boundary_is_explicit():
    m=cfg()["metcase_enclosure"]
    assert m["drawing_source_authority"]=="MANUFACTURER_OFFICIAL"
    assert re.fullmatch(r"[0-9a-f]{64}",m["drawing_sha256"])
    assert m["drawing_bytes"]>100000
    assert m["step_status"]=="AUTHENTICATED_MANUAL_DOWNLOAD_INGESTED"
    assert re.fullmatch(r"[0-9a-f]{64}",m["step_sha256"])
    assert m["step_bytes"]>100000
    assert m["exact_step_ingested"] is True
    assert m["geometry_reconciled_to_controlled_drawing"] is False

def test_neutrik_step_sources():
    c=cfg()
    assert set(c["neutrik_assets"])=={"NC3FD-L-B-1","NC3MD-L-B-1","NC5MD-LX-B","NC5FD-LX-B"}
    for a in c["neutrik_assets"].values():
        assert a["source_authority"]=="MANUFACTURER_OFFICIAL"
        assert re.fullmatch(r"[0-9a-f]{64}",a["sha256"])
        assert a["bytes"]>30000

def test_dc_interface():
    d=cfg()["regulated_dc_interface"]
    assert d["audio_chassis_receptacle"]=="NC5MD-LX-B"
    assert d["psu_chassis_receptacle"]=="NC5FD-LX-B"
    assert d["pin_contract"]=={1:"0VA",2:"+17VA_IN",3:"-17VA_IN",4:"CHASSIS",5:"NC_RESERVED"}
    assert d["pin1_to_shell_bond"]=="PROHIBITED"

def test_pcb_step():
    p=cfg()["pcb_step"]
    assert p["source_commit"]=="1e8702139db68ef42bd0c2dd414db99524948309"
    assert re.fullmatch(r"[0-9a-f]{64}",p["source_board_sha256"])
    assert re.fullmatch(r"[0-9a-f]{64}",p["observed_sha256"])
    assert p["bytes"]>4096
    assert p["tracked"] is False
    assert p["missing_3d_model_refs"]==["C30060","C35060","H901"]
    assert p["geometry_complete"] is False

def test_bom_and_power_entry():
    b=yaml.safe_load(BOM.read_text(encoding="utf-8"))
    ids={x["id"]:x for x in b["items"]}
    assert ids["BOM-POWER-DC-AUDIO-CHASSIS"]["mpn"]=="NC5MD-LX-B"
    assert ids["BOM-POWER-DC-PSU-CHASSIS"]["mpn"]=="NC5FD-LX-B"
    assert ids["BOM-POWER-DC-AUDIO-CHASSIS"]["pin1_shell_bond"]=="PROHIBITED"
    t=POWER.read_text(encoding="utf-8")
    assert '"Physical MPN": "NC5MD-LX-B"' in t
    assert '"Pin1-Shell Bond": "PROHIBITED"' in t

def test_gates_fail_closed():
    g=cfg()["gates"]
    assert g["enclosure_drawing_hash_controlled"] is True
    assert g["metcase_exact_step_ingested"] is True
    assert g["metcase_step_geometry_reconciled"] is False
    assert g["neutrik_panel_geometry_hash_controlled"] is True
    assert g["pcb_step_generated"] is True
    assert g["pcb_step_geometry_complete"] is False
    assert g["rear_dc_connector_selected"] is True
    assert g["full_dimensional_assembly_authorized"] is False
    assert g["native_pcb_mechanical_migration_authorized"] is False
    assert g["routing_authority"] is False
def test_reproduction_helper_enforces_cached_hashes():
    t=HELPER.read_text(encoding="utf-8")
    assert "METCASE STEP SHA drift" in t
    assert "governed PCB source hash drift" in t
    assert "PCB STEP SHA drift" in t
    assert '"status":"HASH_VERIFIED"' in t
