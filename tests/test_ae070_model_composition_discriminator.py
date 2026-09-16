import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CFG = ROOT / "simulation/config/ae070_run07_end_to_end.yaml"
RESULT = ROOT / "simulation/results/run07_end_to_end/ae070_model_composition_discriminator.json"
RUN07 = ROOT / "simulation/results/run07_end_to_end/ae070_run07.json"
RUNNER = ROOT / "simulation/scripts/ae070_run07.py"


def test_ae070_composition_discriminator_is_controlled_and_reproducible():
    c = yaml.safe_load(CFG.read_text(encoding="utf-8"))
    d = c["run07_output_model"]["discriminator"]
    assert d["script"] == "simulation/scripts/ae070_model_composition_discriminator.py"
    assert d["result"] == "simulation/results/run07_end_to_end/ae070_model_composition_discriminator.json"
    assert d["qualification_semantics"] == "CONTROLLED_REPRODUCIBLE_MODEL_COMPOSITION_DIAGNOSTIC"
    assert d["expected"] == {
        "output_pair_only": "PASS",
        "dual_upstream_no_that": "PASS",
        "dual_full_ideal_output": "PASS",
        "dual_full_vendor_that": "TIMEOUT",
    }


def test_ae070_composition_discriminator_matches_expected_pattern():
    r = json.loads(RESULT.read_text(encoding="utf-8"))
    assert r["authority"] == "AE-070"
    assert r["run_id"] == "RUN07_MODEL_COMPOSITION_DISCRIMINATOR"
    assert r["status"] == "MODEL_COMPOSITION_LIMIT_CONFIRMED"
    assert r["pattern_match"] is True
    assert r["actual"] == r["expected"]
    assert len(r["cases"]) == 4


def test_run07_is_fail_closed_on_composition_discriminator():
    text = RUNNER.read_text(encoding="utf-8")
    assert "validate_model_composition_discriminator(cfg)" in text
    assert "COMPOSITION_RESULT" in text
    r = json.loads(RUN07.read_text(encoding="utf-8"))
    d = r["model_composition_discriminator"]
    assert d["status"] == "MODEL_COMPOSITION_LIMIT_CONFIRMED"
    assert d["pattern_match"] is True
