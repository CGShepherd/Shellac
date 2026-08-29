from pathlib import Path

path = Path("generator/blocks/replay_eq.py")
text = path.read_text(encoding="utf-8")

dr039 = '''    # DR-039 common post-EQ DC block before the SCH107 filter/bypass split.
    raw_tp = sheet.add_component(testpoint(
        f"TP{base}4", f"{channel}_EQ_RAW", Point(395, u2_out.y + 5.08)
    ))
    dc_cap = sheet.add_component(capacitor(
        f"C{base}60", "1u", Point(425, u2_out.y),
        dielectric="Film", voltage="50V min",
        function="DR-039 common post-EQ DC block",
        rotation=90,
        footprint="Capacitor_THT:C_Rect_L18.0mm_W5.0mm_P15.00mm"
    ))
    dc_bias = sheet.add_component(resistor(
        f"R{base}60", "330k", Point(455, u2_out.y + 15),
        tolerance="1%", function="DR-039 downstream DC reference"
    ))
    output_tp = sheet.add_component(testpoint(
        f"TP{base}5", f"{channel}_EQ_OUT", Point(455, u2_out.y + 5.08)
    ))
    output_end = Point(485, u2_out.y)
    _wire_path(sheet, u2_out, pin_position(raw_tp, "TP"), pin_position(dc_cap, "1"))
    _wire_path(sheet, pin_position(dc_cap, "2"), pin_position(output_tp, "TP"), output_end)
    sheet.connect_points(pin_position(dc_bias, "1"), pin_position(dc_cap, "2"))
    _label_on_dedicated_stub(sheet, pin_position(dc_bias, "2"), "0VA", dy=5.08, label_dx=5.08)
    sheet.add_label(post, output_end.x, output_end.y)
'''

baseline = '''    output_end = Point(420, u2_out.y)
    output_tp = sheet.add_component(testpoint(
        f"TP{base}4", f"{channel}_EQ_OUT", Point(395, u2_out.y + 5.08)
    ))
    output_tp_pin = pin_position(output_tp, "TP")
    _wire_path(sheet, u2_out, output_tp_pin, output_end)
    sheet.add_label(post, output_end.x, output_end.y)
'''

if dr039 in text:
    text = text.replace(dr039, baseline)
    path.write_text(text, encoding="utf-8")
    print("Restored replay_eq.py to pre-DR039 physical generator baseline.")
elif baseline in text:
    print("replay_eq.py already at pre-DR039 physical baseline.")
else:
    raise SystemExit("Neither expected DR039 nor baseline SCH103 output block was found.")
