"""SCH105 AE-041 3P4T switched-summing channel-mode matrix builder."""
from __future__ import annotations
from generator.component_selection import bulk_decoupling_capacitor_requirements
from generator.core.components import Component, capacitor, resistor, testpoint
from generator.core.geometry import Point
from generator.core.pins import pin_position
from generator.model.mode_matrix import BUFFER_GAIN, DESIGN_OUTPUT_RMS_V, INPUT_BIAS_RESISTOR_OHM, OPAMP, DIRECT_SOURCE_ISOLATION_OHM, SWITCH_TYPE

def _mode_switch(ref: str, at: Point) -> Component:
    return Component(ref=ref, lib_id="ProjectShellac:Mode_Switch_Block",
        value="MODE 3P4T — A30403RNCB", at=at, footprint="",
        fields={"Function":"DUAL L / STEREO / L+R / DUAL R","Type":SWITCH_TYPE,
            "Pole A":"Left output: L / L / MONO_AVG / R",
            "Pole B":"Right output: L / R / MONO_AVG / R",
            "Pole C":"MONO_R_LEG open / open / connect to MONO_AVG / open",
            "SUM_R symbol pin":"Repurposed as active Pole-C MONO_R_LEG connection",
            "SUM_L symbol pin":"NC — legacy symbol pin retained cosmetically"}, on_board=False)

def _buffer(ref: str, channel: str, at: Point) -> Component:
    return Component(ref=ref,lib_id="ProjectShellac:OpAmp_Buffer_Block",value=f"{channel} MODE BUFFER",at=at,
        footprint="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm",
        fields={"Function":"Unity-gain matrix output buffer","Intended Device":OPAMP,"Supply":"+18V / -18V",
                "Gain":f"{BUFFER_GAIN:.3f}x","Design Output Ceiling":f"{DESIGN_OUTPUT_RMS_V:g} V RMS"})

def _wire_testpoint(sheet,tp,net_name): sheet.connect_pin_to_net(tp,"TP",net_name,stub_dy=-3.0)

def add_mode_matrix(sheet) -> None:
    sheet.add_note("SCH105 AE-041: 3P4T source selection followed by dual OPA1656 unity buffers.")
    sheet.add_note("CCW->CW: DUAL L, STEREO, L+R, DUAL R.")
    sheet.add_note("Pole C connects MONO_R_LEG to MONO_AVG only in L+R; no intentional L-R bridge exists otherwise.")
    sheet.add_note("Existing Mode_Switch_Block SUM_R pin carries Pole C; SUM_L remains intentionally NC.")
    sheet.add_note("BBM switching plus 2.2M input returns prevents materially floating buffer inputs; operational rule MUTE -> MATRIX -> RUN.")
    y_l,y_r=90.0,210.0
    sw=sheet.add_component(_mode_switch("SW501",Point(215.0,150.0)))
    sheet.add_no_connect_pin(sw,"SUM_L")
    sheet.connect_pin_to_net(sw,"L_IN","BUFFERED_L",stub_dx=-18.0)
    sheet.connect_pin_to_net(sw,"R_IN","BUFFERED_R",stub_dx=-18.0)
    sheet.connect_pin_to_net(sw,"MONO","MONO_AVG",stub_dy=10.0)
    sheet.connect_pin_to_net(sw,"SUM_R","MONO_R_LEG",stub_dy=-10.0)
    for ref,name,y,net in (("TP501","L_MODE_IN",y_l,"BUFFERED_L"),("TP502","R_MODE_IN",y_r,"BUFFERED_R"),
                           ("TP503","MONO_AVG",170.0,"MONO_AVG"),("TP506","MONO_R_LEG",190.0,"MONO_R_LEG")):
        tp=sheet.add_component(testpoint(ref,name,Point(145.0 if ref not in ("TP503","TP506") else 215.0,y))); _wire_testpoint(sheet,tp,net)
    for idx,(ch,y,sw_pin) in enumerate((("L",y_l,"L_OUT"),("R",y_r,"R_OUT"))):
        base=510+idx*10; buf=sheet.add_component(_buffer(f"U{501+idx}",ch,Point(315.0,y)))
        bias=sheet.add_component(resistor(f"R{base}",f"{INPUT_BIAS_RESISTOR_OHM:g}",Point(278.0,y+25.0),tolerance="1%",function=f"{ch} switch-open input bias",rotation=90.0))
        out_r=sheet.add_component(resistor(f"R{base+1}",f"{DIRECT_SOURCE_ISOLATION_OHM:g}",Point(365.0,y),tolerance="1%",function=f"{ch} mode-buffer output isolation"))
        route_x=262.0 if ch=="L" else 272.0; sheet.connect_pins_manhattan(sw,sw_pin,buf,"IN",via_x=route_x)
        bias_pin=pin_position(bias,"1"); buffer_input=pin_position(buf,"IN")
        sheet.connect_points(bias_pin,Point(buffer_input.x,bias_pin.y)); sheet.connect_points(Point(buffer_input.x,bias_pin.y),buffer_input)
        sheet.connect_pin_to_net(bias,"2","0VA",stub_dy=6.0); sheet.connect_pin_to_net(buf,"+V","+18V",stub_dy=6.0); sheet.connect_pin_to_net(buf,"-V","-18V",stub_dy=-6.0)
        fbin=pin_position(buf,"IN-"); fbout=pin_position(buf,"OUT"); corner=Point(fbin.x,fbout.y)
        sheet.connect_points(fbout,corner); sheet.connect_points(corner,fbin); sheet.connect_pins(buf,"OUT",out_r,"1")
        sheet.connect_pin_to_net(out_r,"2",f"MODE_{ch}",stub_dx=12.0)
        tp=sheet.add_component(testpoint(f"TP{504+idx}",f"{ch}_MODE_OUT",Point(395.0,y+18.0))); _wire_testpoint(sheet,tp,f"MODE_{ch}")
    for ref,value,at,rail,kind in (("C5091","100n",Point(285.0,245.0),"+18V","HF"),("C5092","100n",Point(315.0,245.0),"-18V","HF"),("C5093","10u",Point(345.0,245.0),"+18V","bulk"),("C5094","10u",Point(375.0,245.0),"-18V","bulk")):
        cap=sheet.add_component(capacitor(ref,value,at,dielectric="C0G/X7R" if kind=="HF" else "Low-ESR electrolytic",voltage="50V min" if kind=="HF" else "35V min",function=f"Local {rail} {kind} decoupling",footprint=(bulk_decoupling_capacitor_requirements().selected_footprint if kind=="bulk" else "Capacitor_SMD:C_0805_2012Metric")))
        sheet.connect_vertical_two_pin(cap,rail,"0VA") if rail=="+18V" else sheet.connect_vertical_two_pin(cap,"0VA",rail)
