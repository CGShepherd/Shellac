from generator.model.sch101_precision_candidate import candidate_settings, validate_ae014

def test_ae014_candidate():
    validate_ae014()

def test_total_gain_targets_preserved():
    assert max(abs(x.error_db) for x in candidate_settings()) < 0.07

def test_candidate_cmrr_floor():
    assert min(x.worst_case_cmrr_db for x in candidate_settings()) > 69.5

def test_candidate_noise():
    default=next(x for x in candidate_settings() if x.name=="DEFAULT")
    assert default.input_noise_nv_rt_hz < 9.5
