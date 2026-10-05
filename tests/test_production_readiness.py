from generator.model.production_readiness import GateState,GATES,release_blockers,validate_production_gates
from tools.ae030_production_readiness_audit import render

def test_current_gate_model_is_fail_closed():
    validate_production_gates()

def test_electrical_design_driving_work_is_blocker():
    g=next(g for g in GATES if g.identifier=="ELEC-SIGNAL")
    assert g.state is GateState.BLOCKED and g.release_blocker

def test_controls_native_stack_and_routing_are_blockers():
    for ident in ("MECH-CONTROLS","PCB-NATIVE","PCB-STACK","PCB-ROUTING"):
        g=next(g for g in GATES if g.identifier==ident)
        assert g.state is GateState.BLOCKED and g.release_blocker

def test_release_blockers_have_actions():
    assert all(g.next_action for g in release_blockers())

def test_generated_report_has_current_critical_path(tmp_path):
    (tmp_path/"generator").mkdir()
    text,_,_=render(tmp_path)
    assert "pre-layout technical-debt clearance" in text
    assert "RUN08-RUN14" in text
    assert "routing release" in text.lower()
