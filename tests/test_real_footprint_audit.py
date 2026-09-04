from generator.layout.footprint_contract import build_footprint_contract
from generator.layout.real_footprint_audit import (
    build_real_footprint_audit,
    validate_real_footprint_audit,
)


def test_real_footprint_audit_is_deterministic_and_balanced():
    audit = build_real_footprint_audit()
    assert validate_real_footprint_audit(audit) == []
    expected=len(build_footprint_contract().board_population_refs)
    assert audit.board_population_count == expected
    assert audit.accepted_identity_count == expected
    assert audit.review_count == 0
    assert audit.blocker_count == 0
    assert audit.status == "READY"


def test_replay_capacitors_are_decomposed_into_physical_parts():
    audit = build_real_footprint_audit()
    compound = [f for f in audit.findings if f.category == "compound_capacitor_not_physical"]
    assert compound == []


def test_ten_microfarad_physical_classes_are_closed():
    audit = build_real_footprint_audit()
    non_polar = [f for f in audit.findings if f.category == "non_polar_10u_physical_unresolved"]
    bulk = [f for f in audit.findings if f.category == "10u_bulk_physical_identity_review"]
    assert non_polar == []
    assert bulk == []
