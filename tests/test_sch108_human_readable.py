from generator.blocks.balanced_output import add_balanced_output
from generator.core.geometry import Point
from generator.core.pins import pin_position
from generator.core.sheet import Sheet


def _sheet():
    sheet = Sheet("SCH108", "ProjectShellac_SCH108.kicad_sch")
    add_balanced_output(sheet)
    return sheet


def _edges(sheet):
    return {
        frozenset(((wire.x1, wire.y1), (wire.x2, wire.y2)))
        for wire in sheet.wires
    }


def test_sch108_uses_only_interface_and_domain_labels():
    sheet = _sheet()
    labels = {label.name for label in sheet.labels}

    assert {
        "MODE_L", "MODE_R", "+18V", "-18V", "0VA", "CHASSIS",
        "OUTPUT_L_POS", "OUTPUT_L_NEG", "OUTPUT_R_POS", "OUTPUT_R_NEG",
    } == labels
    assert not any(
        token in label
        for label in labels
        for token in ("DRIVER_IN", "DRV_OUT")
    )


def test_sch108_signal_wiring_is_orthogonal_except_direct_sense_links():
    sheet = _sheet()
    assert sheet.wires
    components = {component.ref: component for component in sheet.components}

    allowed_diagonal_edges = set()
    for driver_ref, pos_cap_ref, neg_cap_ref in (
        ("U8001", "C80010", "C80011"),
        ("U9001", "C90010", "C90011"),
    ):
        driver = components[driver_ref]
        for output_name, sense_name, cap_ref in (
            ("OUT+", "SNS+", pos_cap_ref),
            ("OUT-", "SNS-", neg_cap_ref),
        ):
            cap = components[cap_ref]
            output_pin = pin_position(driver, output_name)
            sense_pin = pin_position(driver, sense_name)
            cap_pins = [pin_position(cap, "1"), pin_position(cap, "2")]
            output_cap_pin = min(
                cap_pins, key=lambda point: abs(point.y - output_pin.y)
            )
            sense_cap_pin = next(
                point for point in cap_pins if point != output_cap_pin
            )
            allowed_diagonal_edges.add(frozenset((
                (output_pin.x, output_pin.y),
                (output_cap_pin.x, output_cap_pin.y),
            )))
            allowed_diagonal_edges.add(frozenset((
                (sense_cap_pin.x, sense_cap_pin.y),
                (sense_pin.x, sense_pin.y),
            )))

    for wire in sheet.wires:
        edge = frozenset(((wire.x1, wire.y1), (wire.x2, wire.y2)))
        assert (
            wire.x1 == wire.x2
            or wire.y1 == wire.y2
            or edge in allowed_diagonal_edges
        )
        assert (wire.x1, wire.y1) != (wire.x2, wire.y2)


def test_sch108_mode_inputs_and_driver_inputs_are_visible_conductors():
    sheet = _sheet()
    components = {component.ref: component for component in sheet.components}
    edges = _edges(sheet)

    mute = components["SW801"]
    for signal_pin, tp_ref, driver_ref, mute_out in (
        ("L_SIGNAL", "TP8010", "U8001", "L_OUT"),
        ("R_SIGNAL", "TP8011", "U9001", "R_OUT"),
    ):
        signal = pin_position(mute, signal_pin)
        tp = pin_position(components[tp_ref], "TP")
        assert signal.y == tp.y
        assert frozenset(((tp.x, tp.y), (signal.x, signal.y))) in edges

        driver_in = pin_position(components[driver_ref], "IN")
        selected = pin_position(mute, mute_out)
        assert any(
            (wire.x1, wire.y1) == (selected.x, selected.y)
            or (wire.x2, wire.y2) == (selected.x, selected.y)
            for wire in sheet.wires
        )
        assert any(
            (wire.x1, wire.y1) == (driver_in.x, driver_in.y)
            or (wire.x2, wire.y2) == (driver_in.x, driver_in.y)
            for wire in sheet.wires
        )


def test_sch108_driver_outputs_reach_beads_and_xlr_pins_visibly():
    sheet = _sheet()
    components = {component.ref: component for component in sheet.components}

    for base in (800, 900):
        driver = components[f"U{base}1"]
        xlr = components[f"J{base}1"]
        for driver_pin_name, bead_ref, xlr_pin_name in (
            ("OUT+", f"FB{base}1", "2"),
            ("OUT-", f"FB{base}2", "3"),
        ):
            driver_pin = pin_position(driver, driver_pin_name)
            bead_1 = pin_position(components[bead_ref], "1")
            xlr_pin = pin_position(xlr, xlr_pin_name)

            assert frozenset(
                ((driver_pin.x, driver_pin.y), (bead_1.x, bead_1.y))
            ) in _edges(sheet)
            assert any(
                (wire.x1, wire.y1) == (xlr_pin.x, xlr_pin.y)
                or (wire.x2, wire.y2) == (xlr_pin.x, xlr_pin.y)
                for wire in sheet.wires
            )


