"""Full-band replay-curve analysis for SCH103.

The analysis compares the realised P06/P91 networks against idealised target
families derived from the Project 91 table. Responses are normalised at 1 kHz,
so the report measures equalisation-shape error rather than absolute stage gain.

Historical 78 targets are intentionally treated as nominal families. Project 91
itself notes that the source standards and mastering practice are inconsistent;
therefore these results guide switch coverage rather than assert archival truth.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import atan2, log10, pi
import cmath

from .replay_eq import (
    BASS_NETWORKS,
    RIAA_BASS_NETWORK,
    TREBLE_NETWORKS,
    BassNetwork,
    TrebleNetwork,
)
from .replay_eq_transfer import active_stage_transfer, logarithmic_frequencies

REFERENCE_HZ = 1000.0
ANALYSIS_START_HZ = 20.0
ANALYSIS_STOP_HZ = 20_000.0


@dataclass(frozen=True, slots=True)
class CurveTarget:
    identifier: str
    name: str
    bass_name: str
    treble_name: str
    lower_pole_hz: float | None
    upper_zero_hz: float | None
    treble_pole_hz: float | None
    exact_standard: bool = False
    notes: str = ""


@dataclass(frozen=True, slots=True)
class CurveErrorSummary:
    target: CurveTarget
    worst_error_db: float
    worst_error_frequency_hz: float
    rms_error_db: float
    error_20_hz_db: float
    error_50_hz_db: float
    error_100_hz_db: float
    error_1_khz_db: float
    error_10_khz_db: float
    error_20_khz_db: float


@dataclass(frozen=True, slots=True)
class LabelRecommendation:
    label: str
    bass_selection: str
    treble_selection: str
    notes: str = ""


def _normalise(value: complex, reference: complex) -> complex:
    if abs(reference) == 0:
        raise ZeroDivisionError("Reference response must not be zero.")
    return value / reference


def ideal_bass_transfer(s: complex, lower_pole_hz: float | None, upper_zero_hz: float | None) -> complex:
    if lower_pole_hz is None and upper_zero_hz is None:
        return 1.0 + 0j
    if lower_pole_hz is None or upper_zero_hz is None:
        raise ValueError("Bass target requires both lower pole and upper zero, or neither.")
    if lower_pole_hz <= 0 or upper_zero_hz <= lower_pole_hz:
        raise ValueError("Bass target requires 0 < lower pole < upper zero.")
    wp = 2.0 * pi * lower_pole_hz
    wz = 2.0 * pi * upper_zero_hz
    return (1.0 + s / wz) / (1.0 + s / wp)


def passive_treble_transfer(s: complex, pole_hz: float | None) -> complex:
    if pole_hz is None:
        return 1.0 + 0j
    if pole_hz <= 0:
        raise ValueError("Treble pole must be positive.")
    return 1.0 / (1.0 + s / (2.0 * pi * pole_hz))


def ideal_curve_transfer(s: complex, target: CurveTarget) -> complex:
    return ideal_bass_transfer(s, target.lower_pole_hz, target.upper_zero_hz) * passive_treble_transfer(
        s, target.treble_pole_hz
    )


def realised_bass_transfer(s: complex, network: BassNetwork) -> complex:
    if network.switch_condition == "SHORT":
        # C -> infinity: the branch becomes RS. The resulting constant gain
        # disappears when normalised at 1 kHz, giving a flat shape.
        return 1.0 + 0j
    if None in (network.rf_ohm, network.rs_ohm, network.rg_ohm, network.capacitance_nf):
        raise ValueError(f"Incomplete bass network: {network.name}")
    return active_stage_transfer(
        s,
        network.rf_ohm,
        network.rs_ohm,
        network.rg_ohm,
        network.capacitance_nf * 1e-9,
    )


def realised_treble_transfer(s: complex, network: TrebleNetwork) -> complex:
    if network.switch_condition == "OPEN":
        return 1.0 + 0j
    if network.resistor_ohm is None or network.capacitance_nf is None:
        raise ValueError(f"Incomplete treble network: {network.name}")
    tau = network.resistor_ohm * network.capacitance_nf * 1e-9
    return 1.0 / (1.0 + s * tau)


def realised_curve_transfer(s: complex, bass: BassNetwork, treble: TrebleNetwork) -> complex:
    return realised_bass_transfer(s, bass) * realised_treble_transfer(s, treble)


def response_error_db(frequency_hz: float, target: CurveTarget, bass: BassNetwork, treble: TrebleNetwork) -> float:
    if frequency_hz <= 0:
        raise ValueError("Frequency must be positive.")
    s = 1j * 2.0 * pi * frequency_hz
    s_ref = 1j * 2.0 * pi * REFERENCE_HZ
    ideal = _normalise(ideal_curve_transfer(s, target), ideal_curve_transfer(s_ref, target))
    actual = _normalise(realised_curve_transfer(s, bass, treble), realised_curve_transfer(s_ref, bass, treble))
    return 20.0 * log10(abs(actual / ideal))


def analyse_curve(
    target: CurveTarget,
    bass: BassNetwork,
    treble: TrebleNetwork,
    frequencies_hz: tuple[float, ...] | None = None,
) -> CurveErrorSummary:
    frequencies = frequencies_hz or logarithmic_frequencies(ANALYSIS_START_HZ, ANALYSIS_STOP_HZ, 601)
    errors = tuple(response_error_db(f, target, bass, treble) for f in frequencies)
    worst_index = max(range(len(errors)), key=lambda index: abs(errors[index]))
    rms = (sum(error * error for error in errors) / len(errors)) ** 0.5

    def at(frequency_hz: float) -> float:
        return response_error_db(frequency_hz, target, bass, treble)

    return CurveErrorSummary(
        target=target,
        worst_error_db=errors[worst_index],
        worst_error_frequency_hz=frequencies[worst_index],
        rms_error_db=rms,
        error_20_hz_db=at(20.0),
        error_50_hz_db=at(50.0),
        error_100_hz_db=at(100.0),
        error_1_khz_db=at(1000.0),
        error_10_khz_db=at(10_000.0),
        error_20_khz_db=at(20_000.0),
    )


def _bass(name: str) -> BassNetwork:
    if name == RIAA_BASS_NETWORK.name:
        return RIAA_BASS_NETWORK
    return next(item for item in BASS_NETWORKS if item.name == name)


def _treble(name: str) -> TrebleNetwork:
    return next(item for item in TREBLE_NETWORKS if item.name == name)


# Idealised families used to assess the switch positions. The historical
# families use P91's nominal 20 Hz low-bass assumption and nominal turnover.
CURVE_TARGETS: tuple[CurveTarget, ...] = (
    CurveTarget("FLAT", "Acoustic / Flat", "FLAT", "FLAT", None, None, None, notes="No replay equalisation."),
    CurveTarget("78-200-FLAT", "200 Hz bass / flat treble", "200 Hz", "FLAT", 20.0, 200.0, None),
    CurveTarget("78-200-1600", "200 Hz / 1600 Hz", "200 Hz", "1600 Hz", 20.0, 200.0, 1600.0),
    CurveTarget("78-200-3400", "200 Hz / 3400 Hz", "200 Hz", "3400 Hz", 20.0, 200.0, 3400.0),
    CurveTarget("78-200-5800", "200 Hz / 5800 Hz", "200 Hz", "5800 Hz", 20.0, 200.0, 5800.0),
    CurveTarget("78-400-FLAT", "400 Hz bass / flat treble", "400 Hz", "FLAT", 20.0, 400.0, None),
    CurveTarget("78-400-1600", "400 Hz / 1600 Hz", "400 Hz", "1600 Hz", 20.0, 400.0, 1600.0),
    CurveTarget("78-400-3400", "400 Hz / 3400 Hz", "400 Hz", "3400 Hz", 20.0, 400.0, 3400.0),
    CurveTarget("78-400-5800", "400 Hz / 5800 Hz", "400 Hz", "5800 Hz", 20.0, 400.0, 5800.0),
    CurveTarget("78-500-FLAT", "500 Hz bass / flat treble", "500 Hz 78", "FLAT", 20.0, 500.0, None),
    CurveTarget("78-500-1600", "500 Hz / 1600 Hz", "500 Hz 78", "1600 Hz", 20.0, 500.0, 1600.0),
    CurveTarget("78-500-3400", "500 Hz / 3400 Hz", "500 Hz 78", "3400 Hz", 20.0, 500.0, 3400.0),
    CurveTarget("78-500-5800", "500 Hz / 5800 Hz", "500 Hz 78", "5800 Hz", 20.0, 500.0, 5800.0),
    CurveTarget(
        "RIAA",
        "True RIAA",
        RIAA_BASS_NETWORK.name,
        "2121 Hz RIAA",
        50.05,
        500.5,
        2121.0,
        exact_standard=True,
        notes="Dedicated active branch plus 750 ohm / 100 nF passive treble network.",
    ),
)


# Practical label groupings from the P91 source table. These are user-facing
# starting points, not claims that every pressing followed the stated curve.
LABEL_RECOMMENDATIONS: tuple[LabelRecommendation, ...] = (
    LabelRecommendation("Acoustic", "FLAT", "FLAT"),
    LabelRecommendation("Brunswick / Parlophone", "500 Hz 78", "FLAT"),
    LabelRecommendation("Columbia 1925–1937", "200 Hz", "3400 Hz"),
    LabelRecommendation("Columbia late 1938", "400 Hz", "1600 Hz"),
    LabelRecommendation("Columbia English", "200 Hz", "FLAT", "P91 groups 250 Hz with 200 Hz."),
    LabelRecommendation("Decca early 1930s", "200 Hz", "5800 Hz", "Approximation to 150 Hz / 5.8 kHz."),
    LabelRecommendation("Decca 1934", "400 Hz", "1600 Hz", "Approximation to 375 Hz / 2 kHz."),
    LabelRecommendation("Decca 78", "200 Hz", "3400 Hz", "Approximation to 150 Hz / 3.4 kHz."),
    LabelRecommendation("Decca London ffrr 1949", "200 Hz", "5800 Hz", "Approximation to 250 Hz / 6.36 kHz."),
    LabelRecommendation("EMI 1931", "200 Hz", "FLAT"),
    LabelRecommendation("HMV / Blumlein", "200 Hz", "FLAT", "P91 groups 250 Hz with 200 Hz."),
    LabelRecommendation("Mercury", "400 Hz", "1600 Hz", "Approximation to 400 Hz / 2 kHz."),
    LabelRecommendation("MGM", "500 Hz 78", "1600 Hz", "Approximation to 500 Hz / 2 kHz."),
    LabelRecommendation("US mid-1930s", "400 Hz", "FLAT", "Try 500 Hz 78 where preferable by ear."),
    LabelRecommendation("Victor 1925", "400 Hz", "5800 Hz", "Approximation to 375 Hz / 6.36 kHz."),
    LabelRecommendation("Victor 1938–1952", "500 Hz 78", "3400 Hz"),
    LabelRecommendation("Victor 1947–1952", "500 Hz 78", "1600 Hz", "Approximation to 2 kHz treble."),
    LabelRecommendation("Westrex", "200 Hz", "FLAT"),
    LabelRecommendation("RIAA / CCIR LP", RIAA_BASS_NETWORK.name, "2121 Hz RIAA"),
)


def analyse_all_targets() -> tuple[CurveErrorSummary, ...]:
    return tuple(analyse_curve(target, _bass(target.bass_name), _treble(target.treble_name)) for target in CURVE_TARGETS)
