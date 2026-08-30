from pathlib import Path

# Pin contract
p=Path("generator/core/pins.py")
text=p.read_text(encoding="utf-8")
start=text.find('    "ProjectShellac:LT5400_Network": {')
if start < 0:
    raise SystemExit("LT5400 pin contract not found")
end=text.find('    },', start)
if end < 0:
    raise SystemExit("LT5400 pin contract end not found")
end += 7
new_block = (
'    "ProjectShellac:LT5400_Network": {\n'
'        "1": PinContract("1", Point(-12.70, -7.62)),\n'
'        "2": PinContract("2", Point(-12.70, -2.54)),\n'
'        "3": PinContract("3", Point(-12.70, 2.54)),\n'
'        "4": PinContract("4", Point(-12.70, 7.62)),\n'
'        "5": PinContract("5", Point(12.70, 7.62)),\n'
'        "6": PinContract("6", Point(12.70, 2.54)),\n'
'        "7": PinContract("7", Point(12.70, -2.54)),\n'
'        "8": PinContract("8", Point(12.70, -7.62)),\n'
'        "9": PinContract("9", Point(0.0, 12.70)),\n'
'    },\n'
)
p.write_text(text[:start]+new_block+text[end:],encoding="utf-8")
print("LT5400 semantic pin geometry expanded.")

# Writer symbol geometry
p=Path("generator/writers/kicad9.py")
text=p.read_text(encoding="utf-8")
for oldv,newv in {
    '(at -7.62 -3.81 0)':'(at -12.70 -7.62 0)',
    '(at -7.62 -1.27 0)':'(at -12.70 -2.54 0)',
    '(at -7.62 1.27 0)':'(at -12.70 2.54 0)',
    '(at -7.62 3.81 0)':'(at -12.70 7.62 0)',
    '(at 7.62 3.81 180)':'(at 12.70 7.62 180)',
    '(at 7.62 1.27 180)':'(at 12.70 2.54 180)',
    '(at 7.62 -1.27 180)':'(at 12.70 -2.54 180)',
    '(at 7.62 -3.81 180)':'(at 12.70 -7.62 180)',
    '(at 0 7.62 270)':'(at 0 12.70 270)',
}.items():
    text=text.replace(oldv,newv)
p.write_text(text,encoding="utf-8")
print("LT5400 embedded symbol synchronized.")

# Replace _diff with explicit geometry
p=Path("generator/blocks/balanced_input.py")
text=p.read_text(encoding="utf-8")
start=text.find("def _diff(sheet,ch,base,cy,po,mo):")
end=text.find("\ndef _channel(",start)
if start < 0 or end < 0:
    raise SystemExit("Could not locate _diff")
new_diff = (
'def _diff(sheet,ch,base,cy,po,mo):\n'
'    amp=sheet.add_component(diff_converter_block(\n'
'        f"U{base}03",f"{ch} DIFF {DIFF_CONVERTER_GAIN:.2f}x",Point(360,cy),f"{ch} OPA1656 differential converter"\n'
'    ))\n'
'    rn=sheet.add_component(lt5400_network(f"RN{base}30",f"{ch} LT5400-7 1:4",Point(315,cy)))\n'
'    pp=pin_position(amp,"IN+")\n'
'    mp=pin_position(amp,"IN-")\n'
'    ao=pin_position(amp,"OUT")\n'
'    _wire_path(sheet,pin_position(po,"OUT"),Point(285,pin_position(po,"OUT").y),Point(285,pin_position(rn,"3").y),pin_position(rn,"3"))\n'
'    _wire_path(sheet,pin_position(mo,"OUT"),Point(280,pin_position(mo,"OUT").y),Point(280,pin_position(rn,"2").y),pin_position(rn,"2"))\n'
'    plus_join=Point(340,pp.y)\n'
'    _wire_path(sheet,pin_position(rn,"6"),Point(335,pin_position(rn,"6").y),Point(335,pp.y),plus_join,pp)\n'
'    _wire_path(sheet,pin_position(rn,"4"),Point(270,pin_position(rn,"4").y),Point(270,pp.y+12.70),Point(340,pp.y+12.70),plus_join)\n'
'    sheet.connect_pin_to_net(rn,"5","0VA",stub_dy=10.16)\n'
'    minus_join=Point(340,mp.y)\n'
'    _wire_path(sheet,pin_position(rn,"7"),Point(335,pin_position(rn,"7").y),Point(335,mp.y),minus_join,mp)\n'
'    _wire_path(sheet,pin_position(rn,"1"),Point(265,pin_position(rn,"1").y),Point(265,mp.y-12.70),Point(340,mp.y-12.70),minus_join)\n'
'    fb_y=cy-22.86\n'
'    _wire_path(sheet,pin_position(rn,"8"),Point(pin_position(rn,"8").x,fb_y),Point(385,fb_y),Point(385,ao.y),ao)\n'
'    sheet.add_no_connect_pin(rn,"9")\n'
'    out=Point(405,cy)\n'
'    sheet.connect_points(ao,out)\n'
'    sheet.add_label(f"PRE_EQ_{ch}",out.x,out.y)\n'
'    sheet.connect_pin_to_net(amp,"+V","+18V",stub_dy=-6)\n'
'    sheet.connect_pin_to_net(amp,"-V","-18V",stub_dy=6)\n'
)
p.write_text(text[:start]+new_diff+text[end:],encoding="utf-8")
print("SCH101 explicit LT5400 geometry restored.")

# Replace/remove obsolete named-net regression and retain audit regression
p=Path("tests/test_erc_branch_routing.py")
text=p.read_text(encoding="utf-8")
start=text.find("def test_sch101_lt5400_converter_named_net_contract():")
if start >= 0:
    end=text.find("\ndef test_sch101_no_vertical_conductor_runs_between_both_diff_inputs():",start)
    if end > start:
        replacement=(
'def test_lt5400_primitive_pins_are_geometrically_distinct():\n'
'    sheet=Sheet("SCH101","SCH101.kicad_sch")\n'
'    add_sch101_diff_converter_slice(sheet)\n'
'    c={x.ref:x for x in sheet.components}\n'
'    for ref in ("RN130","RN230"):\n'
'        rn=c[ref]\n'
'        pts=[pin_position(rn,str(i)) for i in range(1,10)]\n'
'        assert len({(p.x,p.y) for p in pts}) == 9\n'
)
        text=text[:start]+replacement+text[end:]
text=text.replace("from generator.core.electrical_audit import audit_sheet","from generator.electrical_audit import audit_sheet_electrical")
text=text.replace("audit=audit_sheet(sheet)","audit=audit_sheet_electrical(sheet)")
p.write_text(text,encoding="utf-8")
print("ERC regressions updated.")

print("AE-022F applied.")
