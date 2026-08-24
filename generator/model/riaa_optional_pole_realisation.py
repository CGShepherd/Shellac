"""G3-026 component-level realisation of the optional 3180 us RIAA section.

The selected topology is deliberately simple and polarity-preserving:

    RIAA_CORE_OUT -> R_TIMING -> node -> non-inverting OPA1656 -> RIAA_3180_OUT
                                  |
                                  C_TIMING
                                  |
                                 0VA

The non-inverting stage gain is chosen so the optional section is approximately
unity magnitude at 1 kHz while providing the canonical 3180 us low-frequency
boost relative to 1 kHz. A stereo DPDT switch selects either RIAA_CORE_OUT
(straight-through BYPASS) or RIAA_3180_OUT (ON) for each channel.

This module freezes the nominal electrical realisation. PCB footprint and final
physical placement remain separate manufacturing-control gates.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import log10, pi, sqrt

BOLTZMANN = 1.380649e-23
TEMPERATURE_K = 300.0

REFERENCE_HZ = 1000.0
TIMING_R_OHM = 31_500.0
TIMING_R_TOL = 0.001

# Parallel C0G/NP0 timing capacitors: 68 nF + 33 nF.
TIMING_C_68_F = 68e-9
TIMING_C_33_F = 33e-9
TIMING_C_F = TIMING_C_68_F + TIMING_C_33_F
TIMING_C_TOL = 0.01

GAIN_RG_OHM = 267.0
GAIN_RF_OHM = 5_080.0
GAIN_R_TOL = 0.001
GAIN = 1.0 + GAIN_RF_OHM / GAIN_RG_OHM

OPA_MFR = "Texas Instruments"
OPA_MPN = "OPA1656"
SWITCH_MFR = "Nidec Components"
SWITCH_MPN = "ASE2D-2M-10-Z"

CAP_68_MFR = "KEMET"
CAP_68_MPN = "C1206C683F5GECAUTO7210"
CAP_33_MFR = "KEMET"
CAP_33_MPN = "C1206C333F5GEC7210"

OPA_VOLTAGE_NOISE_1KHZ_NV_RT_HZ = 4.3
OPA_CURRENT_NOISE_1KHZ_FA_RT_HZ = 6.0

DESIGN_OUTPUT_RMS_V = 10.0


class RealisationStatus(str, Enum):
    CANDIDATE = "candidate"
    SELECTED = "selected"
    ELECTRICALLY_FROZEN = "electrically_frozen"


STATUS = RealisationStatus.ELECTRICALLY_FROZEN


@dataclass(frozen=True, slots=True)
class OptionalPoleRealisation:
    identifier: str
    topology: str
    channels: int
    op_amp_mfr: str
    op_amp_mpn: str
    switch_mfr: str
    switch_mpn: str
    switch_requirement: str
    bypass_connection: str
    timing_resistor_ohm: float
    timing_capacitance_f: float
    gain: float
    manufacturing_released: bool


REALISATION = OptionalPoleRealisation(
    identifier="RIAA-OPT-3180-REAL-A",
    topology="RC low-pass ahead of non-inverting gain; output-path DPDT select",
    channels=2,
    op_amp_mfr=OPA_MFR,
    op_amp_mpn=OPA_MPN,
    switch_mfr=SWITCH_MFR,
    switch_mpn=SWITCH_MPN,
    switch_requirement="DPDT ON-ON, through-hole, gold finish, non-shorting/BBM",
    bypass_connection="each channel common selects RIAA_CORE_OUT directly",
    timing_resistor_ohm=TIMING_R_OHM,
    timing_capacitance_f=TIMING_C_F,
    gain=GAIN,
    manufacturing_released=False,
)


def time_constant_s() -> float:
    return TIMING_R_OHM * TIMING_C_F


def pole_hz() -> float:
    return 1.0 / (2.0 * pi * time_constant_s())


def transfer(s: complex) -> complex:
    return GAIN / (1.0 + s * time_constant_s())


def magnitude(frequency_hz: float) -> float:
    if frequency_hz <= 0:
        raise ValueError("frequency_hz must be positive")
    return abs(transfer(1j * 2.0 * pi * frequency_hz))


def gain_db(frequency_hz: float) -> float:
    return 20.0 * log10(magnitude(frequency_hz))


def reference_error_db() -> float:
    return gain_db(REFERENCE_HZ)


def timing_pole_bounds_hz() -> tuple[float, float]:
    tau_min = (
        TIMING_R_OHM * (1.0 - TIMING_R_TOL)
        * TIMING_C_F * (1.0 - TIMING_C_TOL)
    )
    tau_max = (
        TIMING_R_OHM * (1.0 + TIMING_R_TOL)
        * TIMING_C_F * (1.0 + TIMING_C_TOL)
    )
    return (
        1.0 / (2.0 * pi * tau_max),
        1.0 / (2.0 * pi * tau_min),
    )


def reference_gain_bounds_db() -> tuple[float, float]:
    values: list[float] = []
    for rsign in (-1.0, 1.0):
        for csign in (-1.0, 1.0):
            for rgsign in (-1.0, 1.0):
                for rfsign in (-1.0, 1.0):
                    r = TIMING_R_OHM * (1.0 + rsign * TIMING_R_TOL)
                    c = TIMING_C_F * (1.0 + csign * TIMING_C_TOL)
                    rg = GAIN_RG_OHM * (1.0 + rgsign * GAIN_R_TOL)
                    rf = GAIN_RF_OHM * (1.0 + rfsign * GAIN_R_TOL)
                    gain = 1.0 + rf / rg
                    mag = gain / sqrt(
                        1.0 + (2.0 * pi * REFERENCE_HZ * r * c) ** 2
                    )
                    values.append(20.0 * log10(mag))
    return min(values), max(values)


def thermal_noise_nv_rt_hz(resistance_ohm: float) -> float:
    return sqrt(4.0 * BOLTZMANN * TEMPERATURE_K * resistance_ohm) * 1e9


def output_noise_proxy_1khz_nv_rt_hz() -> float:
    """White-noise proxy at 1 kHz, not an integrated system-noise claim."""
    signal_path = magnitude(REFERENCE_HZ)
    timing_r = thermal_noise_nv_rt_hz(TIMING_R_OHM) * signal_path
    op_amp = OPA_VOLTAGE_NOISE_1KHZ_NV_RT_HZ * GAIN
    rg = thermal_noise_nv_rt_hz(GAIN_RG_OHM) * (GAIN - 1.0)
    rf = thermal_noise_nv_rt_hz(GAIN_RF_OHM)
    return sqrt(timing_r**2 + op_amp**2 + rg**2 + rf**2)


def max_section_input_rms_v(frequency_hz: float) -> float:
    return DESIGN_OUTPUT_RMS_V / magnitude(frequency_hz)


def validate_realisation() -> None:
    assert STATUS is RealisationStatus.ELECTRICALLY_FROZEN
    assert REALISATION.channels == 2
    assert REALISATION.op_amp_mpn == "OPA1656"
    assert REALISATION.switch_mpn == "ASE2D-2M-10-Z"
    assert abs(pole_hz() - 50.0) < 0.1
    assert abs(reference_error_db()) < 0.01
    low, high = timing_pole_bounds_hz()
    assert 49.4 < low < 50.0
    assert 50.0 < high < 50.7
    g_low, g_high = reference_gain_bounds_db()
    assert g_low > -0.12
    assert g_high < 0.13
    assert output_noise_proxy_1khz_nv_rt_hz() < 110.0
    assert max_section_input_rms_v(20.0) > 0.53
    assert REALISATION.manufacturing_released is False
