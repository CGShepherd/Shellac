from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
DECISIONS = ROOT / "config/decisions/current_decision_index.yaml"
AUTHORITY = ROOT / "config/decisions/document_authority.yaml"
RECORD = ROOT / "docs/design_pack/AE-075E_B03_Shared_CK_Local_Control_PCB_Ownership_Rev_A0.md"


def _record() -> str:
    return RECORD.read_text(encoding="utf-8")


def test_ae075e_record_preserves_ck_manufacturer_semantics():
    text = _record()
    assert "`R` mounting as 3/8-32 threaded" in text
    assert "`C` termination as PC through-hole" in text
    assert "`Y` as the 0.350 inch / 8.89 mm high 1/4-40 threaded bushing" in text
    assert "0.250 inch / 6.35 mm long PC pins" in text
    assert "does **not** define a unique installed panel-to-PCB plane" in text


def test_ae075e_record_selects_local_ck_pcb_ownership_without_fake_z():
    text = _record()
    assert "Direct mounting of Channel, Rumble and Mute on the current main audio PCB is rejected" in text
    assert "distributed local control PCB(s)" in text
    assert "design downselect, not a claim that every hypothetical elevated-main-board redesign is physically impossible" in text
    assert "exact carrier/main-PCB Z relative to the upper-cover inner face" in text


def test_ae075e_record_preserves_no_flying_switch_harness_boundary():
    text = _record()
    assert "switch terminals are soldered directly to those local PCBs" in text
    assert "no-flying-switch-harness requirement remains satisfied" in text
    assert "inter-board connection" in text
    assert "is not itself a flying switch-terminal harness" in text


def test_ae075e_record_keeps_partition_support_interconnect_and_geometry_open():
    text = _record()
    assert "exact partition into one or more local modules remains open" in text
    assert "local-control-PCB standoff/support architecture" in text
    assert "rigid board-to-board versus short serviceable inter-board connection" in text
    assert "No native PCB geometry" in text


def test_ae075e_historical_record_remains_cross_registered():
    decisions = yaml.safe_load(DECISIONS.read_text(encoding="utf-8"))
    authority = yaml.safe_load(AUTHORITY.read_text(encoding="utf-8"))
    rel = "docs/design_pack/AE-075E_B03_Shared_CK_Local_Control_PCB_Ownership_Rev_A0.md"
    assert decisions["pre_spice_assurance"]["AE-075E"] == rel
    assert rel in authority["pre_spice_assurance_evidence"]
    assert RECORD.exists()
