from pathlib import Path
p=Path("config/decisions/current_decision_index.yaml")
t=p.read_text(encoding="utf-8")
t=t.replace("  branch: main\n","  branch: develop\n")
needle="authority: This file is the authoritative current decision-status index. Narrative records remain evidence/history.\n"
if "authority_scope:" not in t:
    t=t.replace(needle, needle+"authority_scope: Working design authority is develop until a tagged production baseline is promoted to main.\n")
p.write_text(t,encoding="utf-8")
print("Reconciled current decision-index working branch authority.")
