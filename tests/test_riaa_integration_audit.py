from generator.model.riaa_integration_audit import (
    IntegrationStatus, audit, validate_integration_audit,
)

def test_legacy_true_riaa_branch_is_blocked_only_for_duplicate_3180():
    validate_integration_audit()
    a = audit()
    assert a.status is IntegrationStatus.BLOCKED_DUPLICATED_3180
    assert a.double_3180_possible_if_unmodified

def test_third_pole_remains_independent_operator_control():
    a = audit()
    assert a.independent_operator_control_required
    assert a.bass_treble_interlock_required is False

def test_operator_may_combine_3180_with_any_bass_treble_state():
    a = audit()
    assert 'independent operator-controlled 3180 us stage' in a.required_action
