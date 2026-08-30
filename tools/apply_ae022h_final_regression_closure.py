from pathlib import Path

p=Path("tests/test_balanced_input.py")
text=p.read_text(encoding="utf-8")
old = (
'    for name in (\n'
'        "INPUT_L_POS", "INPUT_L_NEG", "PRE_EQ_L",\n'
'        "INPUT_R_POS", "INPUT_R_NEG", "PRE_EQ_R",\n'
'    ):\n'
'        assert labels.count(name) == 1\n'
)
new = (
'    for name in (\n'
'        "INPUT_L_POS", "INPUT_L_NEG",\n'
'        "INPUT_R_POS", "INPUT_R_NEG",\n'
'    ):\n'
'        assert labels.count(name) == 1\n'
'\n'
'    # DR-038 uses PRE_EQ_L/R as the local feedback/output net name and the\n'
'    # exported sheet interface, so each must appear exactly twice.\n'
'    assert labels.count("PRE_EQ_L") == 2\n'
'    assert labels.count("PRE_EQ_R") == 2\n'
)
if old in text:
    text=text.replace(old,new,1)
    p.write_text(text,encoding="utf-8")
    print("Balanced-input PRE_EQ label contract migrated.")
elif new in text:
    print("Balanced-input PRE_EQ label contract already migrated.")
else:
    raise SystemExit("Expected balanced-input label-count assertion not found.")

p=Path("tests/test_erc_branch_routing.py")
text=p.read_text(encoding="utf-8")
old = (
'    labels={(x.name,x.x,x.y) for x in sheet.labels}\n'
'    for rn_ref in ("RN130","RN230"):\n'
'        rn=c[rn_ref]\n'
'        ref=pin_position(rn,"5")\n'
'        assert any(name=="0VA" and x==ref.x for name,x,y in labels)\n'
'        assert pin_position(rn,"9") in sheet.no_connects\n'
)
new = (
'    labels={(x.name,x.x,x.y) for x in sheet.labels}\n'
'    for rn_ref in ("RN130","RN230"):\n'
'        rn=c[rn_ref]\n'
'        ref=pin_position(rn,"5")\n'
'        matching=[(x,y) for name,x,y in labels if name=="0VA" and y==ref.y and x>ref.x]\n'
'        assert matching\n'
'        assert all(x != ref.x for x,y in matching)\n'
'        assert pin_position(rn,"9") in sheet.no_connects\n'
)
if old in text:
    text=text.replace(old,new,1)
    p.write_text(text,encoding="utf-8")
    print("LT5400 pin-5 safety regression migrated.")
elif new in text:
    print("LT5400 pin-5 safety regression already migrated.")
else:
    raise SystemExit("Expected LT5400 pin-5 safety assertion not found.")

print("AE-022H final regression closure applied.")
