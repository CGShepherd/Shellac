from pathlib import Path
import json
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
PCB = ROOT / "out/kicad/ProjectShellac.kicad_pcb"
RESULT = ROOT / "simulation/results/ae075g_pre90_output/ae075g_pre90_output.json"
INDEX = ROOT / "config/decisions/current_decision_index.yaml"
AUTHORITY = ROOT / "config/decisions/document_authority.yaml"
HOLD = ROOT / "config/release/ae071_prerouting_hold.yaml"
BOM = ROOT / "config/bom/shellac_bom.yaml"
RECORD_REL = "docs/design_pack/AE-075G_SCH108_Output_Interface_and_PRE90_Compatibility_Reconciliation_Rev_A0.md"


def _footprint(text: str, ref: str) -> str:
    pos = text.index(f'(property "Reference" "{ref}"')
    start = text.rfind("(footprint ", 0, pos)
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    raise AssertionError(ref)


def _pad_net(block: str, pad: str):
    pos = block.index(f'(pad "{pad}"')
    next_pad = block.find('\n\t\t(pad "', pos + 6)
    chunk = block[pos:] if next_pad < 0 else block[pos:next_pad]
    m = re.search(r'\(net\s+\d+\s+"([^"]+)"\)', chunk)
    return None if not m else m.group(1)


def test_ae075g_native_output_header_electrical_contract():
    text = PCB.read_text(encoding="utf-8")
    expected = {
        "H801": ("/OUTPUT_L_POS", "/OUTPUT_L_NEG"),
        "H802": ("/OUTPUT_R_POS", "/OUTPUT_R_NEG"),
    }
    for ref, nets in expected.items():
        block = _footprint(text, ref)
        assert "Molex_MicroLockPlus_5055780221_1x02_P2.00mm_Horizontal" in block
        assert _pad_net(block, "1") == nets[0]
        assert _pad_net(block, "2") == nets[1]
        assert _pad_net(block, "3") is None
        assert _pad_net(block, "4") is None
        for pad in ("1", "2", "3", "4"):
            assert _pad_net(block, pad) != "0VA"


def test_ae075g_pre90_result_passes_load_gate_but_retains_bench_boundary():
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    h = result["headline"]
    assert result["authority"] == "AE-075G"
    assert result["historical_run06_modified"] is False
    assert result["application"]["balanced_input_load_ohm"] == 2000
    assert h["worst_abs_insertion_loss_db_vs_100k"] <= 0.30
    assert h["worst_passband_peak_db"] <= 0.10
    assert h["load_compatibility_pass"] is True
    assert result["high_gain_level_disposition"] == "MARGINAL_BENCH_CONFIRMATION_REQUIRED"
    assert result["bench_gates_retained"]["output_load_cable_stability_bench_gate_retained"] is True
    assert result["bench_gates_retained"]["dynamic_thd_bench_gate_retained"] is True
    assert result["bench_gates_retained"]["output_header_xy_provisional"] is True


def test_ae075g_record_and_resolutions_remain_cross_registered():
    index = yaml.safe_load(INDEX.read_text(encoding="utf-8"))
    authority = yaml.safe_load(AUTHORITY.read_text(encoding="utf-8"))
    hold = yaml.safe_load(HOLD.read_text(encoding="utf-8"))
    bom = yaml.safe_load(BOM.read_text(encoding="utf-8"))

    assert index["pre_spice_assurance"]["AE-075G"] == RECORD_REL
    assert RECORD_REL in authority["pre_spice_assurance_evidence"]
    assert (ROOT / RECORD_REL).exists()
    resolved = {x["id"]: x for x in hold["resolved_after_ae075g"]}
    assert resolved["AE075G-O01"]["resolution"] == (
        "AE075G_H801_H802_5055780221_NATIVE_F8_PAD_NET_MAPPING_VALIDATED"
    )
    assert resolved["AE071-S01"]["per_leg_ohm"] == 25.0
    assert resolved["AE071-S01"]["differential_ohm"] == 50.0
    assert resolved["AE075G-PRE90"]["load_ohm"] == 2000
    assert resolved["AE075G-PRE90"]["run06_bench_gates_retained"] is True

    h = next(x for x in bom["items"] if x["id"] == "BOM-SCH108-OUTPUT-HARNESS-PCB")
    assert h["mpn"] == "5055780221"
    assert h["pin_contract"] == "PIN1_HOT_POS_PIN2_COLD_NEG"
    assert h["native_validation"] == "PASS"
