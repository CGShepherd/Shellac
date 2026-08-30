from generator.core.sheet import Sheet
from generator.electrical_audit import audit_sheet_electrical

def test_internal_audit_models_same_name_local_labels_as_one_net():
    sheet=Sheet("LABEL_SEMANTICS","LABEL_SEMANTICS.kicad_sch")

    sheet.add_wire(0.0,0.0,5.08,0.0)
    sheet.add_label("SHARED",0.0,0.0)
    sheet.add_label("LEFT_ALIAS",5.08,0.0)

    sheet.add_wire(20.32,0.0,25.40,0.0)
    sheet.add_label("SHARED",20.32,0.0)
    sheet.add_label("RIGHT_ALIAS",25.40,0.0)

    audit=audit_sheet_electrical(sheet)

    assert any(
        set(conflict.names)=={"LEFT_ALIAS","RIGHT_ALIAS","SHARED"}
        for conflict in audit.net_name_conflicts
    )
