from pathlib import Path
import re

from tools.ae024_design_record_audit import (
    parse_decision_status_yaml,
    status_vocabulary_findings,
)


def test_scoped_vocabularies_parse_from_inline_lists(tmp_path):
    p = tmp_path / "decision_status.yaml"
    p.write_text(
        "authoritative_current_status: [CURRENT_IMPLEMENTED, SUPERSEDED]\n"
        "narrative_status: [PROPOSED, SELECTED, SUPERSEDED]\n",
        encoding="utf-8",
    )
    doc = parse_decision_status_yaml(p)
    assert doc["authoritative_current_status"] == ["CURRENT_IMPLEMENTED", "SUPERSEDED"]
    assert doc["narrative_status"] == ["PROPOSED", "SELECTED", "SUPERSEDED"]


def test_scoped_status_vocabulary_has_no_findings(tmp_path):
    (tmp_path / "config/decisions").mkdir(parents=True)
    (tmp_path / "config/decisions/decision_status.yaml").write_text(
        "authoritative_current_status: [CURRENT_IMPLEMENTED, SUPERSEDED]\n"
        "allowed_status: [SELECTED, SUPERSEDED, CURRENT_IMPLEMENTED]\n",
        encoding="utf-8",
    )
    (tmp_path / "config/decisions/current_decision_index.yaml").write_text(
        "status_vocabulary:\n"
        "  - CURRENT_IMPLEMENTED\n"
        "  - SUPERSEDED\n"
        "decisions:\n"
        "  DR-001:\n"
        "    status: CURRENT_IMPLEMENTED\n",
        encoding="utf-8",
    )
    assert status_vocabulary_findings(tmp_path) == []


def test_validated_baseline_branch_remains_main():
    text = Path("config/decisions/current_decision_index.yaml").read_text(encoding="utf-8")
    assert re.search(r"(?m)^  branch:\s*main\s*$", text)
    assert "authority_scope:" not in text
