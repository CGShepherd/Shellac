from generator.blocks.balanced_input import add_sch101_diff_converter_slice
from generator.blocks.mode_matrix import add_mode_matrix
from generator.core.pins import pin_position
from generator.core.sheet import Sheet

def _edges(sheet):
    return {frozenset(((w.x1,w.y1),(w.x2,w.y2))) for w in sheet.wires}

def test_sch101_no_vertical_conductor_runs_between_both_diff_inputs():
    sheet=Sheet("SCH101","SCH101.kicad_sch")
    add_sch101_diff_converter_slice(sheet)
    c={x.ref:x for x in sheet.components}
    for d in ("U103","U203"):
        plus=pin_position(c[d],"IN+")
        minus=pin_position(c[d],"IN-")
        lo,hi=sorted((plus.y,minus.y))
        for w in sheet.wires:
            if w.x1==w.x2==plus.x:
                slo,shi=sorted((w.y1,w.y2))
                assert not (slo < hi and shi > lo)

def test_sch105_bias_resistors_approach_buffer_inputs_vertically():
    sheet=Sheet("SCH105","SCH105.kicad_sch")
    add_mode_matrix(sheet)
    c={x.ref:x for x in sheet.components}
    edges=_edges(sheet)
    for br,ur in (("R510","U501"),("R520","U502")):
        b=pin_position(c[br],"1")
        i=pin_position(c[ur],"IN")
        corner=(i.x,b.y)
        assert frozenset(((b.x,b.y),corner)) in edges
        assert frozenset((corner,(i.x,i.y))) in edges

def test_sch101_lt5400_reference_and_ep_are_safe():
    sheet=Sheet("SCH101","SCH101.kicad_sch")
    add_sch101_diff_converter_slice(sheet)
    c={x.ref:x for x in sheet.components}
    labels={(x.name,x.x,x.y) for x in sheet.labels}
    for rn_ref in ("RN130","RN230"):
        rn=c[rn_ref]
        ref=pin_position(rn,"5")
        matching=[(x,y) for name,x,y in labels if name=="0VA" and y==ref.y and x>ref.x]
        assert matching
        assert all(x != ref.x for x,y in matching)
        assert pin_position(rn,"9") in sheet.no_connects

def test_sch101_converter_named_nets_remain_separate():
    from generator.electrical_audit import audit_sheet_electrical
    sheet=Sheet("SCH101","SCH101.kicad_sch")
    add_sch101_diff_converter_slice(sheet)
    audit=audit_sheet_electrical(sheet)
    assert audit.net_name_conflicts == ()
    assert audit.unterminated_pins == ()




def test_sch101_lt5400_short_stub_net_contract():
    from generator.electrical_audit import audit_sheet_electrical
    sheet=Sheet("SCH101","SCH101.kicad_sch")
    add_sch101_diff_converter_slice(sheet)
    audit=audit_sheet_electrical(sheet)
    assert audit.passed
    assert audit.net_name_conflicts == ()
    assert audit.unterminated_pins == ()

    labels=[label.name for label in sheet.labels]
    for ch in ("L","R"):
        assert labels.count(f"SCH101_{ch}_LT5400_PLUS_SRC") == 2
        assert labels.count(f"SCH101_{ch}_LT5400_PLUS_SUM") == 3
        assert labels.count(f"SCH101_{ch}_LT5400_MINUS_SRC") == 2
        assert labels.count(f"SCH101_{ch}_LT5400_MINUS_SUM") == 3
        assert labels.count(f"PRE_EQ_{ch}") == 2
