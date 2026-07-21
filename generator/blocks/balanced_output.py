"""SCH108 human-reviewable THAT1646 balanced-output and mute builder.

The approved electrical topology is unchanged.  The sheet is arranged for
conventional review: signal flow is visible from MODE_L/R through the mute,
THAT1646, output protection and panel XLRs without internal net labels standing
in for conductors.
"""

from __future__ import annotations

from generator.core.components import Component, capacitor, testpoint
from generator.core.geometry import Point
from generator.core.pins import pin_position
from generator.model.output_driver import (
    COMMON_MODE_CAPACITANCE_UF,
    DECOUPLING_BULK_UF,
    DECOUPLING_HF_NF,
    DESIGN_OUTPUT_RMS_V,
    DIFFERENTIAL_GAIN_DB,
    DRIVER,
    MUTE_SWITCH,
    RFI_CAPACITANCE_PF,
    SURGE_DIODE,
)


def _driver(ref: str, ch: str, at: Point) -> Component:
    return Component(
        ref=ref,
        lib_id="ProjectShellac:Balanced_Line_Driver_Block",
        value=f"{ch} {DRIVER}",
        at=at,
        footprint="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm",
        fields={
            "Function": "Floating balanced line driver",
            "Device": DRIVER,
            "Supply": "+18V / -18V",
            "Differential Gain": f"2.000x / {DIFFERENTIAL_GAIN_DB:.3f} dB",
            "Design Output Ceiling": f"{DESIGN_OUTPUT_RMS_V:g} V RMS differential",
            "Pinout": "1 OUT-, 2 SNS-, 3 GND, 4 IN, 5 VEE, 6 VCC, 7 SNS+, 8 OUT+",
        },
    )


def _mute(ref: str, at: Point) -> Component:
    return Component(
        ref=ref,
        lib_id="ProjectShellac:Switch_Mute_Block",
        value="STEREO OUTPUT MUTE",
        at=at,
        footprint="",
        fields={
            "Function": "Select MODE_L/R or 0VA into each THAT1646 input",
            "Type": MUTE_SWITCH,
            "Muted state": "Both line-driver inputs connected to 0VA",
        },
        on_board=False,
    )


def _xlr(ref: str, ch: str, at: Point) -> Component:
    return Component(
        ref=ref,
        lib_id="Connector_Generic:Conn_01x03",
        value=f"{ch} BALANCED OUTPUT XLR",
        at=at,
        footprint="",
        fields={
            "Function": "Panel-mounted male XLR output",
            "Pin 1": "CHASSIS",
            "Pin 2": "HOT/+",
            "Pin 3": "COLD/-",
            "Wiring": "Internal star-quad; no connector PCB",
        },
        on_board=False,
    )


def _diode(
    ref: str,
    value: str,
    at: Point,
    function: str,
    *,
    rotation: float = 0.0,
) -> Component:
    return Component(
        ref=ref,
        lib_id="Device:D",
        value=value,
        at=at,
        footprint="Diode_SMD:D_SMA",
        fields={"Function": function},
        rotation=rotation,
    )


def _ferrite(ref: str, at: Point, function: str) -> Component:
    return Component(
        ref=ref,
        lib_id="Device:Ferrite_Bead",
        value="Ferrite bead",
        at=at,
        footprint="Inductor_SMD:L_0805_2012Metric",
        fields={"Function": function},
    )


def _wire_path(sheet, *points: Point) -> None:
    for start, end in zip(points, points[1:]):
        sheet.connect_points(start, end)


def _inline_testpoint(sheet, ref: str, value: str, at: Point, start: Point, end: Point):
    tp = sheet.add_component(testpoint(ref, value, at))
    tp_pin = pin_position(tp, "TP")
    _wire_path(sheet, start, tp_pin, end)
    return tp


