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
        assert by_ref[f"C{base}60"].value == "1u"
        assert by_ref[f"C{base}60"].footprint == "Capacitor_THT:C_Rect_L7.2mm_W5.0mm_P5.00mm"
        assert by_ref[f"R{base}60"].value == "330k"


def test_sch103_selector_branches_are_directly_wired():
    sheet = _sheet()
    by_ref = {component.ref: component for component in sheet.components}
    edges = _edges(sheet)
    for base in (300, 350):
        swb = by_ref[f"SW{base}1"]
        bass_refs = {
            "B200": (10, 11),
            "B400": (12, 13, 14),
            "B500": (15, 16, 17),
            "RIAA": (18, 19),
        }
        for pin_name, suffixes in bass_refs.items():
            for suffix in suffixes:
                cap = by_ref[f"C{base}{suffix}"]
                assert frozenset((
                    (pin_position(cap, "2").x, pin_position(cap, "2").y),
                    (pin_position(swb, pin_name).x, pin_position(swb, pin_name).y),
                )) in edges
        swt = by_ref[f"SW{base}2"]
        treble_refs = {
            "T1600": (20, 21),
            "T2121": (22,),
            "T3400": (23, 24),
            "T5800": (25, 26),
        }
        for pin_name, suffixes in treble_refs.items():
            for suffix in suffixes:
                cap = by_ref[f"C{base}{suffix}"]
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
        for index in range(1, 6):
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


def test_sch103_physical_capacitor_values_and_packages_are_mirrored():
    from generator.physical_parts import timing_capacitor_footprint

    sheet = _sheet()
    by_ref = {component.ref: component for component in sheet.components}

    expected_parts = []
    next_suffix = 10
    for network in list(BASS_NETWORKS[1:]) + [RIAA_BASS_NETWORK]:
        for value_nf in network.capacitor_parts_nf:
            expected_parts.append((next_suffix, value_nf))
            next_suffix += 1

    next_suffix = 20
    for network in TREBLE_NETWORKS[1:]:
        for value_nf in network.capacitor_parts_nf:
            expected_parts.append((next_suffix, value_nf))
            next_suffix += 1

    def formatted_value(value_nf):
        if value_nf < 1.0:
            return f"{value_nf * 1000:g}p"
        return f"{value_nf:g}n"

    for base in (300, 350):
        for suffix, value_nf in expected_parts:
            component = by_ref[f"C{base}{suffix}"]
            assert component.value == formatted_value(value_nf)
            assert component.footprint == timing_capacitor_footprint(value_nf)
            assert "+" not in component.value
