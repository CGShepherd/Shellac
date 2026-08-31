"""AE-023 production SCH101 CMRR and signal-chain assurance model.

Uses the implemented DR-038 values, not the earlier candidate baseline.
The frequency-dependent CMRR corner model includes:
- 100 ohm RF series pair at 0.1%;
- 1 nF common-mode C0G pair at 0.5%;
- gain-leg ratio elements at 0.01%;
- LT5400-7 A-grade CMRR matching at 0.005%;
- a defined 50 ohm/leg common-mode test source.

The 220 pF differential RF capacitor is deliberately omitted from the
common-mode mismatch model. That is conservative once mismatch creates a
differential error because the capacitor can only shunt differential energy.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import log10, pi

from .balanced_input import (
    DIFF_RFB_OHM,
    DIFF_RIN_OHM,
    GAIN_RG_OHM,
    GAIN_SETTINGS,
)

RF_SERIES_OHM = 100.0
RF_SERIES_TOL = 0.001
RF_CM_CAP_F = 1.0e-9
RF_CM_CAP_TOL = 0.005
GAIN_RATIO_TOL = 0.0001
LT5400_CMRR_MATCH_TOL = 0.00005
CMRR_TEST_SOURCE_OHM_PER_LEG = 50.0

CMRR_REQUIREMENT_LOW_MID_DB = 70.0
CMRR_REQUIREMENT_20KHZ_DB = 60.0


@dataclass(frozen=True, slots=True)
class CmrrPoint:
    gain_name: str
    frequency_hz: float
    worst_case_db: float
    requirement_db: float
    margin_db: float


def _rf_common_mode_transfer(f_hz: float, series_r: float, cap_f: float) -> complex:
    zc = 1.0 / (1j * 2.0 * pi * f_hz * cap_f)
    return zc / (CMRR_TEST_SOURCE_OHM_PER_LEG + series_r + zc)


def _diff_out(vplus: complex, vminus: complex, r1: float, r2: float, r3: float, r4: float) -> complex:
    plus_node = vplus * r4 / (r3 + r4)
    return (1.0 + r2 / r1) * plus_node - (r2 / r1) * vminus


def worst_case_cmrr(gain_name: str, frequency_hz: float) -> CmrrPoint:
    setting = next(x for x in GAIN_SETTINGS if x.name == gain_name)
    worst = float("inf")

    # 12 independent binary corners:
    # RF R+/R-, C+/C-, RF/Rg for each gain leg, four LT5400 ratios.
    for s in product((-1.0, 1.0), repeat=12):
        rp = RF_SERIES_OHM * (1.0 + s[0] * RF_SERIES_TOL)
        rm = RF_SERIES_OHM * (1.0 + s[1] * RF_SERIES_TOL)
        cp = RF_CM_CAP_F * (1.0 + s[2] * RF_CM_CAP_TOL)
        cm = RF_CM_CAP_F * (1.0 + s[3] * RF_CM_CAP_TOL)

        gp = 1.0 + (
            setting.rf_ohm * (1.0 + s[4] * GAIN_RATIO_TOL)
            / (GAIN_RG_OHM * (1.0 + s[5] * GAIN_RATIO_TOL))
        )
        gm = 1.0 + (
            setting.rf_ohm * (1.0 + s[6] * GAIN_RATIO_TOL)
            / (GAIN_RG_OHM * (1.0 + s[7] * GAIN_RATIO_TOL))
        )

        r1 = DIFF_RIN_OHM * (1.0 + s[8] * LT5400_CMRR_MATCH_TOL)
        r2 = DIFF_RFB_OHM * (1.0 + s[9] * LT5400_CMRR_MATCH_TOL)
        r3 = DIFF_RIN_OHM * (1.0 + s[10] * LT5400_CMRR_MATCH_TOL)
        r4 = DIFF_RFB_OHM * (1.0 + s[11] * LT5400_CMRR_MATCH_TOL)

        hp = _rf_common_mode_transfer(frequency_hz, rp, cp)
        hm = _rf_common_mode_transfer(frequency_hz, rm, cm)
        common_out = _diff_out(hp * gp, hm * gm, r1, r2, r3, r4)

        # Differential gain reference at the same frequency with nominal RF
        # network but the same precision-resistor corner.
        hnom = _rf_common_mode_transfer(
            frequency_hz, RF_SERIES_OHM, RF_CM_CAP_F
        )
        diff_out = _diff_out(0.5 * hnom * gp, -0.5 * hnom * gm, r1, r2, r3, r4)

        if abs(common_out) < 1e-20:
            cmrr = float("inf")
        else:
            cmrr = 20.0 * log10(abs(diff_out / common_out))
        worst = min(worst, cmrr)

    requirement = (
        CMRR_REQUIREMENT_20KHZ_DB
        if frequency_hz >= 20_000.0
        else CMRR_REQUIREMENT_LOW_MID_DB
    )
    return CmrrPoint(
        gain_name, frequency_hz, worst, requirement, worst - requirement
    )


def production_cmrr_matrix():
    return tuple(
        worst_case_cmrr(gain, f)
        for gain in ("LOW", "DEFAULT", "HIGH")
        for f in (20.0, 1000.0, 20_000.0)
    )


def validate_production_cmrr() -> None:
    points = production_cmrr_matrix()
    assert all(p.margin_db >= 0.0 for p in points)
    high_1k = next(
        p for p in points if p.gain_name == "HIGH" and p.frequency_hz == 1000.0
    )
    assert high_1k.worst_case_db >= 70.0
    high_20k = next(
        p for p in points if p.gain_name == "HIGH" and p.frequency_hz == 20_000.0
    )
    assert high_20k.worst_case_db >= 60.0
