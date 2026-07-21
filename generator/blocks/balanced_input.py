"""SCH101 human-reviewable balanced-input schematic builder.

The electrical design remains the frozen AE-010 implementation.  SR-018 only
changes its schematic presentation: the signal and feedback paths are drawn as
continuous conductors, while labels are retained for true hierarchy, power and
the deliberately remote DIP-selector contacts.
"""

from __future__ import annotations

from generator.core.components import (
    Component,
    capacitor,
    diff_converter_block,
    opa1656_gain_block,
    resistor,
    xlr3,
    jst_vh_3,
)
from generator.core.geometry import Point
from generator.core.pins import pin_position
from generator.model.balanced_input import (
    DIFF_CONVERTER_GAIN,
    GAIN_BASE_RF_OHM,
    GAIN_DEFAULT_ADD_OHM,
    GAIN_HIGH_ADD_OHM,
    GAIN_RG_OHM,
    SELECTOR,
)


def _wire_path(sheet, *points: Point) -> None:
    for start, end in zip(points, points[1:]):
        if start != end:
            sheet.connect_points(start, end)


def _label_branch(sheet, name: str, node: Point, *, dy: float) -> None:
    if dy == 0:
        sheet.add_label(name, node.x, node.y)
        return
    end = Point(node.x, node.y + dy)
    sheet.connect_points(node, end)
    sheet.add_label(name, end.x, end.y)


def _gain_selector(ref: str, prefix: str, at: Point) -> Component:
    return Component(
        ref=ref,
        lib_id="ProjectShellac:DIP_Switch_Block",
        value="STEREO GAIN DIP",
        at=at,
        footprint="Button_Switch_THT:SW_DIP_SPSTx08_Slide_9.78x22.5mm_W7.62mm_P2.54mm",
        fields={
            "Function": "Internal matched gain selection for four OPA1656 legs",
            "Type": SELECTOR,
            "Settings": "LOW=00 / DEFAULT=01 / HIGH=10; repeat for L+, L-, R+, R-",
            "Invalid": "11 reserved; do not fit/select",
        },
    )


def _rf_input(sheet, channel: str, refbase: int, centre_y: float, plus_y: float, minus_y: float):
    panel = sheet.add_component(xlr3(
        f"J{refbase}01",
        f"{channel} PANEL INPUT XLR",
        Point(25, centre_y),
        f"{channel} balanced cartridge input",
    ))
    connector = sheet.add_component(jst_vh_3(
        f"H{refbase}01",
        f"{channel} INPUT HARNESS",
        Point(48, centre_y),
        f"{channel} panel-XLR to PCB harness",
        rotation=0,
    ))
    for pin_name in ("1", "2", "3"):
        sheet.connect_points(
            pin_position(panel, pin_name),
            pin_position(connector, pin_name),
        )
    r_plus = sheet.add_component(resistor(
        f"R{refbase}02", "100R", Point(75, plus_y),
        tolerance="1%", function="RF series isolation IN+",
    ))
    r_minus = sheet.add_component(resistor(
        f"R{refbase}03", "100R", Point(75, minus_y),
        tolerance="1%", function="RF series isolation IN-",
    ))

    c_plus = sheet.add_component(capacitor(
        f"C{refbase}01", "1n", Point(108, plus_y - 2.54),
        dielectric="C0G/NP0", voltage="50V", function="Common-mode RF shunt IN+",
    ))
    c_minus = sheet.add_component(capacitor(
        f"C{refbase}02", "1n", Point(108, minus_y + 2.54),
        dielectric="C0G/NP0", voltage="50V", function="Common-mode RF shunt IN-",
    ))
    c_diff = sheet.add_component(capacitor(
        f"C{refbase}03", "220p", Point(130, centre_y),
        dielectric="C0G/NP0", voltage="50V", function="Differential RF shunt",
    ))

    j_plus = pin_position(connector, "2")
    j_minus = pin_position(connector, "3")
    sheet.connect_pin_to_net(connector, "1", "CHASSIS", stub_dx=-8)
    sheet.add_label(f"INPUT_{channel}_POS", j_plus.x, j_plus.y)
    sheet.add_label(f"INPUT_{channel}_NEG", j_minus.x, j_minus.y)

    # Direct pin-to-pin conductors avoid ambiguous intermediate bend endpoints.
    sheet.connect_points(j_plus, pin_position(r_plus, "1"))
    sheet.connect_points(j_minus, pin_position(r_minus, "1"))

    plus_cm_pin = pin_position(c_plus, "1")
    minus_cm_pin = pin_position(c_minus, "2")
    plus_diff_node = Point(130, plus_y)
    minus_diff_node = Point(130, minus_y)
    _wire_path(sheet, pin_position(r_plus, "2"), plus_cm_pin, plus_diff_node)
    _wire_path(sheet, pin_position(r_minus, "2"), minus_cm_pin, minus_diff_node)

    sheet.connect_points(pin_position(c_diff, "2"), plus_diff_node)
    sheet.connect_points(pin_position(c_diff, "1"), minus_diff_node)
    sheet.connect_pin_to_net(c_plus, "2", "CHASSIS", stub_dy=-6)
    sheet.connect_pin_to_net(c_minus, "1", "CHASSIS", stub_dy=6)

    return plus_diff_node, minus_diff_node


