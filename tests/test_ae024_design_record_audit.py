import builtins
from pathlib import Path

from tools.ae024_design_record_audit import (
    collect_claims,
    contradictory_claims,
    parse_current_decision_index,
    parse_decision_status_yaml,
    render,
    status_vocabulary_findings,
)


def _repo(tmp_path):
    (tmp_path/"config/decisions").mkdir(parents=True)
    (tmp_path/"docs").mkdir()
    return tmp_path


def test_decision_status_parser_handles_inline_list_without_pyyaml(tmp_path):
    p = tmp_path/"decision_status.yaml"
    p.write_text(
        "schema_version: 1\n"
        "allowed_status: [PROPOSED, SELECTED, SUPERSEDED]\n",
        encoding="utf-8",
    )
    doc = parse_decision_status_yaml(p)
    assert doc["allowed_status"] == ["PROPOSED", "SELECTED", "SUPERSEDED"]


def test_current_index_parser_handles_block_list_and_decisions(tmp_path):
    p = tmp_path/"current_decision_index.yaml"
    p.write_text(
        "status_vocabulary:\n"
        "  - CURRENT_IMPLEMENTED\n"
        "  - SUPERSEDED\n"
        "decisions:\n"
        "  DR-001:\n"
        "    status: CURRENT_IMPLEMENTED\n"
        "    primary_record: docs/x.md\n",
        encoding="utf-8",
    )
    doc = parse_current_decision_index(p)
    assert doc["status_vocabulary"] == ["CURRENT_IMPLEMENTED", "SUPERSEDED"]
    assert doc["decisions"]["DR-001"]["status"] == "CURRENT_IMPLEMENTED"


def test_detects_status_vocabulary_mismatch(tmp_path):
    r=_repo(tmp_path)
    (r/"config/decisions/decision_status.yaml").write_text(
        "allowed_status: [SELECTED, SUPERSEDED]\n", encoding="utf-8")
    (r/"config/decisions/current_decision_index.yaml").write_text(
        "status_vocabulary:\n"
        "  - CURRENT_IMPLEMENTED\n"
        "  - SUPERSEDED\n"
        "decisions:\n"
        "  DR-001:\n"
        "    status: CURRENT_IMPLEMENTED\n",
        encoding="utf-8")
    assert status_vocabulary_findings(r)


def test_detects_conflicting_current_claim(tmp_path):
    r=_repo(tmp_path)
    (r/"config/decisions/current_decision_index.yaml").write_text(
        "status_vocabulary:\n"
        "  - CURRENT_IMPLEMENTED\n"
        "  - CURRENT_SELECTED_PENDING_IMPLEMENTATION\n"
        "decisions:\n"
        "  DR-001:\n"
        "    status: CURRENT_IMPLEMENTED\n"
        "    primary_record: x\n",
        encoding="utf-8")
    (r/"config/decisions/decision_status.yaml").write_text(
        "allowed_status: [CURRENT_IMPLEMENTED, CURRENT_SELECTED_PENDING_IMPLEMENTATION]\n",
        encoding="utf-8")
    (r/"docs/x.md").write_text("DR-001 status CURRENT_SELECTED_PENDING_IMPLEMENTATION\n", encoding="utf-8")
    claims,_=collect_claims(r)
    assert contradictory_claims(r,claims)


def test_module_does_not_import_yaml():
    import tools.ae024_design_record_audit as audit
    assert "yaml" not in audit.__dict__


def test_render_defines_maintenance_and_historical_pack_layers(tmp_path):
    r=_repo(tmp_path)
    (r/"config/decisions/current_decision_index.yaml").write_text(
        "decisions:\n", encoding="utf-8")
    text=render(r,[],[],[],[])
    assert "07 Maintenance guide" in text
    assert "99 Historical evidence" in text
