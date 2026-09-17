"""SCH101 DR-038 / AE-042 precision balanced-input schematic builder."""
from generator.core.components import (
    capacitor,diff_converter_block,opa1656_gain_block,resistor,xlr3,jst_vh_3,
    lt5400_network,service_header_4gang,service_header_2gang,
)
from generator.core.geometry import Point
from generator.core.pins import pin_position
from generator.model.balanced_input import (
    DIFF_CONVERTER_GAIN,GAIN_FIXED_RF_OHM,GAIN_HIGH_PARALLEL_RG_OHM,
    GAIN_LOW_PARALLEL_RF_OHM,GAIN_RG_OHM,INPUT_CM_SHUNT_PF,
    INPUT_LOAD_LEG_OHM,
)

def _wire_path(sheet,*points):
    for a,b in zip(points,points[1:]):
        if a!=b:
            sheet.connect_points(a,b)

def _service_headers(sheet):
    headers={
        "GAIN_LOW":sheet.add_component(service_header_4gang(
            "H110","GAIN LOW 4-GANG",Point(455,65),
            "AE-042 LOW: bridge four 332R RF-parallel branches"
        )),
        "GAIN_HIGH":sheet.add_component(service_header_4gang(
            "H111","GAIN HIGH 4-GANG",Point(455,145),
            "AE-042 HIGH: bridge four 866R RG-parallel branches"
        )),
        "GAIN_PARK":sheet.add_component(service_header_4gang(
            "H112","GAIN DEFAULT / PARK",Point(455,225),
            "AE-042 normal parking position; electrically inert"
        )),
        "CAP_47":sheet.add_component(service_header_2gang(
            "H120","LOAD +47p L/R",Point(410,80),
            "AE-042/AE-066 ganged L/R +47p differential loading"
        )),
        "CAP_BASE":sheet.add_component(service_header_2gang(
            "H121","LOAD BASE / PARK",Point(410,145),
            "AE-042 normal capacitance-shunt parking position; electrically inert"
        )),
        "CAP_100":sheet.add_component(service_header_2gang(
            "H122","LOAD +100p L/R",Point(410,210),
            "AE-042/AE-066 ganged L/R +100p differential loading"
        )),
    }
    for pin in ("A1","B1","A2","B2","A3","B3","A4","B4"):
        sheet.add_no_connect_pin(headers["GAIN_PARK"],pin)
    for pin in ("A1","B1","A2","B2"):
        sheet.add_no_connect_pin(headers["CAP_BASE"],pin)
    return headers

