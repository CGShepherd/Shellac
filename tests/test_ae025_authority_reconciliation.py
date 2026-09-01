from pathlib import Path
from tools.ae024_design_record_audit import current_authority_paths, status_vocabulary_findings

def test_scoped_current_status_vocabulary_is_supported(tmp_path):
    (tmp_path/"config/decisions").mkdir(parents=True)
    (tmp_path/"config/decisions/decision_status.yaml").write_text(
        "authoritative_current_status: [CURRENT_IMPLEMENTED, SUPERSEDED]\n"
        "allowed_status: [SELECTED, SUPERSEDED, CURRENT_IMPLEMENTED]\n",
        encoding="utf-8",
    )
    (tmp_path/"config/decisions/current_decision_index.yaml").write_text(
        "status_vocabulary:\n"
        "  - CURRENT_IMPLEMENTED\n"
        "  - SUPERSEDED\n"
        "decisions:\n"
        "  DR-001:\n"
        "    status: CURRENT_IMPLEMENTED\n",
        encoding="utf-8",
    )
    assert status_vocabulary_findings(tmp_path) == []

def test_current_authority_path_is_loaded(tmp_path):
    (tmp_path/"config/decisions").mkdir(parents=True)
    (tmp_path/"config/decisions/document_authority.yaml").write_text(
        "current_authority:\n  - README.md\n",
        encoding="utf-8",
    )
    assert "README.md" in current_authority_paths(tmp_path)
