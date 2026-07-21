from generator.layout.real_footprint_audit import (
    build_real_footprint_audit,
    validate_real_footprint_audit,
)


def test_real_footprint_audit_is_deterministic_and_balanced():
    audit = build_real_footprint_audit()
    assert validate_real_footprint_audit(audit) == []
    assert audit.board_population_count == 225
    assert audit.accepted_identity_count == 191
    assert audit.review_count == 16
    assert audit.blocker_count == 18
    assert audit.status.startswith("BLOCKED")


def test_compound_replay_capacitors_are_not_treated_as_physical_parts():
    audit = build_real_footprint_audit()
    compound = [f for f in audit.findings if f.category == "compound_capacitor_not_physical"]
    assert len(compound) == 14
    assert {f.sheet_id for f in compound} == {"SCH103"}
    assert all("+" in f.value for f in compound)
    assert all(f.severity == "BLOCKER" for f in compound)


def test_unresolved_ten_microfarad_classes_remain_visible():
    audit = build_real_footprint_audit()
    non_polar = [f for f in audit.findings if f.category == "non_polar_10u_0805_unresolved"]
    rail_or_decoupling = [f for f in audit.findings if f.category == "10u_0805_derating_review"]
    assert len(non_polar) == 4
    assert len(rail_or_decoupling) == 16
