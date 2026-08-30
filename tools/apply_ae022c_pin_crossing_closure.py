from pathlib import Path

p=Path("generator/blocks/balanced_input.py")
text=p.read_text(encoding="utf-8")

old = '''    plus_ref_lane_x = pp.x - 10.16
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
'''

new = '''    # Pin 4 is on the LEFT side of LT5400 and shares its Y coordinate with
    # pin 5 on the RIGHT. Route outward-left first so the conductor does not
    # pass through pin 5 and short the 0VA reference.
    rn_left_escape_x = pin_position(rn,"4").x - 5.08
    plus_ref_lane_x = pp.x - 10.16
    _wire_path(
        sheet,
        pin_position(rn,"4"),
        Point(rn_left_escape_x,pin_position(rn,"4").y),
        Point(rn_left_escape_x,pp.y + 7.62),
        Point(plus_ref_lane_x,pp.y + 7.62),
        Point(plus_ref_lane_x,pp.y),
        pp,
    )
    sheet.connect_pin_to_net(rn,"5","0VA",stub_dy=8)

    sheet.connect_points(pin_position(mo,"OUT"),pin_position(rn,"2"))
    minus_lane_x = mp.x - 5.08
    _wire_path(sheet,pin_position(rn,"7"),Point(minus_lane_x,pin_position(rn,"7").y),Point(minus_lane_x,mp.y),mp)

    # Pin 1 is on the LEFT side and shares its Y coordinate with feedback
    # pin 8 on the RIGHT. Escape left before moving toward the summing node.
    minus_sum_escape_x = pin_position(rn,"1").x - 5.08
    minus_sum_lane_x = mp.x - 10.16
    _wire_path(
        sheet,
        pin_position(rn,"1"),
        Point(minus_sum_escape_x,pin_position(rn,"1").y),
        Point(minus_sum_escape_x,mp.y - 7.62),
        Point(minus_sum_lane_x,mp.y - 7.62),
        Point(minus_sum_lane_x,mp.y),
        mp,
    )

    amp_out=pin_position(amp,"OUT")
    feedback_y = cy - 15.24
    feedback_x = amp_out.x + 5.08
    _wire_path(sheet,pin_position(rn,"8"),Point(pin_position(rn,"8").x,feedback_y),Point(feedback_x,feedback_y),Point(feedback_x,amp_out.y),amp_out)
'''

if new in text:
    print("AE-022C pin-crossing fix already applied.")
elif old in text:
    p.write_text(text.replace(old,new,1),encoding="utf-8")
    print("AE-022C LT5400 left-pin escape routing applied.")
else:
    raise SystemExit("Expected AE-022B routing block not found.")

# Replace AE-022B routing regression with path-aware checks and correct audit import.
test=Path("tests/test_erc_branch_routing.py")
t=test.read_text(encoding="utf-8")

start=t.find("def test_sch101_lt5400_converter_pin_routes_are_explicit():")
end=t.find("\ndef test_sch101_no_vertical_conductor_runs_between_both_diff_inputs():",start)
if start >= 0 and end > start:
    replacement='''def test_sch101_lt5400_converter_pin_routes_are_explicit():
    sheet=Sheet("SCH101","SCH101.kicad_sch")
    add_sch101_diff_converter_slice(sheet)
    c={x.ref:x for x in sheet.components}
    # Pin endpoints must all participate in conductors; exact segment shape is
    # deliberately free to use safe Manhattan routing.
    for diff_ref,rn_ref,plus_ref,minus_ref in (
        ("U103","RN130","U101","U102"),
        ("U203","RN230","U201","U202"),
    ):
        d,rn,po,mo=c[diff_ref],c[rn_ref],c[plus_ref],c[minus_ref]
        required=(
            pin_position(po,"OUT"), pin_position(rn,"3"), pin_position(rn,"6"),
            pin_position(d,"IN+"), pin_position(rn,"4"), pin_position(rn,"5"),
            pin_position(mo,"OUT"), pin_position(rn,"2"), pin_position(rn,"7"),
            pin_position(d,"IN-"), pin_position(rn,"1"), pin_position(rn,"8"),
            pin_position(d,"OUT"),
        )
        for point in required:
            assert any(
                (w.x1,w.y1)==(point.x,point.y) or (w.x2,w.y2)==(point.x,point.y)
                or (
                    min(w.x1,w.x2) <= point.x <= max(w.x1,w.x2)
                    and min(w.y1,w.y2) <= point.y <= max(w.y1,w.y2)
                    and abs((point.x-w.x1)*(w.y2-w.y1)-(point.y-w.y1)*(w.x2-w.x1)) < 1e-7
                )
                for w in sheet.wires
            )
'''
    t=t[:start]+replacement+t[end:]

t=t.replace(
    "from generator.core.electrical_audit import audit_sheet",
    "from generator.electrical_audit import audit_sheet_electrical"
)
t=t.replace("audit=audit_sheet(sheet)","audit=audit_sheet_electrical(sheet)")
test.write_text(t,encoding="utf-8")
print("AE-022B regression defects corrected.")

# Add a specific no-through-opposite-pin regression.
if "test_lt5400_left_pin_routes_do_not_cross_opposite_terminals" not in t:
    with test.open("a",encoding="utf-8") as f:
        f.write('''

def test_lt5400_left_pin_routes_do_not_cross_opposite_terminals():
    from generator.electrical_audit import _point_on_segment
    sheet=Sheet("SCH101","SCH101.kicad_sch")
    add_sch101_diff_converter_slice(sheet)
    c={x.ref:x for x in sheet.components}
    for rn_ref in ("RN130","RN230"):
        rn=c[rn_ref]
        # No conductor starting at left pin 4 may pass through right pin 5,
        # and no conductor starting at left pin 1 may pass through right pin 8.
        p4,p5=pin_position(rn,"4"),pin_position(rn,"5")
        p1,p8=pin_position(rn,"1"),pin_position(rn,"8")
        for wire in sheet.wires:
            if (wire.x1,wire.y1)==(p4.x,p4.y) or (wire.x2,wire.y2)==(p4.x,p4.y):
                assert not _point_on_segment(p5,wire)
            if (wire.x1,wire.y1)==(p1.x,p1.y) or (wire.x2,wire.y2)==(p1.x,p1.y):
                assert not _point_on_segment(p8,wire)
''')

print("AE-022C closure complete.")
