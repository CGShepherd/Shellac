from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
WRITER = REPO / "generator/writers/kicad9.py"
TEST = REPO / "tests/test_clean_output.py"
NEW_FUNCTION = 'def clean_output(\n    out_dir,\n    *,\n    attempts=6,\n    initial_delay_s=0.20,\n    preserve_patterns=("*.kicad_pcb", "*.kicad_dru"),\n):\n    """Remove generator-owned output while preserving native PCB authority."""\n    out_dir = Path(out_dir)\n    if not out_dir.exists():\n        return\n\n    preserved = {}\n    for pattern in preserve_patterns:\n        for path in out_dir.glob(pattern):\n            if path.is_file():\n                preserved[path.name] = path.read_bytes()\n\n    last_error = None\n    for attempt in range(1, attempts + 1):\n        try:\n            shutil.rmtree(out_dir)\n            if preserved:\n                out_dir.mkdir(parents=True, exist_ok=True)\n                for name, payload in preserved.items():\n                    (out_dir / name).write_bytes(payload)\n            return\n        except PermissionError as error:\n            last_error = error\n            if attempt == attempts:\n                break\n            time.sleep(initial_delay_s * attempt)\n\n    raise PermissionError(\n        f"Could not clean generated output {out_dir!s} after {attempts} attempts. "\n        "Close KiCad or Explorer windows using the folder, allow Dropbox to finish "\n        "syncing, then rerun the build."\n    ) from last_error\n'
NEW_TESTS = '\n\ndef test_clean_output_preserves_native_pcb(tmp_path):\n    out_dir = tmp_path / "kicad"\n    out_dir.mkdir()\n    pcb = out_dir / "ProjectShellac.kicad_pcb"\n    pcb.write_text("(kicad_pcb native-authority-sentinel)", encoding="utf-8")\n    generated = out_dir / "ProjectShellac.kicad_sch"\n    generated.write_text("generated schematic", encoding="utf-8")\n    clean_output(out_dir)\n    assert pcb.read_text(encoding="utf-8") == "(kicad_pcb native-authority-sentinel)"\n    assert not generated.exists()\n\n\ndef test_clean_output_preserves_native_design_rules(tmp_path):\n    out_dir = tmp_path / "kicad"\n    out_dir.mkdir()\n    rules = out_dir / "ProjectShellac.kicad_dru"\n    rules.write_text("(rule native)", encoding="utf-8")\n    clean_output(out_dir)\n    assert rules.read_text(encoding="utf-8") == "(rule native)"\n'

def main():
    wt = WRITER.read_text(encoding="utf-8")
    if 'preserve_patterns=("*.kicad_pcb", "*.kicad_dru")' not in wt:
        s = wt.find("def clean_output(")
        e = wt.find("\ndef write_schematic(", s)
        if s < 0 or e < 0:
            raise SystemExit("Could not locate clean_output()")
        wt = wt[:s] + NEW_FUNCTION + "\n\n" + wt[e+1:]
        WRITER.write_text(wt, encoding="utf-8")

    tt = TEST.read_text(encoding="utf-8")
    if "def test_clean_output_preserves_native_pcb(" not in tt:
        TEST.write_text(tt.rstrip() + NEW_TESTS + "\n", encoding="utf-8")

    wt = WRITER.read_text(encoding="utf-8")
    tt = TEST.read_text(encoding="utf-8")
    assert 'preserve_patterns=("*.kicad_pcb", "*.kicad_dru")' in wt
    assert "def test_clean_output_preserves_native_pcb(" in tt
    assert "def test_clean_output_preserves_native_design_rules(" in tt
    print("AE-036B APPLIED AND VERIFIED")
    print("Expected targeted clean-output test count: 4")

if __name__ == "__main__":
    main()