def _gain_leg(
    sheet,
    leg_name: str,
    refbase: int,
    suffix: int,
    input_node: Point,
    y: float,
    switch,
    high_bit: int,
    default_bit: int,
):
    leg_code = {
        "L_PLUS": "LP",
        "L_MINUS": "LM",
        "R_PLUS": "RP",
        "R_MINUS": "RM",
    }[leg_name]
    opamp = sheet.add_component(opa1656_gain_block(
        f"U{refbase}0{suffix}",
        f"{leg_name.replace('_PLUS', '+').replace('_MINUS', '-')} GAIN 2.270x",
        Point(190, y),
        f"{leg_name} balanced leg; default 2.270x",
    ))
    fb_pin = pin_position(opamp, "FB-")
    # Keep the positive-leg ladder above its signal path and the negative-leg
    # ladder below.  This leaves a clear central routing corridor to the
    # differential converter.
    feedback_y = y - 20 if suffix == 1 else y + 20

    rg = sheet.add_component(resistor(
        f"R{refbase}{suffix}1", f"{GAIN_RG_OHM:g}", Point(165, fb_pin.y),
        tolerance="0.1%", function="Gain-to-ground resistor",
    ))
    high_add = sheet.add_component(resistor(
        f"R{refbase}{suffix}4", f"{GAIN_HIGH_ADD_OHM:g}", Point(220, feedback_y),
        tolerance="0.1%", function="High-gain feedback segment",
    ))
    default_add = sheet.add_component(resistor(
        f"R{refbase}{suffix}3", f"{GAIN_DEFAULT_ADD_OHM:g}", Point(250, feedback_y),
        tolerance="0.1%", function="Default-gain feedback segment",
    ))
    base = sheet.add_component(resistor(
        f"R{refbase}{suffix}2", f"{GAIN_BASE_RF_OHM:g}", Point(280, feedback_y),
        tolerance="0.1%", function="Fixed feedback base",
    ))

    input_pin = pin_position(opamp, "IN+")
    _wire_path(sheet, input_node, Point(155, input_node.y), Point(155, y), input_pin)

    # Rg is shown explicitly from the inverting node to analogue zero.
    sheet.connect_points(pin_position(rg, "2"), fb_pin)
    sheet.connect_pin_to_net(rg, "1", "0VA", stub_dx=-8)

    # The complete feedback ladder is visible from FB- to OUT.
    high_1, high_2 = pin_position(high_add, "1"), pin_position(high_add, "2")
    default_1, default_2 = pin_position(default_add, "1"), pin_position(default_add, "2")
    base_1, base_2 = pin_position(base, "1"), pin_position(base, "2")
    sheet.connect_points(high_2, default_1)
    sheet.connect_points(default_2, base_1)
    # Return directly to OUT.  A single pin-to-pin conductor avoids
    # intermediate corner endpoints that KiCad may treat as dangling.
    sheet.connect_points(base_2, pin_position(opamp, "OUT"))

    fb3 = f"{leg_code}_FB"
    fb2 = f"{leg_code}_HI"
    fb1 = f"{leg_code}_DEF"
    ladder_label_dy = -10 if suffix == 1 else 10
    fb_label_dy = 10 if suffix == 1 else -10
    _label_branch(sheet, fb3, pin_position(rg, "2"), dy=fb_label_dy)
    _label_branch(sheet, fb3, high_1, dy=ladder_label_dy)
    _label_branch(sheet, fb2, high_2, dy=-ladder_label_dy)
    _label_branch(sheet, fb1, default_2, dy=ladder_label_dy)

    # Remote DIP contacts are identified by the same local node names.  This
    # is clearer than eight long control wires crossing both audio channels.
    sheet.connect_pin_to_net(switch, f"{high_bit}A", fb2, stub_dx=-8)
    sheet.connect_pin_to_net(switch, f"{high_bit}B", fb3, stub_dx=8)
    sheet.connect_pin_to_net(switch, f"{default_bit}A", fb1, stub_dx=-8)
    sheet.connect_pin_to_net(switch, f"{default_bit}B", fb2, stub_dx=8)

    sheet.connect_pin_to_net(opamp, "+V", "+18V", stub_dy=-6)
    sheet.connect_pin_to_net(opamp, "-V", "-18V", stub_dy=6)
    return opamp


