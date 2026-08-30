from pathlib import Path
import re
DR=re.compile(r"\b(DR-\d{3})\b",re.I); AE=re.compile(r"\b(AE-\d{3}[A-Z]?)\b",re.I); ST=re.compile(r"\b(PROPOSED|SELECTED|CLOSED|SUPERSEDED|REJECTED|OPEN|PENDING|IMPLEMENTED|BASELINE)\b",re.I)
def scan(repo):
 out=[]
 for p in repo.rglob("*.md"):
  if any(x in p.parts for x in (".git","out","generated")): continue
  t=p.read_text(encoding="utf-8",errors="ignore"); ids=sorted(set(x.upper() for x in DR.findall(t)+AE.findall(t)))
  if ids: out.append((p.relative_to(repo).as_posix(),ids,sorted(set(x.upper() for x in ST.findall(t)))))
 return out
def main():
 repo=Path.cwd(); rows=scan(repo); lines=["# AE-019 Generated Design Record Reconciliation","",f"Files audited: **{len(rows)}**","","| File | IDs | Status tokens |","|---|---|---|"]
 for p,ids,st in rows: lines.append(f"| `{p}` | {', '.join(ids)} | {', '.join(st) or 'NONE'} |")
 lines += ["","## Reconciliation gates","","- One authoritative current status per decision.","- Superseded decisions retained with explicit successor links.","- Assurance evidence identifies the baseline it analysed.","- Current design baseline separated from historical evidence.","- Commissioning and maintenance guidance traces to implemented hardware."]
 out=repo/"docs/AE-019_Generated_Design_Record_Reconciliation.md"; out.write_text("\n".join(lines),encoding="utf-8"); print(f"Wrote {out}; {len(rows)} files audited")
if __name__=="__main__": main()
