"""AE-011 A1 end-to-end signal-chain model.

DR-037 restores the legacy complete-RIAA architecture. There is no independent
3180 us stage in the authoritative signal path.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import log10, pi

from .balanced_input import GAIN_SETTINGS
from .replay_eq import (
    BASS_NETWORKS,
    TREBLE_NETWORKS,
    RIAA_BASS_NETWORK,
    RECOVERY_GAIN,
    NOMINAL_CARTRIDGE_RMS_V,
    OPA1612_DESIGN_OUTPUT_RMS_V,
)
from .replay_curve_analysis import realised_bass_transfer, realised_treble_transfer
from .rumble_filter import filter_transfer
from .output_driver import DIFFERENTIAL_GAIN_LINEAR, DESIGN_OUTPUT_RMS_V


@dataclass(frozen=True, slots=True)
class SignalChainPoint:
    gain_setting: str
    bass: str
    treble: str
    rumble_enabled: bool
    frequency_hz: float
    sch101_gain: float
    active_lf_gain: float
    passive_hf_gain: float
    rumble_gain: float
    first_active_output_rms_v: float
    sch103_output_rms_v: float
    xlr_output_rms_v: float
    first_active_margin_db: float
    xlr_margin_db: float


def db(value: float) -> float:
    if value <= 0:
        raise ValueError("value must be positive")
    return 20.0 * log10(value)


def _lf(bass, frequency_hz: float) -> float:
    if bass.switch_condition == "SHORT":
        return 1.0
    s = 1j * 2.0 * pi * frequency_hz
    return abs(realised_bass_transfer(s, bass))


def _hf(treble, frequency_hz: float) -> float:
    s = 1j * 2.0 * pi * frequency_hz
    return abs(realised_treble_transfer(s, treble))


def signal_point(
    *,
    gain_setting,
    bass,
    treble,
    frequency_hz: float,
    rumble_enabled: bool = False,
    cartridge_rms_v: float = NOMINAL_CARTRIDGE_RMS_V,
) -> SignalChainPoint:
    lf = _lf(bass, frequency_hz)
    hf = _hf(treble, frequency_hz)
    rumble = abs(filter_transfer(frequency_hz)) if rumble_enabled else 1.0

    first_active = cartridge_rms_v * gain_setting.total_gain * lf
    sch103 = first_active * hf * RECOVERY_GAIN
    xlr = sch103 * rumble * DIFFERENTIAL_GAIN_LINEAR

    return SignalChainPoint(
        gain_setting.name,
        bass.name,
        treble.name,
        rumble_enabled,
        frequency_hz,
        gain_setting.total_gain,
        lf,
        hf,
        rumble,
        first_active,
        sch103,
        xlr,
        float("inf") if first_active == 0 else db(OPA1612_DESIGN_OUTPUT_RMS_V / first_active),
        float("inf") if xlr == 0 else db(DESIGN_OUTPUT_RMS_V / xlr),
    )


def historical_combinations():
    return tuple(product(BASS_NETWORKS, TREBLE_NETWORKS))


def riaa_combination():
    treble = next(item for item in TREBLE_NETWORKS if item.name == "2121 Hz RIAA")
    return RIAA_BASS_NETWORK, treble


def sweep(frequencies_hz=(5.0, 10.0, 15.0, 20.0, 30.0, 50.0, 100.0,
                          1000.0, 10000.0, 20000.0)):
    points = []
    combinations = list(historical_combinations())
    combinations.append(riaa_combination())
    for gain_setting in GAIN_SETTINGS:
        for bass, treble in combinations:
            for rumble_enabled in (False, True):
                for frequency_hz in frequencies_hz:
                    points.append(signal_point(
                        gain_setting=gain_setting,
                        bass=bass,
                        treble=treble,
                        frequency_hz=frequency_hz,
                        rumble_enabled=rumble_enabled,
                    ))
    return tuple(points)


def validate_signal_chain() -> None:
    assert abs(RECOVERY_GAIN - 2.1) < 1e-12
    assert DIFFERENTIAL_GAIN_LINEAR == 2.0

    default = next(x for x in GAIN_SETTINGS if x.name == "DEFAULT")
    flat_bass = next(x for x in BASS_NETWORKS if x.name == "FLAT")
    flat_treble = next(x for x in TREBLE_NETWORKS if x.name == "FLAT")

    flat = signal_point(
        gain_setting=default,
        bass=flat_bass,
        treble=flat_treble,
        frequency_hz=1000.0,
    )
    expected = (
        NOMINAL_CARTRIDGE_RMS_V
        * default.total_gain
        * RECOVERY_GAIN
        * DIFFERENTIAL_GAIN_LINEAR
    )
    assert abs(flat.xlr_output_rms_v - expected) < 1e-12

    bass_200 = next(x for x in BASS_NETWORKS if x.name == "200 Hz")
    nominal = signal_point(
        gain_setting=default,
        bass=bass_200,
        treble=flat_treble,
        frequency_hz=1000.0,
    )
    assert 0.63 < nominal.xlr_output_rms_v < 0.66

    riaa_bass, riaa_treble = riaa_combination()
    riaa = signal_point(
        gain_setting=default,
        bass=riaa_bass,
        treble=riaa_treble,
        frequency_hz=1000.0,
    )
    assert 0.62 < riaa.xlr_output_rms_v < 0.66
