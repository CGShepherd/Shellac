from generator.blocks.controls import add_controls
from generator.core.pins import pin_position
from generator.core.sheet import Sheet


def _sheet():
    sheet = Sheet("SCH109", "ProjectShellac_SCH109.kicad_sch")
    add_controls(sheet)
    return sheet


def _edges(sheet):
    return {
        frozenset(((wire.x1, wire.y1), (wire.x2, wire.y2)))
        for wire in sheet.wires
    }


def test_sch109_uses_only_control_interface_and_domain_labels():
    labels = {label.name for label in _sheet().labels}
    assert labels == {
        "BASS_SELECT", "TREBLE_SELECT", "MODE_SELECT",
        "RUMBLE_BYPASS", "MUTE_CONTROL", "+18V", "-18V", "0VA",
    }


def test_sch109_control_interfaces_are_visible_single_stubs():
    sheet = _sheet()
    components = {component.ref: component for component in sheet.components}
    labels = {label.name: (label.x, label.y) for label in sheet.labels}
    edges = _edges(sheet)
    expected = {
        "SW901": "BASS_SELECT",
        "SW902": "TREBLE_SELECT",
        "SW903": "MODE_SELECT",
        "SW904": "RUMBLE_BYPASS",
        "SW905": "MUTE_CONTROL",
    }
    for ref, net in expected.items():
        pin = pin_position(components[ref], "CONTROL")
        label = labels[net]
        assert frozenset(((pin.x, pin.y), label)) in edges


def test_sch109_indicator_branches_are_complete_and_orthogonal():
    sheet = _sheet()
    components = {component.ref: component for component in sheet.components}
    edges = _edges(sheet)

    assert all(
        wire.x1 == wire.x2 or wire.y1 == wire.y2
        for wire in sheet.wires
    )

    for led_ref, resistor_ref, tp_ref, rail in (
        ("LED901", "R906", "TP9901", "+18V"),
        ("LED902", "R907", "TP9902", "-18V"),
    ):
        led = components[led_ref]
        resistor = components[resistor_ref]
        tp = components[tp_ref]
        drive_led_pin = pin_position(led, "A" if rail == "+18V" else "K")
        return_led_pin = pin_position(led, "K" if rail == "+18V" else "A")
        drive_resistor_pin = pin_position(resistor, "1")
        tp_pin = pin_position(tp, "TP")

        assert frozenset((
            (drive_resistor_pin.x, drive_resistor_pin.y),
            (drive_led_pin.x, drive_led_pin.y),
        )) in edges
        assert frozenset((
            (tp_pin.x, tp_pin.y),
            (drive_led_pin.x, drive_led_pin.y),
        )) in edges
        assert any(
            (wire.x1, wire.y1) == (return_led_pin.x, return_led_pin.y)
            or (wire.x2, wire.y2) == (return_led_pin.x, return_led_pin.y)
            for wire in sheet.wires
        )


def test_sch109_testpoint_taps_are_horizontal_not_diagonal():
    sheet = _sheet()
    components = {component.ref: component for component in sheet.components}
    edges = _edges(sheet)
    for led_ref, tp_ref, pin_name in (
        ("LED901", "TP9901", "A"),
        ("LED902", "TP9902", "K"),
    ):
        led_pin = pin_position(components[led_ref], pin_name)
        tp_pin = pin_position(components[tp_ref], "TP")
        assert led_pin.y == tp_pin.y
        assert frozenset(((led_pin.x, led_pin.y), (tp_pin.x, tp_pin.y))) in edges
