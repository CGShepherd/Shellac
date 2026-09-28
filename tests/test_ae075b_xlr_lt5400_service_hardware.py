from pathlib import Path
import math
import yaml

ROOT = Path(__file__).resolve().parents[1]
HOLD = ROOT / "config/release/ae071_prerouting_hold.yaml"
BOM = ROOT / "config/bom/shellac_bom.yaml"
BOARD = ROOT / "out/kicad/ProjectShellac.kicad_pcb"
COMP = ROOT / "generator/core/components.py"
INPUT = ROOT / "generator/blocks/balanced_input.py"
OUTPUT = ROOT / "generator/blocks/balanced_output.py"


def _balanced(text, start):
    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    raise AssertionError("unterminated KiCad expression")


def _footprint(text, ref):
    marker = f'(property "Reference" "{ref}"'
    p = text.index(marker)
    start = text.rfind("(footprint ", 0, p)
    return _balanced(text, start)


def test_ae075b_b06_exact_neutrik_xlrs_and_local_chassis_contract():
    comp = COMP.read_text(encoding="utf-8")
    out = OUTPUT.read_text(encoding="utf-8")
    bom = BOM.read_text(encoding="utf-8")
    assert "NC3FD-L-B-1" in comp and "NC3FD-L-B-1" in bom
    assert "NC3MD-L-B-1" in out and "NC3MD-L-B-1" in bom
    assert 'Shell/front-panel contact": "CHASSIS via explicit local bond' in comp
    assert 'Shell/front-panel contact": "CHASSIS via explicit local bond' in out
    assert 'Local 0VA": "NONE"' in comp
    assert 'Local 0VA": "NONE"' in out
    hold = yaml.safe_load(HOLD.read_text(encoding="utf-8"))
    blockers = {x["id"] for x in hold["routing_blockers"]}
    assert "AE071-B06" not in blockers
    assert hold["resolved_after_ae075b"][0]["id"] == "AE071-B06"


def test_ae075b_lt5400_exact_mpn_ep_and_run10_boundary():
    bom = BOM.read_text(encoding="utf-8")
    inp = INPUT.read_text(encoding="utf-8")
    assert "LT5400BIMS8E-7#PBF" in bom
    assert "EXACT_MPN_SELECTED_EP_IMPLEMENTED_RUN10_OPEN" in bom
    assert 'sheet.connect_pin_to_net(rn,"9","0VA"' in inp
    assert 'sheet.add_no_connect_pin(rn,"9")' not in inp
    hold = yaml.safe_load(HOLD.read_text(encoding="utf-8"))
    b04 = next(x for x in hold["routing_blockers"] if x["id"] == "AE071-B04")
    assert b04["exact_mpn"] == "LT5400BIMS8E-7#PBF"
    assert b04["ep_disposition"] == "PIN9_TO_QUIET_0VA_IMPLEMENTED"
    assert "RUN10" in b04["remaining_scope"]


def test_ae075b_lt5400_b_grade_network_only_cmrr_floor():
    matching = 0.00015
    ratio = 0.25
    residual = matching * (4.0 * ratio) / (2.0 + ratio + ratio)
    cmrr_db = -20.0 * math.log10(residual)
    assert abs(residual - 0.00006) < 1e-12
    assert 84.43 < cmrr_db < 84.45
    assert cmrr_db > 75.0


def test_ae075b_native_lt5400_ep_pads_are_0va_and_not_no_connect():
    text = BOARD.read_text(encoding="utf-8")
    assert "unconnected-(RN130-EP-Pad9)" not in text
    assert "unconnected-(RN230-EP-Pad9)" not in text
    for ref in ("RN130", "RN230"):
        block = _footprint(text, ref)
        p = block.index('(pad "9"')
        pad = _balanced(block, p)
        assert '(net 4 "0VA")' in pad
        assert '(pintype "passive")' in pad
        assert "no_connect" not in pad
        assert "Pin 9 bonded to quiet 0VA" in block


def test_ae075b_b08_is_narrowed_but_still_fail_closed():
    hold = yaml.safe_load(HOLD.read_text(encoding="utf-8"))
    blockers = {x["id"]: x for x in hold["routing_blockers"]}
    assert set(blockers) == {"AE071-B03", "AE071-B04", "AE071-B08"}
    b08 = blockers["AE071-B08"]
    assert b08["hardware_selection"] == "SELECTED_COMPATIBLE"
    assert b08["gain_header"] == "SAMTEC_TSW-104-07-G-D"
    assert b08["gain_shunt"] == "SAMTEC_MNT-104-BK-G"
    assert b08["load_header"] == "SAMTEC_TSW-102-07-G-D"
    assert b08["load_shunt"] == "SAMTEC_MNT-102-BK-G"
    assert "PHYSICAL_CONTINUITY" in b08["remaining_scope"]
    assert hold["permissions"]["final_routing"] is False
