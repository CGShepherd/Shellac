from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]
CFG = ROOT / "simulation/config/ae070_run07_end_to_end.yaml"
RESULT = ROOT / "simulation/results/run07_end_to_end/ae070_run07.json"
RECORD = ROOT / "docs/design_pack/AE-070_RUN07_End_to_End_Nominal_Chain_Evidence_Rev_A0.md"


def config():
    return yaml.safe_load(CFG.read_text(encoding="utf-8"))


def result():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_ae070_scope_covers_controlled_run07_dimensions_without_overload():
    c = config()
    roles = {x["role"] for x in c["cases"]}
    assert {
        "REPRESENTATIVE_78_NOMINAL",
        "REPRESENTATIVE_RUMBLE_IN",
        "REPRESENTATIVE_78_ALTERNATE_EQ",
        "RIAA_COMPATIBILITY",
        "REPRESENTATIVE_MONO",
    } <= roles
    assert {x["rumble"] for x in c["cases"]} == {"BYPASS", "FILTER"}
    assert {x["mode"] for x in c["cases"]} == {"STEREO", "MONO"}
    assert c["decision_policy"]["overload_deferred_to"] == "RUN08"
    assert c["decision_policy"]["ferrite_selection_automatic"] is False
    assert c["generator_migration_implied"] is False


def test_ae070_runner_assembles_qualified_block_libraries_not_ae065_run00_model():
    text = (ROOT / "simulation/scripts/ae070_run07.py").read_text(encoding="utf-8")
    for token in (
        "sch101_sch103_ae066.lib",
        "dr039_sch107_ae067.lib",
        "sch104_sch105_ae068.lib",
        "sch108_ae070_ac_surrogate.lib",
    ):
        assert token in text
    assert "shellac_top_ae065.lib" not in text
    assert "AE067_BRANCH_LOCAL" in text
    assert "AE068_MATRIX_STEREO" in text
    assert "AE068_MATRIX_MONO" in text
    assert "AE070_SCH108_AC_SURROGATE" in text
    assert "AE069_SCH108" not in text
    assert 'resolve_source("THAT1646"' not in text


def test_ae070_structured_result_and_gates():
    r = result()
    assert r["authority"] == "AE-070"
    assert r["run_id"] == "RUN07"
    assert r["repository_commit_before_ae070"] == "2f1446881db130f91dbc7820f61a5887abe1ee97"
    assert r["generator_migration_implied"] is False
    assert r["case_count"] == 10
    assert r["gates"]["replay_and_tracking_pass"] is True
    assert r["gates"]["rumble_pass"] is True
    assert r["gates"]["mono_pass"] is True
    assert r["gates"]["run07_nominal_ac_pass"] is True
    assert r["gates"]["ferrite_selected"] is False
    assert r["gates"]["overload_qualified"] is False
    assert r["gates"]["noise_qualified"] is False
    assert r["gates"]["bench_correlation_required"] is True
    assert r["output_model_correlation"]["source_authority"] == "AE-069"
    assert r["output_model_correlation"]["pass"] is True
    assert r["output_model_correlation"]["worst_delta_or_vendor_shape_db"] <= 0.005


def test_ae070_record_preserves_boundaries():
    text = RECORD.read_text(encoding="utf-8")
    assert "RUN07 NOMINAL AC QUALIFIED" in text
    assert "AE-070 does not select a ferrite" in text
    assert "qualification-only small-signal AC surrogate correlated to AE-069" in text
    assert "cannot support DC, CM, stability, distortion, overload, switching or fault claims" in text
    assert "RUN08 first-clipping/headroom/recovery" in text
    assert "still-open RUN06 load-stability and dynamic-THD gates" in text
