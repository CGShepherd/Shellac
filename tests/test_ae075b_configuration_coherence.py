from pathlib import Path
import subprocess
import yaml

ROOT = Path(__file__).resolve().parents[1]

def test_ae075b_resolutions_remain_present_after_later_authority_advances():
    hold = yaml.safe_load((ROOT / "config/release/ae071_prerouting_hold.yaml").read_text(encoding="utf-8"))
    # AE-075B owns its resolutions and fail-closed boundaries, not the identity
    # of whichever later assurance increment owns the live routing-hold header.
    resolved = {x["id"]: x for x in hold["resolved_after_ae075b"]}
    assert resolved["AE071-B06"]["resolution"] == "AE075B_NEUTRIK_DL_EXACT_PART_PIN1_AND_SHELL_LOCAL_CHASSIS_CONTRACT"
    blockers = {x["id"]: x for x in hold["routing_blockers"]}
    assert "AE071-B06" not in blockers
    record = (
        ROOT / "docs/design_pack/AE-075B_XLR_LT5400_and_Service_Hardware_Reconciliation_Rev_A0.md"
    ).read_text(encoding="utf-8")
    assert "`LT5400BIMS8E-7#PBF`" in record
    assert "B08 remains open only for:" in record

def test_pre_spice_index_is_registered_in_document_authority():
    decisions = yaml.safe_load((ROOT / "config/decisions/current_decision_index.yaml").read_text(encoding="utf-8"))
    authority = yaml.safe_load((ROOT / "config/decisions/document_authority.yaml").read_text(encoding="utf-8"))
    registered = set(authority["pre_spice_assurance_evidence"])
    for record, rel in decisions["pre_spice_assurance"].items():
        assert rel in registered, (record, rel)
        assert (ROOT / rel).exists(), (record, rel)

def test_current_facing_documents_retain_ae075b_engineering_state():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    index = (ROOT / "docs/knowledge/DESIGN_PACK_INDEX.md").read_text(encoding="utf-8")
    maintenance = (ROOT / "docs/maintenance/Signal_Chain_Commissioning_and_Maintenance_Baseline_Rev_A0.md").read_text(encoding="utf-8")
    for current_text in (readme, index, maintenance):
        assert "LT5400BIMS8E-7#PBF" in current_text
    # Later assurance increments may extend the chain tail; AE-075B's actual
    # engineering contribution must remain represented instead.
    assert "AE-075B closes B06" in index

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
