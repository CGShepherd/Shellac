"""SCH103 human-reviewable replay-equalisation builder.

The approved AE-002/003/004 electrical values and topology are unchanged.
Each channel is drawn as one visible left-to-right signal chain with explicit
bass, treble and feedback branches. Internal net labels are not used as
substitutes for conductors.
"""
from __future__ import annotations

from generator.core.components import Component, capacitor, resistor, testpoint
from generator.core.geometry import Point
from generator.core.pins import pin_position
from generator.physical_parts import timing_capacitor_footprint
from generator.model.replay_eq import (
    BASS_NETWORKS, OPA1612_DESIGN_OUTPUT_RMS_V, RECOVERY_RF_OHM,
    RECOVERY_RG_OHM, RIAA_BASS_NETWORK, TREBLE_NETWORKS, SOURCE_URL,
)


def _opamp(ref, value, function, at, gain):
    return Component(
        ref=ref, lib_id="ProjectShellac:OpAmp_NonInv_Block",
        value=value, at=at,
        footprint="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm",
        fields={
            "Function": function, "Device": "OPA1612",
            "Supply": "+18V / -18V", "Gain": gain,
            "Design Output Ceiling": f"{OPA1612_DESIGN_OUTPUT_RMS_V:g} V RMS",
        },
    )


def _physical_cap_value(value_nf: float) -> str:
    """Format one physical capacitor value for KiCad and the BOM."""
    if value_nf < 1.0:
        return f"{value_nf * 1000:g}p"
    return f"{value_nf:g}n"



def _add_parallel_capacitors(
    sheet,
    *,
    refs: tuple[str, ...],
    values_nf: tuple[float, ...],
    x: float,
    y: float,
    node_a: Point,
    node_b: Point,
    function: str,
):
    """Add explicitly referenced physical capacitors in parallel.

    Each capacitor owns one footprint and is wired to the same two electrical
    nodes. Vertical staggering keeps the schematic human-reviewable.
    """
    if len(refs) != len(values_nf):
        raise ValueError("one reference is required for each physical capacitor")
    capacitors = []
    spacing = 5.08
    y0 = y - spacing * (len(values_nf) - 1) / 2
    for index, (ref, value_nf) in enumerate(zip(refs, values_nf)):
        cap = sheet.add_component(capacitor(
            ref,
            _physical_cap_value(value_nf),
            Point(x, y0 + index * spacing),
            dielectric="C0G/NP0",
            voltage="50V min",
            function=function,
            rotation=90,
            footprint=timing_capacitor_footprint(value_nf),
        ))
        sheet.connect_points(node_a, pin_position(cap, "1"))
        sheet.connect_points(pin_position(cap, "2"), node_b)
        capacitors.append(cap)
    return tuple(capacitors)


def _wire_path(sheet, *points):
    for start, end in zip(points, points[1:]):
        sheet.connect_points(start, end)


def _inline_testpoint(sheet, ref, value, at, start, end):
    tp = sheet.add_component(testpoint(ref, value, at))
    tp_pin = pin_position(tp, "TP")
    _wire_path(sheet, start, tp_pin, end)
    return tp


def _label_on_dedicated_stub(sheet, start, net_name, *, dx=0.0, dy=0.0, label_dx=0.0, label_dy=0.0):
    """Attach a net label beyond a dedicated two-segment stub.

    KiCad warns when a label is placed directly at a junction shared by more
    than one conductor.  The first segment reaches the intended electrical
    node; the second segment moves the label to an isolated endpoint.
    """
    corner = Point(start.x + dx, start.y + dy)
    end = Point(corner.x + label_dx, corner.y + label_dy)
    sheet.connect_points(start, corner)
    sheet.connect_points(corner, end)
    sheet.add_label(net_name, end.x, end.y)
    return end


