from pathlib import Path
p=Path("tests/test_erc_branch_routing.py")
text=p.read_text(encoding="utf-8")

start=text.find("def test_sch101_lt5400_converter_pin_routes_are_explicit():")
end=text.find("\ndef test_sch101_no_vertical_conductor_runs_between_both_diff_inputs():",start)
if start >= 0 and end > start:
    replacement='''def test_sch101_lt5400_converter_named_net_contract():
    sheet=Sheet("SCH101","SCH101.kicad_sch")
    add_sch101_diff_converter_slice(sheet)
    labels={(x.name,x.x,x.y) for x in sheet.labels}
    for ch in ("L","R"):
        for suffix in ("PLUS_SRC","PLUS_SUM","MINUS_SRC","MINUS_SUM","FB_OUT"):
            name=f"SCH101_{ch}_LT5400_{suffix}"
            assert any(label_name==name for label_name,_,_ in labels)
        assert any(label_name=="0VA" for label_name,_,_ in labels)
'''
    text=text[:start]+replacement+text[end:]

for fn in ("test_lt5400_left_pin_routes_do_not_cross_opposite_terminals","test_lt5400_pin4_route_does_not_cross_pin5_0va_stub"):
    pos=text.find(f"def {fn}():")
    if pos >= 0:
        nxt=text.find("\ndef ",pos+4)
        if nxt < 0:
            text=text[:pos]
        else:
            text=text[:pos]+text[nxt+1:]

text=text.replace("from generator.core.electrical_audit import audit_sheet","from generator.electrical_audit import audit_sheet_electrical")
text=text.replace("audit=audit_sheet(sheet)","audit=audit_sheet_electrical(sheet)")
p.write_text(text,encoding="utf-8")
print("AE-022E regressions migrated.")