def _rf_input(sheet,ch,base,cy,py,my,headers,pair_index):
    panel=sheet.add_component(xlr3(f"J{base}01",f"{ch} PANEL INPUT XLR",Point(25,cy),f"{ch} balanced cartridge input"))
    conn=sheet.add_component(jst_vh_3(f"H{base}01",f"{ch} INPUT HARNESS",Point(48,cy),f"{ch} panel-XLR to PCB harness"))
    for pin in ("1","2","3"):
        sheet.connect_points(pin_position(panel,pin),pin_position(conn,pin))
    rp=sheet.add_component(resistor(f"R{base}02","100R",Point(75,py),tolerance="0.1%",function="Matched RF series isolation IN+"))
    rm=sheet.add_component(resistor(f"R{base}03","100R",Point(75,my),tolerance="0.1%",function="Matched RF series isolation IN-"))
    cp=sheet.add_component(capacitor(f"C{base}01",f"{INPUT_CM_SHUNT_PF:g}p",Point(108,py-2.54),dielectric="C0G/NP0",voltage="50V",function="1% matched common-mode RF shunt IN+"))
    cm=sheet.add_component(capacitor(f"C{base}02",f"{INPUT_CM_SHUNT_PF:g}p",Point(108,my+2.54),dielectric="C0G/NP0",voltage="50V",function="1% matched common-mode RF shunt IN-"))
    c47=sheet.add_component(capacitor(
        f"C{base}03","47p",Point(136,cy-8.89),dielectric="C0G/NP0",voltage="50V",
        function="AE-042 service +47p differential cartridge load; shunt-selected",rotation=90,
    ))
    c100=sheet.add_component(capacitor(
        f"C{base}04","100p",Point(136,cy+8.89),dielectric="C0G/NP0",voltage="50V",
        function="AE-042 service +100p differential cartridge load; shunt-selected",rotation=90,
    ))
    lp=sheet.add_component(resistor(f"R{base}04",f"{INPUT_LOAD_LEG_OHM:g}",Point(150,py+7.62),tolerance="0.1%",function="Balanced cartridge load + IN+ DC bias return"))
    lm=sheet.add_component(resistor(f"R{base}05",f"{INPUT_LOAD_LEG_OHM:g}",Point(150,my-7.62),tolerance="0.1%",function="Balanced cartridge load + IN- DC bias return"))

    jp,jm=pin_position(conn,"2"),pin_position(conn,"3")
    sheet.connect_pin_to_net(conn,"1","CHASSIS",stub_dx=-8)
    sheet.add_label(f"INPUT_{ch}_POS",jp.x,jp.y)
    sheet.add_label(f"INPUT_{ch}_NEG",jm.x,jm.y)
    sheet.connect_points(jp,pin_position(rp,"1"))
    sheet.connect_points(jm,pin_position(rm,"1"))
    pp,mm=Point(130,py),Point(130,my)
    _wire_path(sheet,pin_position(rp,"2"),pin_position(cp,"1"),pp)
    _wire_path(sheet,pin_position(rm,"2"),pin_position(cm,"2"),mm)
    sheet.connect_pin_to_net(cp,"2","CHASSIS",stub_dy=-6)
    sheet.connect_pin_to_net(cm,"1","CHASSIS",stub_dy=6)
    sheet.connect_points(pin_position(lp,"1"),pp)
    sheet.connect_pin_to_net(lp,"2","0VA",stub_dy=6)
    sheet.connect_points(pin_position(lm,"2"),mm)
    sheet.connect_pin_to_net(lm,"1","0VA",stub_dy=-6)

    pos_net=f"SCH101_{ch}_LOAD_POS"
    neg_net=f"SCH101_{ch}_LOAD_NEG"
    sheet.add_label(pos_net,pp.x,pp.y)
    sheet.add_label(neg_net,mm.x,mm.y)

    a,b=f"A{pair_index}",f"B{pair_index}"
    cap47_branch=f"SCH101_{ch}_LOAD47_BRANCH"
    cap100_branch=f"SCH101_{ch}_LOAD100_BRANCH"
    sheet.connect_pin_to_net(c47,"1",pos_net,stub_dx=5.08)
    sheet.connect_pin_to_net(c47,"2",cap47_branch,stub_dx=-5.08)
    sheet.connect_pin_to_net(headers["CAP_47"],a,cap47_branch,stub_dx=-5.08)
    sheet.connect_pin_to_net(headers["CAP_47"],b,neg_net,stub_dx=5.08)
    sheet.connect_pin_to_net(c100,"1",pos_net,stub_dx=5.08)
    sheet.connect_pin_to_net(c100,"2",cap100_branch,stub_dx=-5.08)
    sheet.connect_pin_to_net(headers["CAP_100"],a,cap100_branch,stub_dx=-5.08)
    sheet.connect_pin_to_net(headers["CAP_100"],b,neg_net,stub_dx=5.08)
    return pp,mm