def _add_channel(sheet, channel, index, y):
    base = 300 + index * 50
    pre = f"PRE_EQ_{channel}"
    post = f"POST_EQ_{channel}"

    # Main active LF stage.
    u1 = sheet.add_component(_opamp(
        f"U{base}1", f"{channel} ACTIVE LF EQ",
        "P06/P91 active pole-zero stage", Point(80, y),
        "Frequency dependent",
    ))
    u1_in = pin_position(u1, "IN+")
    u1_out = pin_position(u1, "OUT")
    u1_fb = pin_position(u1, "FB-")

    input_end = Point(20, u1_in.y)
    input_tp = sheet.add_component(testpoint(
        f"TP{base}1", f"{channel}_EQ_IN", Point(45, u1_in.y + 5.08)
    ))
    input_tp_pin = pin_position(input_tp, "TP")
    _wire_path(sheet, input_end, input_tp_pin, u1_in)
    sheet.add_label(pre, input_end.x, input_end.y)

    _label_on_dedicated_stub(
        sheet, pin_position(u1, "+V"), "+18V",
        dy=-6, label_dx=-5.08,
    )
    _label_on_dedicated_stub(
        sheet, pin_position(u1, "-V"), "-18V",
        dy=6, label_dx=-5.08,
    )

    # Active LF feedback divider. Direct pin-to-pin conductors avoid ambiguous
    # endpoint-on-segment T-connections.
    rf = sheet.add_component(resistor(
        f"R{base}01", "100k", Point(80, y-30),
        tolerance="0.1%", function="Active LF feedback RF",
    ))
    rg = sheet.add_component(resistor(
        f"R{base}02", "2.70k", Point(110, y-30),
        tolerance="0.1%", function="Active LF feedback-ground RG",
    ))
    sheet.connect_points(u1_out, pin_position(rf, "1"))
    sheet.connect_points(pin_position(rf, "2"), u1_fb)
    sheet.connect_points(pin_position(rg, "1"), u1_fb)
    _label_on_dedicated_stub(
        sheet, pin_position(rg, "2"), "0VA",
        dy=5.08, label_dx=5.08,
    )

    # LF output evidence point sits directly on the visible path to the common
    # treble resistor.
    lf_tp = sheet.add_component(testpoint(
        f"TP{base}2", f"{channel}_LF_EQ_OUT", Point(118, y + 5.08)
    ))
    lf_tp_pin = pin_position(lf_tp, "TP")
    rt = sheet.add_component(resistor(
        f"R{base}30", "750", Point(225, y),
        tolerance="0.1%", function="Common passive treble resistor",
    ))
    rt_1 = pin_position(rt, "1")
    rt_2 = pin_position(rt, "2")
    _wire_path(sheet, u1_out, lf_tp_pin, rt_1)

    # Bass selector and four complete R-C branches. Selector OUT returns to the
    # LF output and COMMON returns to the op-amp feedback pin. Each branch is
    # physically visible from LF output through R and C to one selector contact.
    swb = sheet.add_component(Component(
        f"SW{base}1", "ProjectShellac:Bass_Select_Block",
        f"{channel} BASS 1P5", Point(165, y-58),
        fields={"Function": "Select complete RS+C branch"}, on_board=False,
    ))
    sheet.connect_points(pin_position(swb, "OUT"), u1_out)
    sheet.connect_points(pin_position(swb, "COMMON"), u1_fb)

    branches = list(BASS_NETWORKS[1:]) + [RIAA_BASS_NETWORK]
    branch_pins = ("B200", "B400", "B500", "RIAA")
    bass_cap_index = 10
    for i, (item, pin_name) in enumerate(zip(branches, branch_pins)):
        yy = y - 45 + i * 15
        r = sheet.add_component(resistor(
            f"R{base}{10+i}", f"{item.rs_ohm:g}", Point(118, yy),
            tolerance="0.1%", function=f"{item.name} series R",
        ))
        sheet.connect_points(u1_out, pin_position(r, "1"))
        refs = tuple(
            f"C{base}{bass_cap_index + offset}"
            for offset in range(len(item.capacitor_parts_nf))
        )
        _add_parallel_capacitors(
            sheet,
            refs=refs,
            values_nf=item.capacitor_parts_nf,
            x=145,
            y=yy,
            node_a=pin_position(r, "2"),
            node_b=pin_position(swb, pin_name),
            function=f"{item.name} branch",
        )
        bass_cap_index += len(item.capacitor_parts_nf)

    # Passive treble selector. The main 750-ohm path remains continuous; each
    # selected capacitor is a visible branch from its contact to 0VA.
    swt = sheet.add_component(Component(
        f"SW{base}2", "ProjectShellac:Treble_Select_Block",
        f"{channel} TREBLE 1P5", Point(270, y),
        fields={"Function": "Select passive treble capacitor"}, on_board=False,
    ))
    # Split the main passive path explicitly at the selector common pin.
    # This avoids an endpoint-on-segment overlap where KiCad sees the COMMON
    # branch as disconnected even though Foundry's coordinate graph joins it.
    treble_common = pin_position(swt, "COMMON")
    sheet.connect_points(rt_2, treble_common)

    treble_cap_index = 20
    for i, (item, pin_name) in enumerate(
        zip(TREBLE_NETWORKS[1:], ("T1600", "T2121", "T3400", "T5800"))
    ):
        yy = y - 35 + i * 18
        refs = tuple(
            f"C{base}{treble_cap_index + offset}"
            for offset in range(len(item.capacitor_parts_nf))
        )
        ground_node = Point(325, yy + 10)
        _add_parallel_capacitors(
            sheet,
            refs=refs,
            values_nf=item.capacitor_parts_nf,
            x=310,
            y=yy,
            node_a=pin_position(swt, pin_name),
            node_b=ground_node,
            function=f"{item.name} treble",
        )
        _label_on_dedicated_stub(
            sheet, ground_node, "0VA",
            dx=5.08, label_dx=5.08,
        )
        treble_cap_index += len(item.capacitor_parts_nf)

    # Recovery stage and feedback divider.
    u2 = sheet.add_component(_opamp(
        f"U{base}2", f"{channel} RECOVERY",
        "Post-EQ non-inverting recovery", Point(360, y),
        "2.100x / 6.444 dB",
    ))
    u2_in = pin_position(u2, "IN+")
    u2_out = pin_position(u2, "OUT")
    u2_fb = pin_position(u2, "FB-")
    sheet.connect_points(treble_common, u2_in)
    _label_on_dedicated_stub(
        sheet, pin_position(u2, "+V"), "+18V",
        dy=-6, label_dx=5.08,
    )
    _label_on_dedicated_stub(
        sheet, pin_position(u2, "-V"), "-18V",
        dy=6, label_dx=5.08,
    )

    rgr = sheet.add_component(resistor(
        f"R{base}40", f"{RECOVERY_RG_OHM:g}", Point(340, y-30),
        tolerance="0.1%", function="Recovery RG",
    ))
    rfr = sheet.add_component(resistor(
        f"R{base}41", f"{RECOVERY_RF_OHM:g}", Point(375, y-30),
        tolerance="0.1%", function="Recovery RF",
    ))
    sheet.connect_points(pin_position(rfr, "1"), u2_out)
    sheet.connect_points(pin_position(rfr, "2"), u2_fb)
    sheet.connect_points(pin_position(rgr, "1"), u2_fb)
    _label_on_dedicated_stub(
        sheet, pin_position(rgr, "2"), "0VA",
        dy=5.08, label_dx=5.08,
    )

    hf_tp = sheet.add_component(testpoint(
        f"TP{base}3", f"{channel}_HF_EQ_OUT", Point(300, y + 5.08)
    ))
    hf_tp_pin = pin_position(hf_tp, "TP")
    # The test point is connected to the actual passive-EQ/recovery input node.
    sheet.connect_points(hf_tp_pin, u2_in)

    output_end = Point(420, u2_out.y)
    output_tp = sheet.add_component(testpoint(
        f"TP{base}4", f"{channel}_EQ_OUT", Point(395, u2_out.y + 5.08)
    ))
    output_tp_pin = pin_position(output_tp, "TP")
    _wire_path(sheet, u2_out, output_tp_pin, output_end)
    sheet.add_label(post, output_end.x, output_end.y)

    # One dual OPA1612 package per channel; local decoupling remains grouped.
    for n, rail in enumerate(("+18V", "-18V")):
        hf_x = 330 + n * 50
        bulk_x = hf_x + 20
        hf_dec = sheet.add_component(capacitor(
            f"C{base}{50+n}", "100n", Point(hf_x, y+42),
            dielectric="C0G/X7R", voltage="50V min",
            function=f"{rail} HF decoupling",
        ))
        bulk = sheet.add_component(capacitor(
            f"C{base}{52+n}", "10u", Point(bulk_x, y+55),
            dielectric="Low-ESR electrolytic", voltage="35V min",
            function=f"{rail} bulk decoupling",
        ))
        for cap in (hf_dec, bulk):
            _label_on_dedicated_stub(
                sheet, pin_position(cap, "1"), rail,
                dy=4.0, label_dx=5.08,
            )
            _label_on_dedicated_stub(
                sheet, pin_position(cap, "2"), "0VA",
                dy=-4.0, label_dx=5.08,
            )


def add_replay_equalisation(sheet):
    sheet.add_note(
        "SCH103 HUMAN-REVIEWABLE: visible OPA1612 LF stage, switched bass "
        "branches, passive treble bank, and 2.1x recovery."
    )
    sheet.add_note(
        "True RIAA requires TRUE-RIAA bass and 2121-Hz treble positions. "
        "Keep switch wiring extremely short."
    )
    sheet.add_note(
        f"Source topology: {SOURCE_URL}; final values from AE-002/003/004."
    )
    _add_channel(sheet, "L", 0, 85)
    _add_channel(sheet, "R", 1, 195)
