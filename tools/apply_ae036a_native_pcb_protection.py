from __future__ import annotations
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
WRITER = REPO / "generator/writers/kicad9.py"
TEST = REPO / "tests/test_clean_output.py"

NEW_FUNCTION = 'def clean_output(\n    out_dir,\n    *,\n    attempts=6,\n    initial_delay_s=0.20,\n    preserve_patterns=("*.kicad_pcb", "*.kicad_dru"),\n):\n    """Remove generator-owned output while preserving native PCB authority.\n\n    The KiCad schematic generator and the editor-owned native PCB currently\n    share ``out/kicad``. Until those authorities are moved into separate\n    directories, a clean build must preserve native ``.kicad_pcb`` and\n    ``.kicad_dru`` files.\n\n    Windows Explorer, KiCad, antivirus and Dropbox can hold transient handles on\n    freshly generated files. Retry only PermissionError; all other failures are\n    surfaced immediately.\n    """\n    out_dir = Path(out_dir)\n    if not out_dir.exists():\n        return\n\n    preserved = {}\n    for pattern in preserve_patterns:\n        for path in out_dir.glob(pattern):\n            if path.is_file():\n                preserved[path.name] = path.read_bytes()\n\n    last_error = None\n    for attempt in range(1, attempts + 1):\n        try:\n            shutil.rmtree(out_dir)\n            if preserved:\n                out_dir.mkdir(parents=True, exist_ok=True)\n                for name, payload in preserved.items():\n                    (out_dir / name).write_bytes(payload)\n            return\n        except PermissionError as error:\n            last_error = error\n            if attempt == attempts:\n                break\n            time.sleep(initial_delay_s * attempt)\n\n    raise PermissionError(\n        f"Could not clean generated output {out_dir!s} after {attempts} attempts. "\n        "Close KiCad or Explorer windows using the folder, allow Dropbox to finish "\n        "syncing, then rerun the build."\n    ) from last_error\n'
NEW_TESTS = '\n\ndef test_clean_output_preserves_native_pcb(tmp_path):\n    out_dir = tmp_path / "kicad"\n    out_dir.mkdir()\n    pcb = out_dir / "ProjectShellac.kicad_pcb"\n    pcb.write_text("(kicad_pcb native-authority-sentinel)", encoding="utf-8")\n    generated = out_dir / "ProjectShellac.kicad_sch"\n    generated.write_text("generated schematic", encoding="utf-8")\n\n    clean_output(out_dir)\n\n    assert pcb.read_text(encoding="utf-8") == "(kicad_pcb native-authority-sentinel)"\n    assert not generated.exists()\n\n\ndef test_clean_output_preserves_native_design_rules(tmp_path):\n    out_dir = tmp_path / "kicad"\n    out_dir.mkdir()\n    rules = out_dir / "ProjectShellac.kicad_dru"\n    rules.write_text("(rule native)", encoding="utf-8")\n\n    clean_output(out_dir)\n\n    assert rules.read_text(encoding="utf-8") == "(rule native)"\n'

def replace_function(text: str) -> str:
    start = text.find("def clean_output(")
    end = text.find("\ndef write_schematic(", start)
    if start < 0 or end < 0:
        raise SystemExit("Could not locate clean_output/write_schematic boundaries; no changes made.")
    return text[:start] + NEW_FUNCTION + "\n\n" + text[end+1:]

def main():
    writer_text = WRITER.read_text(encoding="utf-8")
    if 'preserve_patterns=("*.kicad_pcb", "*.kicad_dru")' not in writer_text:
        WRITER.write_text(replace_function(writer_text), encoding="utf-8")
        print(f"Updated {WRITER}")
    else:
        print(f"{WRITER} already contains AE-036A protection.")

    test_text = TEST.read_text(encoding="utf-8")
    if "def test_clean_output_preserves_native_pcb(" not in test_text:
        TEST.write_text(test_text.rstrip() + NEW_TESTS + "\n", encoding="utf-8")
        print(f"Updated {TEST}")
    else:
        print(f"{TEST} already contains AE-036A regressions.")

    print("AE-036A applied. No manual source editing required.")

if __name__ == "__main__":
    main()
