from generator.model.bom_cost import category_subtotals,summarise,validate_ledger
from generator.model.prerouting_readiness import (
    control_dependent_rules,independent_rules,validate_prerouting_contract
)

def test_ae031_cost_snapshot():
    validate_ledger()
    s=summarise()
    assert s.quoted_design_gbp == 233.67
    assert s.priced_lines == 4
    assert s.total_lines == 5
    assert round(s.confidence_pct,1) == 80.0

def test_enclosures_dominate_current_verified_subtotal():
    cats=category_subtotals()
    assert cats["enclosure_mechanics"] == 187.10
    assert cats["enclosure_mechanics"] > cats["controls"]

def test_prerouting_contract():
    validate_prerouting_contract()
    assert len(independent_rules()) > len(control_dependent_rules())

def test_rotary_geometry_does_not_block_all_routing_preparation():
    assert all(not r.control_dependent for r in independent_rules())
    assert any(r.identifier=="ROTARY-KEEP-OUT" for r in control_dependent_rules())