def test_sch108_sense_capacitors_connect_matching_output_and_sense_pins():
    sheet = _sheet()
    components = {component.ref: component for component in sheet.components}

    for base in (800, 900):
        driver = components[f"U{base}1"]
        for cap_ref, out_pin, sense_pin in (
            (f"C{base}10", "OUT+", "SNS+"),
            (f"C{base}11", "OUT-", "SNS-"),
        ):
            cap = components[cap_ref]
            endpoints = {
                (wire.x1, wire.y1)
                for wire in sheet.wires
            } | {
                (wire.x2, wire.y2)
                for wire in sheet.wires
            }
            assert (pin_position(driver, out_pin).x, pin_position(driver, out_pin).y) in endpoints
            assert (pin_position(driver, sense_pin).x, pin_position(driver, sense_pin).y) in endpoints
            assert (pin_position(cap, "1").x, pin_position(cap, "1").y) in endpoints
            assert (pin_position(cap, "2").x, pin_position(cap, "2").y) in endpoints


def _wire_component(sheet, start):
    adjacency = {}
    for wire in sheet.wires:
        a = (wire.x1, wire.y1)
        b = (wire.x2, wire.y2)
        adjacency.setdefault(a, set()).add(b)
        adjacency.setdefault(b, set()).add(a)
    seen = {start}
    stack = [start]
    while stack:
        point = stack.pop()
        for neighbour in adjacency.get(point, ()):
            if neighbour not in seen:
                seen.add(neighbour)
                stack.append(neighbour)
    return seen


def test_sch108_mute_outputs_use_separate_routing_lanes():
    sheet = _sheet()
    components = {component.ref: component for component in sheet.components}
    mute = components["SW801"]
    l_out = pin_position(mute, "L_OUT")
    r_out = pin_position(mute, "R_OUT")

    l_first = next(
        wire for wire in sheet.wires
        if (wire.x1, wire.y1) == (l_out.x, l_out.y)
        or (wire.x2, wire.y2) == (l_out.x, l_out.y)
    )
    r_first = next(
        wire for wire in sheet.wires
        if (wire.x1, wire.y1) == (r_out.x, r_out.y)
        or (wire.x2, wire.y2) == (r_out.x, r_out.y)
    )
    l_lane_x = l_first.x2 if l_first.x1 == l_out.x else l_first.x1
    r_lane_x = r_first.x2 if r_first.x1 == r_out.x else r_first.x1
    assert l_lane_x != r_lane_x
    assert r_out not in _wire_component(sheet, (l_out.x, l_out.y))


def test_sch108_capacitor_terminals_are_not_shortened_by_routing():
    sheet = _sheet()
    components = {component.ref: component for component in sheet.components}
    for ref in (
        "C80010", "C80011", "C90010", "C90011",
        "C80020", "C80021", "C90020", "C90021",
    ):
        pin_1 = pin_position(components[ref], "1")
        pin_2 = pin_position(components[ref], "2")
        assert (pin_2.x, pin_2.y) not in _wire_component(
            sheet, (pin_1.x, pin_1.y)
        )


def test_sch108_output_interfaces_are_on_real_output_conductors():
    sheet = _sheet()
    endpoints = {
        (wire.x1, wire.y1) for wire in sheet.wires
    } | {
        (wire.x2, wire.y2) for wire in sheet.wires
    }
    labels = {label.name: (label.x, label.y) for label in sheet.labels}
    for name in (
        "OUTPUT_L_POS", "OUTPUT_L_NEG", "OUTPUT_R_POS", "OUTPUT_R_NEG",
    ):
        assert labels[name] in endpoints


def test_sense_capacitors_use_direct_pin_to_pin_conductors():
    from generator.blocks.balanced_output import add_balanced_output
    from generator.core.pins import pin_position
    from generator.core.sheet import Sheet

    sheet = Sheet("SCH108", "SCH108.kicad_sch")
    add_balanced_output(sheet)
    components = {component.ref: component for component in sheet.components}
    edges = {
        frozenset(((wire.x1, wire.y1), (wire.x2, wire.y2)))
        for wire in sheet.wires
    }

    for driver_ref, pos_cap_ref, neg_cap_ref in (
        ("U8001", "C80010", "C80011"),
        ("U9001", "C90010", "C90011"),
    ):
        driver = components[driver_ref]
        pos_cap = components[pos_cap_ref]
        neg_cap = components[neg_cap_ref]

        for output_name, sense_name, cap in (
            ("OUT+", "SNS+", pos_cap),
            ("OUT-", "SNS-", neg_cap),
        ):
            output_pin = pin_position(driver, output_name)
            sense_pin = pin_position(driver, sense_name)
            cap_pins = [pin_position(cap, "1"), pin_position(cap, "2")]
            output_cap_pin = min(
                cap_pins, key=lambda point: abs(point.y - output_pin.y)
            )
            sense_cap_pin = next(
                point for point in cap_pins if point != output_cap_pin
            )
            assert frozenset((
                (output_pin.x, output_pin.y),
                (output_cap_pin.x, output_cap_pin.y),
            )) in edges
            assert frozenset((
                (sense_cap_pin.x, sense_cap_pin.y),
                (sense_pin.x, sense_pin.y),
            )) in edges
