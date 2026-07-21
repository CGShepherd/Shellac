"""SCH106 human-reviewable power-entry and ground-bond builder.

SR-020 retains the accepted electrical design but replaces repeated labelled
stubs with continuous, conventional rail and bond conductors.
"""

from __future__ import annotations

from generator.core.components import Component, capacitor, resistor, testpoint, minifit_6
from generator.core.geometry import Point
from generator.core.grid import align_coordinate
from generator.core.pins import pin_position


def connector_5(ref, label, at):
    return Component(
        ref=ref, lib_id="Connector_Generic:Conn_01x05", value=label, at=at,
        footprint="",
        fields={
            "Function": "Panel-mounted regulated DC input from external PSU",
            "Pin 1": "0VA", "Pin 2": "+18VA_IN", "Pin 3": "-18VA_IN",
            "Pin 4": "CHASSIS", "Pin 5": "NC_RESERVED",
            "Ownership": "Panel-mounted; harnessed to PCB",
        },
        on_board=False, rotation=180,
    )


def diode(ref, value, at, function="", dnp=False, rotation=0.0):
    fields = {"Function": function}
    if dnp:
        fields["DNP"] = "YES"
    return Component(
        ref=ref,
        lib_id="Device:D",
        value=value,
        at=at,
        footprint="Diode_SMD:D_SOD-123",
        fields=fields,
        dnp=dnp,
        rotation=rotation,
    )


def _wire_path(sheet, *points: Point) -> None:
    for start, end in zip(points, points[1:]):
        if start != end:
            sheet.connect_points(start, end)


def _horizontal_bus(sheet, y: float, xs: tuple[float, ...]) -> None:
    """Draw a bus as explicit endpoint-to-endpoint segments.

    Branch coordinates are included in ``xs`` so SR-019's deterministic
    junction rule can mark every intentional electrical branch.
    """
    _wire_path(sheet, *(Point(x, y) for x in xs))


def _connect_branch(sheet, component, upper_net_pin: str, upper_y: float,
                    lower_net_pin: str, lower_y: float) -> None:
    upper = pin_position(component, upper_net_pin)
    lower = pin_position(component, lower_net_pin)
    sheet.connect_points(Point(upper.x, upper_y), upper)
    sheet.connect_points(lower, Point(lower.x, lower_y))


def _connect_power_entry(sheet, parts) -> None:
    panel = parts["J901"]
    connector = parts["H901"]

    for pin_name in ("1", "2", "3", "4", "5"):
        sheet.connect_points(pin_position(panel, pin_name), pin_position(connector, pin_name))

    # Each inlet pin leaves through an independent short labelled stub.  The
    # matching labels at the visible rail starts avoid any crossing or overlap
    # between the four domains while preserving a conventional sheet interface.
    inlet_lanes = {
        "1": ("0VA", align_coordinate(90.0)),
        "2": ("+18VA_IN", align_coordinate(60.0)),
        "3": ("-18VA_IN", align_coordinate(120.0)),
        "4": ("CHASSIS", align_coordinate(160.0)),
    }
    for pin_name, (net_name, lane_y) in inlet_lanes.items():
        sheet.connect_pin_to_net(connector, pin_name, net_name, stub_dx=10.0)
        sheet.add_label(net_name, align_coordinate(65), lane_y)
    sheet.add_no_connect_pin(connector, "6")

    # Put each test-point pin directly in its conductor.
    test_lanes = {
        "TP901": align_coordinate(60.0),
        "TP902": align_coordinate(90.0),
        "TP903": align_coordinate(120.0),
        "TP904": align_coordinate(160.0),
    }
    for ref, lane_y in test_lanes.items():
        tp_pin = pin_position(parts[ref], "TP")
        assert tp_pin.y == lane_y

    plus_y = test_lanes["TP901"]
    zero_y = test_lanes["TP902"]
    minus_y = test_lanes["TP903"]
    chassis_y = test_lanes["TP904"]

    # Input rails pass through their physical 0-ohm links.  The 0VA and
    # chassis conductors have no series element.
    sheet.connect_points(Point(65, plus_y), pin_position(parts["TP901"], "TP"))
    sheet.connect_points(pin_position(parts["TP901"], "TP"), pin_position(parts["R901"], "1"))
    sheet.connect_points(pin_position(parts["R901"], "2"), Point(120, plus_y))
    sheet.connect_points(Point(65, zero_y), pin_position(parts["TP902"], "TP"))
    sheet.connect_points(pin_position(parts["TP902"], "TP"), Point(120, zero_y))
    sheet.connect_points(Point(65, minus_y), pin_position(parts["TP903"], "TP"))
    sheet.connect_points(pin_position(parts["TP903"], "TP"), pin_position(parts["R902"], "1"))
    sheet.connect_points(pin_position(parts["R902"], "2"), Point(120, minus_y))
    sheet.connect_points(Point(65, chassis_y), pin_position(parts["TP904"], "TP"))
    sheet.connect_points(pin_position(parts["TP904"], "TP"), Point(120, chassis_y))

    plus_xs = (120, 140, 160, 180, 200, 340, 365)
    zero_xs = (120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 365)
    minus_xs = (120, 220, 240, 260, 280, 340, 365)
    chassis_xs = (120, 140, 160, 180, 200, 300, 320, 340, 365)
    _horizontal_bus(sheet, plus_y, plus_xs)
    _horizontal_bus(sheet, zero_y, zero_xs)
    _horizontal_bus(sheet, minus_y, minus_xs)
    _horizontal_bus(sheet, chassis_y, chassis_xs)

    for ref in ("C901", "C902", "C903"):
        _connect_branch(sheet, parts[ref], "1", plus_y, "2", zero_y)
    _connect_branch(sheet, parts["R903"], "1", plus_y, "2", zero_y)
    for ref in ("C904", "C905", "C906"):
        _connect_branch(sheet, parts[ref], "1", zero_y, "2", minus_y)
    _connect_branch(sheet, parts["R904"], "1", zero_y, "2", minus_y)

    # Four explicit parallel bond options join 0VA to chassis.  R909 is the
    # initial fitted direct bond; C909 is the HF bond; the opposed clamps are
    # DNP.  The two domains are otherwise kept visibly separate.
    _connect_branch(sheet, parts["R909"], "1", zero_y, "2", chassis_y)
    _connect_branch(sheet, parts["C909"], "1", zero_y, "2", chassis_y)
    _connect_branch(sheet, parts["D901"], "K", zero_y, "A", chassis_y)
    _connect_branch(sheet, parts["D902"], "A", zero_y, "K", chassis_y)

    # ERC power declarations and the hierarchy interface labels share the
    # actual post-link rails instead of separate labelled stubs.
    sheet.connect_points(Point(340, plus_y), pin_position(parts["PWR901"], "POWER_OUT"))
    sheet.connect_points(Point(340, minus_y), pin_position(parts["PWR902"], "POWER_OUT"))
    for name, y in (("+18V", plus_y), ("0VA", zero_y), ("-18V", minus_y), ("CHASSIS", chassis_y)):
        sheet.add_label(name, 365, y)


