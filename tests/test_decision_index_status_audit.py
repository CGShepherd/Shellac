from tools.audit_current_decision_index import audit


def test_audit_accepts_coherent_implemented_state():
    text = """decisions:
  DR-038:
    status: CURRENT_IMPLEMENTED
    implementation: LT5400 is installed.
  DR-039:
    status: CURRENT_IMPLEMENTED
    implementation: DC block is installed.
historical_implementation_events:
"""
    assert audit(text) == []


def test_audit_rejects_staging_language_under_implemented_status():
    text = """decisions:
  DR-038:
    status: CURRENT_IMPLEMENTED
    note: Active SCH101 remains the pre-DR038 implementation until atomic CAD migration.
  DR-039:
    status: CURRENT_IMPLEMENTED
    implementation: DC block is installed.
historical_implementation_events:
"""
    assert audit(text)
