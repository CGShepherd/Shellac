from generator.layout.real_footprint_audit import (
    build_real_footprint_audit,
    validate_real_footprint_audit,
)


def test_real_footprint_audit_is_deterministic_and_balanced():
    audit = build_real_footprint_audit()
    assert validate_real_footprint_audit(audit) == []
    assert audit.board_population_count == 243
    assert audit.accepted_identity_count == 223
    assert audit.review_count == 16
    assert audit.blocker_count == 4
    assert audit.status.startswith("BLOCKED")


def test_replay_capacitors_are_decomposed_into_physical_parts():
    audit = build_real_footprint_audit()
    compound = [f for f in audit.findings if f.category == "compound_capacitor_not_physical"]
    assert compound == []


def test_unresolved_ten_microfarad_classes_remain_visible():
    audit = build_real_footprint_audit()
    non_polar = [f for f in audit.findings if f.category == "non_polar_10u_0805_unresolved"]
    rail_or_decoupling = [f for f in audit.findings if f.category == "10u_0805_derating_review"]
    assert len(non_polar) == 4
    assert len(rail_or_decoupling) == 16
