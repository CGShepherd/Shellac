from generator.layout.detailed_placement_readiness import (
    FindingKind,
    FindingSeverity,
    build_detailed_placement_readiness,
)


def test_detailed_candidate_has_no_geometric_blockers():
    model = build_detailed_placement_readiness()
    assert model.proposal_count == 250
    assert model.blocker_count == 0
    assert not [f for f in model.findings if f.severity is FindingSeverity.BLOCKER]


def test_human_authority_is_preserved_as_explicit_review_gate():
    model = build_detailed_placement_readiness()
    manual = [f for f in model.findings if f.kind is FindingKind.MANUAL_CLUSTER]
    assert len(manual) == model.manual_review_cluster_count == 15
    assert all(f.severity is FindingSeverity.REVIEW for f in manual)
    assert model.status == "HUMAN_REVIEW_REQUIRED"


def test_conservative_courtyard_proximity_is_reported_not_silently_accepted():
    model = build_detailed_placement_readiness()
    courtyard = [f for f in model.findings if f.kind is FindingKind.COURTYARD_PROXIMITY]
    assert courtyard
    assert all(f.severity is FindingSeverity.REVIEW for f in courtyard)


def test_unfrozen_mechanical_datums_are_reported_not_invented():
    model = build_detailed_placement_readiness()
    mechanical = [f for f in model.findings if f.kind is FindingKind.MECHANICAL_DATUM]
    assert len(mechanical) == 1
    assert model.unresolved_mechanical_inputs
