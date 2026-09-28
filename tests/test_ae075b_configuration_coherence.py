from pathlib import Path
import subprocess
import yaml

ROOT = Path(__file__).resolve().parents[1]

def test_ae075b_routing_hold_header_and_blockers_are_current():
    hold = yaml.safe_load((ROOT / "config/release/ae071_prerouting_hold.yaml").read_text(encoding="utf-8"))
    assert hold["authority"] == "AE-075B"
    assert hold["previous_authority"] == "AE-075A"
    assert hold["baseline_commit"] == "5b51964c2282083c7d767f330966905d34fe47e6"
    assert {x["id"] for x in hold["routing_blockers"]} == {"AE071-B03", "AE071-B04", "AE071-B08"}
    assert hold["permissions"]["final_routing"] is False

def test_pre_spice_index_is_registered_in_document_authority():
    decisions = yaml.safe_load((ROOT / "config/decisions/current_decision_index.yaml").read_text(encoding="utf-8"))
    authority = yaml.safe_load((ROOT / "config/decisions/document_authority.yaml").read_text(encoding="utf-8"))
    registered = set(authority["pre_spice_assurance_evidence"])
    for record, rel in decisions["pre_spice_assurance"].items():
        assert rel in registered, (record, rel)
        assert (ROOT / rel).exists(), (record, rel)

def test_current_facing_documents_reflect_ae075b_state():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    index = (ROOT / "docs/knowledge/DESIGN_PACK_INDEX.md").read_text(encoding="utf-8")
    maintenance = (ROOT / "docs/maintenance/Signal_Chain_Commissioning_and_Maintenance_Baseline_Rev_A0.md").read_text(encoding="utf-8")
    for text in (readme, index, maintenance):
        assert "LT5400BIMS8E-7#PBF" in text
    assert "AE-042 through AE-075B" in index

def test_native_pcb_is_not_ignored_by_rule():
    p = subprocess.run(["git", "check-ignore", "--no-index", "-q", "out/kicad/ProjectShellac.kicad_pcb"], cwd=ROOT)
    assert p.returncode == 1

def test_ae075b_record_is_closed_after_final_qualification():
    record = (
        ROOT
        / "docs/design_pack/AE-075B_XLR_LT5400_and_Service_Hardware_Reconciliation_Rev_A0.md"
    ).read_text(encoding="utf-8")
    assert "**Status:** CLOSED — PRE-ROUTING DESIGN IMPLEMENTATION VALIDATED" in record
    assert "full regression suite: **682 passed**" in record
    assert "native hierarchical ERC: **0 violations**" in record
