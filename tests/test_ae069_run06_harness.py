import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_ae069_model_domains_and_bench_gates_are_explicit():
    runner = (ROOT / "simulation/scripts/ae069_run06.py").read_text(encoding="utf-8")
    config = (ROOT / "simulation/config/ae069_run06_output.yaml").read_text(encoding="utf-8")

    assert "OFFICIAL_MURATA_EXACT_TOPOLOGY_SMALL_SIGNAL_AC_EVIDENCE" in runner
    assert "diagnostic_transient_stability_case" in runner
    assert "transient_stability_reproducibly_qualified" in runner
    assert "bench_load_stability_required" in runner
    assert "run06_fully_qualified" in runner
    assert "simulation_evidence_complete" in runner

    assert "stability_model_limitation:" in config
    assert "TRANSIENT_SOLVER_NONREPRODUCIBILITY_CONFIRMED" in config
    assert "normal_threads_1: 0_of_3_completed" in config
    assert "alternate_threads_1: 0_of_3_completed" in config
    assert "headroom_input_rms_v: [0.321, 3.21, 5.0]" in config
    assert "ferrite_manufacturer_model_still_required: false" in config


def test_ae069_does_not_overclaim_large_signal_or_dynamic_thd():
    runner = (ROOT / "simulation/scripts/ae069_run06.py").read_text(encoding="utf-8")
    config = (ROOT / "simulation/config/ae069_run06_output.yaml").read_text(encoding="utf-8")

    assert "QUASI_STATIC_TRANSFER_DERIVED_HARMONIC_ESTIMATE" in runner
    assert "transient_large_signal_thd_qualified" in runner
    assert "bench_dynamic_thd_required" in runner
    assert "sine_case" not in runner
    assert ".four" not in runner

    assert "quasistatic_validated_input_rms_v_max: 5.0" in config
    assert "7.5 and" in config
    assert "9 Vrms" in config


def test_ae069_config_is_json_serializable_after_yaml_load():
    config_path = ROOT / "simulation/config/ae069_run06_output.yaml"
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    evidence_date = config["vendor_macro_limitation"]["evidence_date"]
    assert evidence_date == "2026-09-15"
    assert isinstance(evidence_date, str)
    json.dumps(config)


def test_ae069_renderer_has_no_transient_stability_overclaim():
    r=(ROOT / "simulation/scripts/ae069_run06.py").read_text(encoding="utf-8")
    assert "fast transient stability and quasi-static nonlinear transfer remain usable evidence domains" not in r
    assert "approximately +/-17.87 V differential output limit" not in r
    assert "Fast transient results are supportive diagnostic evidence where they converge, not a reproducible qualification gate." in r
    assert "wider exploratory sweeps are not used to infer the physical clipping limit" in r

def test_ae069_bench_gates_remain_open_after_ae070_advances_campaign_to_run08():
    baseline_path = ROOT / "simulation/config/integrated_baseline.yaml"
    baseline = yaml.safe_load(baseline_path.read_text(encoding="utf-8"))

    remaining = baseline["integrated_ac_campaign"]["remaining_runs"]
    assert "RUN06" not in remaining
    assert "RUN07" not in remaining
    assert remaining[0] == "RUN08"

    run06 = baseline["run06_output"]
    assert run06["authority"] == "AE-069"
    assert run06["status"] == "SIMULATION_EVIDENCE_COMPLETE_BENCH_GATES_OPEN"
    assert run06["transient_stability_reproducibly_qualified"] is False
    assert run06["bench_load_stability_required"] is True
    assert run06["dynamic_large_signal_thd_qualified"] is False
    assert run06["bench_dynamic_thd_required"] is True
    assert run06["ferrite_selected"] is False
    assert run06["sense_capacitor_mechanical_freeze"] is False
    assert run06["generator_migration_implied"] is False

    run07 = baseline["run07_end_to_end"]
    assert run07["authority"] == "AE-070"
    assert run07["status"] == "QUALIFIED_NOMINAL_REPRESENTATIVE_STATES"
    assert run07["generator_migration_implied"] is False
    assert run07["ferrite_selected"] is False
