"""AE-031 generated pre-routing/control-geometry audit, current reconciliation AE-076D."""
from pathlib import Path
import sys
_REPO_ROOT=Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path: sys.path.insert(0,str(_REPO_ROOT))
from generator.model.prerouting_readiness import RULES,independent_rules,control_dependent_rules
PROVENANCE_GRAYHILL_ALLOW={'config/procurement/sourcing_snapshot_2026-08-24.yaml','generator/mechanical/control_hardware.py','generator/model/production_integrity_audit.py'}
def live_grayhill_files(repo):
 hits=[]
 for root in (repo/'config',repo/'generator',repo/'README.md'):
  ps=[root] if root.is_file() else root.rglob('*')
  for p in ps:
   if not p.is_file(): continue
   if p.suffix.lower() not in {'.py','.yaml','.yml','.md','.txt'} and p.name!='README.md': continue
   rel=p.relative_to(repo).as_posix()
   if rel in PROVENANCE_GRAYHILL_ALLOW: continue
   t=p.read_text(encoding='utf-8',errors='ignore')
   if '71BDF30' in t or 'GRAYHILL' in t.upper(): hits.append(rel)
 return sorted(set(hits))
def render(repo):
 hits=live_grayhill_files(repo)
 lines=['# AE-031 Generated Pre-Routing / Control-Geometry Audit','','**Current reconciliation:** AE-076D','',f'- unexpected live Grayhill-reference files: **{len(hits)}**',f'- routing rules independent of control geometry: **{len(independent_rules())}**',f'- routing rules gated by control geometry: **{len(control_dependent_rules())}**','','## Unexpected live Grayhill references','']
 lines += [f'- `{x}`' for x in hits] or ['- None. Historical/provenance references are excluded by explicit allow-list.']
 lines += ['','## Pre-routing rules','','| ID | Requirement | Control-geometry dependent? |','|---|---|---|']
 for r in RULES: lines.append(f"| {r.identifier} | {r.requirement} | {'YES' if r.control_dependent else 'NO'} |")
 lines += ['','## Disposition','','Analysis and non-binding placement preparation may continue.','Do not freeze control routing endpoints, exact B.Cu control footprints/keep-outs, top-cover apertures or the six-support stack until current AE071-B03 closes.','This audit does not grant routing authority; config/release/ae071_prerouting_hold.yaml remains the current fail-closed release authority.','']
 return '\n'.join(lines),hits
def main():
 text,hits=render(_REPO_ROOT); out=_REPO_ROOT/'docs/design_pack/AE-031_Generated_PreRouting_Control_Decoupling_Audit.md'; out.write_text(text,encoding='utf-8',newline='\n'); print(f'Wrote {out}'); print(f'Unexpected live Grayhill-reference files: {len(hits)}'); return 0 if not hits else 2
if __name__=='__main__': raise SystemExit(main())
