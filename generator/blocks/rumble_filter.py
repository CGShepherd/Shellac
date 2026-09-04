"""SCH107 human-reviewable fourth-order rumble-filter builder.

SR-021 preserves the electrically validated AE-005/SR-004 design while
replacing labelled component stubs with conventional continuous conductors.
Each channel reads left-to-right through two explicit unity-gain Sallen-Key
high-pass sections.  The direct and filtered paths remain continuously visible
at the stereo bypass selector.
"""

from __future__ import annotations

from generator.component_selection import bulk_decoupling_capacitor_requirements
from generator.core.components import Component, capacitor, resistor, testpoint
from generator.core.geometry import Point
from generator.core.pins import pin_position
from generator.model.rumble_filter import (
    BYPASS_SWITCH,
    CAPACITANCE_VALUE,
    FILTER_ORDER,
    OPAMP,
    OUTPUT_ISOLATION_OHM,
    SECTIONS,
    TARGET_CUTOFF_HZ,
)

def _opamp_block(ref: str, channel: str, section: str, at: Point) -> Component:
    return Component(
        ref=ref,
        lib_id="ProjectShellac:OpAmp_Buffer_Block",
        value=f"{channel} HP SECTION {section}",
        at=at,
        footprint="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm",
        fields={
            "Function": "Unity-gain Sallen-Key high-pass follower",
            "Device": OPAMP,
            "Supply": "+18V / -18V",
            "Filter": f"4th-order Butterworth, {TARGET_CUTOFF_HZ:g} Hz nominal",
        },
    )

def _bypass_switch(ref: str, at: Point) -> Component:
    return Component(
        ref=ref,
        lib_id="ProjectShellac:Switch_Bypass_Block",
        value="STEREO RUMBLE BYPASS",
        at=at,
        footprint="",
        fields={
            "Function": "Select filtered or direct signal independently for both channels",
            "Type": BYPASS_SWITCH,
            "Preferred behaviour": "Filter remains driven in bypass mode",
        },
        on_board=False,
    )

def _wire_path(sheet, *points: Point) -> None:
    """Draw a conventional endpoint-to-endpoint orthogonal path."""
    for start, end in zip(points, points[1:]):
        if start != end:
            sheet.connect_points(start, end)

def _add_section(
    sheet,
    *,
    channel: str,
    channel_index: int,
    section_index: int,
    x: float,
    y: float,
    input_point: Point,
) -> tuple[Point, Component]:
    """Draw one complete unity-gain Sallen-Key section.

    The main signal path is C1 -> C2 -> OPA1656.  R1 is the visible feedback
    branch from the C1/C2 junction to the op-amp output, and R2 is the visible
    shunt branch from the C2/op-amp-input junction to 0VA.
    """
    section = SECTIONS[section_index]
    base = 700 + channel_index * 50 + section_index * 20

    c1 = sheet.add_component(capacitor(
        f"C{base}1", CAPACITANCE_VALUE, Point(x, y), dielectric="Film",
        voltage="50V min", function=f"{channel} HP{section.identifier} C1",
        rotation=90.0,
    ))
    c2 = sheet.add_component(capacitor(
        f"C{base}2", CAPACITANCE_VALUE, Point(x + 30, y), dielectric="Film",
        voltage="50V min", function=f"{channel} HP{section.identifier} C2",
        rotation=90.0,
    ))
    opamp = sheet.add_component(_opamp_block(
        f"U{base}", channel, section.identifier, Point(x + 75, y),
    ))
    r1 = sheet.add_component(resistor(
        f"R{base}1", f"{section.r1_ohm:g}", Point(x + 40, y + 35),
        tolerance="0.1%", function=f"{channel} HP{section.identifier} feedback R1",
    ))
    r2 = sheet.add_component(resistor(
        f"R{base}2", f"{section.r2_ohm:g}", Point(x + 55, y + 31),
        tolerance="0.1%", function=f"{channel} HP{section.identifier} shunt R2",
        rotation=90.0,
    ))

    c1_in = pin_position(c1, "2")
    c1_out = pin_position(c1, "1")
    c2_in = pin_position(c2, "2")
    c2_out = pin_position(c2, "1")
    opamp_in = pin_position(opamp, "IN")
    opamp_out = pin_position(opamp, "OUT")
    opamp_inverting = pin_position(opamp, "IN-")
    r1_left = pin_position(r1, "1")
    r1_right = pin_position(r1, "2")
    r2_top = pin_position(r2, "2")
    r2_bottom = pin_position(r2, "1")

    node_1 = Point(x + 15, y)
    node_2 = Point(x + 45, y)
    output_branch = Point(x + 86, y)
    feedback_y = y + 35

    # Main left-to-right signal conductor, segmented at intentional branches.
    _wire_path(sheet, input_point, c1_in)
    _wire_path(sheet, c1_out, node_1, c2_in)
    _wire_path(sheet, c2_out, node_2, opamp_in)
    _wire_path(sheet, opamp_out, output_branch)
    _wire_path(sheet, opamp_out, Point(opamp_out.x, opamp_inverting.y), opamp_inverting)

    # Visible Sallen-Key feedback and shunt branches.
    _wire_path(
        sheet,
        node_1,
        Point(node_1.x, feedback_y),
        r1_left,
    )
    _wire_path(
        sheet,
        r1_right,
        Point(output_branch.x, feedback_y),
        output_branch,
    )
    _wire_path(sheet, node_2, Point(node_2.x, r2_top.y), r2_top)
    _wire_path(sheet, r2_bottom, Point(r2_bottom.x, y + 48))
    sheet.add_label("0VA", r2_bottom.x, y + 48)

    # Explicit local supply/reference connections.
    sheet.connect_pin_to_net(opamp, "+V", "+18V", stub_dy=6.0)
    sheet.connect_pin_to_net(opamp, "-V", "-18V", stub_dy=-6.0)

    return output_branch, opamp

