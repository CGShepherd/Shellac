"""AE-015 full-chain noise and DC-offset review for Project Shellac.

This model is intentionally first-order but end-to-end.  It uses the accepted
DR-038 candidate SCH101 precision architecture as the front-end reference and
the controlled SCH103/SCH107/SCH104/SCH105/SCH108 transfer functions.

Noise results are intended for architecture decisions, not final production
limits.  DC analysis uses conservative datasheet offset maxima to identify
whether the present direct-coupled topology is intrinsically robust.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import log10, pi, sqrt
import cmath

from .replay_eq import RIAA_BASS_NETWORK, TREBLE_NETWORKS, RECOVERY_GAIN
from .replay_curve_analysis import realised_bass_transfer, realised_treble_transfer
from .rumble_filter import SECTIONS, filter_transfer

K = 1.380649e-23
T = 300.0

# DR-038 candidate default gain: 4x diff converter, Rg=1k, RF=999R.
SCH101_DEFAULT_GAIN = 4.0 * (1.0 + 999.0 / 1000.0)

# AE-014 first-order input-referred white-noise result, rounded conservatively.
SCH101_INPUT_NOISE_NV_RT_HZ = 9.0

OPA1656_EN_NV_RT_HZ = 4.3
OPA1612_EN_NV_RT_HZ = 1.1

# Conservative 25 C input-offset maxima.
OPA1656_VOS_MAX_V = 1.0e-3
OPA1612_VOS_MAX_V = 0.5e-3

# THAT1646 data-sheet figures.
THAT1646_OUTPUT_NOISE_DBU = -101.0
THAT1646_DIFF_OFFSET_MAX_V = 15e-3
THAT1646_GAIN = 2.0

# SCH103 values.
SCH103_RF_OHM = 100_000.0
SCH103_RG_OHM = 2_700.0
RECOVERY_RG_OHM = 10_000.0
RECOVERY_RF_OHM = 11_000.0
TREBLE_R_OHM = 750.0

# Proposed DR-039 common post-EQ DC block.
DC_BLOCK_C_F = 1.0e-6
DC_BLOCK_R_OHM = 330_000.0


@dataclass(frozen=True, slots=True)
class NoiseBudget:
    rumble_enabled: bool
    output_noise_rms_v: float
    nominal_riaa_output_rms_v: float
    electronics_snr_db: float
    sch101_contribution_rms_v: float
    sch103_contribution_rms_v: float
    sch107_upper_bound_rms_v: float
    downstream_contribution_rms_v: float
    that1646_contribution_rms_v: float


@dataclass(frozen=True, slots=True)
class DcBudget:
    sch101_pre_eq_offset_max_v: float
    sch103_post_eq_offset_max_v: float
    xlr_diff_offset_direct_coupled_max_v: float
    xlr_diff_offset_with_post_eq_block_estimate_v: float


def resistor_noise_v_rt_hz(r_ohm: float) -> float:
    return sqrt(4.0 * K * T * r_ohm)


def _riaa_treble():
    return next(x for x in TREBLE_NETWORKS if x.name == "2121 Hz RIAA")


def _z_feedback(f_hz: float) -> complex:
    s = 1j * 2.0 * pi * f_hz
    n = RIAA_BASS_NETWORK
    z_series = n.rs_ohm + 1.0 / (s * n.capacitance_nf * 1e-9)
    return n.rf_ohm * z_series / (n.rf_ohm + z_series)


def _dc_block_transfer(f_hz: float) -> complex:
    s = 1j * 2.0 * pi * f_hz
    # Series capacitor into the defined 330k bias/load resistor.
    return (s * DC_BLOCK_R_OHM * DC_BLOCK_C_F) / (1.0 + s * DC_BLOCK_R_OHM * DC_BLOCK_C_F)


def _trapz(xs, ys):
    total = 0.0
    for a, b, ya, yb in zip(xs, xs[1:], ys, ys[1:]):
        total += 0.5 * (yb + ya) * (b - a)
    return total


def _logspace(start: float, stop: float, points: int):
    a = log10(start)
    step = (log10(stop) - a) / (points - 1)
    return tuple(10.0 ** (a + i * step) for i in range(points))


def noise_budget(*, rumble_enabled: bool, include_dc_block: bool = False) -> NoiseBudget:
    fs = _logspace(20.0, 20_000.0, 4001)
    treble = _riaa_treble()

    psd_101 = []
    psd_103 = []
    psd_107 = []
    psd_down = []

    for f in fs:
        s = 1j * 2.0 * pi * f
        hb = realised_bass_transfer(s, RIAA_BASS_NETWORK)
        ht = realised_treble_transfer(s, treble)
        hr = filter_transfer(f) if rumble_enabled else 1.0 + 0j
        hdc = _dc_block_transfer(f) if include_dc_block else 1.0 + 0j

        # SCH101 input-referred white noise propagated through the complete chain.
        g_to_xlr = SCH101_DEFAULT_GAIN * abs(hb * ht) * RECOVERY_GAIN * abs(hr * hdc) * THAT1646_GAIN
        n101 = SCH101_INPUT_NOISE_NV_RT_HZ * 1e-9 * g_to_xlr
        psd_101.append(n101 * n101)

        # SCH103 active LF stage: op-amp en, Rg, and exact real part of Zf.
        zf = _z_feedback(f)
        ng = abs(1.0 + zf / SCH103_RG_OHM)
        n_lf_out_sq = (
            (OPA1612_EN_NV_RT_HZ * 1e-9 * ng) ** 2
            + (resistor_noise_v_rt_hz(SCH103_RG_OHM) * abs(zf / SCH103_RG_OHM)) ** 2
            + 4.0 * K * T * max(zf.real, 0.0)
        )
        post_lf_gain = abs(ht) * RECOVERY_GAIN * abs(hr * hdc) * THAT1646_GAIN

        # Passive treble resistor contribution.
        n_treble = resistor_noise_v_rt_hz(TREBLE_R_OHM) * abs(ht)
        n_treble_out_sq = (n_treble * RECOVERY_GAIN * abs(hr * hdc) * THAT1646_GAIN) ** 2

        # Recovery stage op-amp and feedback resistors.
        recovery_ng = RECOVERY_GAIN
        n_recovery_out_sq = (
            (OPA1612_EN_NV_RT_HZ * 1e-9 * recovery_ng) ** 2
            + (resistor_noise_v_rt_hz(RECOVERY_RG_OHM) * (RECOVERY_RF_OHM / RECOVERY_RG_OHM)) ** 2
            + resistor_noise_v_rt_hz(RECOVERY_RF_OHM) ** 2
        )
        n_recovery_to_xlr_sq = (sqrt(n_recovery_out_sq) * abs(hr * hdc) * THAT1646_GAIN) ** 2

        psd_103.append(n_lf_out_sq * post_lf_gain**2 + n_treble_out_sq + n_recovery_to_xlr_sq)

        # SCH107 conservative upper bound: op-amp en plus RSS of both section resistors.
        if rumble_enabled:
            sec_a, sec_b = SECTIONS
            na = sqrt(
                (OPA1656_EN_NV_RT_HZ * 1e-9) ** 2
                + resistor_noise_v_rt_hz(sec_a.r1_ohm) ** 2
                + resistor_noise_v_rt_hz(sec_a.r2_ohm) ** 2
            )
            nb = sqrt(
                (OPA1656_EN_NV_RT_HZ * 1e-9) ** 2
                + resistor_noise_v_rt_hz(sec_b.r1_ohm) ** 2
                + resistor_noise_v_rt_hz(sec_b.r2_ohm) ** 2
            )
            # A is filtered by B; B is already at filter output.
            # This deliberately over-bounds resistor-noise transfer.
            h_b = abs(
                (sec_b.r1_ohm * sec_b.r2_ohm * sec_b.capacitance_f**2 * s**2)
                / (
                    sec_b.r1_ohm * sec_b.r2_ohm * sec_b.capacitance_f**2 * s**2
                    + 2.0 * sec_b.r1_ohm * sec_b.capacitance_f * s + 1.0
                )
            )
            n107 = sqrt((na * h_b) ** 2 + nb**2) * abs(hdc) * THAT1646_GAIN
        else:
            n107 = 0.0
        psd_107.append(n107 * n107)

        # SCH104 + SCH105 unity buffers and their 100R output isolators.
        one_unity = sqrt((OPA1656_EN_NV_RT_HZ * 1e-9) ** 2 + resistor_noise_v_rt_hz(100.0) ** 2)
        nd = sqrt(2.0) * one_unity * THAT1646_GAIN
        psd_down.append(nd * nd)

    def integ(psd):
        return sqrt(_trapz(fs, psd))

    n101 = integ(psd_101)
    n103 = integ(psd_103)
    n107 = integ(psd_107)
    nd = integ(psd_down)
    that = 0.775 * 10.0 ** (THAT1646_OUTPUT_NOISE_DBU / 20.0)
    total = sqrt(n101*n101 + n103*n103 + n107*n107 + nd*nd + that*that)

    # Nominal 1 kHz RIAA output for 5mV reference with DR-038 candidate default gain.
    f = 1000.0
    s = 1j * 2.0 * pi * f
    h = abs(realised_bass_transfer(s, RIAA_BASS_NETWORK) * realised_treble_transfer(s, treble))
    nominal = 0.005 * SCH101_DEFAULT_GAIN * h * RECOVERY_GAIN * THAT1646_GAIN
    snr = 20.0 * log10(nominal / total)

    return NoiseBudget(
        rumble_enabled, total, nominal, snr, n101, n103, n107, nd, that
    )


def dc_budget_default_gain() -> DcBudget:
    # Conservative independent worst-case signs:
    # two first-stage OPA1656 offsets oppose each other, then the converter
    # OPA1656 contributes its own offset with noise gain 1+4 = 5.
    leg_gain = 1.0 + 999.0 / 1000.0
    pre_eq = (
        (2.0 * OPA1656_VOS_MAX_V * leg_gain) * 4.0
        + OPA1656_VOS_MAX_V * 5.0
    )

    # Non-flat SCH103 active stage DC gain.
    lf_dc_gain = 1.0 + SCH103_RF_OHM / SCH103_RG_OHM
    post_lf = pre_eq * lf_dc_gain + OPA1612_VOS_MAX_V * lf_dc_gain

    # Recovery stage.
    post_eq = post_lf * RECOVERY_GAIN + OPA1612_VOS_MAX_V * RECOVERY_GAIN

    # Two downstream OPA1656 unity stages + THAT1646 differential offset.
    direct = (post_eq + 2.0 * OPA1656_VOS_MAX_V) * THAT1646_GAIN + THAT1646_DIFF_OFFSET_MAX_V

    # A common post-EQ AC block removes all SCH101/SCH103 static offset.
    # Remaining conservative DC is from downstream unity buffers and THAT1646.
    blocked = (2.0 * OPA1656_VOS_MAX_V) * THAT1646_GAIN + THAT1646_DIFF_OFFSET_MAX_V

    return DcBudget(pre_eq, post_eq, direct, blocked)


def validate_ae015() -> None:
    bypass = noise_budget(rumble_enabled=False)
    inserted = noise_budget(rumble_enabled=True)
    dc = dc_budget_default_gain()

    assert 70.0 < bypass.electronics_snr_db < 80.0
    assert 70.0 < inserted.electronics_snr_db < 80.0
    assert inserted.output_noise_rms_v < bypass.output_noise_rms_v * 1.05
    assert dc.xlr_diff_offset_direct_coupled_max_v > 3.0
    assert dc.xlr_diff_offset_with_post_eq_block_estimate_v < 0.025

    fc = 1.0 / (2.0 * pi * DC_BLOCK_R_OHM * DC_BLOCK_C_F)
    assert 0.4 < fc < 0.6
    attenuation_20 = abs(_dc_block_transfer(20.0))
    assert 20.0 * log10(attenuation_20) > -0.01
