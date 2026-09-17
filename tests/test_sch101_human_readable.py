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

def _connected_label_names(sheet, start):
    point = (start.x, start.y)
    adjacency = {}
    for wire in sheet.wires:
        a = (wire.x1, wire.y1); b = (wire.x2, wire.y2)
        adjacency.setdefault(a, set()).add(b)
        adjacency.setdefault(b, set()).add(a)
    labels_by_point = {}
    for label in sheet.labels:
        labels_by_point.setdefault((label.x, label.y), set()).add(label.name)
    seen = {point}; stack = [point]; labels = set()
    while stack:
        current = stack.pop()
        labels |= labels_by_point.get(current, set())
        for nxt in adjacency.get(current, ()):
            if nxt not in seen:
                seen.add(nxt); stack.append(nxt)
    return labels


def test_sch101_every_physical_opamp_package_has_local_hf_bypassing():
    sheet = _sch101()
    components = {component.ref: component for component in sheet.components}
    expected = {
        "C191": ("+18V", "0VA"), "C192": ("0VA", "-18V"),
        "C193": ("+18V", "0VA"), "C194": ("0VA", "-18V"),
        "C291": ("+18V", "0VA"), "C292": ("0VA", "-18V"),
        "C293": ("+18V", "0VA"), "C294": ("0VA", "-18V"),
    }
    for ref, (pin1_net, pin2_net) in expected.items():
        cap = components[ref]
        assert cap.value == "100n"
        assert pin1_net in _connected_label_names(sheet, pin_position(cap, "1"))
        assert pin2_net in _connected_label_names(sheet, pin_position(cap, "2"))


def test_sch101_live_converter_and_lt5400_annotations_are_procurement_realistic():
    sheet = _sch101()
    components = {component.ref: component for component in sheet.components}
    assert "OPA1655" in components["U103"].fields["Function"]
    assert "OPA1655" in components["U203"].fields["Function"]
    for ref in ("RN130", "RN230"):
        rn = components[ref]
        assert rn.fields["Device"] == "LT5400-7"
        assert "B-grade" in rn.fields["Grade"]
        assert "RUN10" in rn.fields["Grade"]
        assert "final EP disposition open" in rn.fields["EP"]