def _add_decoupling(sheet, channel: str, base: int, *, y_hf: float, y_bulk: float) -> None:
    plus_hf = sheet.add_component(capacitor(
        f"C{base}91", "100n", Point(255, y_hf), dielectric="C0G/X7R",
        voltage="50V min", function=f"{channel} local +18V HF decoupling",
    ))
    minus_hf = sheet.add_component(capacitor(
        f"C{base}92", "100n", Point(280, y_hf), dielectric="C0G/X7R",
        voltage="50V min", function=f"{channel} local -18V HF decoupling",
    ))
    plus_bulk = sheet.add_component(capacitor(
        f"C{base}93", "10u", Point(255, y_bulk), dielectric="Low-ESR electrolytic",
        voltage="35V min", function=f"{channel} local +18V bulk decoupling",
        footprint=bulk_decoupling_capacitor_requirements().selected_footprint,
    ))
    minus_bulk = sheet.add_component(capacitor(
        f"C{base}94", "10u", Point(280, y_bulk), dielectric="Low-ESR electrolytic",
        voltage="35V min", function=f"{channel} local -18V bulk decoupling",
        footprint=bulk_decoupling_capacitor_requirements().selected_footprint,
    ))

    for component in (plus_hf, plus_bulk):
        sheet.connect_vertical_two_pin(component, "+18V", "0VA")
    for component in (minus_hf, minus_bulk):
        sheet.connect_vertical_two_pin(component, "0VA", "-18V")

