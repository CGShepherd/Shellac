from pathlib import Path

p=Path("tests/test_sr039_schematic_to_layout_release.py")
text=p.read_text(encoding="utf-8")

text=text.replace("import yaml\n","")

old = (
'def test_sr039_controlled_validation_evidence():\n'
'    data=yaml.safe_load(Path("config/release/sr039_schematic_to_layout.yaml").read_text(encoding="utf-8"))\n'
'    assert data["validation"]["pytest"] == {"passed":374,"failed":0}\n'
'    assert data["validation"]["native_kicad_erc"]["errors"] == 0\n'
'    assert data["validation"]["native_kicad_erc"]["warnings"] == 0\n'
)

new = (
'def test_sr039_controlled_validation_evidence():\n'
'    text=Path("config/release/sr039_schematic_to_layout.yaml").read_text(encoding="utf-8")\n'
'    assert "passed: 374" in text\n'
'    assert "failed: 0" in text\n'
'    assert "native_kicad_erc:" in text\n'
'    assert "errors: 0" in text\n'
'    assert "warnings: 0" in text\n'
'    assert "exit_code: 0" in text\n'
)

if new in text:
    print("SR-039A test already dependency-free.")
elif old in text:
    p.write_text(text.replace(old,new,1),encoding="utf-8")
    print("SR-039A removed PyYAML dependency from release-gate test.")
else:
    raise SystemExit("Expected SR-039 validation-evidence test not found.")

print("SR-039A hotfix applied.")
