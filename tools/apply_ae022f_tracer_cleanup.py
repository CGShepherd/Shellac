from pathlib import Path
p=Path("tools/trace_sch101_nets.py")
if p.exists():
    text=p.read_text(encoding="utf-8")
    marker='    targets=["0VA","PRE_EQ_L","PRE_EQ_R"]'
    if marker in text:
        start=text.find(marker)
        end=text.find("\n    for target in targets:",start)
        if end > start:
            text=text[:start]+marker+text[end:]
            p.write_text(text,encoding="utf-8")
print("Tracer simplified.")