def _sense_capacitor(
    sheet,
    *,
    ref: str,
    value: str,
    at: Point,
    output_pin: Point,
    sense_pin: Point,
    function: str,
):
    """Place one OUT-to-SNS capacitor between two separate conductors."""
    cap = sheet.add_component(capacitor(
        ref,
        value,
        at,
        dielectric="Non-polar electrolytic",
        voltage="35V min",
        function=function,
    ))
    pin_1 = pin_position(cap, "1")
    pin_2 = pin_position(cap, "2")

    # Use the capacitor terminal physically nearest each driver pin.  The two
    # routes remain on opposite sides of the capacitor and can never collapse
    # onto one shared vertical lane.
    if abs(pin_1.y - output_pin.y) <= abs(pin_2.y - output_pin.y):
        output_cap_pin, sense_cap_pin = pin_1, pin_2
    else:
        output_cap_pin, sense_cap_pin = pin_2, pin_1

    # Use direct pin-to-pin conductors.  Native KiCad ERC has shown that the
    # generated multi-segment bend routes can be interpreted as separate
    # dangling segments even when their displayed endpoints coincide.  A
    # single conductor per capacitor terminal is electrically unambiguous.
    sheet.connect_points(output_pin, output_cap_pin)
    sheet.connect_points(sense_cap_pin, sense_pin)
    return cap


def _protection_leg(
    sheet,
    *,
    ch: str,
    base: int,
    index: int,
    driver_pin: Point,
    xlr_pin: Point,
    y: float,
    polarity: str,
):
    """Draw one output leg with explicit, non-crossing protection branches."""
    bead = sheet.add_component(_ferrite(
        f"FB{base}{1 + index}",
        Point(250.0, y),
        f"{ch} {polarity} output RFI isolation",
    ))
    bead_1 = pin_position(bead, "1")
    bead_2 = pin_position(bead, "2")
    sheet.connect_points(driver_pin, bead_1)

    # Three explicit branch points split the main conductor.  The upper output
    # leg branches upward and the lower output leg branches downward, so the
    # two protection networks cannot cross or merge.
    outward = -1.0 if index == 1 else 1.0
    branch_points = (
        Point(285.0, y),
        Point(320.0, y),
        Point(355.0, y),
    )
    sheet.connect_points(bead_2, branch_points[0])
    sheet.connect_points(branch_points[0], branch_points[1])
    sheet.connect_points(branch_points[1], branch_points[2])

    tp = sheet.add_component(testpoint(
        f"TP{base}{2 + index}",
        f"{ch}_OUT_{'POS' if polarity == 'positive' else 'NEG'}",
        Point(branch_points[0].x, y - 5.08),
    ))
    sheet.connect_points(branch_points[0], pin_position(tp, "TP"))

    rf_cap = sheet.add_component(capacitor(
        f"C{base}{20 + index}",
        f"{RFI_CAPACITANCE_PF:g}p",
        Point(branch_points[0].x, y + outward * 18.0),
        dielectric="C0G",
        voltage="100V min",
        function=f"{ch} connector-side RF shunt to CHASSIS",
    ))
    # Device:C pin geometry is expressed in symbol coordinates and inverted
    # onto the sheet.  Select the terminal nearest the signal conductor after
    # rendering, rather than inferring it from the nominal pin number.
    rf_pin_1 = pin_position(rf_cap, "1")
    rf_pin_2 = pin_position(rf_cap, "2")
    if abs(rf_pin_1.y - y) <= abs(rf_pin_2.y - y):
        rf_near, rf_far = rf_pin_1, rf_pin_2
    else:
        rf_near, rf_far = rf_pin_2, rf_pin_1
    sheet.connect_points(branch_points[0], rf_near)
    sheet.connect_points(rf_far, Point(rf_far.x, rf_far.y + outward * 6.0))
    sheet.add_label("CHASSIS", rf_far.x, rf_far.y + outward * 6.0)

    # Vertical clamp symbols keep rail stubs away from both signal conductors.
    if outward > 0:
        d_pos_rotation, d_neg_rotation = 90.0, 270.0
        d_pos_output_pin, d_neg_output_pin = "A", "K"
        d_pos_rail_pin, d_neg_rail_pin = "K", "A"
    else:
        d_pos_rotation, d_neg_rotation = 270.0, 90.0
        d_pos_output_pin, d_neg_output_pin = "A", "K"
        d_pos_rail_pin, d_neg_rail_pin = "K", "A"

    d_pos = sheet.add_component(_diode(
        f"D{base}{30 + index * 2}",
        SURGE_DIODE,
        Point(branch_points[1].x, y + outward * 18.0),
        f"{ch} phantom clamp from output to +18V",
        rotation=d_pos_rotation,
    ))
    d_neg = sheet.add_component(_diode(
        f"D{base}{31 + index * 2}",
        SURGE_DIODE,
        Point(branch_points[2].x, y + outward * 18.0),
        f"{ch} phantom clamp from -18V to output",
        rotation=d_neg_rotation,
    ))
    sheet.connect_points(branch_points[1], pin_position(d_pos, d_pos_output_pin))
    sheet.connect_points(branch_points[2], pin_position(d_neg, d_neg_output_pin))
    sheet.connect_pin_to_net(
        d_pos, d_pos_rail_pin, "+18V", stub_dy=outward * 6.0
    )
    sheet.connect_pin_to_net(
        d_neg, d_neg_rail_pin, "-18V", stub_dy=outward * 6.0
    )

    interface_name = f"OUTPUT_{ch}_{'POS' if polarity == 'positive' else 'NEG'}"
    sheet.add_label(interface_name, branch_points[2].x, branch_points[2].y)

    _wire_path(
        sheet,
        branch_points[2],
        Point(385.0, y),
        Point(385.0, xlr_pin.y),
        xlr_pin,
    )


