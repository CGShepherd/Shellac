from pathlib import Path
import yaml

CFG = Path("simulation/config/integrated_baseline.yaml")

def data():
    return yaml.safe_load(CFG.read_text(encoding="utf-8"))

def test_candidate_analysis_is_separate_from_live_generator():
    d = data()
    assert d["top_level"] == "SHELLAC_TOP"
    assert d["model_semantics"]["product_generator"] == "LIVE_IMPLEMENTATION"
    assert d["model_semantics"]["integrated_spice"] == "SELECTED_NEXT_CANDIDATE_ANALYSIS"
    assert d["model_semantics"]["generator_migration_implied"] is False

def test_nominal_shellac_rails_remain_plus_minus_18v():
    assert data()["nominal_rails_v"] == {"plus": 18.0, "minus": -18.0}

def test_sch101_candidate_contract_is_ae042():
    s = data()["selected_next_contract"]["sch101"]
    assert s["authority"] == "AE-042"
    assert s["gain_db"] == [14, 18, 22]
    assert s["no_shunt_state_db"] == 18
    assert s["converter_gain"] == 4.0

def test_dr039_selected_contract_is_ae067():
    s = data()["selected_next_contract"]["dr039_sch107"]
    assert s["authority"] == "AE-067"
    assert s["preferred_candidate"] == "BRANCH_LOCAL_DIRECT_BYPASS_BLOCK"
    assert s["selected_topology"] == "BRANCH_LOCAL_DIRECT_BYPASS_BLOCK"
    assert s["status"] == "CURRENT_SELECTED_PENDING_IMPLEMENTATION"
    assert s["generator_migration_implied"] is False
    assert s["direct_branch_c_f"] == 1.0e-6
    assert s["direct_branch_r_ohm"] == 330000
    assert s["filtered_branch_dc_blocking"] == "INTRINSIC_SCH107_HIGHPASS"

def test_mute_remains_mechanical_without_automatic_sequence():
    m = data()["selected_next_contract"]["mute"]
    assert m["type"] == "MECHANICAL_DPDT_INPUT_MUTE"
    assert m["mute_source"] == "ZERO_VA"
    assert m["automatic_sequencing"] is False

def test_model_source_gate_remains_closed_and_ae065_run00_is_claimed():
    r = data()["integrated_run00"]
    assert r["status"] == "PASSED_NOMINAL_SANITY"
    assert r["authority"] == "AE-065"
    assert r["existing_divider_run00_is_toolchain_only"] is True
    assert r["shellac_top_implemented"] is True
    assert r["shellac_top_run00_executed"] is True
    assert r["result_record"] == "simulation/results/run00_sanity/ae065_integrated_run00.json"


def test_run07_end_to_end_is_ae070_and_non_migrating():
    r = data()["run07_end_to_end"]
    assert r["authority"] == "AE-070"
    assert r["status"] == "QUALIFIED_NOMINAL_REPRESENTATIVE_STATES"
    assert r["generator_migration_implied"] is False
    assert r["ferrite_selected"] is False
    assert r["replay_and_nominal_symmetry_pass"] is True
    assert r["nominal_lr_tracking_semantics"] == "NOMINAL_MODEL_SYMMETRY_ONLY"
    assert r["tolerance_tracking_deferred_to"] == ["RUN10", "RUN11"]
    assert r["overload_qualified"] is False
    assert r["noise_qualified"] is False
