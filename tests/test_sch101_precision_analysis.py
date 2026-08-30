from generator.model.sch101_precision_analysis import (
    candidate_cmrr_summaries,
    candidate_noise_summaries,
    current_cmrr_summaries,
    current_noise_summaries,
    validate_ae013,
)


def test_ae013_validation():
    validate_ae013()


def test_historical_discrete_0p1_percent_cmrr_was_not_precision_balanced():
    values = {x.gain_name: x.worst_case_cmrr_db for x in current_cmrr_summaries()}
    assert values["LOW"] < 54.0
    assert values["DEFAULT"] < 51.0
    assert values["HIGH"] < 49.0


def test_candidate_ratio_tracking_exceeds_68db_all_gains():
    assert min(x.worst_case_cmrr_db for x in candidate_cmrr_summaries()) > 68.0


def test_lower_impedance_candidate_reduces_front_end_noise():
    now = {x.gain_name: x for x in current_noise_summaries()}
    candidate = {x.gain_name: x for x in candidate_noise_summaries()}
    assert candidate["DEFAULT"].input_referred_density_nv_rt_hz < 0.55 * now["DEFAULT"].input_referred_density_nv_rt_hz
