from generator.model.production_cmrr import (
    production_cmrr_matrix,
    validate_production_cmrr,
)
from generator.model.production_signal_chain_closure import (
    production_closure,
    validate_production_closure,
)


def test_production_cmrr():
    validate_production_cmrr()


def test_all_production_cmrr_points_meet_requirement():
    assert all(x.margin_db >= 0.0 for x in production_cmrr_matrix())


def test_production_signal_chain_closure():
    validate_production_closure()


def test_dr039_is_used_in_production_noise_budget():
    x = production_closure()
    assert x.dc_block_cutoff_hz < 0.6
    assert x.dc_block_loss_20hz_db > -0.01


def test_two_second_muted_startup_reduces_dc_block_charge_to_below_0p3_percent():
    assert production_closure().residual_fraction_after_2s < 0.003
