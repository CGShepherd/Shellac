from pathlib import Path

p=Path("generator/blocks/balanced_input.py")
text=p.read_text(encoding="utf-8")

old='''    rn_left_escape_x = pin_position(rn,"4").x - 5.08
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
'''

new='''    rn_left_escape_x = pin_position(rn,"4").x - 5.08
    # AE-022D: stay left of the LT5400 until the Ux03 IN+ Y-level.
    # The previous route crossed the vertical 0VA stub from pin 5.
    _wire_path(
        sheet,
        pin_position(rn,"4"),
        Point(rn_left_escape_x,pin_position(rn,"4").y),
        Point(rn_left_escape_x,pp.y),
        pp,
    )
    sheet.connect_pin_to_net(rn,"5","0VA",stub_dy=8)
'''

if new in text:
    print("AE-022D exact pin4/0VA crossing fix already applied.")
elif old in text:
    p.write_text(text.replace(old,new,1),encoding="utf-8")
    print("AE-022D exact pin4/0VA crossing fixed.")
else:
    raise SystemExit("Expected AE-022C plus-reference route not found.")
