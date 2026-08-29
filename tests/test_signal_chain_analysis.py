from generator.model.signal_chain_analysis import (
    riaa_combination,
    signal_point,
    sweep,
    validate_signal_chain,
)
from generator.model.balanced_input import GAIN_SETTINGS


def test_signal_chain_validation():
    validate_signal_chain()


def test_restored_riaa_is_in_active_sweep():
    default = next(item for item in GAIN_SETTINGS if item.name == "DEFAULT")
    bass, treble = riaa_combination()
    point = signal_point(
        gain_setting=default,
        bass=bass,
        treble=treble,
        frequency_hz=1000.0,
        rumble_enabled=False,
    )
    assert bass.name == "TRUE RIAA 3180/318 us"
    assert treble.name == "2121 Hz RIAA"
    assert 0.62 < point.xlr_output_rms_v < 0.66


def test_sweep_has_no_optional_3180_state():
    points = sweep((1000.0,))
    assert points
    assert all(not hasattr(point, "optional_3180_enabled") for point in points)
