from generator.blocks.final_gain import add_final_gain
from generator.core.geometry import Point
from generator.core.pins import pin_position
from generator.core.sheet import Sheet


def _sch104():
    sheet = Sheet(
        title="SCH104 - Post-filter isolation buffer",
        filename="ProjectShellac_SCH104.kicad_sch",
    )
    add_final_gain(sheet)
    return sheet


def _wire_endpoints(sheet):
    return {
        frozenset(((wire.x1, wire.y1), (wire.x2, wire.y2)))
        for wire in sheet.wires
    }


def test_sch104_interface_labels_are_not_repeated_as_component_stubs():
    sheet = _sch104()
    names = [label.name for label in sheet.labels]

    for name in ("FILTERED_L", "BUFFERED_L", "FILTERED_R", "BUFFERED_R"):
        assert names.count(name) == 1


def test_sch104_signal_chain_is_drawn_with_visible_continuous_wires():
    sheet = _sch104()
    wires = _wire_endpoints(sheet)
    components = {component.ref: component for component in sheet.components}

    for channel, opamp_ref, resistor_ref, input_tp_ref, output_tp_ref in (
        ("L", "U401", "R4001", "TP4001", "TP4002"),
        ("R", "U402", "R4501", "TP4501", "TP4502"),
    ):
        opamp = components[opamp_ref]
        output_resistor = components[resistor_ref]
        input_tp = components[input_tp_ref]
        output_tp = components[output_tp_ref]

        input_tp_pin = pin_position(input_tp, "TP")
        output_tp_pin = pin_position(output_tp, "TP")
        y = input_tp_pin.y
        from generator.core.grid import align_coordinate
        assert frozenset(((align_coordinate(125), y), (input_tp_pin.x, y))) in wires
        assert frozenset(((input_tp_pin.x, y), (pin_position(opamp, "IN").x, y))) in wires
        assert frozenset((
            (pin_position(opamp, "OUT").x, y),
            (pin_position(output_resistor, "1").x, y),
        )) in wires
        assert frozenset(((pin_position(output_resistor, "2").x, y), (output_tp_pin.x, y))) in wires
        assert frozenset(((output_tp_pin.x, y), (align_coordinate(310), y))) in wires
        assert input_tp_pin == Point(input_tp.at.x, y)
        assert output_tp_pin == Point(output_tp.at.x, y)
