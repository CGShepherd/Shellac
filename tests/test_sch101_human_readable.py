from generator.blocks.balanced_input import add_sch101_diff_converter_slice
from generator.core.geometry import Point
from generator.core.grid import align_coordinate
from generator.core.pins import pin_position
from generator.core.sheet import Sheet


def _sch101():
    sheet = Sheet(
        title="SCH101 - Balanced Input and Differential Conversion",
        filename="ProjectShellac_SCH101.kicad_sch",
    )
    add_sch101_diff_converter_slice(sheet)
    return sheet


def _edges(sheet):
    return {
        frozenset(((wire.x1, wire.y1), (wire.x2, wire.y2)))
        for wire in sheet.wires
        if (wire.x1, wire.y1) != (wire.x2, wire.y2)
    }


def test_sch101_contains_no_zero_length_wires():
    sheet = _sch101()
    assert all(
        (wire.x1, wire.y1) != (wire.x2, wire.y2)
        for wire in sheet.wires
    )


def test_sch101_main_signal_paths_use_visible_conductors():
    sheet = _sch101()
    components = {component.ref: component for component in sheet.components}
    edges = _edges(sheet)

    for channel, refbase in (("L", 1), ("R", 2)):
        r_plus = components[f"R{refbase}02"]
        r_minus = components[f"R{refbase}03"]
        plus_opamp = components[f"U{refbase}01"]
        minus_opamp = components[f"U{refbase}02"]
        diff = components[f"U{refbase}03"]

        plus_y = pin_position(r_plus, "2").y
        minus_y = pin_position(r_minus, "2").y
        lane_x = align_coordinate(108)
        assert frozenset(((pin_position(r_plus, "2").x, plus_y), (lane_x, plus_y))) in edges
        assert frozenset(((pin_position(r_minus, "2").x, minus_y), (lane_x, minus_y))) in edges
        assert any(
            (pin_position(plus_opamp, "OUT").x, plus_y) in edge
            for edge in edges
        )
        assert any(
            (pin_position(minus_opamp, "OUT").x, minus_y) in edge
            for edge in edges
        )
        assert any(
            (pin_position(diff, "OUT").x, diff.at.y) in edge
            for edge in edges
        )


def test_feedback_ladders_are_physical_series_connections():
    sheet = _sch101()
    components = {component.ref: component for component in sheet.components}
    edges = _edges(sheet)

    for refbase in (1, 2):
        for suffix in (1, 2):
            high = components[f"R{refbase}{suffix}4"]
            default = components[f"R{refbase}{suffix}3"]
            base = components[f"R{refbase}{suffix}2"]
            assert frozenset((
                (pin_position(high, "2").x, pin_position(high, "2").y),
                (pin_position(default, "1").x, pin_position(default, "1").y),
            )) in edges
            assert frozenset((
                (pin_position(default, "2").x, pin_position(default, "2").y),
                (pin_position(base, "1").x, pin_position(base, "1").y),
            )) in edges
