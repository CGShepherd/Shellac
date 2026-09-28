from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
DECISIONS = ROOT / "config/decisions/current_decision_index.yaml"
AUTHORITY = ROOT / "config/decisions/document_authority.yaml"
RECORD = ROOT / "docs/design_pack/AE-075C_Control_Hardware_and_Vertical_Stack_Reconciliation_Rev_A0.md"


def _record() -> str:
    return RECORD.read_text(encoding="utf-8")


def test_ae075c_record_freezes_historical_control_selection():
    text = _record()
    assert "NR01105ANG13-2C" in text
    assert "NR01105ANG13-2A" in text
    assert "A30403RNCB" in text
    assert "7201SYCBE" in text
    assert "AT3009" in text
    assert "no threaded mounting bushing" in text


def test_ae075c_record_preserves_its_historical_b03_boundary():
    text = _record()
    assert "Freeze control-plane Z relative to the top cover" in text
    assert "Downselect direct-main-PCB versus REG-08 control-PCB ownership" in text
    assert "Create exact footprints/pin maps/courtyards/body envelopes" in text
    assert "does not prematurely select a REG-08 control PCB" in text
    assert "Routing, layout freeze, BOM freeze and manufacturing release remain explicitly unauthorised." in text


def test_ae075c_record_retains_closed_validation_evidence():
    text = _record()
    assert "**Status:** CLOSED — PRE-ROUTING DESIGN IMPLEMENTATION VALIDATED" in text
    assert "full regression suite: **689 passed**" in text
    assert "native hierarchical ERC: **0 violations**" in text


def test_ae075c_historical_record_remains_cross_registered():
    decisions = yaml.safe_load(DECISIONS.read_text(encoding="utf-8"))
    authority = yaml.safe_load(AUTHORITY.read_text(encoding="utf-8"))
    rel = "docs/design_pack/AE-075C_Control_Hardware_and_Vertical_Stack_Reconciliation_Rev_A0.md"
    assert decisions["pre_spice_assurance"]["AE-075C"] == rel
    assert rel in authority["pre_spice_assurance_evidence"]
    assert RECORD.exists()
