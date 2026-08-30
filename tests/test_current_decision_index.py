from pathlib import Path
import re

INDEX = Path("config/decisions/current_decision_index.yaml")

def _text():
    return INDEX.read_text(encoding="utf-8")

def _decision_status(decision_id):
    text=_text()
    m=re.search(
        rf"(?ms)^  {re.escape(decision_id)}:\s*\n.*?^    status:\s*([^\n]+)",
        text,
    )
    assert m, f"Missing status for {decision_id}"
    return m.group(1).strip()

def test_authoritative_decision_index_is_well_formed():
    text=_text()
    assert re.search(r"(?m)^  branch:\s*main\s*$", text)
    assert _decision_status("DR-037") == "CURRENT_IMPLEMENTED"
    assert _decision_status("DR-039") == "CURRENT_IMPLEMENTED"
    for decision in ("DR-038", "DR-040"):
        assert _decision_status(decision) == "CURRENT_SELECTED_PENDING_IMPLEMENTATION"

def test_selected_pending_is_not_claimed_implemented():
    text=_text()
    assert re.search(r"(?m)^      converter_gain:\s*3\.48\s*$", text)
    dr039 = text.split("  DR-039:", 1)[1].split("  DR-040:", 1)[0]
    assert "status: CURRENT_IMPLEMENTED" in dr039
    assert "SCH103 includes 1uF film / 330k DC block" in dr039

def test_design_pack_and_maintenance_structure_exist():
    assert Path("docs/knowledge/DESIGN_PACK_INDEX.md").exists()
    assert Path("docs/maintenance/MAINTENANCE_GUIDE_SKELETON.md").exists()

