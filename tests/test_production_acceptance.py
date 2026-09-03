from generator.model.production_acceptance import (
    Evidence,
    acceptance_items,
    counts_by_evidence,
    release_blockers,
    validate_acceptance_matrix,
)


def test_ae029_acceptance_matrix_is_well_formed():
    validate_acceptance_matrix()


def test_acceptance_matrix_covers_all_three_evidence_states():
    counts = counts_by_evidence()
    assert counts[Evidence.ANALYTICALLY_CLOSED] > 0
    assert counts[Evidence.VERIFY_ON_PROTOTYPE] > 0
    assert counts[Evidence.OPEN_DESIGN] > 0


def test_open_design_items_are_release_blockers():
    assert all(x.release_blocker for x in acceptance_items() if x.evidence is Evidence.OPEN_DESIGN)


def test_prototype_measurements_dominate_remaining_release_work():
    counts = counts_by_evidence()
    assert counts[Evidence.VERIFY_ON_PROTOTYPE] > counts[Evidence.OPEN_DESIGN]


def test_every_release_blocker_has_a_defined_test_method():
    assert all(x.method for x in release_blockers())
