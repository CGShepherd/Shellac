from pathlib import Path
p=Path("tools/ae024_design_record_audit.py")
t=p.read_text(encoding="utf-8")
t=t.replace(
'    allowed = set(status_doc.get("allowed_status", []))\n    index_vocab = set(index_doc.get("status_vocabulary", []))\n',
'    allowed = set(status_doc.get("authoritative_current_status", status_doc.get("allowed_status", [])))\n    index_vocab = set(index_doc.get("status_vocabulary", []))\n'
)
if "def current_authority_paths(" not in t:
    marker="def contradictory_claims(repo: Path, claims):\n"
    helper='''def current_authority_paths(repo: Path):
    path = repo / "config/decisions/document_authority.yaml"
    if not path.exists():
        return set()
    paths=set(); active=False
    for raw in path.read_text(encoding="utf-8").splitlines():
        line=raw.split("#",1)[0].rstrip()
        if line=="current_authority:":
            active=True; continue
        if active:
            s=line.strip()
            if s.startswith("- "):
                paths.add(s[2:].strip()); continue
            if s and not line.startswith(" "):
                break
    return paths

'''
    t=t.replace(marker,helper+marker)
t=t.replace(
'    authoritative = authoritative_decisions(repo)\n    findings = []\n',
'    authoritative = authoritative_decisions(repo)\n    authority_paths = current_authority_paths(repo)\n    findings = []\n',
1
)
t=t.replace(
'        for c in claims:\n            if decision not in c.ids or not c.statuses:\n                continue\n',
'        for c in claims:\n            if authority_paths and c.path not in authority_paths:\n                continue\n            if decision not in c.ids or not c.statuses:\n                continue\n'
)
p.write_text(t,encoding="utf-8")
print("Updated AE-024 audit for scoped status vocabulary and authority-aware contradictions.")
