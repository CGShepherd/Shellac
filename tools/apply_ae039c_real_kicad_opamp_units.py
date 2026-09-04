from pathlib import Path
REPO=Path(__file__).resolve().parents[1]
PINS=REPO/"generator/core/pins.py"
WRITER=REPO/"generator/writers/kicad9.py"
FINAL=REPO/"generator/blocks/final_gain.py"
MODE=REPO/"generator/blocks/mode_matrix.py"
RUMBLE=REPO/"generator/blocks/rumble_filter.py"
KWTEST=REPO/"tests/test_kicad_writer_instances.py"
PINTEST=REPO/"tests/test_pin_connectivity.py"
PATCH=REPO/"patches/ae039c"

def replace_once(text,old,new,path):
    if new in text: return text
    n=text.count(old)
    if n!=1: raise SystemExit(f"{path}: expected one occurrence; found {n}: {old!r}")
    return text.replace(old,new,1)

def replace_between(text,start,end,replacement,path):
    s=text.find(start); e=text.find(end,s)
    if s<0 or e<0: raise SystemExit(f"{path}: replacement boundary not found")
    return text[:s]+replacement+text[e:]

def main():
    text=PINS.read_text(encoding="utf-8")
    old='    "ProjectShellac:OpAmp_Buffer_Block": {\n        "IN": PinContract("1", Point(-11.43, 0.0)),\n        "OUT": PinContract("2", Point(11.43, 0.0)),\n        "+V": PinContract("3", Point(2.54, -10.16)),\n        "-V": PinContract("4", Point(2.54, 10.16)),\n        "0VA": PinContract("5", Point(-2.54, 10.16)),\n    },\n'
    new='    "ProjectShellac:OpAmp_Buffer_Block": {\n        "IN": PinContract("IN", Point(-11.43, 0.0)),\n        "IN-": PinContract("IN-", Point(-2.54, 10.16)),\n        "OUT": PinContract("OUT", Point(11.43, 0.0)),\n        "+V": PinContract("V+", Point(2.54, -10.16)),\n        "-V": PinContract("V-", Point(2.54, 10.16)),\n    },\n'
    text=replace_once(text,old,new,PINS); PINS.write_text(text,encoding="utf-8")

    text=WRITER.read_text(encoding="utf-8")
    imp="from generator.model.opamp_package_allocation import ALLOCATIONS\n"
    if imp not in text: text=text.replace("from generator.core.geometry import Point\n","from generator.core.geometry import Point\n"+imp,1)
    helper='\n_OPAMP_ALLOCATION_BY_LOGICAL_REF = {a.logical_ref: a for a in ALLOCATIONS}\nif len(_OPAMP_ALLOCATION_BY_LOGICAL_REF) != len(ALLOCATIONS):\n    raise RuntimeError("op-amp logical references must be globally unique")\n\ndef opamp_render_identity(component):\n    allocation=_OPAMP_ALLOCATION_BY_LOGICAL_REF.get(component.ref)\n    if allocation is None: return None\n    unit=1 if allocation.unit in {"A","S"} else 2\n    if allocation.device in {"OPA1656","OPA1612"}:\n        pins=("1","2","3","4","8") if unit==1 else ("4","5","6","7","8")\n    elif allocation.device=="OPA1655":\n        pins=("2","3","4","6","7")\n    else: raise ValueError(f"unsupported op-amp device {allocation.device}")\n    return {"reference":allocation.physical_ref,"value":allocation.device,"unit":unit,"pins":pins,"allocation":allocation}\n\n'
    if "def opamp_render_identity(component):" not in text: text=text.replace('PROJECT_NAME = "ProjectShellac"\n','PROJECT_NAME = "ProjectShellac"\n'+helper,1)
    text=replace_between(text,'(symbol "ProjectShellac:OpAmp_NonInv_Block"','(symbol "ProjectShellac:Replay_EQ_Core_Block"',(PATCH/"noninv.txt").read_text(),WRITER)
    text=replace_between(text,'(symbol "ProjectShellac:DiffAmp_Block"','(symbol "ProjectShellac:OpAmp_Buffer_Block"',(PATCH/"diff.txt").read_text(),WRITER)
    text=replace_between(text,'(symbol "ProjectShellac:OpAmp_Buffer_Block"','(symbol "ProjectShellac:TestPoint"',(PATCH/"buffer.txt").read_text(),WRITER)
    text=replace_between(text,"def symbol_instance(c, instance_path, standalone_path=None):","def hierarchical_label(" ,(PATCH/"symbol_instance.txt").read_text(),WRITER)
    WRITER.write_text(text,encoding="utf-8")

    text=FINAL.read_text(encoding="utf-8")
    text=replace_once(text,'    sheet.connect_pin_to_net(opamp, "0VA", "0VA", stub_dx=-12)\n',"",FINAL)
    if 'feedback_pin = pin_position(opamp, "IN-")' not in text:
        anchor='    sheet.connect_pin_to_net(opamp, "-V", "-18V", stub_dy=-6)\n'
        insert=anchor+'    feedback_pin = pin_position(opamp, "IN-")\n    feedback_out = pin_position(opamp, "OUT")\n    feedback_corner = Point(feedback_out.x, feedback_pin.y)\n    sheet.connect_points(feedback_out, feedback_corner)\n    sheet.connect_points(feedback_corner, feedback_pin)\n'
        text=replace_once(text,anchor,insert,FINAL)
    FINAL.write_text(text,encoding="utf-8")

    text=MODE.read_text(encoding="utf-8")
    text=replace_once(text,'        sheet.connect_pin_to_net(buf, "0VA", "0VA", stub_dx=-7.0)\n',"",MODE)
    if 'feedback_pin = pin_position(buf, "IN-")' not in text:
        anchor='        sheet.connect_pin_to_net(buf, "-V", "-18V", stub_dy=-6.0)\n'
        insert=anchor+'        feedback_pin = pin_position(buf, "IN-")\n        feedback_out = pin_position(buf, "OUT")\n        feedback_corner = Point(feedback_out.x, feedback_pin.y)\n        sheet.connect_points(feedback_out, feedback_corner)\n        sheet.connect_points(feedback_corner, feedback_pin)\n'
        text=replace_once(text,anchor,insert,MODE)
    MODE.write_text(text,encoding="utf-8")

    text=RUMBLE.read_text(encoding="utf-8")
    text=replace_once(text,'    sheet.connect_pin_to_net(opamp, "0VA", "0VA", stub_dx=-10.0)\n',"",RUMBLE)
    if 'opamp_inverting = pin_position(opamp, "IN-")' not in text:
        text=replace_once(text,'    opamp_out = pin_position(opamp, "OUT")\n','    opamp_out = pin_position(opamp, "OUT")\n    opamp_inverting = pin_position(opamp, "IN-")\n',RUMBLE)
        anchor='    _wire_path(sheet, opamp_out, output_branch)\n'
        insert=anchor+'    _wire_path(sheet, opamp_out, Point(opamp_out.x, opamp_inverting.y), opamp_inverting)\n'
        text=replace_once(text,anchor,insert,RUMBLE)
    RUMBLE.write_text(text,encoding="utf-8")

    text=PINTEST.read_text(encoding="utf-8")
    old='    assert pin_position(component, "IN") == align_point(Point(origin.x - 11.43, origin.y))\n    assert pin_position(component, "OUT") == align_point(Point(origin.x + 11.43, origin.y))\n'
    new='    assert pin_position(component, "IN") == align_point(Point(origin.x - 11.43, origin.y))\n    assert pin_position(component, "IN-") == align_point(Point(origin.x - 2.54, origin.y - 10.16))\n    assert pin_position(component, "OUT") == align_point(Point(origin.x + 11.43, origin.y))\n'
    text=replace_once(text,old,new,PINTEST); PINTEST.write_text(text,encoding="utf-8")

    text=KWTEST.read_text(encoding="utf-8")
    old='def test_reference_ground_pins_are_passive_not_undriven_power_inputs():\n    from generator.writers.kicad9 import local_symbol_library\n    library = local_symbol_library()\n    assert \'(pin passive line (at -2.54 10.16 270) (length 3.81) (name "0VA"\' in library\n    assert \'(pin passive line (at -5.08 12.70 270) (length 2.54) (name "GND"\' in library\n'
    new='def test_real_opamp_symbols_have_no_synthetic_ground_pin():\n    from generator.writers.kicad9 import local_symbol_library\n    library = local_symbol_library()\n    start=library.index(\'symbol "ProjectShellac:OpAmp_Buffer_Block"\')\n    end=library.index(\'symbol "ProjectShellac:TestPoint"\',start)\n    buffer=library[start:end]\n    assert \'(name "IN-"\' in buffer\n    assert \'(name "0VA"\' not in buffer\n    assert \'(number "8"\' in buffer\n    assert \'(number "4"\' in buffer\n    assert \'(pin passive line (at -5.08 12.70 270) (length 2.54) (name "GND"\' in library\n'
    text=replace_once(text,old,new,KWTEST); KWTEST.write_text(text,encoding="utf-8")

    print("AE-039C APPLIED")
    print("Dual A/B unit mapping and real SOIC-8 pin numbers installed.")
    print("Synthetic op-amp 0VA removed; explicit follower feedback added.")
    print("Expected physical board population remains 246.")

if __name__=="__main__": main()
