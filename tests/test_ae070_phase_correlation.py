import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CFG = ROOT / "simulation/config/ae070_run07_end_to_end.yaml"
RESULT = ROOT / "simulation/results/run07_end_to_end/ae070_output_phase_correlation.json"
RECORD = ROOT / "docs/design_pack/AE-070_RUN07_End_to_End_Nominal_Chain_Evidence_Rev_A0.md"


def test_ae070_phase_correlation_configuration_is_explicit():
    c = yaml.safe_load(CFG.read_text(encoding="utf-8"))
    p = c["run07_output_model"]["phase_correlation"]
    assert p["required_before_governance"] is True
    assert p["frequencies_hz"] == [20, 1000, 20000]
    assert p["max_abs_delta_deg"] == 1.0
    assert p["result"] == "simulation/results/run07_end_to_end/ae070_output_phase_correlation.json"


def test_ae070_output_phase_correlation_result_passes():
    r = json.loads(RESULT.read_text(encoding="utf-8"))
    assert r["authority"] == "AE-070"
    assert r["run_id"] == "RUN07_PHASE_CORRELATION"
    assert r["acceptance"]["pass"] is True
    assert r["acceptance"]["worst_abs_delta_deg"] <= r["acceptance"]["max_abs_delta_deg"]
    assert len(r["rows"]) == 6
    assert {x["frequency_hz"] for x in r["rows"]} == {20, 1000, 20000}
    assert {x["ferrite_bracket"] for x in r["rows"]} == {
        "LOW_60OHM_100MHZ", "HIGH_220OHM_100MHZ"
    }


def test_ae070_record_does_not_overclaim_tracking_or_surrogate_phase():
    text = RECORD.read_text(encoding="utf-8")
    assert "nominal model symmetry" in text
    assert "tolerance tracking remains RUN10/RUN11 work" in text
    assert "output-stage phase contribution" in text
    assert "ae070_output_phase_correlation.json" in text
