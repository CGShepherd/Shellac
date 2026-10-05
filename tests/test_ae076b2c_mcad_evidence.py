from pathlib import Path
import re
import yaml

ROOT=Path(__file__).resolve().parents[1]
B2B=ROOT/"config/mechanical/ae076b2b_mcad_sources.yaml"
B2C=ROOT/"config/mechanical/ae076b2c_mcad_sources.yaml"

def _load(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def test_b2b_record_remains_immutable_pre_reconciliation_evidence():
    c=_load(B2B)
    assert c["authority"]=="AE-076B2B"
    assert c["metcase_enclosure"]["geometry_reconciled_to_controlled_drawing"] is False
    assert c["gates"]["metcase_step_geometry_reconciled"] is False
    assert c["pcb_step"]["missing_3d_model_refs"]==["C30060","C35060","H901"]
    assert c["pcb_step"]["geometry_complete"] is False

def test_b2c_promotes_external_body_evidence_without_native_release():
    c=_load(B2C)
    assert c["authority"]=="AE-076B2C"
    assert c["previous_authority"]=="AE-076B2B"
    m=c["metcase_enclosure"]
    assert m["geometry_reconciled_to_controlled_drawing"] is True
    assert m["measured_external_body_mm"]==[260.004806,250.0,90.204806]
    assert m["reconciliation"]=="PASS_EXTERNAL_BODY_INTERNAL_DATUMS_OPEN"
    g=c["gates"]
    assert g["metcase_step_geometry_reconciled"] is True
    assert g["pcb_step_geometry_complete"] is False
    assert g["native_pcb_mechanical_migration_authorized"] is False
    assert g["routing_authority"] is False
    assert g["layout_freeze"] is False
    assert g["manufacturing_release"] is False

def test_b2c_exact_model_sources_are_proven_but_native_binding_open():
    c=_load(B2C)["pcb_model_closure_evidence"]
    h=c["H901"]
    assert h["exact_mpn"]=="39-29-9063"
    assert h["canonical_mpn"]=="0039299063"
    assert h["family"]=="5566-06A2"
    assert re.fullmatch(r"[0-9a-f]{64}",h["exact_step_zip_sha256"])
    assert re.fullmatch(r"[0-9a-f]{64}",h["exact_kicad_zip_sha256"])
    assert h["exact_model_probe"]=="PASS"
    assert h["native_binding"]=="OPEN_CONTROLLED_MIGRATION"
    cap=c["C30060_C35060"]
    assert cap["installed_kicad_model"].endswith("C_Rect_L7.2mm_W5.0mm_P5.00mm.wrl")
    assert cap["temporary_export_probe"]=="PASS"
    assert cap["native_binding"]=="OPEN_CONTROLLED_MIGRATION"
    assert c["temporary_complete_board_export"]["missing_3d_models"]==0
