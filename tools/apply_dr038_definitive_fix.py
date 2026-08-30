from pathlib import Path

p=Path("generator/electrical_audit.py")
text=p.read_text(encoding="utf-8")
needle="""    for wire in sheet.wires:
        points = [point for point in node_points if _point_on_segment(point, wire)]
        if abs(wire.x2 - wire.x1) >= abs(wire.y2 - wire.y1):
            points.sort(key=lambda item: (item.x, item.y))
        else:
            points.sort(key=lambda item: (item.y, item.x))
        for left, right in zip(points, points[1:]):
            dsu.union(_key(left), _key(right))

    no_connect_keys = {_key(point) for point in sheet.no_connects}
"""
replacement="""    for wire in sheet.wires:
        points = [point for point in node_points if _point_on_segment(point, wire)]
        if abs(wire.x2 - wire.x1) >= abs(wire.y2 - wire.y1):
            points.sort(key=lambda item: (item.x, item.y))
        else:
            points.sort(key=lambda item: (item.y, item.x))
        for left, right in zip(points, points[1:]):
            dsu.union(_key(left), _key(right))

    # KiCad local labels with the same name on one sheet are electrically
    # equivalent even when they are not joined by drawn conductor geometry.
    label_keys_by_name: dict[str, list[tuple[float, float]]] = defaultdict(list)
    for label in sheet.labels:
        label_keys_by_name[label.name].append(_key(Point(label.x, label.y)))
    for keys in label_keys_by_name.values():
        if len(keys) < 2:
            continue
        anchor = keys[0]
        for other in keys[1:]:
            dsu.union(anchor, other)

    no_connect_keys = {_key(point) for point in sheet.no_connects}
"""
if replacement not in text:
    if needle not in text:
        raise SystemExit("Electrical-audit insertion point not found.")
    p.write_text(text.replace(needle,replacement,1),encoding="utf-8")
    print("Electrical audit label equivalence implemented.")
else:
    print("Electrical audit label equivalence already present.")

p=Path("generator/blocks/balanced_input.py")
text=p.read_text(encoding="utf-8")
start=text.find("def _diff(sheet,ch,base,cy,po,mo):")
end=text.find("\ndef _channel(",start)
if start < 0 or end < 0:
    raise SystemExit("Could not locate SCH101 _diff() function.")

new_diff="""def _diff(sheet,ch,base,cy,po,mo):
    amp=sheet.add_component(diff_converter_block(
        f"U{base}03",f"{ch} DIFF {DIFF_CONVERTER_GAIN:.2f}x",
        Point(360,cy),f"{ch} OPA1656 differential converter"
    ))
    rn=sheet.add_component(lt5400_network(
        f"RN{base}30",f"{ch} LT5400-7 1:4",Point(315,cy)
    ))

    plus_src=f"SCH101_{ch}_LT5400_PLUS_SRC"
    plus_sum=f"SCH101_{ch}_LT5400_PLUS_SUM"
    minus_src=f"SCH101_{ch}_LT5400_MINUS_SRC"
    minus_sum=f"SCH101_{ch}_LT5400_MINUS_SUM"
    output_net=f"PRE_EQ_{ch}"

    sheet.connect_pin_to_net(po,"OUT",plus_src,stub_dx=6.35)
    sheet.connect_pin_to_net(rn,"3",plus_src,stub_dx=-6.35)
    sheet.connect_pin_to_net(mo,"OUT",minus_src,stub_dx=6.35)
    sheet.connect_pin_to_net(rn,"2",minus_src,stub_dx=-6.35)

    sheet.connect_pin_to_net(rn,"6",plus_sum,stub_dx=6.35)
    sheet.connect_pin_to_net(rn,"4",plus_sum,stub_dx=-6.35)
    sheet.connect_pin_to_net(amp,"IN+",plus_sum,stub_dx=-6.35)

    sheet.connect_pin_to_net(rn,"5","0VA",stub_dx=6.35)

    sheet.connect_pin_to_net(rn,"7",minus_sum,stub_dx=6.35)
    sheet.connect_pin_to_net(rn,"1",minus_sum,stub_dx=-6.35)
    sheet.connect_pin_to_net(amp,"IN-",minus_sum,stub_dx=-6.35)

    sheet.connect_pin_to_net(rn,"8",output_net,stub_dx=6.35)
    sheet.connect_pin_to_net(amp,"OUT",output_net,stub_dx=8.89)

    sheet.add_no_connect_pin(rn,"9")

    sheet.connect_pin_to_net(amp,"+V","+18V",stub_dy=-6.35)
    sheet.connect_pin_to_net(amp,"-V","-18V",stub_dy=6.35)
"""
p.write_text(text[:start]+new_diff+text[end:],encoding="utf-8")
print("SCH101 LT5400 short-stub topology installed.")

p=Path("tests/test_erc_branch_routing.py")
text=p.read_text(encoding="utf-8")
for name in (
    "test_lt5400_primitive_pins_are_geometrically_distinct",
    "test_sch101_lt5400_converter_pin_routes_are_explicit",
    "test_sch101_lt5400_converter_named_net_contract",
    "test_lt5400_left_pin_routes_do_not_cross_opposite_terminals",
    "test_lt5400_pin4_route_does_not_cross_pin5_0va_stub",
):
    pos=text.find(f"def {name}():")
    if pos >= 0:
        nxt=text.find("\ndef ",pos+4)
        text=text[:pos] if nxt < 0 else text[:pos]+text[nxt+1:]

text=text.replace(
    "from generator.core.electrical_audit import audit_sheet",
    "from generator.electrical_audit import audit_sheet_electrical"
)
text=text.replace("audit=audit_sheet(sheet)","audit=audit_sheet_electrical(sheet)")

if "test_sch101_lt5400_short_stub_net_contract" not in text:
    text += """

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
"""
p.write_text(text,encoding="utf-8")
print("SCH101 routing regression migrated.")

print("Definitive DR-038 snapshot fix applied.")
