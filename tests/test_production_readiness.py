from generator.model.production_readiness import GateState,GATES,release_blockers,validate_production_gates
from tools.ae030_production_readiness_audit import render
def test_current_gate_model_is_fail_closed(): validate_production_gates()
def test_electrical_design_driving_work_is_blocker():
 g=next(g for g in GATES if g.identifier=='ELEC-SIGNAL'); assert g.state is GateState.BLOCKED and g.release_blocker
def test_controls_native_stack_and_routing_are_blockers():
 for ident in ('MECH-CONTROLS','PCB-NATIVE','PCB-STACK','PCB-ROUTING'):
  g=next(g for g in GATES if g.identifier==ident); assert g.state is GateState.BLOCKED and g.release_blocker
def test_ae076d_closes_current_document_authority_debt_only():
 g=next(g for g in GATES if g.identifier=='DOC-AUTHORITY'); assert g.state is GateState.CLOSED and not g.release_blocker and 'AE-076D' in g.evidence
def test_release_blockers_have_actions(): assert all(g.next_action for g in release_blockers())
def test_generated_report_has_post_ae076d_critical_path(tmp_path):
 (tmp_path/'generator').mkdir(); text,_,_=render(tmp_path); assert 'personality-interface and native-model migration' in text and 'RUN08-RUN14' in text and 'routing release' in text.lower() and 'Complete pre-layout technical-debt clearance under AE-076D' not in text
 assert 'Prototype electrical acceptance' not in text
 assert 'prototype hardware' not in text.lower()
 assert 'Complete prototype/bench commissioning and correlation.' not in text
 assert 'HARDWARE_EVIDENCE_REQUIRED' in text
 assert 'Prototype_Commissioning_Acceptance_Matrix_Rev_A0.md' in text