def _gain_leg(sheet,name,base,suffix,input_node,y,headers,pair_index):
    op=sheet.add_component(opa1656_gain_block(
        f"U{base}0{suffix}",f"{name} PRECISION GAIN",Point(190,y),f"{name}; DR-038 / AE-042"
    ))
    fb=pin_position(op,"FB-")
    out=pin_position(op,"OUT")
    fy=y-20 if suffix==1 else y+20

    rg=sheet.add_component(resistor(
        f"R{base}{suffix}1",f"{GAIN_RG_OHM:g}",Point(165,fb.y),
        tolerance="RUN10 OPEN",function="AE-042 fixed RG; ratio/matching qualification RUN10",
    ))
    rf=sheet.add_component(resistor(
        f"R{base}{suffix}2",f"{GAIN_FIXED_RF_OHM:g}",Point(270,fy),
        tolerance="RUN10 OPEN",function="AE-042 fixed RF; DEFAULT complete without shunt",
    ))
    low=sheet.add_component(resistor(
        f"R{base}{suffix}3",f"{GAIN_LOW_PARALLEL_RF_OHM:g}",Point(230,fy-7.62),
        tolerance="RUN10 OPEN",function="AE-042 LOW programming resistor; parallel with RF when shunted",
    ))
    high=sheet.add_component(resistor(
        f"R{base}{suffix}4",f"{GAIN_HIGH_PARALLEL_RG_OHM:g}",Point(230,fy+7.62),
        tolerance="RUN10 OPEN",function="AE-042 HIGH programming resistor; parallel with RG when shunted",
    ))

    _wire_path(sheet,input_node,Point(155,input_node.y),Point(155,y),pin_position(op,"IN+"))
    sheet.connect_points(pin_position(rg,"2"),fb)
    sheet.connect_pin_to_net(rg,"1","0VA",stub_dx=-8)
    sheet.connect_points(pin_position(rf,"1"),fb)
    sheet.connect_points(pin_position(rf,"2"),out)
    sheet.connect_points(pin_position(low,"1"),out)
    sheet.connect_points(pin_position(high,"1"),fb)

    fb_net=f"SCH101_{name}_FB"
    sheet.connect_pin_to_net(op,"FB-",fb_net,stub_dx=-6.35)

    a,b=f"A{pair_index}",f"B{pair_index}"
    low_branch=f"SCH101_{name}_LOW_BRANCH"
    high_branch=f"SCH101_{name}_HIGH_BRANCH"
    # PLUS LOW routes upward; MINUS LOW also routes upward beyond the
    # diagonal-feedback bounding region. This keeps LOW/HIGH branches disjoint.
    low_label_dy = -10.16 if suffix == 1 else -15.24
    sheet.connect_pin_to_net(low,"2",low_branch,stub_dy=low_label_dy)
    sheet.connect_pin_to_net(headers["GAIN_LOW"],a,low_branch,stub_dx=-5.08)
    sheet.connect_pin_to_net(headers["GAIN_LOW"],b,fb_net,stub_dx=5.08)
    # PLUS HIGH routes downward beyond the diagonal-feedback bounding region;
    # MINUS HIGH remains downward in its existing clear lane.
    high_label_dy = 25.40 if suffix == 1 else 10.16
    sheet.connect_pin_to_net(high,"2",high_branch,stub_dy=high_label_dy)
    sheet.connect_pin_to_net(headers["GAIN_HIGH"],a,high_branch,stub_dx=-5.08)
    sheet.connect_pin_to_net(headers["GAIN_HIGH"],b,"0VA",stub_dx=5.08)

    sheet.connect_pin_to_net(op,"+V","+18V",stub_dy=-6)
    sheet.connect_pin_to_net(op,"-V","-18V",stub_dy=6)
    return op

