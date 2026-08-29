"""AE-011/AE-012 complete signal-chain gain and headroom analysis.

DR-037 restores the legacy complete-RIAA architecture. This module composes
the controlled block models and provides deterministic spot checks plus dense
logarithmic all-state sweeps.
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
    cartridge_rms_v: float
    sch101_gain: float
    active_lf_gain: float
    passive_hf_gain: float
    rumble_gain: float
    first_active_output_rms_v: float
    sch103_output_rms_v: float
    xlr_output_rms_v: float
    first_active_margin_db: float
    xlr_margin_db: float
    cartridge_limit_first_active_rms_v: float
    cartridge_limit_xlr_rms_v: float


def db(value: float) -> float:
    if value <= 0:
        raise ValueError("value must be positive")
    return 20.0 * log10(value)


def logarithmic_frequencies(start_hz: float, stop_hz: float, points: int) -> tuple[float, ...]:
    if start_hz <= 0 or stop_hz <= start_hz or points < 2:
        raise ValueError("Require 0 < start_hz < stop_hz and points >= 2")
    a = log10(start_hz)
    step = (log10(stop_hz) - a) / (points - 1)
    return tuple(10.0 ** (a + i * step) for i in range(points))


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
    if frequency_hz <= 0:
        raise ValueError("frequency_hz must be positive")
    if cartridge_rms_v <= 0:
        raise ValueError("cartridge_rms_v must be positive")

    lf = _lf(bass, frequency_hz)
    hf = _hf(treble, frequency_hz)
    rumble = abs(filter_transfer(frequency_hz)) if rumble_enabled else 1.0

    first_active = cartridge_rms_v * gain_setting.total_gain * lf
    sch103 = first_active * hf * RECOVERY_GAIN
    xlr = sch103 * rumble * DIFFERENTIAL_GAIN_LINEAR

    first_path_gain = first_active / cartridge_rms_v
    xlr_path_gain = xlr / cartridge_rms_v

    return SignalChainPoint(
        gain_setting.name,
        bass.name,
        treble.name,
        rumble_enabled,
        frequency_hz,
        cartridge_rms_v,
        gain_setting.total_gain,
        lf,
        hf,
        rumble,
        first_active,
        sch103,
        xlr,
        db(OPA1612_DESIGN_OUTPUT_RMS_V / first_active),
        db(DESIGN_OUTPUT_RMS_V / xlr),
        OPA1612_DESIGN_OUTPUT_RMS_V / first_path_gain,
        DESIGN_OUTPUT_RMS_V / xlr_path_gain,
    )


def historical_combinations():
    return tuple(product(BASS_NETWORKS, TREBLE_NETWORKS))


def riaa_combination():
    treble = next(item for item in TREBLE_NETWORKS if item.name == "2121 Hz RIAA")
    return RIAA_BASS_NETWORK, treble


def all_combinations():
    return historical_combinations() + (riaa_combination(),)


def sweep(
    frequencies_hz: tuple[float, ...] | None = None,
    *,
    cartridge_rms_v: float = NOMINAL_CARTRIDGE_RMS_V,
):
    frequencies = frequencies_hz or logarithmic_frequencies(5.0, 20_000.0, 2001)
    points = []
    for gain_setting in GAIN_SETTINGS:
        for bass, treble in all_combinations():
            for rumble_enabled in (False, True):
                for frequency_hz in frequencies:
                    points.append(signal_point(
                        gain_setting=gain_setting,
                        bass=bass,
                        treble=treble,
                        frequency_hz=frequency_hz,
                        rumble_enabled=rumble_enabled,
                        cartridge_rms_v=cartridge_rms_v,
                    ))
    return tuple(points)


def worst_xlr_margin_for_gain(
    gain_name: str,
    *,
    min_frequency_hz: float = 20.0,
    cartridge_rms_v: float = NOMINAL_CARTRIDGE_RMS_V,
):
    candidates = (
        p for p in sweep(cartridge_rms_v=cartridge_rms_v)
        if p.frequency_hz >= min_frequency_hz and p.gain_setting == gain_name
    )
    return min(candidates, key=lambda p: p.xlr_margin_db)


def validate_signal_chain() -> None:
    assert abs(RECOVERY_GAIN - 2.1) < 1e-12
    assert DIFFERENTIAL_GAIN_LINEAR == 2.0

    default = next(item for item in GAIN_SETTINGS if item.name == "DEFAULT")
    flat_bass = next(item for item in BASS_NETWORKS if item.name == "FLAT")
    flat_treble = next(item for item in TREBLE_NETWORKS if item.name == "FLAT")

    flat = signal_point(
        gain_setting=default,
        bass=flat_bass,
        treble=flat_treble,
        frequency_hz=1000.0,
    )
    expected = NOMINAL_CARTRIDGE_RMS_V * default.total_gain * RECOVERY_GAIN * DIFFERENTIAL_GAIN_LINEAR
    assert abs(flat.xlr_output_rms_v - expected) < 1e-12

    bass_200 = next(item for item in BASS_NETWORKS if item.name == "200 Hz")
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

    low = worst_xlr_margin_for_gain("LOW")
    normal = worst_xlr_margin_for_gain("DEFAULT")
    high = worst_xlr_margin_for_gain("HIGH")

    assert low.xlr_margin_db > 8.5
    assert normal.xlr_margin_db > 4.6
    assert 0.5 < high.xlr_margin_db < 0.8
    assert high.bass == RIAA_BASS_NETWORK.name
    assert high.treble == "2121 Hz RIAA"
    assert not high.rumble_enabled
