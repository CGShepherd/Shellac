from pathlib import Path
from generator.model.bom_cost import summarise, validate_ledger

def test_cost_ledger_contract():
    validate_ledger()

def test_unknown_costs_are_not_counted_as_zero_confidence_priced_lines():
    s = summarise()
    assert s.total_lines >= 4
    assert s.unpriced_lines >= 1
    assert 0 <= s.confidence_pct <= 100

def test_prototype_sample_cost_is_not_product_bom():
    import yaml
    data = yaml.safe_load(Path("config/bom/shellac_cost_ledger.yaml").read_text(encoding="utf-8"))
    assert any(x["id"] == "NRE-PT-SAMPLES" for x in data["nre"])
    assert all(x["id"] != "NRE-PT-SAMPLES" for x in data["items"])
