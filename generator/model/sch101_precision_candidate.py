"""AE-014 SCH101 precision-architecture down-selection.

Compares the controlled 3.48x / high-impedance implementation with the
recommended 4.00x precision-converter / low-impedance implementation.

The candidate deliberately uses a commercially standard precision ratio for
the differential converter: LT5400-7, 1.25k / 5k, A-grade where available.
The selectable gain stage is re-partitioned so total SCH101 gains remain
nominally 14/18/22 dB.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product
from math import log10, sqrt

K = 1.380649e-23
T = 300.0
OPA1656_EN_NV_RT_HZ = 4.3
CARTRIDGE_R_OHM = 475.0
RF_SERIES_OHM = 100.0

CANDIDATE_DIFF_RIN_OHM = 1250.0
CANDIDATE_DIFF_RFB_OHM = 5000.0
CANDIDATE_DIFF_GAIN = 4.0
CANDIDATE_RG_OHM = 1000.0

# E96/E192-friendly realised ladder.
CANDIDATE_BASE_RF_OHM = 249.0
CANDIDATE_DEFAULT_ADD_OHM = 750.0
CANDIDATE_HIGH_ADD_OHM = 1910.0

# Ratio policy: gain network 0.01%; LT5400 A-grade CMRR matching 0.005%.
GAIN_RATIO_TOL = 0.0001
DIFF_CMRR_MATCH_TOL = 0.00005

TARGETS = (
    ("LOW", 14.0, CANDIDATE_BASE_RF_OHM),
    ("DEFAULT", 18.0, CANDIDATE_BASE_RF_OHM + CANDIDATE_DEFAULT_ADD_OHM),
    ("HIGH", 22.0, CANDIDATE_BASE_RF_OHM + CANDIDATE_HIGH_ADD_OHM),
)


@dataclass(frozen=True, slots=True)
class CandidateSetting:
    name: str
    target_db: float
    rf_ohm: float
    leg_gain: float
    total_gain: float
    realised_db: float
    error_db: float
    input_noise_nv_rt_hz: float
    flat_20k_snr_db: float
    worst_case_cmrr_db: float


def rn(r: float) -> float:
    return sqrt(4*K*T*r)*1e9


def _diff_out(vp, vm, r1, r2, r3, r4):
    p = vp*r4/(r3+r4)
    return (1+r2/r1)*p - (r2/r1)*vm


def _worst_cmrr(rf: float) -> float:
    worst = float("inf")
    for s in product((-1.0,1.0), repeat=8):
        gp = 1 + rf*(1+s[0]*GAIN_RATIO_TOL)/(CANDIDATE_RG_OHM*(1+s[1]*GAIN_RATIO_TOL))
        gm = 1 + rf*(1+s[2]*GAIN_RATIO_TOL)/(CANDIDATE_RG_OHM*(1+s[3]*GAIN_RATIO_TOL))
        r1=CANDIDATE_DIFF_RIN_OHM*(1+s[4]*DIFF_CMRR_MATCH_TOL)
        r2=CANDIDATE_DIFF_RFB_OHM*(1+s[5]*DIFF_CMRR_MATCH_TOL)
        r3=CANDIDATE_DIFF_RIN_OHM*(1+s[6]*DIFF_CMRR_MATCH_TOL)
        r4=CANDIDATE_DIFF_RFB_OHM*(1+s[7]*DIFF_CMRR_MATCH_TOL)
        c=_diff_out(gp,gm,r1,r2,r3,r4)
        d=_diff_out(0.5*gp,-0.5*gm,r1,r2,r3,r4)
        cmrr=float("inf") if abs(c)<1e-18 else 20*log10(abs(d/c))
        worst=min(worst,cmrr)
    return worst


def _noise(rf: float) -> float:
    g=1+rf/CANDIDATE_RG_OHM
    source=sqrt(rn(CARTRIDGE_R_OHM)**2+2*rn(RF_SERIES_OHM)**2)
    one_leg=sqrt(
        (OPA1656_EN_NV_RT_HZ*g)**2
        +(rn(CANDIDATE_RG_OHM)*(rf/CANDIDATE_RG_OHM))**2
        +rn(rf)**2
    )
    legs=sqrt(2)*one_leg/g
    k=CANDIDATE_DIFF_GAIN
    ng=1+k
    rth=CANDIDATE_DIFF_RIN_OHM*CANDIDATE_DIFF_RFB_OHM/(CANDIDATE_DIFF_RIN_OHM+CANDIDATE_DIFF_RFB_OHM)
    conv_out=sqrt(
        (OPA1656_EN_NV_RT_HZ*ng)**2
        +rn(CANDIDATE_DIFF_RFB_OHM)**2
        +(rn(CANDIDATE_DIFF_RIN_OHM)*k)**2
        +(rn(rth)*ng)**2
    )
    conv=conv_out/(g*k)
    return sqrt(source**2+legs**2+conv**2)


def candidate_settings():
    out=[]
    for name,target,rf in TARGETS:
        leg=1+rf/CANDIDATE_RG_OHM
        total=leg*CANDIDATE_DIFF_GAIN
        realised=20*log10(total)
        noise=_noise(rf)
        rms=noise*sqrt(20_000-20)*1e-9
        snr=20*log10(0.005/rms)
        out.append(CandidateSetting(
            name,target,rf,leg,total,realised,realised-target,
            noise,snr,_worst_cmrr(rf)
        ))
    return tuple(out)


def validate_ae014():
    x={s.name:s for s in candidate_settings()}
    assert abs(x["LOW"].error_db) < 0.04
    assert abs(x["DEFAULT"].error_db) < 0.07
    assert abs(x["HIGH"].error_db) < 0.04
    assert x["DEFAULT"].input_noise_nv_rt_hz < 9.5
    assert min(s.worst_case_cmrr_db for s in x.values()) > 69.5
