import pytest

from generator.mechanical import (
    AccessArchitecture,
    EnclosureRole,
    build_mechanical_baseline,
    build_placement_synthesis,
    evaluate_candidate,
    validate_synthesis,
)


def test_audio_rejects_sliding_cover_but_psu_allows_it():
    model = build_mechanical_baseline()
    assert not model.audio_requirement.sliding_cover_allowed
    assert model.psu_requirement.sliding_cover_allowed


def test_audio_requirement_preserves_300_mm_external_width_limit():
    audio = build_mechanical_baseline().audio_requirement
    assert audio.maximum_external_width_mm == 300.0


def test_all_candidates_have_unique_ids_and_scores():
    candidates = build_mechanical_baseline().candidates
    assert len({candidate.identifier for candidate in candidates}) == len(candidates)
    assert all(candidate.weighted_score > 0 for candidate in candidates)


def test_sliding_psu_candidate_does_not_fail_access_gate():
    model = build_mechanical_baseline()
    candidate = next(item for item in model.candidates if item.identifier == "ENC-P02")
    assert candidate.access is AccessArchitecture.SLIDING_COVER
    failures = evaluate_candidate(candidate, model.psu_requirement)
    assert not any("sliding" in failure for failure in failures)


def test_audio_candidate_with_sliding_cover_would_fail():
    model = build_mechanical_baseline()
    psu_candidate = next(item for item in model.candidates if item.identifier == "ENC-P02")
    from dataclasses import replace
    audio_candidate = replace(psu_candidate, role=EnclosureRole.AUDIO)
    failures = evaluate_candidate(audio_candidate, model.audio_requirement)
    assert any("sliding" in failure for failure in failures)


def test_preferred_placement_is_valid_and_non_overlapping():
    placement = build_placement_synthesis()
    assert validate_synthesis(placement) == []
    assert len(placement.regions) == 7


def test_placement_rejects_board_below_minimum_envelope():
    with pytest.raises(ValueError):
        build_placement_synthesis(180.0, 120.0)


def test_input_and_output_regions_occupy_opposite_edges():
    placement = build_placement_synthesis()
    input_region = next(item for item in placement.regions if item.identifier == "REG-01")
    output_region = next(item for item in placement.regions if item.identifier == "REG-06")
    assert input_region.x_mm > output_region.x_mm
