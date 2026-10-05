from pathlib import Path
from generator.model.bom_cost import category_subtotals,summarise,validate_ledger
from generator.model.prerouting_readiness import RULES,control_dependent_rules,independent_rules,validate_prerouting_contract
from tools.ae031_prerouting_control_audit import live_grayhill_files,render
ROOT=Path(__file__).resolve().parents[1]
def test_ae031_cost_snapshot():
 validate_ledger(); s=summarise(); assert s.quoted_design_gbp==233.67 and s.priced_lines==4 and s.total_lines==5 and round(s.confidence_pct,1)==80.0
def test_enclosures_dominate_current_verified_subtotal():
 cats=category_subtotals(); assert cats['enclosure_mechanics']==187.10 and cats['enclosure_mechanics']>cats['controls']
def test_prerouting_contract_uses_current_control_gate():
 validate_prerouting_contract(); assert len(independent_rules())>len(control_dependent_rules()); r=next(r for r in RULES if r.identifier=='CONTROL-GEOMETRY'); assert 'AE071-B03' in r.requirement and 'AE-027/AE-028' not in r.requirement
def test_generated_control_audit_is_current_and_fail_closed():
 text,hits=render(ROOT); assert hits==[] and 'AE-076D' in text and 'current AE071-B03' in text and 'does not grant routing authority' in text; assert live_grayhill_files(ROOT)==[]