def _add_channel(
    sheet,
    channel: str,
    channel_index: int,
    y: float,
) -> dict[str, Point | Component]:
    base = 700 + channel_index * 50
    input_end = Point(25, y)
    input_branch = Point(35, y)

    input_tp = sheet.add_component(testpoint(
        f"TP{base}1", f"{channel}_RUMBLE_IN", Point(47, y - 5.08)
    ))
    hp1_tp = sheet.add_component(testpoint(
        f"TP{base}2", f"{channel}_HP1_OUT", Point(178, y - 5.08)
    ))
    hp2_tp = sheet.add_component(testpoint(
        f"TP{base}3", f"{channel}_HP2_OUT", Point(318, y - 5.08)
    ))
    output_tp_x = 405 if channel == "L" else 435
    output_tp = sheet.add_component(testpoint(
        f"TP{base}4", f"{channel}_RUMBLE_OUT", Point(output_tp_x, y - 5.08)
    ))

    input_tp_pin = pin_position(input_tp, "TP")
    hp1_tp_pin = pin_position(hp1_tp, "TP")
    hp2_tp_pin = pin_position(hp2_tp, "TP")

    sheet.add_label(f"POST_EQ_{channel}", input_end.x, input_end.y)
    _wire_path(sheet, input_end, input_branch, input_tp_pin)

    hp1_output, _ = _add_section(
        sheet,
        channel=channel,
        channel_index=channel_index,
        section_index=0,
        x=75,
        y=y,
        input_point=input_tp_pin,
    )
    _wire_path(sheet, hp1_output, hp1_tp_pin)

    hp2_output, _ = _add_section(
        sheet,
        channel=channel,
        channel_index=channel_index,
        section_index=1,
        x=215,
        y=y,
        input_point=hp1_tp_pin,
    )
    _wire_path(sheet, hp2_output, hp2_tp_pin)

    isolation = sheet.add_component(resistor(
        f"R{base}90", f"{OUTPUT_ISOLATION_OHM:g}", Point(340, y),
        tolerance="1%", function=f"{channel} filter-output isolation",
    ))
    _wire_path(sheet, hp2_tp_pin, pin_position(isolation, "1"))
    filtered_point = pin_position(isolation, "2")

    if channel == "L":
        # Keep the direct path visibly above the filter channel.
        direct_lane_y = 42
        direct_lane_x = 345
        filter_lane_x = 355
    else:
        # Keep the direct path visibly below the filter channel.
        direct_lane_y = 228
        direct_lane_x = 365
        filter_lane_x = 360

    _wire_path(
        sheet,
        input_branch,
        Point(input_branch.x, direct_lane_y),
        Point(direct_lane_x, direct_lane_y),
    )
    _wire_path(
        sheet,
        filtered_point,
        Point(filter_lane_x, y),
    )

    # Channel-local dual-package decoupling.
    if channel == "L":
        _add_decoupling(sheet, channel, base, y_hf=124, y_bulk=145)
    else:
        _add_decoupling(sheet, channel, base, y_hf=220, y_bulk=242)

    return {
        "direct_route_end": Point(direct_lane_x, direct_lane_y),
        "filtered_route_end": Point(filter_lane_x, y),
        "output_testpoint": output_tp,
    }

def add_rumble_filter(sheet) -> None:
    sheet.add_note(
        f"SCH107 HUMAN-REVIEWABLE: stereo {FILTER_ORDER}th-order Butterworth "
        f"high-pass, nominal -3 dB at {TARGET_CUTOFF_HZ:g} Hz."
    )
    sheet.add_note("Two conventional unity-gain Sallen-Key sections per channel using OPA1656.")
    sheet.add_note(
        "Section A: 20.8k/24.3k; section B: 8.66k/59.0k; all capacitors 470 nF film."
    )
    sheet.add_note(
        "The stereo 2P2T break-before-make bypass selector leaves both filter channels driven."
    )
    sheet.add_note("Match left/right capacitors to 1% or better; 0.1% resistors preferred.")

    left = _add_channel(sheet, "L", 0, 78)
    right = _add_channel(sheet, "R", 1, 185)

    switch = sheet.add_component(_bypass_switch("SW1071", Point(385, 135)))
    l_direct = pin_position(switch, "L_DIRECT")
    l_filter = pin_position(switch, "L_FILTER")
    r_direct = pin_position(switch, "R_DIRECT")
    r_filter = pin_position(switch, "R_FILTER")
    l_out = pin_position(switch, "L_OUT")
    r_out = pin_position(switch, "R_OUT")

    for route_end, switch_pin in (
        (left["direct_route_end"], l_direct),
        (left["filtered_route_end"], l_filter),
        (right["direct_route_end"], r_direct),
        (right["filtered_route_end"], r_filter),
    ):
        _wire_path(sheet, route_end, Point(route_end.x, switch_pin.y), switch_pin)

    for channel, switch_pin, output_tp, end_y in (
        ("L", l_out, left["output_testpoint"], l_out.y),
        ("R", r_out, right["output_testpoint"], r_out.y),
    ):
        output_tp_pin = pin_position(output_tp, "TP")
        # Bring the switch output to the channel test point and hierarchy label
        # on a continuous visible conductor.
        _wire_path(
            sheet,
            switch_pin,
            Point(output_tp_pin.x, switch_pin.y),
            output_tp_pin,
            Point(455, output_tp_pin.y),
        )
        sheet.add_label(f"FILTERED_{channel}", 455, output_tp_pin.y)
