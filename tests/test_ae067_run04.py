from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]

def test_ae067_run04_evidence_and_selected_contract():
    result = json.loads(
        (ROOT / "simulation/results/run04_lf_trade/ae067_run04.json").read_text(encoding="utf-8")
    )
    assert result["authority"] == "AE-067"
    assert result["run_id"] == "RUN04"
    assert result["repository_commit_before_ae067"] == "c29bbadaff34ee8f05668701d5031994f9243a5a"
    assert result["generator_migration_implied"] is False
    assert result["status"] == "EVIDENCE_COMPLETE_REVIEW_REQUIRED"
    assert result["candidate_count"] == 4
    assert result["decision"]["automatic_topology_promotion"] is False
    assert result["decision"]["preferred_topology"] is None

    cases = result["candidates"]
    branch = cases["BRANCH_LOCAL_DIRECT_BYPASS_BLOCK"]
    post = cases["POST_SWITCH_COMMON"]
    current = cases["CURRENT_COMMON_PRE_SPLIT"]
    scale10 = cases["RUMBLE_SCALE10_COMMON_1P2UF"]

    assert branch["ac"]["lf_hard_pass"] is True
    assert branch["ac"]["lf_preferred_pass"] is True
    assert 15.0 <= branch["ac"]["filter_f3_hz"] <= 15.1
    assert branch["ac"]["direct_db_rel_1khz"]["20"] > -0.01
    assert branch["ac"]["filter_db_rel_1khz"]["20"] > -0.60
    assert branch["switch"]["internal_selector_objective_pass"] is True
    assert branch["switch"]["selector_peak_abs_v"] < 0.01
    assert 1.55 <= branch["offset_step"]["direct_settle_to_1pct_s_after_step"] <= 1.65

    assert post["ac"]["lf_hard_pass"] is True
    assert post["switch"]["internal_selector_objective_pass"] is False
    assert post["switch"]["selector_peak_abs_v"] > 0.24

    assert current["ac"]["lf_hard_pass"] is False
    assert current["ac"]["direct_db_rel_1khz"]["20"] < -1.0

    assert scale10["ac"]["lf_hard_pass"] is False
    assert scale10["noise"]["filter_delta_db_vs_branch_local"] > 0.75

    assert result["branch_local_filter_analytical_correlation"]["max_abs_error_db"] < 0.01

    baseline = yaml.safe_load(
        (ROOT / "simulation/config/integrated_baseline.yaml").read_text(encoding="utf-8")
    )
    contract = baseline["selected_next_contract"]["dr039_sch107"]
    assert contract["authority"] == "AE-067"
    assert contract["selected_topology"] == "BRANCH_LOCAL_DIRECT_BYPASS_BLOCK"
    assert contract["preferred_candidate"] == "BRANCH_LOCAL_DIRECT_BYPASS_BLOCK"
    assert contract["status"] == "CURRENT_SELECTED_PENDING_IMPLEMENTATION"
    assert contract["generator_migration_implied"] is False

    run04 = baseline["run04_lf_trade"]
    assert run04["authority"] == "AE-067"
    assert run04["status"] == "SELECTED_BRANCH_LOCAL_QUALIFICATION_OPEN"
    assert run04["selected_topology"] == "BRANCH_LOCAL_DIRECT_BYPASS_BLOCK"
    assert run04["generator_migration_implied"] is False
    assert run04["result_record"] == "simulation/results/run04_lf_trade/ae067_run04.json"
    assert set(run04["follow_on_qualification"]) == {"RUN09", "RUN10", "RUN12", "BENCH"}

def test_dr039_decision_index_promotes_selection_not_implementation():
    data = yaml.safe_load(
        (ROOT / "config/decisions/current_decision_index.yaml").read_text(encoding="utf-8")
    )
    dr039 = data["decisions"]["DR-039"]
    assert dr039["status"] == "CURRENT_SELECTED_PENDING_IMPLEMENTATION"
    assert dr039["primary_record"] == "docs/decisions/DR-039_Branch_Local_DC_Block_SELECTED.md"
    assert dr039["historical_record"] == "docs/decisions/DR-039_Common_Post_EQ_DC_Block_SELECTED.md"
    assert "AE-067_RUN04_DR039_SCH107_LF_Trade_Evidence_Rev_A0.md" in "\n".join(dr039["evidence"])
    impl = dr039["implementation"]
    assert "branch-local" in impl.lower()
    assert "not yet migrated" in impl.lower()
