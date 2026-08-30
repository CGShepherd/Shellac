"""SCH101 DR-038 precision balanced-input schematic builder."""
from generator.core.components import capacitor,diff_converter_block,opa1656_gain_block,resistor,xlr3,jst_vh_3,lt5400_network
from generator.core.geometry import Point
from generator.core.pins import pin_position
from generator.model.balanced_input import DIFF_CONVERTER_GAIN,GAIN_BASE_RF_OHM,GAIN_DEFAULT_ADD_OHM,GAIN_HIGH_ADD_OHM,GAIN_RG_OHM

def _wire_path(sheet,*points):
    for a,b in zip(points,points[1:]):
        if a!=b: sheet.connect_points(a,b)

def _rf_input(sheet,ch,base,cy,py,my):
    panel=sheet.add_component(xlr3(f"J{base}01",f"{ch} PANEL INPUT XLR",Point(25,cy),f"{ch} balanced cartridge input"))
    conn=sheet.add_component(jst_vh_3(f"H{base}01",f"{ch} INPUT HARNESS",Point(48,cy),f"{ch} panel-XLR to PCB harness"))
    for pin in ("1","2","3"): sheet.connect_points(pin_position(panel,pin),pin_position(conn,pin))
    rp=sheet.add_component(resistor(f"R{base}02","100R",Point(75,py),tolerance="0.1%",function="Matched RF series isolation IN+"))
    rm=sheet.add_component(resistor(f"R{base}03","100R",Point(75,my),tolerance="0.1%",function="Matched RF series isolation IN-"))
    cp=sheet.add_component(capacitor(f"C{base}01","1n",Point(108,py-2.54),dielectric="C0G/NP0",voltage="50V",function="0.5% matched common-mode RF shunt IN+"))
    cm=sheet.add_component(capacitor(f"C{base}02","1n",Point(108,my+2.54),dielectric="C0G/NP0",voltage="50V",function="0.5% matched common-mode RF shunt IN-"))
    cd=sheet.add_component(capacitor(f"C{base}03","220p",Point(130,cy),dielectric="C0G/NP0",voltage="50V",function="Differential RF shunt"))
    jp,jm=pin_position(conn,"2"),pin_position(conn,"3")
    sheet.connect_pin_to_net(conn,"1","CHASSIS",stub_dx=-8)
    sheet.add_label(f"INPUT_{ch}_POS",jp.x,jp.y); sheet.add_label(f"INPUT_{ch}_NEG",jm.x,jm.y)
    sheet.connect_points(jp,pin_position(rp,"1")); sheet.connect_points(jm,pin_position(rm,"1"))
    pp,mm=Point(130,py),Point(130,my)
    _wire_path(sheet,pin_position(rp,"2"),pin_position(cp,"1"),pp)
    _wire_path(sheet,pin_position(rm,"2"),pin_position(cm,"2"),mm)
    sheet.connect_points(pin_position(cd,"2"),pp); sheet.connect_points(pin_position(cd,"1"),mm)
    sheet.connect_pin_to_net(cp,"2","CHASSIS",stub_dy=-6); sheet.connect_pin_to_net(cm,"1","CHASSIS",stub_dy=6)
    return pp,mm

