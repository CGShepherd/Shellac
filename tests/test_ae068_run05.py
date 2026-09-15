from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]

def result():
    return json.loads(
        (ROOT / "simulation/results/run05_matrix/ae068_run05.json").read_text(encoding="utf-8")
    )

def baseline():
    return yaml.safe_load(
        (ROOT / "simulation/config/integrated_baseline.yaml").read_text(encoding="utf-8")
    )

def test_ae068_run05_identity_and_primary_gates():
    r = result()
    assert r["authority"] == "AE-068"
    assert r["run_id"] == "RUN05"
    assert r["repository_commit_before_ae068"] == "69ecf0118d2ff733247f9468e620a05b606c3eff"
    assert r["generator_migration_implied"] is False
    assert r["direct_insertion"]["pass"] is True
    assert r["direct_insertion"]["worst_abs_insertion_db"] < 0.001
    assert r["mono_nominal"]["hard_pass"] is True
    assert r["mono_nominal"]["preferred_pass"] is True
    assert abs(r["mono_nominal"]["equal_insertion_db_1khz"]["left"]) < 0.02
    assert abs(r["mono_nominal"]["weight_mismatch_percent_1khz"]) < 1e-6
    assert r["stereo_crosstalk"]["hard_pass"] is True
    assert r["stereo_crosstalk"]["preferred_1khz_pass"] is True
    assert r["stereo_crosstalk"]["qualification_worst_separation_db_1khz"] > 98.0
    assert r["stereo_crosstalk"]["qualification_worst_separation_db_20khz"] > 71.9

def test_ae068_parasitic_return_and_pair_match_evidence():
    r = result()
    ps = r["stereo_crosstalk"]["parasitic_sweep_pf"]
    assert ps["10.0"]["l_to_r_separation_db"]["20000"] > 60.0
    assert ps["10.0"]["r_to_l_separation_db"]["20000"] > 60.0

    rs = r["return_resistor_sweep"]
    assert rs["470000"]["mono_equal_insertion_db_1khz"] < -0.08
    assert rs["1000000"]["mono_equal_insertion_db_1khz"] > -0.05
    assert -0.020 < rs["2200000"]["mono_equal_insertion_db_1khz"] < -0.017
    assert rs["4700000"]["mono_equal_insertion_db_1khz"] > -0.01

    mm = r["mono_pair_mismatch_sweep"]
    assert mm["0.1"]["weight_mismatch_percent_1khz"] <= 0.100001
    assert mm["0.25"]["pass_max_0p25_percent"] is True
    assert mm["0.5"]["pass_max_0p25_percent"] is False

def test_ae068_integrated_contract_retains_open_follow_on_work():
    b = baseline()
    run05 = b["run05_matrix"]
    assert run05["authority"] == "AE-068"
    assert run05["status"] == "QUALIFIED_STEADY_STATE_TRANSIENT_OPEN"
    assert run05["architecture"] == "AE041_A1_3P4T_PASSIVE_MATRIX"
    assert run05["input_return_ohm"] == 2200000
    assert run05["mono_resistor_ohm"] == 4700
    assert run05["mono_resistor_current_tolerance_percent"] == 0.1
    assert run05["derived_pair_match_percent_preferred_for_run10"] == 0.10
    assert run05["derived_pair_match_percent_max_for_run10"] == 0.25
    assert run05["tolerance_relaxation_authorised"] is False
    assert run05["switch_parasitic_qualification_pf"] == 5.0
    assert run05["generator_migration_implied"] is False
    assert set(run05["follow_on_qualification"]) == {"RUN09", "RUN10", "RUN12", "BENCH"}
    # AE-068 owns closure of RUN05. Do not freeze the later campaign
    # pointer here; subsequent assurance records legitimately advance it.
    assert "RUN05" not in b["integrated_ac_campaign"]["remaining_runs"]

def test_ae041_remains_qualification_open_after_run05():
    idx = yaml.safe_load(
        (ROOT / "config/decisions/current_decision_index.yaml").read_text(encoding="utf-8")
    )
    a = idx["decisions"]["AE-041-A1"]
    assert a["status"] == "CURRENT_ARCHITECTURE_QUALIFICATION_OPEN"
    assert any("AE-068_RUN05_SCH104_SCH105_Matrix_Evidence_Rev_A0.md" in x for x in a["evidence"])
    assert "RUN12" in a["implementation"]["note"]
    ae041 = (ROOT / "docs/design_pack/AE-041_3P4T_Matrix_and_Top_Cover_Control_Authority_Rev_A1.md").read_text(encoding="utf-8")
    assert "Two 4.7 kOhm, 0.1% averaging resistors" in ae041
    ae068 = (ROOT / "docs/design_pack/AE-068_RUN05_SCH104_SCH105_Matrix_Evidence_Rev_A0.md").read_text(encoding="utf-8")
    assert "AE-068 does not authorise a BOM tolerance relaxation" in ae068
