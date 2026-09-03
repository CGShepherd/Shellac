"""AE-030 read-only production/design-pack readiness audit."""

from pathlib import Path
import sys

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from generator.model.production_readiness import GATES, GateState

from generator.model.production_readiness import GATES, GateState

REQUIRED_PATHS = (
    "README.md",
    "config/decisions/current_decision_index.yaml",
    "config/decisions/decision_status.yaml",
    "config/decisions/document_authority.yaml",
    "config/bom/shellac_bom.yaml",
    "docs/knowledge/DESIGN_PACK_INDEX.md",
    "docs/maintenance/Signal_Chain_Commissioning_and_Maintenance_Baseline_Rev_A0.md",
    "docs/maintenance/Prototype_Commissioning_Acceptance_Matrix_Rev_A0.md",
    "docs/AE-023_Production_Signal_Chain_Assurance_Closure_Rev_A0.md",
    "docs/design_pack/AE-029_Production_Commissioning_and_Acceptance_Closure_Rev_A0.md",
    "generator/layout/sr043_native_board_audit.py",
    "generator/mechanical/sr040_audio_freeze.py",
)

HISTORICAL_GRAYHILL_ALLOW = (
    "docs/",
    "tests/",
)


def _path_exists(repo: Path, rel: str) -> bool:
    return (repo / rel).exists()


def _scan_live_grayhill(repo: Path):
    live = []
    roots = (
        repo / "config",
        repo / "generator",
        repo / "README.md",
    )
    for root in roots:
        paths = [root] if root.is_file() else root.rglob("*")
        for p in paths:
            if not p.is_file():
                continue
            if p.suffix.lower() not in {".py", ".yaml", ".yml", ".md", ".txt"} and p.name != "README.md":
                continue
            text = p.read_text(encoding="utf-8", errors="ignore")
            if "71BDF30" in text or "GRAYHILL" in text.upper():
                live.append(p.relative_to(repo).as_posix())
    return sorted(set(live))


def render(repo: Path):
    missing = [p for p in REQUIRED_PATHS if not _path_exists(repo, p)]
    grayhill = _scan_live_grayhill(repo)

    lines = [
        "# AE-030 Generated Production Readiness Audit",
        "",
        f"Repository: `{repo.resolve()}`",
        "",
        "## Executive status",
        "",
        f"- production gates: **{len(GATES)}**",
        f"- CLOSED: **{sum(g.state is GateState.CLOSED for g in GATES)}**",
        f"- READY_FOR_NEXT_ACTIVITY: **{sum(g.state is GateState.READY_FOR_NEXT_ACTIVITY for g in GATES)}**",
        f"- PROTOTYPE_EVIDENCE_REQUIRED: **{sum(g.state is GateState.PROTOTYPE_EVIDENCE_REQUIRED for g in GATES)}**",
        f"- BLOCKED: **{sum(g.state is GateState.BLOCKED for g in GATES)}**",
        f"- release blockers: **{sum(g.release_blocker for g in GATES)}**",
        "",
        "## Gate matrix",
        "",
        "| ID | Area | State | Release blocker | Evidence | Next action |",
        "|---|---|---|---|---|---|",
    ]
    for g in GATES:
        ev = g.evidence.replace("|", "\\|")
        nxt = g.next_action.replace("|", "\\|")
        lines.append(f"| {g.identifier} | {g.area} | **{g.state.value}** | {'YES' if g.release_blocker else 'NO'} | {ev} | {nxt} |")

    lines += ["", "## Required design-pack path check", ""]
    if missing:
        lines += [f"- MISSING: `{p}`" for p in missing]
    else:
        lines.append("- All AE-030 required authority/acceptance paths are present.")

    lines += ["", "## Live Grayhill references requiring ECO disposition", ""]
    if grayhill:
        lines += [f"- `{p}`" for p in grayhill]
    else:
        lines.append("- No live Grayhill references detected.")

    lines += [
        "",
        "## Recommended execution order",
        "",
        "1. Close Lorlin PT exact MPN and AE-028 mechanical sample gate.",
        "2. Perform control-hardware ECO: BOM + mechanical model + top-cover stack + footprints/placement.",
        "3. Confirm native KiCad board four-layer stack and plane intent.",
        "4. Route the native PCB under SR-041 critical-net/manual-routing rules.",
        "5. Run full DRC/ERC, return-path/plane review and fabrication-output inspection.",
        "6. Complete general BOM/procurement/lifecycle audit.",
        "7. Fabricate and commission representative hardware using AE-029.",
        "8. Freeze measured acceptance limits and complete maintenance/fault-isolation data.",
        "9. Assemble production design/release pack.",
        "10. Clean-clone reproducibility audit.",
        "11. Repository cleanup and tagged production release.",
        "12. Extract Foundry and Generator into independent versioned dependencies.",
        "",
        "## Interpretation",
        "",
        "The project is no longer primarily blocked by signal-chain design.",
        "The critical path is now controls/mechanics -> native routing/fabrication -> prototype evidence -> release/reproducibility.",
        "",
    ]
    return "\n".join(lines), missing, grayhill


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    repo = Path(args[0]).resolve() if args else Path.cwd().resolve()
    if not (repo / "generator").exists():
        print("ERROR: run from Shellac repository root", file=sys.stderr)
        return 2
    text, missing, grayhill = render(repo)
    out = repo / "docs/design_pack/AE-030_Generated_Production_Readiness_Audit.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(f"Wrote {out}")
    print(f"Missing required paths: {len(missing)}")
    print(f"Live Grayhill-reference files: {len(grayhill)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