def add_power_entry(sheet):
    sheet.add_note("SCH106 POWER ENTRY: regulated dual rails from the external PSU into the audio enclosure.")
    sheet.add_note("SR-020 HUMAN-REVIEW CAPTURE: continuous +18 V, 0VA, -18 V and chassis conductors.")
    sheet.add_note("Initial fit: 0R rail links and R909 direct 0VA-to-chassis bond; clamp diodes remain DNP.")
    sheet.add_note("0VA and CHASSIS are distinct everywhere except the four clearly shown configurable bond branches.")

    components = [
        connector_5("J901", "PANEL PSU DC INPUT", Point(25, 105)),
        minifit_6("H901", "PCB DC HARNESS", Point(48, 105), rotation=180),
        testpoint("TP901", "+18VA_IN", Point(75, 54.92)),
        testpoint("TP902", "0VA_IN", Point(75, 84.92)),
        testpoint("TP903", "-18VA_IN", Point(75, 114.92)),
        testpoint("TP904", "CHASSIS", Point(75, 154.92)),
        resistor("R901", "0R", Point(100, 60), tolerance="1%", function="+18VA entry link"),
        resistor("R902", "0R", Point(100, 120), tolerance="1%", function="-18VA entry link"),
        Component(
            ref="PWR901", lib_id="ProjectShellac:Power_Rail_Source", value="+18V SOURCE",
            at=Point(345.08, 60), in_bom=False, on_board=False,
            fields={"Function": "ERC declaration: post-link +18V rail is driven"},
        ),
        Component(
            ref="PWR902", lib_id="ProjectShellac:Power_Rail_Source", value="-18V SOURCE",
            at=Point(345.08, 120), in_bom=False, on_board=False,
            fields={"Function": "ERC declaration: post-link -18V rail is driven"},
        ),
    ]

    for ref, value, x, function in (
        ("C901", "470u", 140, "+18VA local bulk"),
        ("C902", "1u", 160, "+18VA bypass"),
        ("C903", "100n", 180, "+18VA HF bypass"),
    ):
        components.append(capacitor(
            ref, value, Point(x, 75), dielectric="Film/X7R" if value != "470u" else "Electrolytic",
            voltage="25V" if value != "100n" else "50V", function=function, rotation=180,
            footprint=(
                "Capacitor_THT:CP_Radial_D10.0mm_P5.00mm"
                if value == "470u" else
                "Capacitor_SMD:C_1206_3216Metric" if value == "1u" else
                "Capacitor_SMD:C_0805_2012Metric"
            ),
        ))
    components.append(resistor(
        "R903", "22k", Point(200, 75), tolerance="1%", function="+18VA bleed", rotation=270,
    ))

    for ref, value, x, function in (
        ("C904", "470u", 220, "-18VA local bulk"),
        ("C905", "1u", 240, "-18VA bypass"),
        ("C906", "100n", 260, "-18VA HF bypass"),
    ):
        components.append(capacitor(
            ref, value, Point(x, 105), dielectric="Film/X7R" if value != "470u" else "Electrolytic",
            voltage="25V" if value != "100n" else "50V", function=function, rotation=180,
            footprint=(
                "Capacitor_THT:CP_Radial_D10.0mm_P5.00mm"
                if value == "470u" else
                "Capacitor_SMD:C_1206_3216Metric" if value == "1u" else
                "Capacitor_SMD:C_0805_2012Metric"
            ),
        ))
    components.append(resistor(
        "R904", "22k", Point(280, 105), tolerance="1%", function="-18VA bleed", rotation=270,
    ))

    components.extend([
        resistor("R909", "0R", Point(140, 125), tolerance="1%", function="Initial direct 0VA-CHASSIS bond", rotation=270),
        capacitor("C909", "100n", Point(160, 125), dielectric="Film", voltage="100V", function="HF chassis bond", rotation=180),
        diode("D901", "DNP", Point(180, 125), function="Ground-lift clamp A", dnp=True, rotation=270),
        diode("D902", "DNP", Point(200, 125), function="Ground-lift clamp B", dnp=True, rotation=90),
    ])

    parts = {component.ref: sheet.add_component(component) for component in components}
    _connect_power_entry(sheet, parts)
