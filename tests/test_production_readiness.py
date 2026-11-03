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
 (tmp_path/'generator').mkdir(); text,_,_=render(tmp_path); assert 'Retain the AE-076E-B H120/H220' in text and 'RUN08-RUN14' in text and 'A30403RNCB is the single Matrix production part' not in text and 'routing release' in text.lower() and 'Complete pre-layout technical-debt clearance under AE-076D' not in text
 assert 'Prototype electrical acceptance' not in text
 assert 'prototype hardware' not in text.lower()
 assert 'Complete prototype/bench commissioning and correlation.' not in text
 assert 'HARDWARE_EVIDENCE_REQUIRED' in text
 assert 'Prototype_Commissioning_Acceptance_Matrix_Rev_A0.md' in text

def test_f7gh5_current_narrative_contract():
    gates = {g.identifier: g for g in GATES}
    assert "AE-076E-B implements H120/H220" in gates["ELEC-SIGNAL"].evidence
    assert "RUN08-RUN14" in gates["ELEC-SIGNAL"].evidence
    assert "TE MRJE3404" in gates["MECH-CONTROLS"].evidence
    assert "current AE-076B authority" in gates["PCB-OUTLINE"].evidence
    assert "H120/H220 source/native migration is complete" in gates["PCB-PLACEMENT"].evidence
    assert "AE-076E-B qualified native H901" in gates["PCB-NATIVE"].evidence
    assert "TE MRJE3404 / 1825537-3" in gates["BOM-CONTROLS"].evidence
    assert "C&K A30403RNCB is superseded" in gates["BOM-CONTROLS"].evidence
    assert "H120/H220 sockets are implemented" in gates["DOC-COMMISSION"].evidence
    assert gates["ELEC-SIGNAL"].state is GateState.BLOCKED
    assert gates["MECH-CONTROLS"].state is GateState.BLOCKED
    assert gates["PCB-NATIVE"].state is GateState.BLOCKED
    assert gates["BOM-CONTROLS"].state is GateState.BLOCKED
    assert all(g.next_action for g in GATES)
