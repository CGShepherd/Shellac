"""Audit current Shellac configuration authority."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "config/decisions/current_decision_index.yaml"
STATUS = ROOT / "config/decisions/decision_status.yaml"
AUTHORITY = ROOT / "config/decisions/document_authority.yaml"

BAD_IMPLEMENTED_PHRASES = (
    "remains the pre-DR038 implementation",
    "until atomic CAD migration",
    "pending implementation",
    "not yet substituted",
)

def audit(text: str) -> list[str]:
    errors: list[str] = []
    for decision in ("DR-038", "DR-039"):
        match = re.search(
            rf"(?ms)^  {re.escape(decision)}:\n(.*?)(?=^  DR-\d+:|^historical_implementation_events:|\Z)",
            text,
        )
        if not match:
            errors.append(f"{decision}: missing from authoritative index")
            continue
        block = match.group(1)
        if "status: CURRENT_IMPLEMENTED" not in block:
            errors.append(f"{decision}: expected CURRENT_IMPLEMENTED")
        lower = block.lower()
        for phrase in BAD_IMPLEMENTED_PHRASES:
            if phrase.lower() in lower:
                errors.append(f"{decision}: CURRENT_IMPLEMENTED conflicts with phrase {phrase!r}")
    return errors

EXPECTED = {
    "DR-037": "CURRENT_IMPLEMENTED",
    "DR-038": "CURRENT_ARCHITECTURE_QUALIFICATION_OPEN",
    "DR-039": "CURRENT_SELECTED_PENDING_IMPLEMENTATION",
    "DR-040": "CURRENT_IMPLEMENTED",
    "AE-041-A1": "CURRENT_ARCHITECTURE_QUALIFICATION_OPEN",
}


def list_values(text: str, key: str) -> set[str]:
    match = re.search(
        rf"(?ms)^{re.escape(key)}:\s*\n(.*?)(?=^[A-Za-z_][A-Za-z0-9_]*:|\Z)",
        text,
    )
    if not match:
        return set()
    values = set()
    for raw in match.group(1).splitlines():
        line = raw.strip()
        if line.startswith("- "):
            values.add(line[2:].strip())
    return values


def decision_status(text: str, decision: str) -> str | None:
    match = re.search(
        rf"(?ms)^  {re.escape(decision)}:\n"
        rf"(.*?)(?=^  (?:DR-\d+|AE-\d+-A\d+):|^pre_spice_assurance:)",
        text,
    )
    if not match:
        return None
    status = re.search(r"(?m)^    status:\s*(\S+)\s*$", match.group(1))
    return status.group(1) if status else None


def authority_paths(text: str, section: str) -> list[str]:
    match = re.search(
        rf"(?ms)^{re.escape(section)}:\s*\n"
        rf"(.*?)(?=^[A-Za-z_][A-Za-z0-9_]*:|\Z)",
        text,
    )
    if not match:
        return []
    paths = []
    for raw in match.group(1).splitlines():
        line = raw.strip()
        if line.startswith("- "):
            paths.append(line[2:].strip())
    return paths


def audit_repository() -> list[str]:
    errors = []
    index = INDEX.read_text(encoding="utf-8")
    status = STATUS.read_text(encoding="utf-8")
    authority = AUTHORITY.read_text(encoding="utf-8")

    allowed = list_values(status, "allowed_status")
    current = list_values(status, "authoritative_current_status")

    for decision, expected in EXPECTED.items():
        actual = decision_status(index, decision)
        if actual != expected:
            errors.append(f"{decision}: expected {expected}, found {actual}")
        if expected not in allowed:
            errors.append(f"{decision}: {expected} missing from allowed_status")
        if expected not in current:
            errors.append(f"{decision}: {expected} missing from authoritative_current_status")

    for n in range(42, 72):
        if not re.search(rf"(?m)^  AE-{n:03d}:", index):
            errors.append(f"AE-{n:03d}: missing from pre_spice_assurance")

    if not re.search(r"(?m)^  AE-071A:", index):
        errors.append("AE-071A: missing from pre_spice_assurance")

    dr039_match = re.search(r"(?ms)^  DR-039:\n(.*?)(?=^  DR-040:)", index)
    if not dr039_match:
        errors.append("DR-039: authority block missing")
    else:
        dr039_block = dr039_match.group(1)
        current_record = "primary_record: docs/decisions/DR-039_Branch_Local_DC_Block_SELECTED.md"
        history_record = "historical_record: docs/decisions/DR-039_Common_Post_EQ_DC_Block_SELECTED.md"
        if current_record not in dr039_block:
            errors.append("DR-039: current branch-local primary record missing")
        if history_record not in dr039_block:
            errors.append("DR-039: prior common-block record is not retained as historical provenance")
        if not (ROOT / "docs/decisions/DR-039_Branch_Local_DC_Block_SELECTED.md").exists():
            errors.append("DR-039: branch-local primary record file missing")

    for section in (
        "current_authority",
        "pre_spice_assurance_evidence",
        "historical_state_evidence",
    ):
        for rel in authority_paths(authority, section):
            if not (ROOT / rel).exists():
                errors.append(f"{section}: missing path {rel}")

    if "historical_deleted_artefacts:" not in authority:
        errors.append("historical_deleted_artefacts section missing")

    for rel in (
        "tools/apply_dr038_full_migration.py",
        "tools/apply_dr039_full_closure.py",
    ):
        if rel not in authority:
            errors.append(f"historical-deleted artefact absent: {rel}")
        if (ROOT / rel).exists():
            errors.append(f"historical-deleted artefact unexpectedly exists: {rel}")

    return errors


def main() -> int:
    errors = audit_repository()
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("Shellac decision/configuration authority audit passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