def _gain_leg(sheet,name,base,suffix,input_node,y):
    op=sheet.add_component(opa1656_gain_block(f"U{base}0{suffix}",f"{name} PRECISION GAIN",Point(190,y),f"{name}; DR-038"))
    fb=pin_position(op,"FB-"); fy=y-20 if suffix==1 else y+20
    rg=sheet.add_component(resistor(f"R{base}{suffix}1",f"{GAIN_RG_OHM:g}",Point(165,fb.y),tolerance="0.01%",function="Precision gain-to-ground"))
    hi=sheet.add_component(resistor(f"R{base}{suffix}4",f"{GAIN_HIGH_ADD_OHM:g}",Point(220,fy),tolerance="0.01%",function="HIGH feedback segment"))
    de=sheet.add_component(resistor(f"R{base}{suffix}3",f"{GAIN_DEFAULT_ADD_OHM:g}",Point(250,fy),tolerance="0.01%",function="DEFAULT feedback segment"))
    ba=sheet.add_component(resistor(f"R{base}{suffix}2",f"{GAIN_BASE_RF_OHM:g}",Point(280,fy),tolerance="0.01%",function="Fixed feedback base"))
    _wire_path(sheet,input_node,Point(155,input_node.y),Point(155,y),pin_position(op,"IN+"))
    sheet.connect_points(pin_position(rg,"2"),fb); sheet.connect_pin_to_net(rg,"1","0VA",stub_dx=-8)
    h1,h2=pin_position(hi,"1"),pin_position(hi,"2"); d1,d2=pin_position(de,"1"),pin_position(de,"2")
    sheet.connect_points(h2,d1); sheet.connect_points(d2,pin_position(ba,"1")); sheet.connect_points(pin_position(ba,"2"),pin_position(op,"OUT"))
    off=-7.62 if suffix==1 else 7.62
    lh=sheet.add_component(resistor(f"R{base}{suffix}5","0R",Point(220,fy+off),function="SERVICE LINK high bypass; fitted DEFAULT/LOW"))
    ld=sheet.add_component(resistor(f"R{base}{suffix}6","0R",Point(250,fy+off),function="SERVICE LINK default bypass; DNP DEFAULT")); ld.dnp=True
    sheet.connect_points(pin_position(lh,"1"),h1); sheet.connect_points(pin_position(lh,"2"),h2)
    sheet.connect_points(pin_position(ld,"1"),d1); sheet.connect_points(pin_position(ld,"2"),d2)
    sheet.connect_pin_to_net(op,"+V","+18V",stub_dy=-6); sheet.connect_pin_to_net(op,"-V","-18V",stub_dy=6)
    return op

def _diff(sheet,ch,base,cy,po,mo):
    amp=sheet.add_component(diff_converter_block(f"U{base}03",f"{ch} DIFF {DIFF_CONVERTER_GAIN:.2f}x",Point(350,cy),f"{ch} OPA1656 differential converter"))
    rn=sheet.add_component(lt5400_network(f"RN{base}30",f"{ch} LT5400-7 1:4",Point(315,cy)))
    pp,mp=pin_position(amp,"IN+"),pin_position(amp,"IN-")
    sheet.connect_points(pin_position(po,"OUT"),pin_position(rn,"3")); sheet.connect_points(pin_position(rn,"6"),pp)
    sheet.connect_points(pin_position(rn,"4"),pp); sheet.connect_pin_to_net(rn,"5","0VA",stub_dy=8)
    sheet.connect_points(pin_position(mo,"OUT"),pin_position(rn,"2")); sheet.connect_points(pin_position(rn,"7"),mp)
    sheet.connect_points(pin_position(rn,"1"),mp); sheet.connect_points(pin_position(rn,"8"),pin_position(amp,"OUT"))
    out=Point(390,cy); sheet.connect_points(pin_position(amp,"OUT"),out); sheet.add_label(f"PRE_EQ_{ch}",out.x,out.y)
    sheet.connect_pin_to_net(amp,"+V","+18V",stub_dy=-6); sheet.connect_pin_to_net(amp,"-V","-18V",stub_dy=6)

def _channel(sheet,ch,base,cy):
    py,my=cy-20,cy+20; pp,mm=_rf_input(sheet,ch,base,cy,py,my)
    po=_gain_leg(sheet,f"{ch}_PLUS",base,1,pp,py); mo=_gain_leg(sheet,f"{ch}_MINUS",base,2,mm,my)
    _diff(sheet,ch,base,cy,po,mo)

def add_sch101_diff_converter_slice(sheet):
    sheet.add_note("SCH101 DR-038 IMPLEMENTED: LT5400-7 4x converter + low-impedance precision gain legs.")
    sheet.add_note("Gain settings remain ~14/18/22 dB; default assembled service-link state = 18 dB.")
    sheet.add_note("LT5400-7 A-grade MS8E; EP9 electrically floating.")
    _channel(sheet,"L",1,85); _channel(sheet,"R",2,205)

def add_sch101_rf_slice(sheet): return add_sch101_diff_converter_slice(sheet)
