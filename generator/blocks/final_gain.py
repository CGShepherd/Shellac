"""SCH104 unity isolation-buffer builder with AE-041 switched mono averaging."""
from __future__ import annotations
from generator.component_selection import bulk_decoupling_capacitor_requirements
from generator.core.components import Component, capacitor, resistor, testpoint
from generator.core.geometry import Point
from generator.core.pins import pin_position
from generator.model.final_gain import DESIGN_OUTPUT_RMS_V, GAIN_DB, OPAMP, OUTPUT_ISOLATION_OHM
from generator.model.mode_matrix import SUM_RESISTOR_OHM, SUM_RESISTOR_TOLERANCE_PERCENT

def _opamp(ref: str, channel: str, at: Point) -> Component:
    return Component(ref=ref, lib_id="ProjectShellac:OpAmp_Buffer_Block",
        value=f"{channel} ISOLATION BUFFER", at=at,
        footprint="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm",
        fields={"Function":"Unity-gain isolation buffer","Intended Device":OPAMP,
                "Supply":"+18V / -18V","Gain":f"1.000x / {GAIN_DB:.3f} dB",
                "Design Output Ceiling":f"{DESIGN_OUTPUT_RMS_V:g} V RMS"})

def _channel(sheet, ch: str, idx: int, y: float) -> None:
    base = 400 + idx * 50
    opamp = sheet.add_component(_opamp(f"U{401+idx}", ch, Point(190,y)))
    output_resistor = sheet.add_component(resistor(
        f"R{base}1", f"{OUTPUT_ISOLATION_OHM:g}", Point(250,y), tolerance="1%",
        function=f"{ch} output isolation"))
    sum_resistor = sheet.add_component(resistor(
        f"R{base}2", f"{SUM_RESISTOR_OHM:g}", Point(225,y+28),
        tolerance=f"{SUM_RESISTOR_TOLERANCE_PERCENT:g}%",
        function=(f"{ch} mono averaging branch — " + ("permanent MONO_AVG leg" if ch=="L" else "switched right leg")),
        rotation=90.0))
    input_tp = sheet.add_component(testpoint(f"TP{base}1",f"{ch}_BUFFER_IN",Point(145,y-5.08)))
    output_tp = sheet.add_component(testpoint(f"TP{base}2",f"{ch}_BUFFER_OUT",Point(290,y-5.08)))
    input_pin=pin_position(opamp,"IN"); signal_y=input_pin.y
    input_end=Point(125,signal_y); input_tp_pin=pin_position(input_tp,"TP")
    sheet.connect_points(input_end,input_tp_pin); sheet.connect_points(input_tp_pin,input_pin)
    sheet.add_label(f"FILTERED_{ch}",input_end.x,input_end.y)
    sheet.connect_pins(opamp,"OUT",output_resistor,"1")
    op_out=pin_position(opamp,"OUT"); sum_pin=pin_position(sum_resistor,"1")
    sheet.connect_points(op_out,Point(sum_pin.x,op_out.y)); sheet.connect_points(Point(sum_pin.x,op_out.y),sum_pin)
    sum_net = "MONO_AVG" if ch == "L" else "MONO_R_LEG"
    sheet.connect_pin_to_net(sum_resistor,"2",sum_net,stub_dy=7.0)
    output_pin=pin_position(output_resistor,"2"); output_end=Point(310,signal_y)
    output_tp_pin=pin_position(output_tp,"TP")
    sheet.connect_points(output_pin,output_tp_pin); sheet.connect_points(output_tp_pin,output_end)
    sheet.add_label(f"BUFFERED_{ch}",output_end.x,output_end.y)
    sheet.connect_pin_to_net(opamp,"+V","+18V",stub_dy=6); sheet.connect_pin_to_net(opamp,"-V","-18V",stub_dy=-6)
    feedback_pin=pin_position(opamp,"IN-"); feedback_out=pin_position(opamp,"OUT")
    corner=Point(feedback_pin.x,feedback_out.y); sheet.connect_points(feedback_out,corner); sheet.connect_points(corner,feedback_pin)

def _decoupling(sheet) -> None:
    caps=(("C4091","100n",Point(170,220),"+18V","HF"),("C4092","100n",Point(210,220),"-18V","HF"),
          ("C4093","10u",Point(170,245),"+18V","bulk"),("C4094","10u",Point(210,245),"-18V","bulk"))
    for ref,value,at,rail,kind in caps:
        c=sheet.add_component(capacitor(ref,value,at,dielectric="C0G/X7R" if kind=="HF" else "Low-ESR electrolytic",
            voltage="50V min" if kind=="HF" else "35V min",function=f"Local {rail} {kind} decoupling",
            footprint=(bulk_decoupling_capacitor_requirements().selected_footprint if kind=="bulk" else "Capacitor_SMD:C_0805_2012Metric")))
        sheet.connect_vertical_two_pin(c,rail,"0VA") if rail=="+18V" else sheet.connect_vertical_two_pin(c,"0VA",rail)

def add_final_gain(sheet) -> None:
    sheet.add_note("SCH104 AE-041: stereo unity OPA1656 isolation buffer.")
    sheet.add_note("Each OPA1656 output feeds its existing 100 ohm direct-path isolation resistor.")
    sheet.add_note("L 4.7k/0.1% feeds MONO_AVG permanently; R 4.7k/0.1% feeds MONO_R_LEG for SW903 Pole C.")
    sheet.add_note("Outside L+R the right leg is disconnected, so no intentional L-R resistive bridge exists.")
    sheet.add_note("THAT1646 in SCH108 supplies the final +6 dB differential conversion.")
    _channel(sheet,"L",0,95); _channel(sheet,"R",1,205); _decoupling(sheet)
