from pathlib import Path

p=Path("generator/blocks/balanced_input.py")
text=p.read_text(encoding="utf-8")

old = '''def _diff(sheet,ch,base,cy,po,mo):
    amp=sheet.add_component(diff_converter_block(f"U{base}03",f"{ch} DIFF {DIFF_CONVERTER_GAIN:.2f}x",Point(350,cy),f"{ch} OPA1656 differential converter"))
    rn=sheet.add_component(lt5400_network(f"RN{base}30",f"{ch} LT5400-7 1:4",Point(315,cy)))
    pp,mp=pin_position(amp,"IN+"),pin_position(amp,"IN-")
    sheet.connect_points(pin_position(po,"OUT"),pin_position(rn,"3")); sheet.connect_points(pin_position(rn,"6"),pp)
    sheet.connect_points(pin_position(rn,"4"),pp); sheet.connect_pin_to_net(rn,"5","0VA",stub_dy=8)
    sheet.connect_points(pin_position(mo,"OUT"),pin_position(rn,"2")); sheet.connect_points(pin_position(rn,"7"),mp)
    sheet.connect_points(pin_position(rn,"1"),mp); sheet.connect_points(pin_position(rn,"8"),pin_position(amp,"OUT"))
    sheet.add_no_connect_pin(rn,"9")
    out=Point(390,cy); sheet.connect_points(pin_position(amp,"OUT"),out); sheet.add_label(f"PRE_EQ_{ch}",out.x,out.y)
    sheet.connect_pin_to_net(amp,"+V","+18V",stub_dy=-6); sheet.connect_pin_to_net(amp,"-V","-18V",stub_dy=6)
'''

new = '''def _diff(sheet,ch,base,cy,po,mo):
    amp=sheet.add_component(diff_converter_block(
        f"U{base}03",f"{ch} DIFF {DIFF_CONVERTER_GAIN:.2f}x",
        Point(350,cy),f"{ch} OPA1656 differential converter"
    ))
    rn=sheet.add_component(lt5400_network(
        f"RN{base}30",f"{ch} LT5400-7 1:4",Point(315,cy)
    ))
    pp,mp=pin_position(amp,"IN+"),pin_position(amp,"IN-")

    sheet.connect_points(pin_position(po,"OUT"),pin_position(rn,"3"))
    plus_lane_x = pp.x - 5.08
    _wire_path(sheet,pin_position(rn,"6"),Point(plus_lane_x,pin_position(rn,"6").y),Point(plus_lane_x,pp.y),pp)

    plus_ref_lane_x = pp.x - 10.16
    _wire_path(sheet,pin_position(rn,"4"),Point(plus_ref_lane_x,pin_position(rn,"4").y),Point(plus_ref_lane_x,pp.y),pp)
    sheet.connect_pin_to_net(rn,"5","0VA",stub_dy=8)

    sheet.connect_points(pin_position(mo,"OUT"),pin_position(rn,"2"))
    minus_lane_x = mp.x - 5.08
    _wire_path(sheet,pin_position(rn,"7"),Point(minus_lane_x,pin_position(rn,"7").y),Point(minus_lane_x,mp.y),mp)

    minus_sum_lane_x = mp.x - 10.16
    _wire_path(sheet,pin_position(rn,"1"),Point(minus_sum_lane_x,pin_position(rn,"1").y),Point(minus_sum_lane_x,mp.y),mp)

    amp_out=pin_position(amp,"OUT")
    feedback_y = cy - 15.24
    feedback_x = amp_out.x + 5.08
    _wire_path(sheet,pin_position(rn,"8"),Point(pin_position(rn,"8").x,feedback_y),Point(feedback_x,feedback_y),Point(feedback_x,amp_out.y),amp_out)

    sheet.add_no_connect_pin(rn,"9")
    out=Point(390,cy)
    sheet.connect_points(amp_out,out)
    sheet.add_label(f"PRE_EQ_{ch}",out.x,out.y)
    sheet.connect_pin_to_net(amp,"+V","+18V",stub_dy=-6)
    sheet.connect_pin_to_net(amp,"-V","-18V",stub_dy=6)
'''

if new in text:
    print("AE-022B LT5400 routing already applied.")
elif old in text:
    p.write_text(text.replace(old,new,1),encoding="utf-8")
    print("AE-022B LT5400 non-crossing routing applied.")
else:
    raise SystemExit("Expected AE-022A _diff() block not found; no changes made.")

test_path=Path("tests/test_erc_branch_routing.py")
t=test_path.read_text(encoding="utf-8")
if "test_sch101_converter_named_nets_remain_separate" not in t:
    t += '''
def test_sch101_converter_named_nets_remain_separate():
    from generator.core.electrical_audit import audit_sheet
    sheet=Sheet("SCH101","SCH101.kicad_sch")
    add_sch101_diff_converter_slice(sheet)
    audit=audit_sheet(sheet)
    assert audit.net_name_conflicts == ()
    assert audit.unterminated_pins == ()
'''
    test_path.write_text(t,encoding="utf-8")
    print("Added LT5400 net-separation regression.")

print("AE-022B closure complete.")
