from generator.model.signal_chain_noise_dc import (
    dc_budget_default_gain,
    noise_budget,
    validate_ae015,
)

def test_ae015_validation():
    validate_ae015()

def test_full_chain_noise_is_sch101_dominated():
    x = noise_budget(rumble_enabled=False)
    assert x.sch101_contribution_rms_v > x.sch103_contribution_rms_v
    assert x.sch101_contribution_rms_v > x.that1646_contribution_rms_v

def test_rumble_filter_noise_penalty_is_small():
    a = noise_budget(rumble_enabled=False)
    b = noise_budget(rumble_enabled=True)
    assert b.output_noise_rms_v / a.output_noise_rms_v < 1.05

def test_direct_coupled_dc_worst_case_is_not_acceptable():
    x = dc_budget_default_gain()
    assert x.xlr_diff_offset_direct_coupled_max_v > 3.0

def test_post_eq_dc_block_collapses_worst_case_offset():
    x = dc_budget_default_gain()
    assert x.xlr_diff_offset_with_post_eq_block_estimate_v < 0.025
