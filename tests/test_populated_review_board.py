from generator.mechanical.populated_board import (
    render_populated_board,
    validate_populated_board_text,
)
from generator.layout.preliminary_placement import build_preliminary_placement_baseline


def test_populated_review_board_has_all_proposed_footprints_and_no_routing():
    text = render_populated_board()
    placement = build_preliminary_placement_baseline()
    assert text.count('(footprint "ProjectShellac:ReviewPlaceholder"') == len(placement.proposals)
    assert '(segment ' not in text
    assert '(via ' not in text
    assert '(zone ' not in text
    assert '(footprint "ProjectShellac:MountingHole"' not in text
    assert validate_populated_board_text(text) == []


def test_populated_review_board_preserves_manual_review_status():
    text = render_populated_board()
    placement = build_preliminary_placement_baseline()
    expected_manual = sum(1 for p in placement.proposals if not p.accepted)
    expected_accepted = sum(1 for p in placement.proposals if p.accepted)
    assert text.count('"GATE3A_REVIEW"') >= expected_manual
    assert text.count('"ACCEPTED"') >= expected_accepted
