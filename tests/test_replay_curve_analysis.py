import pytest

from generator.model.replay_curve_analysis import (
    CURVE_TARGETS,
    LABEL_RECOMMENDATIONS,
    analyse_all_targets,
    ideal_bass_transfer,
    response_error_db,
)
from generator.model.replay_eq import BASS_NETWORKS, RIAA_BASS_NETWORK, TREBLE_NETWORKS


def _target(identifier: str):
    return next(item for item in CURVE_TARGETS if item.identifier == identifier)


def _bass(name: str):
    if name == RIAA_BASS_NETWORK.name:
        return RIAA_BASS_NETWORK
    return next(item for item in BASS_NETWORKS if item.name == name)


def _treble(name: str):
    return next(item for item in TREBLE_NETWORKS if item.name == name)


def test_flat_curve_is_exactly_flat_after_normalisation():
    target = _target("FLAT")
    bass = _bass(target.bass_name)
    treble = _treble(target.treble_name)
    for frequency in (20.0, 50.0, 1000.0, 10_000.0, 20_000.0):
        assert response_error_db(frequency, target, bass, treble) == pytest.approx(0.0, abs=1e-12)


def test_true_riaa_is_sub_point_one_db_over_20_hz_to_20_khz():
    summary = next(item for item in analyse_all_targets() if item.target.identifier == "RIAA")
    assert abs(summary.worst_error_db) < 0.1
    assert summary.rms_error_db < 0.05
    assert summary.error_1_khz_db == pytest.approx(0.0, abs=1e-12)


def test_all_targets_are_normalised_at_one_khz():
    for target in CURVE_TARGETS:
        assert response_error_db(1000.0, target, _bass(target.bass_name), _treble(target.treble_name)) == pytest.approx(0.0, abs=1e-12)


def test_historical_analysis_is_complete_and_finite():
    summaries = analyse_all_targets()
    assert len(summaries) == len(CURVE_TARGETS)
    assert all(summary.rms_error_db >= 0 for summary in summaries)
    assert all(abs(summary.worst_error_db) < 20 for summary in summaries)


def test_label_recommendations_include_core_families():
    labels = {item.label for item in LABEL_RECOMMENDATIONS}
    assert "Acoustic" in labels
    assert "Victor 1938–1952" in labels
    assert "RIAA / CCIR LP" in labels


def test_invalid_partial_bass_target_is_rejected():
    with pytest.raises(ValueError):
        ideal_bass_transfer(1j, 20.0, None)
