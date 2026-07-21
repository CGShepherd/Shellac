from generator.blocks.replay_eq import add_replay_equalisation
from generator.core.pins import pin_position
from generator.core.sheet import Sheet
from generator.model.replay_eq import (
    BASS_NETWORKS, RIAA_BASS_NETWORK, TREBLE_NETWORKS,
)


def _sheet():
    sheet = Sheet("SCH103", "SCH103.kicad_sch")
    add_replay_equalisation(sheet)
    return sheet


def _edges(sheet):
    return {
        frozenset(((wire.x1, wire.y1), (wire.x2, wire.y2)))
        for wire in sheet.wires
    }


def test_sch103_uses_only_interface_and_supply_labels():
    sheet = _sheet()
    labels = {label.name for label in sheet.labels}
    assert {"PRE_EQ_L", "PRE_EQ_R", "POST_EQ_L", "POST_EQ_R"}.issubset(labels)
    forbidden_prefixes = (
        "L_LF_", "R_LF_", "L_HF_", "R_HF_", "L_REC_", "R_REC_",
        "L_BASS_", "R_BASS_", "L_TREBLE_", "R_TREBLE_",
    )
    assert not any(name.startswith(forbidden_prefixes) for name in labels)


def test_sch103_component_values_remain_frozen():
    sheet = _sheet()
    by_ref = {component.ref: component for component in sheet.components}
    expected_bass = list(BASS_NETWORKS[1:]) + [RIAA_BASS_NETWORK]
    for base in (300, 350):
        assert by_ref[f"R{base}01"].value == "100k"
        assert by_ref[f"R{base}02"].value == "2.70k"
        assert by_ref[f"R{base}30"].value == "750"
        for i, item in enumerate(expected_bass):
            assert by_ref[f"R{base}{10+i}"].value == f"{item.rs_ohm:g}"
        assert by_ref[f"R{base}40"].value == "10000"
        assert by_ref[f"R{base}41"].value == "11000"


def test_sch103_selector_branches_are_directly_wired():
    sheet = _sheet()
    by_ref = {component.ref: component for component in sheet.components}
    edges = _edges(sheet)
    for base in (300, 350):
        swb = by_ref[f"SW{base}1"]
        for i, pin_name in enumerate(("B200", "B400", "B500", "RIAA")):
            cap = by_ref[f"C{base}{10+i}"]
            assert frozenset((
                (pin_position(cap, "2").x, pin_position(cap, "2").y),
                (pin_position(swb, pin_name).x, pin_position(swb, pin_name).y),
            )) in edges
        swt = by_ref[f"SW{base}2"]
        for i, pin_name in enumerate(("T1600", "T2121", "T3400", "T5800")):
            cap = by_ref[f"C{base}{30+i}"]
            assert frozenset((
                (pin_position(swt, pin_name).x, pin_position(swt, pin_name).y),
                (pin_position(cap, "1").x, pin_position(cap, "1").y),
            )) in edges


def test_sch103_testpoints_are_on_real_signal_nodes():
    sheet = _sheet()
    by_ref = {component.ref: component for component in sheet.components}
    degree = {}
    for wire in sheet.wires:
        for point in ((wire.x1, wire.y1), (wire.x2, wire.y2)):
            degree[point] = degree.get(point, 0) + 1
    for base in (300, 350):
        for index in range(1, 5):
            pin = pin_position(by_ref[f"TP{base}{index}"], "TP")
            assert degree[(pin.x, pin.y)] >= 1


def test_sch103_has_no_zero_length_wires():
    sheet = _sheet()
    assert all((wire.x1, wire.y1) != (wire.x2, wire.y2) for wire in sheet.wires)



def test_treble_selector_common_splits_main_signal_path():
    from generator.blocks.replay_eq import add_replay_equalisation
    from generator.core.pins import pin_position
    from generator.core.sheet import Sheet

    sheet = Sheet("SCH103", "SCH103.kicad_sch")
    add_replay_equalisation(sheet)
    components = {component.ref: component for component in sheet.components}
    edges = {
        frozenset(((wire.x1, wire.y1), (wire.x2, wire.y2)))
        for wire in sheet.wires
    }

    for sw_ref, rt_ref, recovery_ref in (
        ("SW3002", "R30030", "U3002"),
        ("SW3502", "R35030", "U3502"),
    ):
        common = pin_position(components[sw_ref], "COMMON")
        rt_out = pin_position(components[rt_ref], "2")
        recovery_in = pin_position(components[recovery_ref], "IN+")
        assert frozenset(((rt_out.x, rt_out.y), (common.x, common.y))) in edges
        assert frozenset(((common.x, common.y), (recovery_in.x, recovery_in.y))) in edges


def test_sch103_supply_and_ground_labels_terminate_one_wire_only():
    sheet = Sheet("SCH103", "SCH103.kicad_sch")
    add_replay_equalisation(sheet)
    endpoints = {}
    for wire in sheet.wires:
        for point in ((wire.x1, wire.y1), (wire.x2, wire.y2)):
            endpoints[point] = endpoints.get(point, 0) + 1

    for label in sheet.labels:
        if label.name in {"+18V", "-18V", "0VA"}:
            assert endpoints.get((label.x, label.y), 0) == 1


def test_root_only_global_names_cannot_collide_with_engineering_signal_names(tmp_path):
    from generator.dispatch import build_project_from_model, shellac_builder_registry
    from generator.model.shellac import build_shellac_model

    build_project_from_model(
        build_shellac_model(), shellac_builder_registry(),
        out_dir=tmp_path, project_name="ProjectShellac",
    )
    text = (tmp_path / "ProjectShellac.kicad_sch").read_text(encoding="utf-8")
    global_names = set(__import__("re").findall(r'\(global_label "([^"]+)"', text))
    assert global_names
    assert all(name.startswith("ROOT__") for name in global_names)
