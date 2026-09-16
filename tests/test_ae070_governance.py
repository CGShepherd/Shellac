from pathlib import Path
import json
import yaml

ROOT = Path(".")


def test_ae070_governance_chain_and_results():
    baseline = yaml.safe_load((ROOT / "simulation/config/integrated_baseline.yaml").read_text(encoding="utf-8"))
    r = baseline["run07_end_to_end"]
    assert r["authority"] == "AE-070"
    assert r["generator_migration_implied"] is False
    assert r["ferrite_selected"] is False

    result = json.loads((ROOT / r["result_record"]).read_text(encoding="utf-8"))
    phase = json.loads((ROOT / r["phase_correlation_record"]).read_text(encoding="utf-8"))
    comp = json.loads((ROOT / r["model_composition_discriminator_record"]).read_text(encoding="utf-8"))
    assert result["status"] == "QUALIFIED_NOMINAL_REPRESENTATIVE_STATES"
    assert result["gates"]["run07_nominal_ac_pass"] is True
    assert phase["acceptance"]["pass"] is True
    assert comp["status"] == "MODEL_COMPOSITION_LIMIT_CONFIRMED"
    assert comp["pattern_match"] is True


def test_ae070_is_indexed_and_risk_state_advances_to_run08():
    record = "docs/design_pack/AE-070_RUN07_End_to_End_Nominal_Chain_Evidence_Rev_A0.md"
    assert record in (ROOT / "config/decisions/document_authority.yaml").read_text(encoding="utf-8")
    assert "AE-070: " + record in (ROOT / "config/decisions/current_decision_index.yaml").read_text(encoding="utf-8")
    risks = (ROOT / "docs/knowledge/RISK_REGISTER.md").read_text(encoding="utf-8")
    assert "AE-070 qualifies RUN07" in risks
    assert "RUN08-RUN14" in risks
