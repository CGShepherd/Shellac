from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
DECISIONS = ROOT / "config/decisions/current_decision_index.yaml"
AUTHORITY = ROOT / "config/decisions/document_authority.yaml"
RECORD = ROOT / "docs/design_pack/AE-075F_B03_Control_Module_Partition_and_Serviceable_Harness_Architecture_Rev_A0.md"


def _record() -> str:
    return RECORD.read_text(encoding="utf-8")


def test_ae075f_record_freezes_four_module_partition():
    text = _record()
    for token in ("`EQ_L`", "`EQ_R`", "`RUMBLE`", "`MATRIX_MUTE`"):
        assert token in text
    assert "four local control PCBs" in text


def test_ae075f_record_selects_serviceable_harness_not_rigid_board_to_board():
    text = _record()
    assert "short detachable wire harness" in text
    assert "Rigid board-to-board coupling" in text
    assert "rejected as the current architecture" in text


def test_ae075f_record_selects_micro_lock_family_without_premature_exact_variant():
    text = _record()
    assert "Molex Micro-Lock Plus 2.00 mm" in text
    assert "`505575`" in text
    assert "`505578`" in text
    assert "`505570`" in text
    assert "`5055721200`" in text
    assert "Exact header orientation/order code and final circuit count are not frozen" in text


def test_ae075f_record_preserves_eq_run10_passive_partition_gate():
    text = _record()
    assert "reduces the main-board interface to four unique nets per channel" in text
    assert "physical passive partition remains subject to the B03/RUN10 parasitic discriminator" in text


def test_ae075f_historical_record_remains_cross_registered():
    decisions = yaml.safe_load(DECISIONS.read_text(encoding="utf-8"))
    authority = yaml.safe_load(AUTHORITY.read_text(encoding="utf-8"))
    rel = "docs/design_pack/AE-075F_B03_Control_Module_Partition_and_Serviceable_Harness_Architecture_Rev_A0.md"
    assert decisions["pre_spice_assurance"]["AE-075F"] == rel
    assert rel in authority["pre_spice_assurance_evidence"]
    assert RECORD.exists()
