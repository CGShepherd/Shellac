from pathlib import Path

from simulation.scripts.analytical_correlation import build_report
from simulation.scripts.ltspice_correlation import (
    SIM,
    _analytical_value,
    load_yaml,
    prepare_case,
)


def test_ltspice_correlation_config_covers_ae055_cases():
    cfg = load_yaml(SIM / "config" / "correlation_ltspice.yaml")
    assert set(cfg["cases"]) == {
        "dr039_direct_rc",
        "sch101_nominal_gain",
        "matrix_left_only",
        "matrix_right_only",
        "matrix_equal",
        "matrix_opposite",
    }


def test_analytical_mapping_for_direct_rc_20hz():
    analytical = build_report()
    spec = {"analytical_checkpoint_hz": 20.0}
    value = _analytical_value(spec, analytical)
    assert -0.003 < value < -0.002


def test_analytical_mapping_for_matrix_equal():
    analytical = build_report()
    spec = {"analytical_stimulus": "equal"}
    assert _analytical_value(spec, analytical) == 1.0


def test_correlation_templates_render_without_placeholders(tmp_path, monkeypatch):
    cfg = load_yaml(SIM / "config" / "correlation_ltspice.yaml")
    for case_id, spec in cfg["cases"].items():
        path = prepare_case(case_id, spec)
        text = path.read_text(encoding="utf-8")
        assert "{{" not in text


def test_matrix_fixture_is_unloaded_ideal_average():
    template = (SIM / "runs" / "correlation" / "matrix_mono_average.cir.in").read_text(
        encoding="utf-8"
    )
    assert "RLOAD" not in template
    assert "RL L AVG {R_SUM}" in template
    assert "RR R AVG {R_SUM}" in template


def test_dr039_cutoff_sweep_has_numerical_resolution_margin():
    template = (SIM / "runs" / "correlation" / "dr039_direct_rc.cir.in").read_text(
        encoding="utf-8"
    )
    assert ".ac dec 2000 0.05 200" in template
