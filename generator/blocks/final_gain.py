"""SCH104 pin-connected unity isolation-buffer builder.

The THAT1646 in SCH108 supplies the system's final +6 dB differential gain.
SCH104 therefore remains at unity to isolate SCH107 and drive the passive mode
matrix without changing the frozen total gain budget.
"""
from __future__ import annotations

from generator.component_selection import bulk_decoupling_capacitor_requirements
from generator.core.components import Component, capacitor, resistor, testpoint
from generator.core.geometry import Point
from generator.core.pins import pin_position
from generator.model.final_gain import (
    DESIGN_OUTPUT_RMS_V, GAIN_DB, OPAMP, OUTPUT_ISOLATION_OHM,
)


def _opamp(ref: str, channel: str, at: Point) -> Component:
    return Component(
        ref=ref,
        lib_id="ProjectShellac:OpAmp_Buffer_Block",
        value=f"{channel} ISOLATION BUFFER",
        at=at,
        footprint="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm",
        fields={
            "Function": "Unity-gain isolation buffer",
            "Intended Device": OPAMP,
            "Supply": "+18V / -18V",
            "Gain": f"1.000x / {GAIN_DB:.3f} dB",
            "Design Output Ceiling": f"{DESIGN_OUTPUT_RMS_V:g} V RMS",
        },
    )


def _channel(sheet, ch: str, idx: int, y: float) -> None:
    base = 400 + idx * 50
    x_u = 190

    opamp = sheet.add_component(_opamp(f"U{401 + idx}", ch, Point(x_u, y)))
    output_resistor = sheet.add_component(resistor(
        f"R{base}1",
        f"{OUTPUT_ISOLATION_OHM:g}",
        Point(250, y),
        tolerance="1%",
        function=f"{ch} output isolation",
    ))
    input_tp = sheet.add_component(testpoint(
        f"TP{base}1", f"{ch}_BUFFER_IN", Point(145, y - 5.08)
    ))
    output_tp = sheet.add_component(testpoint(
        f"TP{base}2", f"{ch}_BUFFER_OUT", Point(290, y - 5.08)
    ))

    # Draw the complete signal path conventionally.  Labels exist only at the
    # hierarchical interfaces; the buffer, test points and output resistor are
    # joined by visible wires for human review.
    input_pin = pin_position(opamp, "IN")
    signal_y = input_pin.y
    input_end = Point(125, signal_y)
    input_tp_pin = pin_position(input_tp, "TP")
    sheet.connect_points(input_end, input_tp_pin)
    sheet.connect_points(input_tp_pin, input_pin)
    sheet.add_label(f"FILTERED_{ch}", input_end.x, input_end.y)
    # Place the test-point pin directly on the main conductor.  This avoids a
    # generated T-junction; the two wire segments terminate at the pin.
    assert input_tp_pin.y == signal_y

    # Op-amp output through the physical 100-ohm series resistor.
    sheet.connect_pins(opamp, "OUT", output_resistor, "1")
    output_pin = pin_position(output_resistor, "2")
    output_end = Point(310, signal_y)
    output_tp_pin = pin_position(output_tp, "TP")
    sheet.connect_points(output_pin, output_tp_pin)
    sheet.connect_points(output_tp_pin, output_end)
    sheet.add_label(f"BUFFERED_{ch}", output_end.x, output_end.y)
    assert output_tp_pin.y == signal_y

    # Explicit power and analogue-reference connections.
    sheet.connect_pin_to_net(opamp, "+V", "+18V", stub_dy=6)
    sheet.connect_pin_to_net(opamp, "-V", "-18V", stub_dy=-6)
    sheet.connect_pin_to_net(opamp, "0VA", "0VA", stub_dx=-12)


def _decoupling(sheet) -> None:
    # One dual OPA1656 package serves both channels.
    plus_hf = sheet.add_component(capacitor(
        "C4091", "100n", Point(170, 220),
        dielectric="C0G/X7R", voltage="50V min",
        function="Local +18V HF decoupling",
    ))
    minus_hf = sheet.add_component(capacitor(
        "C4092", "100n", Point(210, 220),
        dielectric="C0G/X7R", voltage="50V min",
        function="Local -18V HF decoupling",
    ))
    plus_bulk = sheet.add_component(capacitor(
        "C4093", "10u", Point(170, 245),
        dielectric="Low-ESR electrolytic", voltage="35V min",
        function="Local +18V bulk decoupling",
        footprint=bulk_decoupling_capacitor_requirements().selected_footprint,
    ))
    minus_bulk = sheet.add_component(capacitor(
        "C4094", "10u", Point(210, 245),
        dielectric="Low-ESR electrolytic", voltage="35V min",
        function="Local -18V bulk decoupling",
        footprint=bulk_decoupling_capacitor_requirements().selected_footprint,
    ))

    for component in (plus_hf, plus_bulk):
        sheet.connect_vertical_two_pin(component, "+18V", "0VA")

    # Negative-rail capacitors are drawn from 0VA to -18V.
    for component in (minus_hf, minus_bulk):
        sheet.connect_vertical_two_pin(component, "0VA", "-18V")


def add_final_gain(sheet) -> None:
    sheet.add_note("SCH104 PIN-CONNECTED BY SR-002: stereo unity OPA1656 isolation buffer.")
    sheet.add_note("THAT1646 in SCH108 provides the final +6 dB differential conversion.")
    sheet.add_note("This preserves the intended overall system gain and avoids a 46 dB default chain.")
    sheet.add_note("One dual OPA1656 package serves both channels; nominal rails +/-18 V.")
    sheet.add_note("Per channel: voltage follower plus 100 ohm output isolation.")
    sheet.add_note("Nominal 0.321 V RMS input remains 0.321 V RMS; severe 3.21 V RMS retains >9.8 dB to 10 V RMS ceiling.")
    sheet.add_note("Place 100 nF local decouplers immediately at OPA1656 supply pins; add nearby 10 uF per rail.")

    _channel(sheet, "L", 0, 95)
    _channel(sheet, "R", 1, 205)
    _decoupling(sheet)
