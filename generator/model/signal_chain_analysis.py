"""AE-011 end-to-end signal-chain analysis for Project Shellac.

This model intentionally composes existing controlled sub-models rather than
duplicating their component constants. It is intended to become the single
machine-executable absolute gain/headroom audit from cartridge input to XLR.

Rev A0 does not attempt to hide the G3-027 RIAA integration blocker.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import log10, pi
from itertools import product

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
from .riaa_integration_audit import audit as audit_riaa_integration


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
    sch103_output_rms_v: float
    xlr_output_rms_v: float
    first_active_margin_db: float
    xlr_margin_db: float


def db(value: float) -> float:
    if value <= 0:
        raise ValueError("value must be positive")
    return 20.0 * log10(value)


def _bass_transfer(bass, frequency_hz: float) -> float:
    if bass.switch_condition == "SHORT":
        return 1.0
    s = 1j * 2.0 * pi * frequency_hz
    return abs(realised_bass_transfer(s, bass))


def _treble_transfer(treble, frequency_hz: float) -> float:
    s = 1j * 2.0 * pi * frequency_hz
    return abs(realised_treble_transfer(s, treble))


def signal_point(
    *,
    gain_setting,
    bass,
    treble,
    frequency_hz: float,
    rumble_enabled: bool,
    cartridge_rms_v: float = NOMINAL_CARTRIDGE_RMS_V,
) -> SignalChainPoint:
    if frequency_hz <= 0:
        raise ValueError("frequency_hz must be positive")
    if cartridge_rms_v < 0:
        raise ValueError("cartridge_rms_v must be non-negative")

    lf = _bass_transfer(bass, frequency_hz)
    hf = _treble_transfer(treble, frequency_hz)
    rumble = abs(filter_transfer(frequency_hz)) if rumble_enabled else 1.0

    first_active = cartridge_rms_v * gain_setting.total_gain * lf
    sch103_output = first_active * hf * RECOVERY_GAIN
    # SCH107 is unity in its wanted pass band except for its HP response.
    # SCH104 and SCH105 are unity. SCH108 supplies final differential 2x.
    xlr = sch103_output * rumble * DIFFERENTIAL_GAIN_LINEAR

    first_margin = float("inf") if first_active == 0 else db(
        OPA1612_DESIGN_OUTPUT_RMS_V / first_active
    )
    xlr_margin = float("inf") if xlr == 0 else db(DESIGN_OUTPUT_RMS_V / xlr)

    return SignalChainPoint(
        gain_setting=gain_setting.name,
        bass=bass.name,
        treble=treble.name,
        rumble_enabled=rumble_enabled,
        frequency_hz=frequency_hz,
        sch101_gain=gain_setting.total_gain,
        active_lf_gain=lf,
        passive_hf_gain=hf,
        rumble_gain=rumble,
        sch103_output_rms_v=sch103_output,
        xlr_output_rms_v=xlr,
        first_active_margin_db=first_margin,
        xlr_margin_db=xlr_margin,
    )


def historical_combinations():
    """Return operator-valid historical 78 combinations.

    The dedicated TRUE-RIAA branch is excluded here because G3-027 has already
    shown that it must be resynthesised before the independent 3180 us stage can
    be considered integrated.
    """
    return tuple(product(BASS_NETWORKS, TREBLE_NETWORKS))


def sweep(
    frequencies_hz=(5.0, 10.0, 15.0, 20.0, 30.0, 50.0, 100.0,
                    1000.0, 10000.0, 20000.0),
):
    points = []
    for gain_setting in GAIN_SETTINGS:
        for bass, treble in historical_combinations():
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


def worst_first_active_margin():
    return min(sweep(), key=lambda p: p.first_active_margin_db)


def worst_xlr_margin():
    return min(sweep(), key=lambda p: p.xlr_margin_db)


def validate_signal_chain_a0() -> None:
    # Reconfirm the high-value architecture invariants.
    assert abs(RECOVERY_GAIN - 2.1) < 1e-12
    assert DIFFERENTIAL_GAIN_LINEAR == 2.0

    default = next(item for item in GAIN_SETTINGS if item.name == "DEFAULT")
    flat_bass = next(item for item in BASS_NETWORKS if item.name == "FLAT")
    flat_treble = next(item for item in TREBLE_NETWORKS if item.name == "FLAT")

    p_flat = signal_point(
        gain_setting=default,
        bass=flat_bass,
        treble=flat_treble,
        frequency_hz=1000.0,
        rumble_enabled=False,
    )
    expected_flat = (
        NOMINAL_CARTRIDGE_RMS_V
        * default.total_gain
        * RECOVERY_GAIN
        * DIFFERENTIAL_GAIN_LINEAR
    )
    assert abs(p_flat.xlr_output_rms_v - expected_flat) < 1e-12

    # Representative historical 200-Hz/flat-treble point independently
    # reproduces the long-standing nominal ~0.642 V balanced output.
    bass_200 = next(item for item in BASS_NETWORKS if item.name == "200 Hz")
    p_nominal = signal_point(
        gain_setting=default,
        bass=bass_200,
        treble=flat_treble,
        frequency_hz=1000.0,
        rumble_enabled=False,
    )
    assert 0.63 < p_nominal.xlr_output_rms_v < 0.66

    # Preserve G3-027 as an explicit release blocker at this revision.
    riaa = audit_riaa_integration()
    assert riaa.double_3180_possible_if_unmodified
