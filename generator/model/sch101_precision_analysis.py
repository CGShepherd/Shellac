"""AE-013 SCH101 noise and resistor-tolerance CMRR review.

This module deliberately separates:
1. the current controlled implementation (0.1% discrete resistors);
2. a candidate lower-impedance / tighter-ratio implementation.

It does not change the active schematic.  Its purpose is to quantify whether
the current resistor policy supports the balanced-cartridge architecture.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import log10, sqrt

from .balanced_input import GAIN_SETTINGS

BOLTZMANN = 1.380649e-23
TEMPERATURE_K = 300.0
BANDWIDTH_LOW_HZ = 20.0
BANDWIDTH_HIGH_HZ = 20_000.0

# Grado 78C working source model.
CARTRIDGE_RESISTANCE_OHM = 475.0
INPUT_SERIES_RESISTOR_OHM = 100.0

# OPA1656 conservative 1 kHz noise-density value from current TI product data.
OPA1656_EN_NV_RT_HZ = 4.3

DIFF_RIN_OHM = 10_000.0
DIFF_RFB_OHM = 34_800.0
GAIN_RG_OHM = 10_000.0

CURRENT_RESISTOR_TOLERANCE = 0.001
CANDIDATE_RATIO_TOLERANCE = 0.0001
CANDIDATE_IMPEDANCE_SCALE = 0.1


@dataclass(frozen=True, slots=True)
class NoiseSummary:
    gain_name: str
    impedance_scale: float
    input_referred_density_nv_rt_hz: float
    flat_20hz_20khz_rms_uv: float
    flat_5mv_snr_db: float


@dataclass(frozen=True, slots=True)
class CmrrSummary:
    gain_name: str
    ratio_tolerance: float
    worst_case_cmrr_db: float


def resistor_noise_nv_rt_hz(resistance_ohm: float) -> float:
    if resistance_ohm <= 0:
        raise ValueError("resistance must be positive")
    return sqrt(4.0 * BOLTZMANN * TEMPERATURE_K * resistance_ohm) * 1e9


def _gain_setting(name: str):
    return next(item for item in GAIN_SETTINGS if item.name == name)


def sch101_input_referred_white_noise(
    gain_name: str,
    *,
    impedance_scale: float = 1.0,
) -> NoiseSummary:
    """First-order white-noise budget referred to cartridge differential input.

    Included:
    - Grado 78C DC resistance;
    - two 100-ohm RF series resistors;
    - both OPA1656 leg voltage-noise sources;
    - leg gain-ladder Johnson noise;
    - differential-converter OPA1656 voltage noise;
    - Johnson noise of all four differential-converter resistors.

    OPA1656 current noise is negligible at these source impedances and is not
    material to this comparison.
    """
    if impedance_scale <= 0:
        raise ValueError("impedance_scale must be positive")

    setting = _gain_setting(gain_name)
    rf = setting.rf_ohm * impedance_scale
    rg = GAIN_RG_OHM * impedance_scale
    leg_gain = 1.0 + rf / rg

    # Source-side differential noise.
    source = sqrt(
        resistor_noise_nv_rt_hz(CARTRIDGE_RESISTANCE_OHM) ** 2
        + 2.0 * resistor_noise_nv_rt_hz(INPUT_SERIES_RESISTOR_OHM) ** 2
    )

    # One non-inverting gain leg: op-amp en + Rg + Rf.
    rf_over_rg = rf / rg
    one_leg_resistor_out = sqrt(
        (resistor_noise_nv_rt_hz(rg) * rf_over_rg) ** 2
        + resistor_noise_nv_rt_hz(rf) ** 2
    )
    one_leg_output = sqrt(
        (OPA1656_EN_NV_RT_HZ * leg_gain) ** 2
        + one_leg_resistor_out ** 2
    )
    two_legs_input_referred = sqrt(2.0) * one_leg_output / leg_gain

    # Four-resistor differential converter.
    rin = DIFF_RIN_OHM * impedance_scale
    rfb = DIFF_RFB_OHM * impedance_scale
    converter_gain = rfb / rin
    noise_gain = 1.0 + converter_gain
    plus_node_rth = rin * rfb / (rin + rfb)
    converter_output = sqrt(
        (OPA1656_EN_NV_RT_HZ * noise_gain) ** 2
        + resistor_noise_nv_rt_hz(rfb) ** 2
        + (resistor_noise_nv_rt_hz(rin) * converter_gain) ** 2
        + (resistor_noise_nv_rt_hz(plus_node_rth) * noise_gain) ** 2
    )
    converter_input_referred = converter_output / (leg_gain * converter_gain)

    total = sqrt(
        source**2
        + two_legs_input_referred**2
        + converter_input_referred**2
    )

    bandwidth = BANDWIDTH_HIGH_HZ - BANDWIDTH_LOW_HZ
    rms_uv = total * sqrt(bandwidth) / 1000.0
    snr_db = 20.0 * log10(0.005 / (rms_uv * 1e-6))
    return NoiseSummary(gain_name, impedance_scale, total, rms_uv, snr_db)


def _diff_output(vplus: float, vminus: float, r1: float, r2: float, r3: float, r4: float) -> float:
    """Exact ideal-op-amp four-resistor differential-amplifier response."""
    plus_node = vplus * r4 / (r3 + r4)
    return (1.0 + r2 / r1) * plus_node - (r2 / r1) * vminus


def worst_case_cmrr(gain_name: str, *, ratio_tolerance: float) -> CmrrSummary:
    """Enumerate independent tolerance corners for four gain and four diff resistors."""
    if ratio_tolerance <= 0:
        raise ValueError("ratio_tolerance must be positive")

    setting = _gain_setting(gain_name)
    worst = float("inf")
    t = ratio_tolerance

    for signs in product((-1.0, 1.0), repeat=8):
        srfp, srgp, srfm, srgm, sr1, sr2, sr3, sr4 = signs

        gp = 1.0 + setting.rf_ohm * (1.0 + srfp*t) / (GAIN_RG_OHM * (1.0 + srgp*t))
        gm = 1.0 + setting.rf_ohm * (1.0 + srfm*t) / (GAIN_RG_OHM * (1.0 + srgm*t))

        r1 = DIFF_RIN_OHM * (1.0 + sr1*t)
        r2 = DIFF_RFB_OHM * (1.0 + sr2*t)
        r3 = DIFF_RIN_OHM * (1.0 + sr3*t)
        r4 = DIFF_RFB_OHM * (1.0 + sr4*t)

        common_out = _diff_output(gp, gm, r1, r2, r3, r4)
        diff_out = _diff_output(0.5*gp, -0.5*gm, r1, r2, r3, r4)
        if abs(common_out) < 1e-18:
            cmrr = float("inf")
        else:
            cmrr = 20.0 * log10(abs(diff_out / common_out))
        worst = min(worst, cmrr)

    return CmrrSummary(gain_name, ratio_tolerance, worst)


def current_noise_summaries():
    return tuple(sch101_input_referred_white_noise(item.name) for item in GAIN_SETTINGS)


def candidate_noise_summaries():
    return tuple(
        sch101_input_referred_white_noise(item.name, impedance_scale=CANDIDATE_IMPEDANCE_SCALE)
        for item in GAIN_SETTINGS
    )


def current_cmrr_summaries():
    return tuple(
        worst_case_cmrr(item.name, ratio_tolerance=CURRENT_RESISTOR_TOLERANCE)
        for item in GAIN_SETTINGS
    )


def candidate_cmrr_summaries():
    return tuple(
        worst_case_cmrr(item.name, ratio_tolerance=CANDIDATE_RATIO_TOLERANCE)
        for item in GAIN_SETTINGS
    )


def validate_ae013() -> None:
    current_noise = {x.gain_name: x for x in current_noise_summaries()}
    candidate_noise = {x.gain_name: x for x in candidate_noise_summaries()}
    current_cmrr = {x.gain_name: x for x in current_cmrr_summaries()}
    candidate_cmrr = {x.gain_name: x for x in candidate_cmrr_summaries()}

    assert 17.5 < current_noise["DEFAULT"].input_referred_density_nv_rt_hz < 18.5
    assert 8.5 < candidate_noise["DEFAULT"].input_referred_density_nv_rt_hz < 9.5
    assert candidate_noise["DEFAULT"].flat_5mv_snr_db - current_noise["DEFAULT"].flat_5mv_snr_db > 5.5

    assert 49.5 < current_cmrr["DEFAULT"].worst_case_cmrr_db < 50.7
    assert current_cmrr["HIGH"].worst_case_cmrr_db < 49.0
    assert candidate_cmrr["DEFAULT"].worst_case_cmrr_db > 69.5
    assert candidate_cmrr["HIGH"].worst_case_cmrr_db > 68.0
