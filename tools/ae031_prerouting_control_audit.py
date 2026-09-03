"""AE-031 Grayhill decoupling and pre-routing audit."""
from pathlib import Path
import sys
_REPO_ROOT=Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0,str(_REPO_ROOT))

from generator.model.prerouting_readiness import RULES,independent_rules,control_dependent_rules

def live_grayhill_files(repo):
    roots=(repo/"config",repo/"generator",repo/"README.md")
    hits=[]
    for root in roots:
        ps=[root] if root.is_file() else root.rglob("*")
        for p in ps:
            if not p.is_file(): continue
            if p.suffix.lower() not in {".py",".yaml",".yml",".md",".txt"} and p.name!="README.md": continue
            text=p.read_text(encoding="utf-8",errors="ignore")
            if "71BDF30" in text or "GRAYHILL" in text.upper():
                hits.append(p.relative_to(repo).as_posix())
    return sorted(set(hits))

def main():
    repo=_REPO_ROOT
    hits=live_grayhill_files(repo)
    lines=[
        "# AE-031 Generated Pre-Routing / Control-Decoupling Audit","",
        f"- live Grayhill-reference files: **{len(hits)}**",
        f"- routing rules independent of rotary geometry: **{len(independent_rules())}**",
        f"- routing rules gated by rotary geometry: **{len(control_dependent_rules())}**","",
        "## Live Grayhill references","",
    ]
    lines += [f"- `{x}`" for x in hits] or ["- None."]
    lines += ["","## Pre-routing rules","",
        "| ID | Requirement | Rotary-geometry dependent? |",
        "|---|---|---|"]
    for r in RULES:
        lines.append(f"| {r.identifier} | {r.requirement} | {'YES' if r.control_dependent else 'NO'} |")
    lines += ["","## Disposition","",
        "Proceed now with all geometry-independent four-layer routing preparation.",
        "Do not freeze EQ-selector routing endpoints, rotary footprints, keep-outs or top-panel machining until AE-027/AE-028 closes.",
        "Historical Grayhill evidence may remain; current BOM/mechanical authority must migrate atomically during the later control-hardware ECO.",""]
    out=repo/"docs/design_pack/AE-031_Generated_PreRouting_Control_Decoupling_Audit.md"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text("\n".join(lines),encoding="utf-8")
    print(f"Wrote {out}")
    print(f"Live Grayhill-reference files: {len(hits)}")
    print(f"Geometry-independent routing rules: {len(independent_rules())}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
