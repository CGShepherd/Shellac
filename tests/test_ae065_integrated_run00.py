from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]

def load_yaml(rel):
    return yaml.safe_load((ROOT / rel).read_text(encoding="utf-8"))

def test_ae065_integrated_model_and_runner_exist():
    model = ROOT / "simulation/models/integrated/shellac_top_ae065.lib"
    runner = ROOT / "simulation/scripts/ae065_integrated_run00.py"
    assert model.is_file()
    assert runner.is_file()
    text = model.read_text(encoding="utf-8")
    for token in (
        "SHELLAC_SCH101", "SHELLAC_SCH103_RIAA", "SHELLAC_DR039_SCH107",
        "SHELLAC_SCH104", "SHELLAC_SCH105_MATRIX_STEREO",
        "SHELLAC_SW905_RUN", "SHELLAC_SCH108",
    ):
        assert token in text

def test_ae065_result_is_genuine_integrated_pass():
    result = json.loads(
        (ROOT / "simulation/results/run00_sanity/ae065_integrated_run00.json").read_text(
            encoding="utf-8"
        )
    )
    assert result["authority"] == "AE-065"
    assert result["run_id"] == "RUN00_INTEGRATED"
    assert result["model"] == "SHELLAC_TOP"
    assert result["model_semantics"] == "SELECTED_NEXT_CANDIDATE_ANALYSIS"
    assert result["repository_commit_before_ae065"] == "e83eee5a16ac35ef81046f93e9b37ffd5ce83f3b"
    assert result["returncode"] == 0
    assert result["fatal_terms"] == []
    assert result["parse_error"] is None
    assert result["pass"] is True
    assert len(result["checks"]) == 9
    assert all(result["checks"].values())

def test_ae065_nominal_configuration_and_limits_are_preserved():
    result = json.loads(
        (ROOT / "simulation/results/run00_sanity/ae065_integrated_run00.json").read_text(
            encoding="utf-8"
        )
    )
    c = result["configuration"]
    assert c["cartridge"] == "GRADO_78C"
    assert c["gain"] == "DEFAULT_18DB"
    assert c["bass"] == "TRUE_RIAA"
    assert c["treble"] == "2121HZ_RIAA"
    assert c["rumble"] == "BYPASS"
    assert c["mode"] == "STEREO"
    assert c["mute"] == "RUN"
    assert c["rail_plus_v"] == 18.0
    assert c["rail_minus_v"] == -18.0
    assert c["lf_topology"] == "BRANCH_LOCAL_DIRECT_BYPASS_BLOCK"
    m = result["measurements_v"]
    for name in ("V_N101_L", "V_N103_L", "V_N104_L", "V_N105_L", "V_N108_L"):
        assert abs(m[name]) <= 1.0
    for name in ("V_XLR_L_DIFF", "V_XLR_R_DIFF"):
        assert abs(m[name]) <= 0.025
    for name in ("V_XLR_L_CM", "V_XLR_R_CM"):
        assert abs(m[name]) <= 0.250

def test_ae065_does_not_migrate_selected_next_or_close_later_risks():
    cfg = load_yaml("simulation/config/integrated_baseline.yaml")
    assert cfg["model_semantics"]["integrated_spice"] == "SELECTED_NEXT_CANDIDATE_ANALYSIS"
    assert cfg["model_semantics"]["generator_migration_implied"] is False
    risk = (ROOT / "docs/knowledge/RISK_REGISTER.md").read_text(encoding="utf-8")
    assert "| R-020 " in risk and "OPEN_SYSTEM_QUALIFICATION" in risk
    assert "| R-021 " in risk and "VERIFY_ON_BENCH" in risk
    assert "| R-024 " in risk and "OPEN_SYSTEM_QUALIFICATION" in risk
    assert "| R-026 " in risk and "MITIGATED_INTEGRATED_RUN00_BY_AE065" in risk
