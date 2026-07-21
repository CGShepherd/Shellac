from pathlib import Path


def test_interconnect_report_bootstraps_project_root_before_generator_import():
    script = Path("scripts/report_interconnect_architecture.py").read_text(
        encoding="utf-8"
    )
    root_line = "PROJECT_ROOT = Path(__file__).resolve().parents[1]"
    path_line = "sys.path.insert(0, str(PROJECT_ROOT))"
    import_line = "from generator.layout.interconnect_architecture import"

    assert root_line in script
    assert path_line in script
    assert script.index(path_line) < script.index(import_line)


def test_interconnect_report_writes_relative_to_project_root():
    script = Path("scripts/report_interconnect_architecture.py").read_text(
        encoding="utf-8"
    )
    assert 'PROJECT_ROOT / "out/layout/interconnect_architecture.json"' in script
