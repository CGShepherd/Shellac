from pathlib import Path

p=Path("generator/blocks/balanced_input.py")
text=p.read_text(encoding="utf-8")

start=text.find("def _diff(sheet,ch,base,cy,po,mo):")
end=text.find("\ndef _channel(", start)
if start < 0 or end < 0:
    raise SystemExit("Could not locate _diff() block")

new_diff = '''def _diff(sheet,ch,base,cy,po,mo):
    amp=sheet.add_component(diff_converter_block(
        f"U{base}03",f"{ch} DIFF {DIFF_CONVERTER_GAIN:.2f}x",
        Point(350,cy),f"{ch} OPA1656 differential converter"
    ))
    rn=sheet.add_component(lt5400_network(
        f"RN{base}30",f"{ch} LT5400-7 1:4",Point(315,cy)
    ))

    nets = {
        "PLUS_SRC": f"SCH101_{ch}_LT5400_PLUS_SRC",
        "PLUS_SUM": f"SCH101_{ch}_LT5400_PLUS_SUM",
        "MINUS_SRC": f"SCH101_{ch}_LT5400_MINUS_SRC",
        "MINUS_SUM": f"SCH101_{ch}_LT5400_MINUS_SUM",
        "FB_OUT": f"SCH101_{ch}_LT5400_FB_OUT",
    }

    sheet.connect_pin_to_net(po,"OUT",nets["PLUS_SRC"],stub_dx=6)
    sheet.connect_pin_to_net(rn,"3",nets["PLUS_SRC"],stub_dx=-6)
    sheet.connect_pin_to_net(mo,"OUT",nets["MINUS_SRC"],stub_dx=6)
    sheet.connect_pin_to_net(rn,"2",nets["MINUS_SRC"],stub_dx=-6)

    sheet.connect_pin_to_net(rn,"6",nets["PLUS_SUM"],stub_dx=6)
    sheet.connect_pin_to_net(rn,"4",nets["PLUS_SUM"],stub_dx=-6)
    sheet.connect_pin_to_net(amp,"IN+",nets["PLUS_SUM"],stub_dx=-6)
    sheet.connect_pin_to_net(rn,"5","0VA",stub_dy=8)

    sheet.connect_pin_to_net(rn,"7",nets["MINUS_SUM"],stub_dx=6)
    sheet.connect_pin_to_net(rn,"1",nets["MINUS_SUM"],stub_dx=-6)
    sheet.connect_pin_to_net(amp,"IN-",nets["MINUS_SUM"],stub_dx=-6)

    sheet.connect_pin_to_net(rn,"8",nets["FB_OUT"],stub_dx=6)
    sheet.connect_pin_to_net(amp,"OUT",nets["FB_OUT"],stub_dx=6)

    sheet.add_no_connect_pin(rn,"9")

    out=Point(390,cy)
    sheet.connect_points(pin_position(amp,"OUT"),out)
    sheet.add_label(f"PRE_EQ_{ch}",out.x,out.y)

    sheet.connect_pin_to_net(amp,"+V","+18V",stub_dy=-6)
    sheet.connect_pin_to_net(amp,"-V","-18V",stub_dy=6)
'''

p.write_text(text[:start]+new_diff+text[end:],encoding="utf-8")
print("AE-022E named-net LT5400 converter applied.")
