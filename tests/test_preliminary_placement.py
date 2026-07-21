from generator.layout.footprint_contract import build_footprint_contract
from generator.layout.preliminary_placement import (
    build_preliminary_placement_baseline,
    validate_preliminary_placement,
)


def test_every_approved_board_reference_has_one_coordinate_proposal():
    placement = build_preliminary_placement_baseline()
    contract = build_footprint_contract()
    assert len(placement.proposals) == len(contract.board_population_refs) == 243
    assert {item.ref for item in placement.proposals} == set(contract.board_population_refs)


def test_panel_and_virtual_items_are_never_placed():
    placement = build_preliminary_placement_baseline()
    assert not ({item.ref for item in placement.proposals} & set(placement.excluded_refs))
    assert len(placement.excluded_refs) == 21


def test_manual_authority_clusters_are_not_auto_accepted():
    placement = build_preliminary_placement_baseline()
    manual = [item for item in placement.proposals if item.cluster_id in placement.manual_review_clusters]
    assert manual
    assert all(not item.accepted for item in manual)


def test_preliminary_placement_is_valid_and_non_manufacturing():
    placement = build_preliminary_placement_baseline()
    assert validate_preliminary_placement(placement) == []
    assert "not accepted for manufacture" in placement.status.lower()
