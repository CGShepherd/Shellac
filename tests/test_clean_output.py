from unittest.mock import patch

import pytest

from generator.writers.kicad9 import clean_output


def test_clean_output_retries_transient_permission_error(tmp_path):
    out_dir = tmp_path / "kicad"
    out_dir.mkdir()

    with (
        patch(
            "generator.writers.kicad9.shutil.rmtree",
            side_effect=[PermissionError(), None],
        ) as remove,
        patch("generator.writers.kicad9.time.sleep") as sleep,
    ):
        clean_output(out_dir, attempts=3, initial_delay_s=0.01)

    assert remove.call_count == 2
    sleep.assert_called_once_with(0.01)


def test_clean_output_gives_actionable_error_after_retries(tmp_path):
    out_dir = tmp_path / "kicad"
    out_dir.mkdir()

    with (
        patch("generator.writers.kicad9.shutil.rmtree", side_effect=PermissionError()),
        patch("generator.writers.kicad9.time.sleep"),
    ):
        with pytest.raises(PermissionError, match="Close KiCad or Explorer"):
            clean_output(out_dir, attempts=2, initial_delay_s=0)

def test_clean_output_preserves_native_pcb(tmp_path):
    out_dir = tmp_path / "kicad"
    out_dir.mkdir()
    pcb = out_dir / "ProjectShellac.kicad_pcb"
    pcb.write_text("(kicad_pcb native-authority-sentinel)", encoding="utf-8")
    generated = out_dir / "ProjectShellac.kicad_sch"
    generated.write_text("generated schematic", encoding="utf-8")
    clean_output(out_dir)
    assert pcb.read_text(encoding="utf-8") == "(kicad_pcb native-authority-sentinel)"
    assert not generated.exists()


def test_clean_output_preserves_native_design_rules(tmp_path):
    out_dir = tmp_path / "kicad"
    out_dir.mkdir()
    rules = out_dir / "ProjectShellac.kicad_dru"
    rules.write_text("(rule native)", encoding="utf-8")
    clean_output(out_dir)
    assert rules.read_text(encoding="utf-8") == "(rule native)"