def _diff(sheet,ch,base,cy,po,mo):
    amp=sheet.add_component(diff_converter_block(
        f"U{base}03",f"{ch} DIFF {DIFF_CONVERTER_GAIN:.2f}x",
        Point(360,cy),f"{ch} OPA1655 differential converter"
    ))
    rn=sheet.add_component(lt5400_network(
        f"RN{base}30",f"{ch} LT5400-7 1:4",Point(315,cy)
    ))
    plus_src=f"SCH101_{ch}_LT5400_PLUS_SRC"
    plus_sum=f"SCH101_{ch}_LT5400_PLUS_SUM"
    minus_src=f"SCH101_{ch}_LT5400_MINUS_SRC"
    minus_sum=f"SCH101_{ch}_LT5400_MINUS_SUM"
    output_net=f"PRE_EQ_{ch}"
    # Keep the local label anchor outside diagonal-feedback bounding geometry.
    sheet.connect_pin_to_net(po,"OUT",plus_src,stub_dy=15.24)
    sheet.connect_pin_to_net(rn,"3",plus_src,stub_dx=-6.35)
    # Mirror the minus source label toward the channel centre.
    sheet.connect_pin_to_net(mo,"OUT",minus_src,stub_dy=-15.24)
    sheet.connect_pin_to_net(rn,"2",minus_src,stub_dx=-6.35)
    sheet.connect_pin_to_net(rn,"6",plus_sum,stub_dx=6.35)
    sheet.connect_pin_to_net(rn,"4",plus_sum,stub_dx=-6.35)
    sheet.connect_pin_to_net(amp,"IN+",plus_sum,stub_dx=-6.35)
    sheet.connect_pin_to_net(rn,"5","0VA",stub_dx=6.35)
    sheet.connect_pin_to_net(rn,"7",minus_sum,stub_dx=6.35)
    sheet.connect_pin_to_net(rn,"1",minus_sum,stub_dx=-6.35)
    sheet.connect_pin_to_net(amp,"IN-",minus_sum,stub_dx=-6.35)
    sheet.connect_pin_to_net(rn,"8",output_net,stub_dx=6.35)
    sheet.connect_pin_to_net(amp,"OUT",output_net,stub_dx=8.89)
    sheet.add_no_connect_pin(rn,"9")
    sheet.connect_pin_to_net(amp,"+V","+18V",stub_dy=-6.35)
    sheet.connect_pin_to_net(amp,"-V","-18V",stub_dy=6.35)

def _add_local_decoupling(sheet,ch,base,cy):
    for package_name, ref_plus, ref_minus, x in (
        ("OPA1656 gain package", f"C{base}91", f"C{base}92", 190),
        ("OPA1655 converter package", f"C{base}93", f"C{base}94", 360),
    ):
        plus = sheet.add_component(capacitor(
            ref_plus, "100n", Point(x, cy+48), dielectric="C0G/X7R",
            voltage="50V min", function=f"{ch} {package_name} +18V local HF bypass",
        ))
        minus = sheet.add_component(capacitor(
            ref_minus, "100n", Point(x+20, cy+48), dielectric="C0G/X7R",
            voltage="50V min", function=f"{ch} {package_name} -18V local HF bypass",
        ))
        sheet.connect_vertical_two_pin(plus, "+18V", "0VA")
        sheet.connect_vertical_two_pin(minus, "0VA", "-18V")

def _channel(sheet,ch,base,cy,headers,load_pair,gain_pair_offset):
    py,my=cy-20,cy+20
    pp,mm=_rf_input(sheet,ch,base,cy,py,my,headers,load_pair)
    po=_gain_leg(sheet,f"{ch}_PLUS",base,1,pp,py,headers,gain_pair_offset)
    mo=_gain_leg(sheet,f"{ch}_MINUS",base,2,mm,my,headers,gain_pair_offset+1)
    _diff(sheet,ch,base,cy,po,mo)
    _add_local_decoupling(sheet,ch,base,cy)

def add_sch101_diff_converter_slice(sheet):
    sheet.add_note("SCH101 AE-037: 47.4k balanced cartridge load + explicit DC bias return.")
    sheet.add_note("Fixed RF: 47p C0G each leg to CHASSIS; AE-042 load service states BASE/+47/+100p differential.")
    sheet.add_note("AE-042 gain: fixed RF=999R, RG=1k; LOW adds 332R || RF; HIGH adds 866R || RG; DEFAULT has no active shunt.")
    sheet.add_note("Gain shunt candidate MNT-104-BK-G moves among LOW/HIGH/PARK headers; load shunt MNT-102-BK-G moves among +47/BASE/+100 headers.")
    sheet.add_note("Production shunt pairing/orientation and service-header parasitic/layout correlation remain routing blockers.")
    sheet.add_note("LT5400-7 B-grade procurement candidate; RUN10 tolerance acceptance open; EP9 remains floating pending final EP disposition.")
    sheet.add_note("Each physical SCH101 op-amp package has local 100 nF bypassing from each rail to 0VA.")
    headers=_service_headers(sheet)
    _channel(sheet,"L",1,85,headers,1,1)
    _channel(sheet,"R",2,205,headers,2,3)

def add_sch101_rf_slice(sheet):
    return add_sch101_diff_converter_slice(sheet)