def _add_channel(
    sheet,
    *,
    ch: str,
    idx: int,
    y: float,
    mute_output_pin: Point,
) -> None:
    base = 800 + idx * 100
    driver = sheet.add_component(_driver(f"U{base}1", ch, Point(185.0, y)))
    driver_in = pin_position(driver, "IN")

    # Mute output, input test point and THAT1646 input form one visible path.
    input_tp = sheet.add_component(testpoint(
        f"TP{base}1", f"{ch}_DRIVER_IN", Point(140.0, y - 5.08)
    ))
    input_tp_pin = pin_position(input_tp, "TP")
    route_x = 112.0 + idx * 18.0
    _wire_path(
        sheet,
        mute_output_pin,
        Point(route_x, mute_output_pin.y),
        Point(route_x, input_tp_pin.y),
        input_tp_pin,
        driver_in,
    )

    sheet.connect_pin_to_net(driver, "+V", "+18V", stub_dy=-7.0)
    sheet.connect_pin_to_net(driver, "-V", "-18V", stub_dy=7.0)
    sheet.connect_pin_to_net(driver, "GND", "0VA", stub_dy=7.0)

    out_pos_pin = pin_position(driver, "OUT+")
    out_neg_pin = pin_position(driver, "OUT-")
    sns_pos_pin = pin_position(driver, "SNS+")
    sns_neg_pin = pin_position(driver, "SNS-")

    # Manufacturer-recommended common-mode sense capacitors are shown as
    # visible loops between each output and its matching sense input.
    _sense_capacitor(
        sheet,
        ref=f"C{base}10",
        value=f"{COMMON_MODE_CAPACITANCE_UF:g}u NP",
        at=Point(218.0, (out_pos_pin.y + sns_pos_pin.y) / 2.0),
        output_pin=out_pos_pin,
        sense_pin=sns_pos_pin,
        function=f"{ch} OUT+ to SNS+ common-mode capacitor",
    )
    _sense_capacitor(
        sheet,
        ref=f"C{base}11",
        value=f"{COMMON_MODE_CAPACITANCE_UF:g}u NP",
        at=Point(235.0, (out_neg_pin.y + sns_neg_pin.y) / 2.0),
        output_pin=out_neg_pin,
        sense_pin=sns_neg_pin,
        function=f"{ch} OUT- to SNS- common-mode capacitor",
    )

    xlr = sheet.add_component(_xlr(f"J{base}1", ch, Point(415.0, y)))
    xlr_chassis = pin_position(xlr, "1")
    xlr_pos = pin_position(xlr, "2")
    xlr_neg = pin_position(xlr, "3")
    sheet.connect_pin_to_net(xlr, "1", "CHASSIS", stub_dx=-8.0)

    _protection_leg(
        sheet,
        ch=ch,
        base=base,
        index=0,
        driver_pin=out_pos_pin,
        xlr_pin=xlr_pos,
        y=out_pos_pin.y,
        polarity="positive",
    )
    _protection_leg(
        sheet,
        ch=ch,
        base=base,
        index=1,
        driver_pin=out_neg_pin,
        xlr_pin=xlr_neg,
        y=out_neg_pin.y,
        polarity="negative",
    )

    # Local driver decoupling is grouped beneath each active stage.
    for rail_index, (rail, x) in enumerate((("+18V", 165.0), ("-18V", 205.0))):
        hf = sheet.add_component(capacitor(
            f"C{base}{40 + rail_index}",
            f"{DECOUPLING_HF_NF:g}n",
            Point(x, y + 45.0),
            dielectric="C0G/X7R",
            voltage="50V min",
            function=f"{ch} local {rail} HF decoupling",
        ))
        bulk = sheet.add_component(capacitor(
            f"C{base}{42 + rail_index}",
            f"{DECOUPLING_BULK_UF:g}u",
            Point(x, y + 63.0),
            dielectric="Low-ESR electrolytic",
            voltage="35V min",
            function=f"{ch} local {rail} bulk decoupling",
        ))
        sheet.connect_vertical_two_pin(hf, rail, "0VA")
        sheet.connect_vertical_two_pin(bulk, rail, "0VA")


