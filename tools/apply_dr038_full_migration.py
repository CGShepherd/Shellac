from pathlib import Path
import shutil

shutil.copyfile("payload/balanced_input.py","generator/model/balanced_input.py")
shutil.copyfile("payload/balanced_input_builder.py","generator/blocks/balanced_input.py")

p=Path("generator/core/components.py"); t=p.read_text(encoding="utf-8")
if "def lt5400_network" not in t:
    t += '\n\ndef lt5400_network(ref,label,at):\n    return Component(ref,"ProjectShellac:LT5400_Network",label,at,"Package_SO:MSOP-8-1EP_3x3mm_P0.65mm_EP1.68x1.88mm",{"Function":"DR-038 matched resistor network","Device":"LT5400-7 A-grade","R1/R4":"5k","R2/R3":"1.25k","EP":"Pin 9 floating"})\n'
t=t.replace('"Gain": "3.48x / +10.8 dB",','"Gain": "External LT5400 network defines gain",')
t=t.replace('"Resistor Network": "10k / 34.8k, 0.1% or matched network"','"Resistor Network": "LT5400-7 A-grade"')
p.write_text(t,encoding="utf-8")

p=Path("generator/core/pins.py"); t=p.read_text(encoding="utf-8")
if '"ProjectShellac:LT5400_Network"' not in t:
    marker='    "ProjectShellac:TestPoint": {'
    block='    "ProjectShellac:LT5400_Network": {\n        "1": PinContract("1", Point(-7.62,-3.81)),\n        "2": PinContract("2", Point(-7.62,-1.27)),\n        "3": PinContract("3", Point(-7.62,1.27)),\n        "4": PinContract("4", Point(-7.62,3.81)),\n        "5": PinContract("5", Point(7.62,3.81)),\n        "6": PinContract("6", Point(7.62,1.27)),\n        "7": PinContract("7", Point(7.62,-1.27)),\n        "8": PinContract("8", Point(7.62,-3.81)),\n        "9": PinContract("9", Point(0.0,7.62)),\n    },\n'
    t=t.replace(marker,block+marker,1)
p.write_text(t,encoding="utf-8")

p=Path("generator/writers/kicad9.py"); t=p.read_text(encoding="utf-8")
if '"ProjectShellac:LT5400_Network": 9' not in t:
    t=t.replace('"ProjectShellac:DiffAmp_Block": 5,','"ProjectShellac:DiffAmp_Block": 5,\n    "ProjectShellac:LT5400_Network": 9,',1)
if '"ProjectShellac:LT5400_Network"' not in t.split("def embedded_custom_symbol_ids",1)[1].split("})",1)[0]:
    t=t.replace('"ProjectShellac:DiffAmp_Block",','"ProjectShellac:DiffAmp_Block",\n        "ProjectShellac:LT5400_Network",',1)
if '(symbol "ProjectShellac:LT5400_Network"' not in t:
    marker='    (symbol "ProjectShellac:DIP_Switch_Block"'
    sym='    (symbol "ProjectShellac:LT5400_Network" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom yes) (on_board yes)\n      (property "Reference" "RN" (id 0) (at 0 -10 0) {eff()})\n      (property "Value" "LT5400-7" (id 1) (at 0 10 0) {eff()})\n      (symbol "LT5400_Network_0_1"\n        (rectangle (start -5.08 -6.35) (end 5.08 6.35) (stroke (width 0.1524) (type solid)) (fill (type none)))\n        (pin passive line (at -7.62 -3.81 0) (length 2.54) (name "1" {eff(1.0)}) (number "1" {eff(1.0)}))\n        (pin passive line (at -7.62 -1.27 0) (length 2.54) (name "2" {eff(1.0)}) (number "2" {eff(1.0)}))\n        (pin passive line (at -7.62 1.27 0) (length 2.54) (name "3" {eff(1.0)}) (number "3" {eff(1.0)}))\n        (pin passive line (at -7.62 3.81 0) (length 2.54) (name "4" {eff(1.0)}) (number "4" {eff(1.0)}))\n        (pin passive line (at 7.62 3.81 180) (length 2.54) (name "5" {eff(1.0)}) (number "5" {eff(1.0)}))\n        (pin passive line (at 7.62 1.27 180) (length 2.54) (name "6" {eff(1.0)}) (number "6" {eff(1.0)}))\n        (pin passive line (at 7.62 -1.27 180) (length 2.54) (name "7" {eff(1.0)}) (number "7" {eff(1.0)}))\n        (pin passive line (at 7.62 -3.81 180) (length 2.54) (name "8" {eff(1.0)}) (number "8" {eff(1.0)}))\n        (pin passive line (at 0 7.62 270) (length 1.27) (name "EP" {eff(1.0)}) (number "9" {eff(1.0)}))\n      )\n    )\n'
    t=t.replace(marker,sym+marker,1)
