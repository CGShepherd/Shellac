"""SCH105 pin-aware channel-mode matrix builder."""

from __future__ import annotations

from generator.component_selection import bulk_decoupling_capacitor_requirements
from generator.core.components import Component, capacitor, resistor, testpoint
from generator.core.geometry import Point
from generator.core.pins import pin_position
from generator.model.mode_matrix import (
    BUFFER_GAIN, DESIGN_OUTPUT_RMS_V, INPUT_BIAS_RESISTOR_OHM, OPAMP,
    OUTPUT_ISOLATION_OHM, SUM_RESISTOR_OHM, SWITCH_TYPE,
)

def _mode_switch(ref: str, at: Point) -> Component:
    return Component(
        ref=ref, lib_id="ProjectShellac:Mode_Switch_Block", value="MODE 4P4T",
        at=at, footprint="",
        fields={
            "Function": "Stereo / Dual Left / Dual Right / L+R Mono",
            "Type": SWITCH_TYPE,
            "Pole A": "Left output source selection",
            "Pole B": "Right output source selection",
            "Pole C": "Connect left summing branch only in mono",
            "Pole D": "Connect right summing branch only in mono",
        }, on_board=False,
    )

def _buffer(ref: str, channel: str, at: Point) -> Component:
    return Component(
        ref=ref, lib_id="ProjectShellac:OpAmp_Buffer_Block",
        value=f"{channel} MODE BUFFER", at=at,
        footprint="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm",
        fields={
            "Function": "Unity-gain matrix output buffer",
            "Intended Device": OPAMP, "Supply": "+18V / -18V",
            "Gain": f"{BUFFER_GAIN:.3f}x",
            "Design Output Ceiling": f"{DESIGN_OUTPUT_RMS_V:g} V RMS",
        },
    )

def _wire_testpoint(sheet, tp, net_name):
    sheet.connect_pin_to_net(tp, "TP", net_name, stub_dy=-3.0)

