from generator.model.balanced_input import DIFF_CONVERTER_GAIN, validate_balanced_input
from generator.model.post_eq_dc_block import cutoff_hz, magnitude_db, validate_post_eq_dc_block
from generator.model.sch101_precision_candidate import validate_ae014


def test_active_sch101_is_dr038_implemented_baseline():
    validate_balanced_input()
    assert DIFF_CONVERTER_GAIN == 4.0


def test_dr038_selected_candidate_remains_valid():
    validate_ae014()


def test_dr039_selected_model_remains_valid_pending_atomic_cad_migration():
    validate_post_eq_dc_block()
    assert cutoff_hz() < 0.6
    assert magnitude_db(20.0) > -0.01
