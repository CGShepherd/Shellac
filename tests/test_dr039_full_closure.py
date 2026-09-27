from generator.blocks.replay_eq import add_replay_equalisation
from generator.blocks.rumble_filter import add_rumble_filter
from generator.core.pins import pin_position
from generator.core.sheet import Sheet
from generator.layout.placement_clusters import build_cluster_placement_baseline
from generator.model.post_eq_dc_block import (
    BIAS_RESISTANCE_VALUE,
    CAPACITANCE_VALUE,
    CAPACITOR_DIELECTRIC,
    CAPACITOR_FOOTPRINT,
    CAPACITOR_VOLTAGE,
    DIRECT_BRANCH_REFS,
    cutoff_hz,
    magnitude_db,
)


def _sheet(builder, title):
    sheet = Sheet(title, f"{title}.kicad_sch")
    builder(sheet)
    return sheet


def _wire_graph(sheet):
    graph = {}
    for wire in sheet.wires:
        a = (wire.x1, wire.y1)
        b = (wire.x2, wire.y2)
        graph.setdefault(a, set()).add(b)
        graph.setdefault(b, set()).add(a)
    return graph


def _reachable(sheet, start):
    graph = _wire_graph(sheet)
    todo = [(start.x, start.y)]
    seen = set(todo)
    while todo:
        here = todo.pop()
        for nxt in graph.get(here, ()):
            if nxt not in seen:
                seen.add(nxt)
                todo.append(nxt)
    return seen


def _labels_reachable(sheet, start):
    points = _reachable(sheet, start)
    return {label.name for label in sheet.labels if (label.x, label.y) in points}


def test_dr039_is_absent_from_sch103_common_pre_split_path():
    sheet = _sheet(add_replay_equalisation, "SCH103")
    components = {component.ref: component for component in sheet.components}

    for ref in ("C30060", "R30060", "C35060", "R35060"):
        assert ref not in components

    for channel, base in (("L", 300), ("R", 350)):
        recovery_tp = components[f"TP{base}4"]
        post_eq_tp = components[f"TP{base}5"]
        assert recovery_tp.value == f"{channel}_RECOVERY_OUT"
        assert post_eq_tp.value == f"{channel}_POST_EQ"
        assert f"POST_EQ_{channel}" in _labels_reachable(
            sheet, pin_position(recovery_tp, "TP")
        )
        assert f"POST_EQ_{channel}" in _labels_reachable(
            sheet, pin_position(post_eq_tp, "TP")
        )


def test_dr039_stable_identities_live_only_in_sch107_direct_branches():
    sheet = _sheet(add_rumble_filter, "SCH107")
    components = {component.ref: component for component in sheet.components}
    switch = components["SW1071"]

    for channel, direct_pin_name, filter_pin_name in (
        ("L", "L_DIRECT", "L_FILTER"),
        ("R", "R_DIRECT", "R_FILTER"),
    ):
        cap_ref, bias_ref = DIRECT_BRANCH_REFS[channel]
        cap = components[cap_ref]
        bias = components[bias_ref]

        assert cap.value == CAPACITANCE_VALUE
        assert cap.fields["Dielectric"] == CAPACITOR_DIELECTRIC
        assert cap.fields["Voltage"] == CAPACITOR_VOLTAGE
        assert cap.footprint == CAPACITOR_FOOTPRINT
        assert bias.value == BIAS_RESISTANCE_VALUE
        assert bias.fields["Tolerance"] == "1%"

        cap_in = pin_position(cap, "2")
        cap_out = pin_position(cap, "1")
        assert f"POST_EQ_{channel}" in _labels_reachable(sheet, cap_in)

        direct_points = _reachable(sheet, pin_position(switch, direct_pin_name))
        assert (cap_out.x, cap_out.y) in direct_points

        filter_points = _reachable(sheet, pin_position(switch, filter_pin_name))
        assert (cap_out.x, cap_out.y) not in filter_points

        bias_pins = [pin_position(bias, "1"), pin_position(bias, "2")]
        connected_to_direct = [
            pin for pin in bias_pins if (pin.x, pin.y) in _reachable(sheet, cap_out)
        ]
        assert len(connected_to_direct) == 1
        ground_pin = next(pin for pin in bias_pins if pin not in connected_to_direct)
        assert "0VA" in _labels_reachable(sheet, ground_pin)

    # The filtered path begins with the existing SCH107 high-pass capacitors.
    for channel, ref in (("L", "C7001"), ("R", "C7501")):
        assert f"POST_EQ_{channel}" in _labels_reachable(
            sheet, pin_position(components[ref], "2")
        )


def test_dr039_component_placement_ownership_moves_atomically_to_sch107():
    model = build_cluster_placement_baseline()
    owners = {
        ref: cluster.identifier
        for cluster in model.clusters
        for ref in cluster.member_refs
    }
    assert owners["C30060"] == "CLU-107-L"
    assert owners["R30060"] == "CLU-107-L"
    assert owners["C35060"] == "CLU-107-R"
    assert owners["R35060"] == "CLU-107-R"


def test_dr039_branch_response_contract_is_preserved():
    assert 0.4 < cutoff_hz() < 0.6
    assert magnitude_db(20.0) > -0.01