def add_mode_matrix(sheet) -> None:
    sheet.add_note("SCH105 PIN-AWARE: passive 4P4T routing followed by dual OPA1656 unity buffers.")
    sheet.add_note("Modes: STEREO, DUAL LEFT, DUAL RIGHT, and L+R MONO on both outputs.")
    sheet.add_note("The switch symbol is a functional electrical model of the approved 4P4T contact truth table.")
    sheet.add_note("Poles C and D connect the 4.7k summing branches only in mono mode.")
    sheet.add_note("Break-before-make switching plus 2.2M input bias resistors prevents floating buffer inputs.")

    y_l, y_r = 90.0, 210.0
    sw = sheet.add_component(_mode_switch("SW501", Point(215.0, 150.0)))

    # Source nets and input evidence.
    sheet.connect_pin_to_net(sw, "L_IN", "BUFFERED_L", stub_dx=-18.0)
    sheet.connect_pin_to_net(sw, "R_IN", "BUFFERED_R", stub_dx=-18.0)
    tp_l_in = sheet.add_component(testpoint("TP501", "L_MODE_IN", Point(145.0, y_l)))
    tp_r_in = sheet.add_component(testpoint("TP502", "R_MODE_IN", Point(145.0, y_r)))
    _wire_testpoint(sheet, tp_l_in, "BUFFERED_L")
    _wire_testpoint(sheet, tp_r_in, "BUFFERED_R")

    # Mono averaging branches. Each source reaches the common MONO node only
    # when the switch's summing pole is engaged in L+R mode.
    r_l_sum = sheet.add_component(resistor(
        "R501", f"{SUM_RESISTOR_OHM:g}", Point(175.0, 112.0),
        tolerance="0.1%", function="Left mono averaging resistor", rotation=90.0,
    ))
    r_r_sum = sheet.add_component(resistor(
        "R502", f"{SUM_RESISTOR_OHM:g}", Point(255.0, 112.0),
        tolerance="0.1%", function="Right mono averaging resistor", rotation=90.0,
    ))
    sheet.connect_pin_to_net(r_l_sum, "1", "BUFFERED_L", stub_dy=-6.0)
    sheet.connect_pins_manhattan(r_l_sum, "2", sw, "SUM_L", via_x=195.0)
    sheet.connect_pin_to_net(r_r_sum, "1", "BUFFERED_R", stub_dy=-6.0)
    sheet.connect_pins_manhattan(r_r_sum, "2", sw, "SUM_R", via_x=235.0)
    sheet.connect_pin_to_net(sw, "MONO", "MONO_AVG", stub_dy=10.0)
    tp_mono = sheet.add_component(testpoint("TP503", "MONO_AVG", Point(215.0, 190.0)))
    _wire_testpoint(sheet, tp_mono, "MONO_AVG")

    # Two unity buffers, bias resistors, output isolation and test points.
    for idx, (ch, y, sw_pin) in enumerate((("L", y_l, "L_OUT"), ("R", y_r, "R_OUT"))):
        base = 510 + idx * 10
        buf = sheet.add_component(_buffer(f"U{501 + idx}", ch, Point(315.0, y)))
        bias = sheet.add_component(resistor(
            f"R{base}", f"{INPUT_BIAS_RESISTOR_OHM:g}", Point(278.0, y + 25.0),
            tolerance="1%", function=f"{ch} switch-open input bias", rotation=90.0,
        ))
        out_r = sheet.add_component(resistor(
            f"R{base+1}", f"{OUTPUT_ISOLATION_OHM:g}", Point(365.0, y),
            tolerance="1%", function=f"{ch} mode-buffer output isolation",
        ))
        route_x = 262.0 if ch == "L" else 272.0
        sheet.connect_pins_manhattan(sw, sw_pin, buf, "IN", via_x=route_x)

        # Approach the buffer input vertically from the bias resistor.  The
        # previous Manhattan route overlapped the switch-to-buffer conductor,
        # leaving an unsplit endpoint-on-segment contact at x=292.1 mm.  KiCad
        # correctly treated that contact as an open branch without a junction.
        bias_pin = pin_position(bias, "1")
        buffer_input = pin_position(buf, "IN")
        sheet.connect_points(bias_pin, Point(buffer_input.x, bias_pin.y))
        sheet.connect_points(Point(buffer_input.x, bias_pin.y), buffer_input)
        sheet.connect_pin_to_net(bias, "2", "0VA", stub_dy=6.0)
        sheet.connect_pin_to_net(buf, "+V", "+18V", stub_dy=6.0)
        sheet.connect_pin_to_net(buf, "-V", "-18V", stub_dy=-6.0)
        feedback_pin = pin_position(buf, "IN-")
        feedback_out = pin_position(buf, "OUT")
        feedback_corner = Point(feedback_out.x, feedback_pin.y)
        sheet.connect_points(feedback_out, feedback_corner)
        sheet.connect_points(feedback_corner, feedback_pin)

        sheet.connect_pins(buf, "OUT", out_r, "1")
        sheet.connect_pin_to_net(out_r, "2", f"MODE_{ch}", stub_dx=12.0)
        tp_out = sheet.add_component(testpoint(f"TP{504+idx}", f"{ch}_MODE_OUT", Point(395.0, y + 18.0)))
        _wire_testpoint(sheet, tp_out, f"MODE_{ch}")

    # One dual OPA1656 package; decoupling capacitors connect to real rail nets.
    decoupling = (
        ("C5091", "100n", Point(285.0, 245.0), "+18V", "HF"),
        ("C5092", "100n", Point(315.0, 245.0), "-18V", "HF"),
        ("C5093", "10u", Point(345.0, 245.0), "+18V", "bulk"),
        ("C5094", "10u", Point(375.0, 245.0), "-18V", "bulk"),
    )
    for ref, value, at, rail, kind in decoupling:
        cap = sheet.add_component(capacitor(
            ref, value, at,
            dielectric="C0G/X7R" if kind == "HF" else "Low-ESR electrolytic",
            voltage="50V min" if kind == "HF" else "35V min",
            function=f"Local {rail} {kind} decoupling",
            footprint=(bulk_decoupling_capacitor_requirements().selected_footprint if kind == "bulk" else "Capacitor_SMD:C_0805_2012Metric"),
        ))
        sheet.connect_vertical_two_pin(cap, rail, "0VA")
