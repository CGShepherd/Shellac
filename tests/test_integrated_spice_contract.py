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

def test_dr039_candidate_contract_is_ae052():
    s = data()["selected_next_contract"]["dr039_sch107"]
    assert s["authority"] == "AE-052"
    assert s["preferred_candidate"] == "BRANCH_LOCAL_DIRECT_BYPASS_BLOCK"
    assert s["direct_branch_c_f"] == 1.0e-6
    assert s["direct_branch_r_ohm"] == 330000

def test_mute_remains_mechanical_without_automatic_sequence():
    m = data()["selected_next_contract"]["mute"]
    assert m["type"] == "MECHANICAL_DPDT_INPUT_MUTE"
    assert m["mute_source"] == "ZERO_VA"
    assert m["automatic_sequencing"] is False

def test_existing_run00_is_explicitly_toolchain_only():
    r = data()["integrated_run00"]
    assert r["status"] == "BLOCKED_PENDING_MODEL_IMPLEMENTATION"
    assert r["existing_divider_run00_is_toolchain_only"] is True
