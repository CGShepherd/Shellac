from pathlib import Path
from generator.layout.schematic_release_gate import build_schematic_to_layout_release_gate

def test_sr039_releases_schematic_but_not_manufacture():
    gate=build_schematic_to_layout_release_gate()
    assert gate.disposition.schematic_release == "RELEASED"
    assert gate.disposition.placement_release.startswith("ALLOWED")
    assert gate.disposition.routing_release.startswith("BLOCKED")
    assert gate.disposition.manufacturing_release.startswith("BLOCKED")
    from generator.layout.constraints import build_layout_baseline
    critical_ids={item.identifier for item in build_layout_baseline().critical_nets}
    assert {"NET-011","NET-012","NET-013"} <= critical_ids

def test_sr039_controlled_validation_evidence():
    text=Path("config/release/sr039_schematic_to_layout.yaml").read_text(encoding="utf-8")
    assert "passed: 374" in text
    assert "failed: 0" in text
    assert "native_kicad_erc:" in text
    assert "errors: 0" in text
    assert "warnings: 0" in text
    assert "exit_code: 0" in text

def test_dr038_dr039_records_are_not_pending_after_release():
    for path in (
        "docs/decisions/DR-038_SCH101_Precision_Architecture_SELECTED.md",
        "docs/decisions/DR-039_Common_Post_EQ_DC_Block_SELECTED.md",
    ):
        text=Path(path).read_text(encoding="utf-8").upper()
        assert "MIGRATION PENDING" not in text
        assert "**STATUS:** IMPLEMENTED" in text

def test_current_decision_index_describes_active_dr038():
    text=Path("config/decisions/current_decision_index.yaml").read_text(encoding="utf-8")
    block=text.split("  DR-038:",1)[1].split("  DR-039:",1)[0]
    assert "status: CURRENT_IMPLEMENTED" in block
    assert "converter_gain: 4.0" in block
    assert "pre-DR038 implementation" not in block
