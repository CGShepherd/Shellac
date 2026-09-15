from pathlib import Path
import re

INDEX = Path("config/decisions/current_decision_index.yaml")

def _text():
    return INDEX.read_text(encoding="utf-8")

def _decision_block(decision_id, next_id=None):
    text = _text()
    start = f"  {decision_id}:"
    assert start in text, f"Missing decision {decision_id}"
    block = text.split(start, 1)[1]
    if next_id is not None:
        block = block.split(f"  {next_id}:", 1)[0]
    elif "historical_implementation_events:" in block:
        block = block.split("historical_implementation_events:", 1)[0]
    return block

def _decision_status(decision_id, next_id=None):
    block = _decision_block(decision_id, next_id)
    m = re.search(r"(?m)^    status:\s*([^\n]+)$", block)
    assert m, f"Missing status for {decision_id}"
    return m.group(1).strip()

def test_authoritative_decision_index_is_well_formed():
    text = _text()
    assert re.search(r"(?m)^  branch:\s*main\s*$", text)
    assert "commit: dce5c0ec36e12f979338d8c46106c44a79c7a023" in text
    assert _decision_status("DR-037", "DR-038") == "CURRENT_IMPLEMENTED"
    assert _decision_status("DR-038", "DR-039") == "CURRENT_SELECTED_PENDING_IMPLEMENTATION"
    assert _decision_status("DR-039", "DR-040") == "CURRENT_SELECTED_PENDING_IMPLEMENTATION"
    assert _decision_status("DR-040") == "CURRENT_IMPLEMENTED"

def test_dr038_dr039_record_current_pre_spice_disposition():
    dr038 = _decision_block("DR-038", "DR-039")
    assert "    implementation:" in dr038
    assert "      converter_gain: 4.0" in dr038
    assert "LT5400-7 A-grade retained provisionally" in dr038
    assert "fail-safe removable gold service-shunt topology" in dr038
    assert "approximately 14/18/22 dB" in dr038
    assert "pre-DR038 implementation" not in dr038

    dr039 = _decision_block("DR-039", "DR-040")
    assert "status: CURRENT_SELECTED_PENDING_IMPLEMENTATION" in dr039
    assert "primary_record: docs/decisions/DR-039_Branch_Local_DC_Block_SELECTED.md" in dr039
    assert "historical_record: docs/decisions/DR-039_Common_Post_EQ_DC_Block_SELECTED.md" in dr039
    assert "AE-067 selects branch-local DC blocking for controlled implementation" in dr039
    assert "not yet migrated into the live product" in dr039
    assert "RUN09, RUN10, RUN12 and bench correlation remain open" in dr039

def test_design_pack_and_maintenance_structure_exist():
    assert Path("docs/knowledge/DESIGN_PACK_INDEX.md").exists()
    assert Path("docs/maintenance/MAINTENANCE_GUIDE_SKELETON.md").exists()


def test_pre_spice_assurance_chain_reaches_ae067():
    text = _text()
    for n in range(42, 68):
        assert f"  AE-{n:03d}:" in text
