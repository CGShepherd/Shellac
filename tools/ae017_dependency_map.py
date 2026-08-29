"""AE-017 dependency mapper for the DR-038 / DR-039 atomic CAD migration.

Read-only tool: scans the current repository and writes a markdown dependency
map. It never modifies generator, tests, config, or CAD files.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys

TOKENS = {
    "SCH101_NUMERIC": (
        "DIFF_CONVERTER_GAIN",
        "GAIN_RG_OHM",
        "GAIN_BASE_RF_OHM",
        "GAIN_DEFAULT_ADD_OHM",
        "GAIN_HIGH_ADD_OHM",
        "3.48",
        "4420",
        "8280",
        "21680",
        "12700",
        "26100",
    ),
    "SCH101_CAD": (
        "SW1011",
        "R112",
        "R113",
        "R114",
        "DIP_Switch_Block",
        "STEREO GAIN DIP",
        "3.48x differential converter",
        "10k / 34.8k",
    ),
    "SCH103_OUTPUT": (
        "TP{base}4",
        "_EQ_OUT",
        "output_end = Point(420",
        "POST_EQ",
        "replay_eq.py",
    ),
    "DR039": (
        "post_eq_dc_block",
        "DR-039",
        "1.0 µF",
        "1u",
        "330k",
        "0.48 Hz",
    ),
    "ANALYSIS": (
        "signal_chain_analysis",
        "sch101_precision_candidate",
        "sch101_precision_analysis",
        "signal_chain_noise_dc",
        "AE-012",
        "AE-013",
        "AE-014",
        "AE-015",
    ),
}

TEXT_SUFFIXES = {
    ".py", ".md", ".yaml", ".yml", ".toml", ".txt", ".bat", ".json",
    ".kicad_sch", ".kicad_pcb", ".kicad_sym",
}
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", "generated", "output"}


@dataclass(frozen=True)
class Hit:
    category: str
    token: str
    path: str
    line: int
    text: str


def iter_text_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {"Makefile"}:
            yield path


def scan(repo: Path) -> list[Hit]:
    hits: list[Hit] = []
    for path in iter_text_files(repo):
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        rel = path.relative_to(repo).as_posix()
        for number, line in enumerate(lines, 1):
            for category, tokens in TOKENS.items():
                for token in tokens:
                    if token in line:
                        hits.append(Hit(category, token, rel, number, line.strip()))
    return hits


def classify_path(path: str) -> str:
    if path.startswith("generator/blocks/"):
        return "CAD builder"
    if path.startswith("generator/model/"):
        return "electrical/analysis model"
    if path.startswith("generator/core/"):
        return "CAD infrastructure"
    if path.startswith("generator/layout/"):
        return "layout"
    if path.startswith("tests/"):
        return "regression contract"
    if path.startswith("config/bom/"):
        return "BOM"
    if path.startswith("config/procurement/"):
        return "procurement"
    if path.startswith("docs/"):
        return "controlled documentation"
    return "repository/support"


def render(repo: Path, hits: list[Hit]) -> str:
    unique_paths = sorted({h.path for h in hits})
    lines = [
        "# AE-017 Generated DR-038 / DR-039 Dependency Map",
        "",
        f"Repository scanned: `{repo.resolve()}`",
        "",
        "## Summary",
        "",
        f"- matched files: **{len(unique_paths)}**",
        f"- matched references: **{len(hits)}**",
        "",
        "This report is evidence for an atomic migration. A file appearing here is",
        "not automatically changed; it is a review surface that must be dispositioned.",
        "",
    ]

    for category in TOKENS:
        cat_hits = [h for h in hits if h.category == category]
        paths = sorted({h.path for h in cat_hits})
        lines += [f"## {category}", ""]
        if not cat_hits:
            lines += ["No matches.", ""]
            continue
        lines += ["| File | Contract class | References |", "|---|---|---:|"]
        for path in paths:
            count = sum(1 for h in cat_hits if h.path == path)
            lines.append(f"| `{path}` | {classify_path(path)} | {count} |")
        lines.append("")

    lines += [
        "## Atomic migration gates",
        "",
        "### DR-038 / SCH101",
        "",
        "The migration is not complete until all of these move together:",
        "",
        "1. electrical constants and gain settings;",
        "2. physical LT5400-7 component/symbol/footprint representation;",
        "3. removal/replacement of the ordinary DIP gain selector;",
        "4. precision service-link implementation;",
        "5. SCH101 builder values and annotations;",
        "6. component/BOM/procurement records;",
        "7. numeric gain regressions;",
        "8. rendered-CAD/refdes regressions;",
        "9. AE-012 headroom regression;",
        "10. AE-013/014 noise/CMRR regression.",
        "",
        "### DR-039 / SCH103",
        "",
        "The migration is not complete until all of these move together:",
        "",
        "1. post-EQ DC-block electrical model;",
        "2. SCH103 output builder and test-point allocation;",
        "3. physical film-capacitor selection/footprint;",
        "4. PCB placement allowance;",
        "5. component-count/refdes contracts;",
        "6. replay-curve regression including the ~0.48 Hz pole;",
        "7. AE-012 headroom update;",
        "8. AE-015 DC/noise update;",
        "9. rumble bypass/filter switching transient tests;",
        "10. power-up/power-down transient acceptance.",
        "",
        "## Detailed hits",
        "",
        "| Category | Token | File | Line | Context |",
        "|---|---|---|---:|---|",
    ]
    for h in sorted(hits, key=lambda x: (x.path, x.line, x.category, x.token)):
        context = h.text.replace("|", "\\|")[:160]
        lines.append(f"| {h.category} | `{h.token}` | `{h.path}` | {h.line} | {context} |")
    lines.append("")
    return "\n".join(lines)


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    repo = Path(args[0]).resolve() if args else Path.cwd().resolve()
    if not (repo / "generator").exists() or not (repo / "tests").exists():
        print("ERROR: run from the Shellac repository root.", file=sys.stderr)
        return 2
    hits = scan(repo)
    output = repo / "docs" / "AE-017_Generated_Atomic_Migration_Dependency_Map.md"
    output.write_text(render(repo, hits), encoding="utf-8")
    print(f"Wrote {output}")
    print(f"Matched {len({h.path for h in hits})} files and {len(hits)} references.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
