from pathlib import Path

p=Path("tests/test_current_decision_index.py")
text=p.read_text(encoding="utf-8")

old = (
'def test_selected_pending_is_not_claimed_implemented():\n'
'    text=_text()\n'
'    assert re.search(r"(?m)^      converter_gain:\\s*4\\.0\\s*$", text)\n'
'    dr039 = text.split("  DR-039:", 1)[1].split("  DR-040:", 1)[0]\n'
'    assert "status: CURRENT_IMPLEMENTED" in dr039\n'
'    assert "SCH103 includes 1uF film / 330k DC block" in dr039\n'
)

new = (
'def test_dr038_dr039_are_claimed_as_implemented():\n'
'    text=_text()\n'
'    dr038 = text.split("  DR-038:", 1)[1].split("  DR-039:", 1)[0]\n'
'    assert "status: CURRENT_IMPLEMENTED" in dr038\n'
'    assert re.search(r"(?m)^      converter_gain:\\s*4\\.0\\s*$", dr038)\n'
'    assert "network: LT5400-7 A-grade" in dr038\n'
'    assert "pre-DR038 implementation" not in dr038\n'
'\n'
'    dr039 = text.split("  DR-039:", 1)[1].split("  DR-040:", 1)[0]\n'
'    assert "status: CURRENT_IMPLEMENTED" in dr039\n'
'    assert "SCH103 includes 1uF film / 330k DC block" in dr039\n'
)

if new in text:
    print("SR-039C test already updated.")
elif old in text:
    p.write_text(text.replace(old,new,1),encoding="utf-8")
    print("SR-039C migrated legacy decision-index regression.")
else:
    raise SystemExit("Expected legacy decision-index test not found.")

print("SR-039C applied.")
