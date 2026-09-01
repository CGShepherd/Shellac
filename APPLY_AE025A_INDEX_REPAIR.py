from pathlib import Path

p = Path("config/decisions/current_decision_index.yaml")
t = p.read_text(encoding="utf-8")

t = t.replace("  branch: develop\n", "  branch: main\n")

lines = []
for line in t.splitlines():
    if line.startswith("authority_scope:"):
        continue
    lines.append(line)

p.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("Restored decision-index baseline semantics: branch=main; removed authority_scope.")
