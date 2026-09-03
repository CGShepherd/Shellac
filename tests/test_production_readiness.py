from generator.model.production_readiness import (
    GateState,
    GATES,
    gates_by_state,
    release_blockers,
    validate_production_gates,
)
from tools.ae030_production_readiness_audit import render


def test_ae030_gate_model_is_well_formed():
    validate_production_gates()


def test_signal_chain_is_not_a_design_blocker_anymore():
    gate = next(g for g in GATES if g.identifier == "ELEC-SIGNAL")
    assert gate.state is GateState.CLOSED
    assert not gate.release_blocker


def test_control_mechanics_and_routing_are_release_blockers():
    controls = next(g for g in GATES if g.identifier == "MECH-CONTROLS")
    routing = next(g for g in GATES if g.identifier == "PCB-ROUTING")
    assert controls.release_blocker
    assert routing.release_blocker
    assert controls.state is GateState.BLOCKED
    assert routing.state is GateState.BLOCKED


def test_prototype_measurement_is_required_but_not_open_design():
    gate = next(g for g in GATES if g.identifier == "ELEC-MEASURE")
    assert gate.state is GateState.PROTOTYPE_EVIDENCE_REQUIRED
    assert gate.release_blocker


def test_release_blockers_have_actions():
    assert all(g.next_action for g in release_blockers())


def test_generated_report_states_critical_path(tmp_path):
    (tmp_path/"generator").mkdir()
    text, _, _ = render(tmp_path)
    assert "controls/mechanics -> native routing/fabrication -> prototype evidence" in text
