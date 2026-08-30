from pathlib import Path

p=Path("tests/test_erc_branch_routing.py")
text=p.read_text(encoding="utf-8")
if "test_lt5400_pin4_route_does_not_cross_pin5_0va_stub" not in text:
    text += '''

def test_lt5400_pin4_route_does_not_cross_pin5_0va_stub():
    from generator.electrical_audit import _point_on_segment
    sheet=Sheet("SCH101","SCH101.kicad_sch")
    add_sch101_diff_converter_slice(sheet)
    c={x.ref:x for x in sheet.components}
    for rn_ref in ("RN130","RN230"):
        rn=c[rn_ref]
        p4=pin_position(rn,"4")
        p5=pin_position(rn,"5")
        touching4=[w for w in sheet.wires if _point_on_segment(p4,w)]
        assert touching4
        assert all(not _point_on_segment(p5,w) for w in touching4)
'''
    p.write_text(text,encoding="utf-8")
print("AE-022D exact crossing regression installed.")
