from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]

def y(rel):
    return yaml.safe_load((ROOT / rel).read_text(encoding="utf-8"))

def j(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

def test_ae066_campaign_contract_does_not_migrate_generator():
    cfg = y("simulation/config/ae066_ac_campaign.yaml")
    assert cfg["authority"] == "AE-066"
    assert cfg["model_semantics"] == "SELECTED_NEXT_CANDIDATE_ANALYSIS"
    assert cfg["generator_migration_implied"] is False
    assert cfg["nominal_rails_v"] == {"plus": 18.0, "minus": -18.0}

def test_ae066_run01_matrix_and_predeclared_policy():
    r = j("simulation/results/run01_input_loading/ae066_run01.json")
    assert r["case_count"] == 45
    assert r["hard_gate_pass"] is True
    assert r["at_official_envelope_gating_case_count"] > 0
    assert r["at_official_envelope_all_pass"] is True
    assert r["grado_nominal_100pf_base_audio20_pass"] is True

def test_ae066_run02_nominal_gain_cmrr_passes():
    r = j("simulation/results/run02_gain_cmrr/ae066_run02.json")
    assert r["case_count"] == 3
    assert r["pass"] is True
    assert {c["gain"] for c in r["cases"]} == {"LOW", "DEFAULT", "HIGH"}

def test_ae066_run03_all_25_states_pass_nominal():
    r = j("simulation/results/run03_eq/ae066_run03.json")
    assert r["state_count"] == 25
    assert r["pass"] is True
    assert all(s["pass"] for s in r["states"])
    assert any(s["target_kind"] == "RIAA" for s in r["states"])
    assert any(s["target_kind"] == "UNNAMED_ADJUSTMENT" for s in r["states"])

def test_ae066_summary_preserves_later_open_work():
    r = j("simulation/results/ae066_summary.json")
    assert r["hard_gate_pass"] is True
    assert r["model_semantics"] == "SELECTED_NEXT_CANDIDATE_ANALYSIS"
    assert r["generator_migration_implied"] is False
    assert "RUN04" in r["remaining_runs"] and "RUN14" in r["remaining_runs"]

def test_ae066_forward_model_candidates_are_external_and_not_frozen():
    c = y("simulation/config/run04_run06_model_candidates.yaml")
    beads = c["sch108_output_ferrite"]["candidates"]
    assert {x["mpn"] for x in beads} == {"BLM21PG600SN1D", "BLM21PG221SN1D"}
    assert c["that1646_sense_capacitor"]["preferred_candidate"]["mpn"] == "ECEA1VN100U"
    assert "NOT_FROZEN" in c["that1646_sense_capacitor"]["preferred_candidate"]["status"]
    assert "OPEN" in c["eq_rotary"]["current_authority"]

def test_ae066_service_loading_is_on_post_100r_input_nodes():
    text = (ROOT / "simulation/models/qualification/sch101_sch103_ae066.lib").read_text(encoding="utf-8")
    assert "CDIFFLOAD INP_F INM_F {CDIFF}" in text
    assert "PARAMS: RFPROG=1T RGPROG=1T CDIFF=1e-18" in text

def test_ae066_controlled_summary_does_not_capture_absolute_user_paths():
    text = (ROOT / "simulation/results/ae066_summary.json").read_text(encoding="utf-8")
    assert "C:\\\\Users\\\\" not in text
    assert "/Users/" not in text

def test_ae066_run04_passive_source_prep_respects_affordable_performance_policy():
    c = y("simulation/config/run04_run06_model_candidates.yaml")
    p = c["dr039_sch107_passive_candidates"]
    assert p["direct_branch_dc_block"]["capacitor_family_candidate"]["series"] == "MKS_2"
    rumble = p["rumble_filter_timing_capacitors"]
    assert rumble["capacitor_family_candidate"]["capacitance_nf"] == 470
    assert "HAND_MATCH" in rumble["capacitor_family_candidate"]["status"]
    assert "Do not pay automatically" in rumble["selection_policy"]

def test_ae066_sch103_timing_source_feasibility_is_recorded_without_migration():
    c = y("simulation/config/run04_run06_model_candidates.yaml")
    s = c["sch103_timing_capacitor_source_feasibility"]
    verified = {x["value_nf"]: x for x in s["verified_current_candidates"]}
    assert verified[100]["tolerance_percent"] == 1
    assert verified[68]["package"] == 1206
    v = s["value_engineering_candidates"]["treble_1600"]
    assert v["current_parts_nf"] == [120.0, 12.0]
    assert v["candidate_parts_nf"] == [100.0, 33.0]
    assert v["candidate_nominal_pole_hz"] < 1600 < v["current_nominal_pole_hz"]
    assert v["status"] == "RUN10_VALUE_ENGINEERING_CANDIDATE_NOT_AUTHORITY"
