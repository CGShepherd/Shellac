#!/usr/bin/env python
from __future__ import annotations
import json, subprocess
from pathlib import Path
from datetime import datetime, timezone
ROOT=Path.cwd()
ENV={".venv","__pycache__",".pytest_cache"}

def git(args):
    p=subprocess.run(["git",*args],cwd=ROOT,text=True,capture_output=True)
    return {"returncode":p.returncode,"stdout":p.stdout,"stderr":p.stderr}

def classify(p):
    rel=p.relative_to(ROOT).as_posix(); name=p.name
    if set(p.parts)&ENV: return "environment_or_cache"
    if name.startswith("payload_"): return "extracted_payload"
    if name.startswith("APPLY_") or name.startswith("delete_shellac_") or name=="README_APPLY.txt" or ".reconcile." in name or name.endswith((".zip",".patch")): return "transport_or_patch_artifact"
    if rel.startswith("simulation/generated/") or rel.startswith("simulation/logs/"): return "generated_simulation_artifact"
    return None

def main():
    if not (ROOT/".git").exists(): raise SystemExit("Run from Shellac repository root")
    tracked=set(git(["ls-files"])["stdout"].splitlines()); candidates=[]
    for p in ROOT.rglob("*"):
        cls=classify(p)
        if cls: candidates.append({"path":p.relative_to(ROOT).as_posix(),"type":cls,"is_dir":p.is_dir(),"tracked_by_git":p.relative_to(ROOT).as_posix() in tracked})
    report={"generated_utc":datetime.now(timezone.utc).isoformat(),"head":git(["rev-parse","HEAD"]),"branch":git(["branch","--show-current"]),"status":git(["status","--short"]),"upstream":git(["rev-parse","--abbrev-ref","--symbolic-full-name","@{u}"]),"diff_check":git(["diff","--check"]),"candidate_count":len(candidates),"candidates":candidates,"read_only":True}
    out=ROOT/"simulation"/"results"/"repository_hygiene"; out.mkdir(parents=True,exist_ok=True)
    (out/"repository_hygiene_audit.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    counts={}
    for c in candidates: counts[c["type"]]=counts.get(c["type"],0)+1
    lines=["Project Shellac repository hygiene audit",f"Generated: {report['generated_utc']}",f"Branch: {report['branch']['stdout'].strip()}",f"HEAD: {report['head']['stdout'].strip()}","","Candidate counts:"]+[f"  {k}: {v}" for k,v in sorted(counts.items())]+["","No files were removed.","","Candidates:"]+[f"  [{c['type']}] tracked={c['tracked_by_git']} {c['path']}" for c in candidates]
    (out/"repository_hygiene_audit.txt").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(out/"repository_hygiene_audit.txt"); print(out/"repository_hygiene_audit.json")
if __name__=="__main__": main()
