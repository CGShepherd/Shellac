"""AE-004 electrical closure calculations for SCH103.

The calculations deliberately distinguish:
- shape accuracy, already closed by AE-003;
- absolute gain and overload;
- conservative design limits rather than absolute-maximum operation.

No claim is made that a record produces equal amplitude at all frequencies.
The frequency-dependent cartridge-input limits are test-envelope values.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import log10, pi, sqrt

from .replay_eq import (
    BASS_NETWORKS,
    NOMINAL_CARTRIDGE_RMS_V,
    OPA1612_DESIGN_OUTPUT_RMS_V,
    RECOVERY_GAIN,
    RIAA_BASS_NETWORK,
    SCH101_DEFAULT_GAIN,
    TREBLE_NETWORKS,
    BassNetwork,
    TrebleNetwork,
)
from .replay_curve_analysis import realised_bass_transfer, realised_treble_transfer


@dataclass(frozen=True, slots=True)
class ElectricalPoint:
    curve_name: str
    frequency_hz: float
    active_lf_gain: float
    passive_hf_gain: float
    recovery_gain: float
    sch103_gain: float
    max_cartridge_input_rms_v: float
    nominal_active_output_rms_v: float
    nominal_sch103_output_rms_v: float


def db(value: float) -> float:
    if value <= 0:
        raise ValueError("value must be positive")
    return 20.0 * log10(value)


def johnson_noise_nv_per_rt_hz(resistance_ohm: float, temperature_k: float = 300.0) -> float:
    if resistance_ohm <= 0 or temperature_k <= 0:
        raise ValueError("resistance and temperature must be positive")
    k = 1.380649e-23
    return sqrt(4.0 * k * temperature_k * resistance_ohm) * 1e9


def recovery_gain() -> float:
    return RECOVERY_GAIN


def electrical_point(
    name: str,
    bass: BassNetwork,
    treble: TrebleNetwork,
    frequency_hz: float,
) -> ElectricalPoint:
    if frequency_hz <= 0:
        raise ValueError("frequency_hz must be positive")
    s = 1j * 2.0 * pi * frequency_hz
    lf = abs(realised_bass_transfer(s, bass))
    hf = abs(realised_treble_transfer(s, treble))
    sch103 = lf * hf * RECOVERY_GAIN

    # The first active LF stage is the limiting node before passive attenuation
    # and recovery.  The cartridge limit includes the default SCH101 gain.
    max_input = OPA1612_DESIGN_OUTPUT_RMS_V / (SCH101_DEFAULT_GAIN * lf)
    nominal_active = NOMINAL_CARTRIDGE_RMS_V * SCH101_DEFAULT_GAIN * lf
    nominal_sch103 = NOMINAL_CARTRIDGE_RMS_V * SCH101_DEFAULT_GAIN * sch103
    return ElectricalPoint(
        name,
        frequency_hz,
        lf,
        hf,
        RECOVERY_GAIN,
        sch103,
        max_input,
        nominal_active,
        nominal_sch103,
    )


def _treble(name: str) -> TrebleNetwork:
    return next(item for item in TREBLE_NETWORKS if item.name == name)


def closure_points() -> tuple[ElectricalPoint, ...]:
    points: list[ElectricalPoint] = []
    for bass in BASS_NETWORKS[1:]:
        for frequency in (20.0, 50.0, 1000.0, 20_000.0):
            points.append(electrical_point(bass.name, bass, _treble("FLAT"), frequency))
    for frequency in (20.0, 50.0, 1000.0, 20_000.0):
        points.append(electrical_point("TRUE RIAA", RIAA_BASS_NETWORK, _treble("2121 Hz RIAA"), frequency))
    return tuple(points)


def worst_case_point() -> ElectricalPoint:
    return min(closure_points(), key=lambda item: item.max_cartridge_input_rms_v)


def validate_electrical_closure() -> None:
    assert abs(RECOVERY_GAIN - 2.1) < 1e-12
    worst = worst_case_point()
    assert worst.max_cartridge_input_rms_v > 0.030
    assert worst.nominal_active_output_rms_v < 2.0
    assert johnson_noise_nv_per_rt_hz(100_000.0) < 41.0
