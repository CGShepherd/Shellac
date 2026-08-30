from pathlib import Path

p=Path("tools/apply_sr039_release_gate.py")
text=p.read_text(encoding="utf-8")

replacements = {
    'shutil.copyfile("config/release/sr039_schematic_to_layout.yaml","config/release/sr039_schematic_to_layout.yaml")\n': '',
    'shutil.copyfile("tests/test_sr039_schematic_to_layout_release.py","tests/test_sr039_schematic_to_layout_release.py")\n': '',
    'shutil.copyfile("docs/SR-039_Schematic_to_Layout_Release_Gate_Rev_A0.md","docs/SR-039_Schematic_to_Layout_Release_Gate_Rev_A0.md")\n': '',
}

changed=False
for old,new in replacements.items():
    if old in text:
        text=text.replace(old,new)
        changed=True

if not changed and "SameFileError" not in text:
    print("SR-039B: installer already appears fixed or differs from expected form.")
else:
    p.write_text(text,encoding="utf-8")
    print("SR-039B removed self-copy operations from SR-039 installer.")

print("SR-039B installer fix applied.")
