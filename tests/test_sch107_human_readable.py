from generator.blocks.rumble_filter import add_rumble_filter
from generator.core.geometry import Point
from generator.core.pins import pin_position
from generator.core.sheet import Sheet
from generator.writers.kicad9 import junction_points, snap_coordinate
from generator.core.grid import align_coordinate


def _sch107():
    sheet = Sheet(
        title="SCH107 - Switchable rumble filter",
        filename="ProjectShellac_SCH107.kicad_sch",
    )
    add_rumble_filter(sheet)
    return sheet


def _edges(sheet):
    return {
        frozenset(((wire.x1, wire.y1), (wire.x2, wire.y2)))
        for wire in sheet.wires
        if (wire.x1, wire.y1) != (wire.x2, wire.y2)
    }


def test_sch107_uses_only_interface_and_supply_labels():
    sheet = _sch107()
    names = [label.name for label in sheet.labels]

    for name in ("POST_EQ_L", "POST_EQ_R", "FILTERED_L", "FILTERED_R"):
        assert names.count(name) == 1

    assert {
        "L_HP1_OUT", "R_HP1_OUT", "L_HP2_OUT", "R_HP2_OUT",
        "L_FILTER_BRANCH", "R_FILTER_BRANCH",
    }.isdisjoint(names)


def test_sch107_signal_wiring_is_orthogonal_and_nonzero():
    sheet = _sch107()
    assert all(
        wire.x1 == wire.x2 or wire.y1 == wire.y2
        for wire in sheet.wires
    )
    assert all(
        (wire.x1, wire.y1) != (wire.x2, wire.y2)
        for wire in sheet.wires
    )


def test_sch107_main_filter_paths_are_continuous_and_visible():
    sheet = _sch107()
    components = {component.ref: component for component in sheet.components}
    edges = _edges(sheet)

    for channel, base in (("L", 700), ("R", 750)):
        input_tp = components[f"TP{base}1"]
        hp1_tp = components[f"TP{base}2"]
        hp2_tp = components[f"TP{base}3"]
        input_tp_pin = pin_position(input_tp, "TP")
        hp1_tp_pin = pin_position(hp1_tp, "TP")
        hp2_tp_pin = pin_position(hp2_tp, "TP")

        y = input_tp_pin.y
        assert input_tp_pin == Point(input_tp.at.x, y)
        assert hp1_tp_pin == Point(hp1_tp.at.x, y)
        assert hp2_tp_pin == Point(hp2_tp.at.x, y)
        assert frozenset(((align_coordinate(25), y), (align_coordinate(35), y))) in edges
        assert frozenset(((align_coordinate(35), y), (input_tp_pin.x, y))) in edges

        for section_index, requested_x in ((0, 75), (1, 215)):
            x = requested_x
            section_base = base + section_index * 20
            c1 = components[f"C{section_base}1"]
            c2 = components[f"C{section_base}2"]
            opamp = components[f"U{section_base}"]
            r1 = components[f"R{section_base}1"]
            r2 = components[f"R{section_base}2"]
            node_1 = (align_coordinate(x + 15), y)
            node_2 = (align_coordinate(x + 45), y)
            output_branch = (align_coordinate(x + 86), y)

            assert frozenset((
                (pin_position(c1, "1").x, y), node_1,
            )) in edges
            assert frozenset((
                node_1, (pin_position(c2, "2").x, y),
            )) in edges
            assert frozenset((
                (pin_position(c2, "1").x, y), node_2,
            )) in edges
            assert frozenset((
                node_2, (pin_position(opamp, "IN").x, y),
            )) in edges
            r1_left = pin_position(r1, "1")
            feedback_y = r1_left.y
            r2_top = pin_position(r2, "2")
            assert frozenset((node_1, (node_1[0], feedback_y))) in edges
            assert frozenset(((node_1[0], feedback_y), (r1_left.x, r1_left.y))) in edges
            assert frozenset((node_2, (node_2[0], r2_top.y))) in edges
            assert frozenset(((node_2[0], r2_top.y), (r2_top.x, r2_top.y))) in edges
            assert any(output_branch in edge for edge in edges)


def test_sch107_bypass_paths_are_conventional_visible_routes():
    sheet = _sch107()
    components = {component.ref: component for component in sheet.components}
    edges = _edges(sheet)
    switch = components["SW1071"]

    for pin_name in ("L_DIRECT", "L_FILTER", "R_DIRECT", "R_FILTER"):
        pin = pin_position(switch, pin_name)
        assert any((pin.x, pin.y) in edge for edge in edges)

    for channel, pin_name, tp_ref in (
        ("L", "L_OUT", "TP7004"),
        ("R", "R_OUT", "TP7504"),
    ):
        switch_pin = pin_position(switch, pin_name)
        tp_pin = pin_position(components[tp_ref], "TP")
        assert frozenset((
            (switch_pin.x, switch_pin.y), (tp_pin.x, switch_pin.y),
        )) in edges
        assert frozenset((
            (tp_pin.x, switch_pin.y), (tp_pin.x, tp_pin.y),
        )) in edges
        assert frozenset(((tp_pin.x, tp_pin.y), (align_coordinate(455), tp_pin.y))) in edges


def test_sch107_true_branches_get_deterministic_junction_points():
    sheet = _sch107()
    points = {(round(point.x, 8), round(point.y, 8)) for point in junction_points(sheet.wires)}

    for requested_y in (78, 185):
        sy = align_coordinate(requested_y)
        assert (round(align_coordinate(35), 8), round(sy, 8)) in points
        for x in (90, 120, 230, 260):
            assert (round(align_coordinate(x), 8), round(sy, 8)) in points
