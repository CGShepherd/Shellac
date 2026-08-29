from pathlib import Path
from tools.ae017_dependency_map import scan, render


def test_dependency_mapper_finds_known_contracts(tmp_path):
    (tmp_path / "generator/model").mkdir(parents=True)
    (tmp_path / "tests").mkdir()
    (tmp_path / "generator/model/x.py").write_text(
        "DIFF_CONVERTER_GAIN = 3.48\nGAIN_RG_OHM = 10000\n",
        encoding="utf-8",
    )
    (tmp_path / "tests/test_x.py").write_text(
        'assert "SW1011"\nassert "R112"\n',
        encoding="utf-8",
    )
    hits = scan(tmp_path)
    tokens = {h.token for h in hits}
    assert "DIFF_CONVERTER_GAIN" in tokens
    assert "3.48" in tokens
    assert "SW1011" in tokens
    assert "R112" in tokens


def test_render_contains_atomic_gates(tmp_path):
    (tmp_path / "generator/model").mkdir(parents=True)
    (tmp_path / "tests").mkdir()
    hits = []
    text = render(tmp_path, hits)
    assert "DR-038 / SCH101" in text
    assert "DR-039 / SCH103" in text
    assert "power-up/power-down transient acceptance" in text
