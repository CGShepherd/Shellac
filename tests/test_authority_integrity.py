from pathlib import Path
import re

ROOT = Path(".")
INDEX = ROOT / "config/decisions/current_decision_index.yaml"
STATUS = ROOT / "config/decisions/decision_status.yaml"
AUTHORITY = ROOT / "config/decisions/document_authority.yaml"


def _text(path):
    return path.read_text(encoding="utf-8")


def _list(text, key):
    match = re.search(
        rf"(?ms)^{re.escape(key)}:\s*\n(.*?)(?=^[A-Za-z_][A-Za-z0-9_]*:|\Z)",
        text,
    )
    assert match, key
    values = []
    for raw in match.group(1).splitlines():
        line = raw.strip()
        if line.startswith("- "):
            values.append(line[2:].strip())
    return values


def _paths(text, section):
    match = re.search(
        rf"(?ms)^{re.escape(section)}:\s*\n"
        rf"(.*?)(?=^[A-Za-z_][A-Za-z0-9_]*:|\Z)",
        text,
    )
    assert match, section
    paths = []
    for raw in match.group(1).splitlines():
        line = raw.strip()
        if line.startswith("- "):
            paths.append(line[2:].strip())
    return paths


def test_current_statuses_are_admitted():
    index = _text(INDEX)
    status = _text(STATUS)
    used = set(re.findall(r"(?m)^    status:\s*(\S+)\s*$", index))
    assert used <= set(_list(status, "allowed_status"))
    assert used <= set(_list(status, "authoritative_current_status"))


def test_live_authority_paths_resolve():
    authority = _text(AUTHORITY)
    for section in (
        "current_authority",
        "pre_spice_assurance_evidence",
        "historical_state_evidence",
    ):
        for rel in _paths(authority, section):
            assert (ROOT / rel).exists(), f"Dangling {section}: {rel}"


def test_deleted_migration_tools_are_explicit_history():
    authority = _text(AUTHORITY)
    assert "historical_deleted_artefacts:" in authority
    for rel in (
        "tools/apply_dr038_full_migration.py",
        "tools/apply_dr039_full_closure.py",
    ):
        assert rel in authority
        assert not (ROOT / rel).exists()


def test_assurance_chain_reaches_ae059():
    index = _text(INDEX)
    for n in range(42, 60):
        assert re.search(rf"(?m)^  AE-{n:03d}:", index)


def test_ae058_companion_a2_records_are_explicit():
    authority = _text(AUTHORITY)
    assert "AE-058_Shellac_LTspice26_Correlation_Compatibility_and_RUN00_Correction_Rev_A2.md" in authority
    assert "AE-058_Shellac_LTspice26_Correlation_Numerical_Closure_Rev_A2.md" in authority
