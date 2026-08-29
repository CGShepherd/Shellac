from generator.model.signal_chain_analysis import (
    logarithmic_frequencies,
    riaa_combination,
    signal_point,
    validate_signal_chain,
    worst_xlr_margin_for_gain,
)
from generator.model.balanced_input import GAIN_SETTINGS


def test_signal_chain_validation():
    validate_signal_chain()


def test_dense_frequency_grid_endpoints():
    f = logarithmic_frequencies(5.0, 20_000.0, 2001)
    assert len(f) == 2001
    assert abs(f[0] - 5.0) < 1e-12
    assert abs(f[-1] - 20_000.0) < 1e-8


def test_riaa_default_1khz_nominal_output():
    default = next(item for item in GAIN_SETTINGS if item.name == "DEFAULT")
    bass, treble = riaa_combination()
    p = signal_point(
        gain_setting=default,
        bass=bass,
        treble=treble,
        frequency_hz=1000.0,
    )
    assert 0.62 < p.xlr_output_rms_v < 0.66


def test_high_gain_is_operating_envelope_not_universal_5mv_setting():
    p = worst_xlr_margin_for_gain("HIGH")
    assert p.bass == "TRUE RIAA 3180/318 us"
    assert p.treble == "2121 Hz RIAA"
    assert not p.rumble_enabled
    assert 0.5 < p.xlr_margin_db < 0.8
    assert 0.0052 < p.cartridge_limit_xlr_rms_v < 0.0056