def add_balanced_output(sheet) -> None:
    sheet.add_note("SCH108 HUMAN-REVIEWABLE: visible mute, THAT1646, protection and XLR signal paths.")
    sheet.add_note("One THAT1646 floating balanced line driver per channel; differential gain is +6.021 dB.")
    sheet.add_note("Stereo 2PDT break-before-make mute selects MODE_L/R or 0VA at the driver inputs.")
    sheet.add_note("10 uF NP capacitors visibly connect OUT+ to SNS+ and OUT- to SNS-.")
    sheet.add_note("Each XLR leg has a ferrite bead, 100 pF C0G shunt to CHASSIS, and rail clamps.")
    sheet.add_note("XLR pin 1 connects directly to CHASSIS; pins 2/3 are hot/cold.")

    mute = sheet.add_component(_mute("SW801", Point(75.0, 150.0)))

    # Each external signal approaches its own switch contact horizontally.
    # There are no shared vertical input lanes.
    for ch, signal_pin, interface, tp_ref in (
        ("L", "L_SIGNAL", "MODE_L", "TP8010"),
        ("R", "R_SIGNAL", "MODE_R", "TP8011"),
    ):
        mute_pin = pin_position(mute, signal_pin)
        tp = sheet.add_component(testpoint(
            tp_ref, f"{ch}_MODE_IN", Point(35.0, mute_pin.y - 5.08)
        ))
        tp_pin = pin_position(tp, "TP")
        interface_start = Point(15.0, mute_pin.y)
        sheet.add_label(interface, interface_start.x, interface_start.y)
        _wire_path(sheet, interface_start, tp_pin, mute_pin)

    # Mute returns route rightwards into separate 0VA stubs.  They never cross
    # either MODE input conductor or the two selected-output conductors.
    l_mute = pin_position(mute, "L_MUTE")
    r_mute = pin_position(mute, "R_MUTE")
    _wire_path(sheet, l_mute, Point(67.0, l_mute.y), Point(67.0, 125.0))
    sheet.add_label("0VA", 67.0, 125.0)
    _wire_path(sheet, r_mute, Point(72.0, r_mute.y), Point(72.0, 120.0))
    sheet.add_label("0VA", 72.0, 120.0)

    _add_channel(
        sheet,
        ch="L",
        idx=0,
        y=90.0,
        mute_output_pin=pin_position(mute, "L_OUT"),
    )
    _add_channel(
        sheet,
        ch="R",
        idx=1,
        y=190.0,
        mute_output_pin=pin_position(mute, "R_OUT"),
    )