p.write_text(t,encoding="utf-8")

p=Path("generator/layout/placement_clusters.py"); t=p.read_text(encoding="utf-8")
t=t.replace('"SW1011 U101 U102 R111 R112 R113 R114 R121 R122 R123 R124 U103 R130 R131 R132 R133"','"U101 U102 R111 R112 R113 R114 R115 R116 R121 R122 R123 R124 R125 R126 U103 RN130"')
t=t.replace('"U201 U202 R211 R212 R213 R214 R221 R222 R223 R224 U203 R230 R231 R232 R233"','"U201 U202 R211 R212 R213 R214 R215 R216 R221 R222 R223 R224 R225 R226 U203 RN230"')
p.write_text(t,encoding="utf-8")

p=Path("tests/test_balanced_input_gain.py"); t=p.read_text(encoding="utf-8").replace("pytest.approx(3.48)","pytest.approx(4.0)"); p.write_text(t,encoding="utf-8")
p=Path("tests/test_balanced_input.py"); t=p.read_text(encoding="utf-8")
t=t.replace('assert "SW1011" in by_ref','assert "SW1011" not in by_ref\n    assert "RN130" in by_ref and "RN230" in by_ref')
t=t.replace('"4420"','"249"').replace('"8280"','"750"').replace('"21680"','"1910"').replace("== 12700.0","== 999.0").replace("== 26100.0","== 2159.0")
p.write_text(t,encoding="utf-8")

p=Path("config/decisions/current_decision_index.yaml"); t=p.read_text(encoding="utf-8")
t=t.replace("  DR-038:\n    title: SCH101 precision architecture\n    status: CURRENT_SELECTED_PENDING_IMPLEMENTATION","  DR-038:\n    title: SCH101 precision architecture\n    status: CURRENT_IMPLEMENTED")
t=t.replace("  DR-040:\n    title: Precision CAD primitive staging rule\n    status: CURRENT_SELECTED_PENDING_IMPLEMENTATION","  DR-040:\n    title: Precision CAD primitive staging rule\n    status: CURRENT_IMPLEMENTED")
t=t.replace("converter_gain: 3.48","converter_gain: 4.0")
p.write_text(t,encoding="utf-8")

p=Path("tests/test_current_decision_index.py"); t=p.read_text(encoding="utf-8")
t=t.replace('for decision in ("DR-038", "DR-040"):\n        assert _decision_status(decision) == "CURRENT_SELECTED_PENDING_IMPLEMENTATION"','for decision in ("DR-038", "DR-039", "DR-040"):\n        assert _decision_status(decision) == "CURRENT_IMPLEMENTED"')
t=t.replace(r'converter_gain:\s*3\.48',r'converter_gain:\s*4\.0')
p.write_text(t,encoding="utf-8")

for p in Path("tests").glob("test_*.py"):
    txt=p.read_text(encoding="utf-8")
    if any(k in p.name for k in ("placement","footprint","pipeline","board","readiness","audit")):
        p.write_text(txt.replace("== 249","== 250"),encoding="utf-8")

p=Path("config/bom/shellac_bom.yaml"); t=p.read_text(encoding="utf-8")
if "BOM-SCH101-LT5400" not in t:
    t += "\n  - id: BOM-SCH101-LT5400\n    function: sch101_precision_resistor_network\n    manufacturer: Analog Devices\n    mpn: LT5400-7A\n    quantity: 2\n    package: MS8E\n    footprint: Package_SO:MSOP-8-1EP_3x3mm_P0.65mm_EP1.68x1.88mm\n    status: SELECTED\n    decision: DR-038\n"
p.write_text(t,encoding="utf-8")
print("DR-038 full SCH101 migration applied")
