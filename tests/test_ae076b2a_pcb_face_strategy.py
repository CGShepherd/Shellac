from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
CFG=ROOT/"config/mechanical/ae076b2a_pcb_face_strategy.yaml"

def load():
    return yaml.safe_load(CFG.read_text(encoding="utf-8"))

def test_audit_and_face_strategy():
    c=load()
    assert c["audit"]["total_footprints"]==261
    assert c["audit"]["f_cu_footprints"]==261
    assert c["audit"]["b_cu_footprints"]==0
    assert c["audit"]["sense_cap_refs"]==["C80010","C80011","C90010","C90011"]
    assert c["selected_orientation"]["f_cu"]=="ENCLOSURE_FACING_DOWN"
    assert c["selected_orientation"]["b_cu"]=="TOP_COVER_FACING_UP"

def test_geometry_remains_fail_closed():
    c=load()
    assert c["control_implementation"]["exact_b_cu_footprints_verified"] is False
    assert c["control_implementation"]["c_and_k_common_plane_verified"] is False
    assert c["support_system"]["selected_support_count"]==6
    assert c["support_system"]["xy_frozen"] is False
    assert c["native_pcb"]["support_or_control_migration_authorized"] is False
    assert all(v is False for v in c["gates"].values())