def _diff_converter(sheet, channel: str, refbase: int, centre_y: float, plus_opamp, minus_opamp):
    diff = sheet.add_component(diff_converter_block(
        f"U{refbase}03",
        f"{channel} DIFF {DIFF_CONVERTER_GAIN:.2f}x",
        Point(350, centre_y),
        f"{channel} precision differential converter",
    ))
    plus_pin = pin_position(diff, "IN+")
    minus_pin = pin_position(diff, "IN-")

    r_in_p = sheet.add_component(resistor(
        f"R{refbase}30", "10k", Point(315, plus_pin.y),
        tolerance="0.1%", function="Differential converter + input",
    ))
    r_in_m = sheet.add_component(resistor(
        f"R{refbase}31", "10k", Point(315, minus_pin.y),
        tolerance="0.1%", function="Differential converter - input",
    ))
    r_fb = sheet.add_component(resistor(
        f"R{refbase}32", "34.8k", Point(350, centre_y - 20),
        tolerance="0.1%", function="Differential converter feedback",
    ))
    r_ref = sheet.add_component(resistor(
        f"R{refbase}33", "34.8k", Point(315, centre_y + 20),
        tolerance="0.1%", function="Differential converter reference",
    ))

    plus_out = pin_position(plus_opamp, "OUT")
    minus_out = pin_position(minus_opamp, "OUT")
    r_plus_1, r_plus_2 = pin_position(r_in_p, "1"), pin_position(r_in_p, "2")
    r_minus_1, r_minus_2 = pin_position(r_in_m, "1"), pin_position(r_in_m, "2")

    _wire_path(sheet, plus_out, Point(300, plus_out.y), Point(300, r_plus_1.y), r_plus_1)
    sheet.connect_points(r_plus_2, plus_pin)
    _wire_path(sheet, minus_out, Point(305, minus_out.y), Point(305, r_minus_1.y), r_minus_1)
    sheet.connect_points(r_minus_2, minus_pin)

    diff_out = pin_position(diff, "OUT")

    # Use direct pin-to-pin conductors for the feedback and reference legs.
    # This removes all intermediate corners from the precision converter and
    # prevents KiCad from interpreting a bend as a dangling endpoint.
    sheet.connect_points(pin_position(r_fb, "2"), diff_out)
    sheet.connect_points(pin_position(r_fb, "1"), minus_pin)
    sheet.connect_points(pin_position(r_ref, "2"), plus_pin)

    # Route the reference resistor to 0VA vertically, away from both signal
    # output lanes.  The former leftward stub landed on the minus-leg output
    # conductor and shorted that output to 0VA.
    sheet.connect_pin_to_net(r_ref, "1", "0VA", stub_dy=8)

    output_end = Point(390, centre_y)
    sheet.connect_points(diff_out, output_end)
    sheet.add_label(f"PRE_EQ_{channel}", output_end.x, output_end.y)
    sheet.connect_pin_to_net(diff, "+V", "+18V", stub_dy=-6)
    sheet.connect_pin_to_net(diff, "-V", "-18V", stub_dy=6)


def _channel(sheet, channel: str, refbase: int, centre_y: float, switch, bit_base: int) -> None:
    plus_y, minus_y = centre_y - 20, centre_y + 20
    plus_input, minus_input = _rf_input(sheet, channel, refbase, centre_y, plus_y, minus_y)
    plus_opamp = _gain_leg(
        sheet, f"{channel}_PLUS", refbase, 1, plus_input, plus_y,
        switch, bit_base, bit_base + 1,
    )
    minus_opamp = _gain_leg(
        sheet, f"{channel}_MINUS", refbase, 2, minus_input, minus_y,
        switch, bit_base + 2, bit_base + 3,
    )
    _diff_converter(sheet, channel, refbase, centre_y, plus_opamp, minus_opamp)


def add_sch101_diff_converter_slice(sheet) -> None:
    sheet.add_note("SCH101 ELECTRICALLY CLOSED: RF/load network, selectable matched OPA1656 gain pair, precision differential converter.")
    sheet.add_note("SR-018 HUMAN-REVIEW CAPTURE: continuous signal and feedback conductors; labels limited to interfaces, rails and remote DIP contacts.")
    sheet.add_note("Signal path: floating cartridge -> RF/load -> matched JFET leg gain -> 3.48x differential converter -> pre-EQ.")
    sheet.add_note("Total gain settings: LOW 14 dB / DEFAULT 18 dB / HIGH 22 dB. Default aligns with downstream headroom models.")
    sheet.add_note("Internal 8-way DIP repeats the same two-bit setting across L+, L-, R+, and R-. Never mix settings between legs.")
    sheet.add_note("Differential converter: 3.48x using 10k / 34.8k, 0.1% or matched network.")

    switch = sheet.add_component(_gain_selector("SW1011", "STEREO", Point(125, 155)))
    _channel(sheet, "L", 1, 85, switch, 1)
    _channel(sheet, "R", 2, 205, switch, 5)


def add_sch101_rf_slice(sheet):
    """Backward-compatible entry point retained for the existing tests."""
    return add_sch101_diff_converter_slice(sheet)
