"""AE-024A project-wide decision/document reconciliation audit.

Standard-library only.  The audit intentionally parses only the narrow YAML
structures used by Shellac's decision-control files:
- top-level scalar/list keys;
- top-level `decisions:` mapping;
- per-decision scalar fields.

It does not attempt to implement general YAML.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import ast
import re
import sys

DECISION_RE = re.compile(r"\b(DR-\d{3}|DEC-\d{3}|SR-\d{3}|G3-\d{3}|AE-\d{3}[A-Z]?)\b")
STATUS_RE = re.compile(
    r"\b(PROPOSED|SELECTED|FROZEN|DEFERRED|REJECTED|SUPERSEDED|"
    r"CURRENT_IMPLEMENTED|CURRENT_SELECTED_PENDING_IMPLEMENTATION|"
    r"HISTORICAL|CURRENT_IMPLEMENTATION_STAGING_EVIDENCE)\b"
)
BASELINE_RE = re.compile(r"(?i)\b(?:current controlled baseline|release baseline|baseline)\b")

SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", "out"}
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".txt", ".py", ".bat", ".toml", ".json"}


@dataclass(frozen=True)
class Claim:
    path: str
    line: int
    ids: tuple[str, ...]
    statuses: tuple[str, ...]
    text: str


def iter_files(repo: Path):
    for p in repo.rglob("*"):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix.lower() in TEXT_SUFFIXES or p.name in {"README"}:
            yield p


def collect_claims(repo: Path):
    claims = []
    baselines = []
    for p in iter_files(repo):
        rel = p.relative_to(repo).as_posix()
        for n, line in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            ids = tuple(sorted(set(DECISION_RE.findall(line))))
            statuses = tuple(sorted(set(STATUS_RE.findall(line))))
            if ids or statuses:
                claims.append(Claim(rel, n, ids, statuses, line.strip()))
            if BASELINE_RE.search(line):
                baselines.append((rel, n, line.strip()))
    return claims, baselines


def _strip_comment(line: str) -> str:
    # Shellac control YAML does not use quoted # characters in the structures
    # parsed by AE-024A, so a simple split is sufficient and intentionally narrow.
    return line.split("#", 1)[0].rstrip()


def _parse_scalar(text: str):
    text = text.strip()
    if not text:
        return ""
    if text.startswith("[") and text.endswith("]"):
        try:
            return ast.literal_eval(text)
        except Exception:
            return [x.strip() for x in text[1:-1].split(",") if x.strip()]
    if (text.startswith('"') and text.endswith('"')) or (
        text.startswith("'") and text.endswith("'")
    ):
        try:
            return ast.literal_eval(text)
        except Exception:
            return text[1:-1]
    if text.lower() in {"true", "false"}:
        return text.lower() == "true"
    try:
        return int(text)
    except ValueError:
        pass
    try:
        return float(text)
    except ValueError:
        return text


def parse_decision_status_yaml(path: Path):
    doc = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = _strip_comment(raw)
        if not line.strip() or line.startswith(" "):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        doc[key.strip()] = _parse_scalar(value)
    return doc


def parse_current_decision_index(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    doc = {"status_vocabulary": [], "decisions": {}}
    section = None
    current_decision = None

    for raw in lines:
        line = _strip_comment(raw)
        if not line.strip():
            continue

        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()

        if indent == 0:
            current_decision = None
            if stripped == "decisions:":
                section = "decisions"
                continue
            section = None
            if ":" in stripped:
                key, value = stripped.split(":", 1)
                if key == "status_vocabulary":
                    parsed = _parse_scalar(value)
                    doc["status_vocabulary"] = parsed if isinstance(parsed, list) else []
            continue

        # Handle block list under status_vocabulary.
        if indent == 2 and stripped.startswith("- "):
            if section is None and "status_vocabulary" in doc:
                doc["status_vocabulary"].append(stripped[2:].strip())
            continue

        if section == "decisions":
            if indent == 2 and stripped.endswith(":"):
                current_decision = stripped[:-1]
                doc["decisions"][current_decision] = {}
                continue
            if indent == 4 and current_decision and ":" in stripped:
                key, value = stripped.split(":", 1)
                # We only need scalar decision fields for the audit.
                if value.strip():
                    doc["decisions"][current_decision][key.strip()] = _parse_scalar(value)

    return doc


def status_vocabulary_findings(repo: Path):
    findings = []
    status_file = repo / "config/decisions/decision_status.yaml"
    index_file = repo / "config/decisions/current_decision_index.yaml"
    if not status_file.exists() or not index_file.exists():
        return ["decision-status configuration files are missing"]

    status_doc = parse_decision_status_yaml(status_file)
    index_doc = parse_current_decision_index(index_file)

    allowed = set(status_doc.get("allowed_status", []))
    index_vocab = set(index_doc.get("status_vocabulary", []))
    used = {
        str(v.get("status"))
        for v in index_doc.get("decisions", {}).values()
        if isinstance(v, dict) and v.get("status")
    }

    if allowed != index_vocab:
        findings.append(
            "status vocabulary mismatch: decision_status.yaml="
            f"{sorted(allowed)} vs current_decision_index.yaml={sorted(index_vocab)}"
        )
    unknown = used - index_vocab
    if unknown:
        findings.append(f"current decision index uses statuses outside its vocabulary: {sorted(unknown)}")
    forbidden = used - allowed
    if forbidden:
        findings.append(
            "current decision index uses statuses forbidden by decision_status.yaml: "
            f"{sorted(forbidden)}"
        )
    return findings


def authoritative_decisions(repo: Path):
    index_file = repo / "config/decisions/current_decision_index.yaml"
    if not index_file.exists():
        return {}
    return parse_current_decision_index(index_file).get("decisions", {})


def contradictory_claims(repo: Path, claims):
    authoritative = authoritative_decisions(repo)
    findings = []
    for decision, record in authoritative.items():
        if not isinstance(record, dict):
            continue
        auth_status = str(record.get("status", ""))
        if not auth_status:
            continue
        for c in claims:
            if decision not in c.ids or not c.statuses:
                continue
            if auth_status not in c.statuses:
                if set(c.statuses) & {"SUPERSEDED", "HISTORICAL", "REJECTED"}:
                    continue
                findings.append(
                    f"{decision}: authoritative={auth_status}, "
                    f"{c.path}:{c.line} claims {','.join(c.statuses)}"
                )
    return findings


def classify_doc(path: str) -> str:
    name = Path(path).name
    if path.startswith("config/"):
        return "authoritative machine-readable baseline"
    if path.startswith("docs/decisions/"):
        return "decision evidence"
    if path.startswith("docs/maintenance/"):
        return "maintenance/commissioning"
    if path.startswith("docs/knowledge/"):
        return "knowledge summary"
    if name.startswith("AE-"):
        return "design assurance evidence"
    if name.startswith("SR-"):
        return "review/closure evidence"
    if name.startswith("G3-"):
        return "gate/history evidence"
    if path == "README.md":
        return "project entry point"
    return "supporting/history"


def render(repo: Path, claims, baselines, vocab, contradictions):
    files = sorted({c.path for c in claims})
    auth = authoritative_decisions(repo)
    lines = [
        "# AE-024 Generated Design Record Reconciliation Audit",
        "",
        f"Repository: `{repo.resolve()}`",
        "",
        "## Executive summary",
        "",
        f"- files containing decision/status references: **{len(files)}**",
        f"- decision/status claim lines: **{len(claims)}**",
        f"- baseline declaration lines: **{len(baselines)}**",
        f"- status-vocabulary findings: **{len(vocab)}**",
        f"- potential authoritative-status contradictions: **{len(contradictions)}**",
        "",
        "This is an audit report, not an automatic rewrite instruction.",
        "",
        "## Status-vocabulary findings",
        "",
    ]
    lines += [f"- {x}" for x in vocab] or ["- None detected."]
    lines += ["", "## Potential status contradictions", ""]
    lines += [f"- {x}" for x in contradictions] or ["- None detected."]

    lines += ["", "## Authoritative decision index", "", "| ID | Status | Primary record |", "|---|---|---|"]
    for k, v in sorted(auth.items()):
        if isinstance(v, dict):
            lines.append(f"| {k} | {v.get('status','')} | `{v.get('primary_record','')}` |")

    lines += ["", "## Baseline declarations requiring reconciliation", ""]
    for p, n, text in baselines:
        safe = text.replace("|", "\\|")[:180]
        lines.append(f"- `{p}:{n}` — {safe}")

    lines += [
        "",
        "## Design-pack document inventory",
        "",
        "| File | Proposed production-pack role |",
        "|---|---|",
    ]
    for p in files:
        lines.append(f"| `{p}` | {classify_doc(p)} |")

    lines += [
        "",
        "## Required production design-pack structure",
        "",
        "1. **00 Release authority** — release manifest, version/tag, toolchain pins.",
        "2. **01 Requirements and architecture** — current functional/electrical/mechanical baseline.",
        "3. **02 Decision register** — one authoritative status per decision plus supersession links.",
        "4. **03 Schematics and PCB** — production source and fabrication outputs.",
        "5. **04 BOM and procurement** — controlled BOM, alternates, sourcing policy.",
        "6. **05 Design assurance** — AE/SR evidence, simulations, margins, validation.",
        "7. **06 Commissioning and acceptance** — production tests and measured limits.",
        "8. **07 Maintenance guide** — test points, expected values, service configuration, fault isolation.",
        "9. **08 Build/reproducibility** — clean-clone build instructions and pinned dependencies.",
        "10. **99 Historical evidence** — superseded analyses retained but clearly non-authoritative.",
        "",
    ]
    return "\n".join(lines)


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    repo = Path(args[0]).resolve() if args else Path.cwd().resolve()
    if not (repo / "config/decisions").exists():
        print("ERROR: run from Shellac repository root", file=sys.stderr)
        return 2
    claims, baselines = collect_claims(repo)
    vocab = status_vocabulary_findings(repo)
    contradictions = contradictory_claims(repo, claims)
    output = repo / "docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(repo, claims, baselines, vocab, contradictions), encoding="utf-8")
    print(f"Wrote {output}")
    print(f"Vocabulary findings: {len(vocab)}")
    print(f"Potential status contradictions: {len(contradictions)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
