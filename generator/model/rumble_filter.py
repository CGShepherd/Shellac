"""AE-005 SCH107 rumble-filter engineering model.

The approved implementation is a stereo, switchable, fourth-order Butterworth
high-pass filter with a nominal 15 Hz -3 dB frequency.  Each channel uses two
unity-gain Sallen-Key sections implemented with OPA1656.

For a unity-gain high-pass Sallen-Key section with C1 = C2 = C:

    H(s) = R1*R2*C^2*s^2 /
           (R1*R2*C^2*s^2 + 2*R1*C*s + 1)

and:

    f0 = 1 / (2*pi*C*sqrt(R1*R2))
    Q  = 0.5*sqrt(R2/R1)

The two Butterworth Q values are 0.541196 and 1.306563.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import atan2, log10, pi, sqrt
import cmath


class RumbleFilterStatus(str, Enum):
    DESIGNED = "designed"
    ELECTRICALLY_CLOSED = "electrically_closed"


DESIGN_STATUS = RumbleFilterStatus.ELECTRICALLY_CLOSED
FILTER_ORDER = 4
TARGET_CUTOFF_HZ = 15.0
CAPACITANCE_F = 470e-9
CAPACITANCE_VALUE = "470n"
OPAMP = "OPA1656"
BYPASS_SWITCH = "2P2T break-before-make"
OUTPUT_ISOLATION_OHM = 100.0


@dataclass(frozen=True, slots=True)
class HighPassSection:
    identifier: str
    target_q: float
    r1_ohm: float
    r2_ohm: float
    capacitance_f: float = CAPACITANCE_F

    @property
    def realised_f0_hz(self) -> float:
        return 1.0 / (
            2.0 * pi * self.capacitance_f * sqrt(self.r1_ohm * self.r2_ohm)
        )

    @property
    def realised_q(self) -> float:
        return 0.5 * sqrt(self.r2_ohm / self.r1_ohm)


SECTIONS: tuple[HighPassSection, ...] = (
    HighPassSection("A", 0.5411961, 20_800.0, 24_300.0),
    HighPassSection("B", 1.3065630, 8_660.0, 59_000.0),
)


def section_transfer(section: HighPassSection, frequency_hz: float) -> complex:
    if frequency_hz <= 0:
        raise ValueError("frequency_hz must be positive")
    s = 1j * 2.0 * pi * frequency_hz
    c = section.capacitance_f
    numerator = section.r1_ohm * section.r2_ohm * c * c * s * s
    denominator = numerator + 2.0 * section.r1_ohm * c * s + 1.0
    return numerator / denominator


def filter_transfer(frequency_hz: float) -> complex:
    result = 1.0 + 0.0j
    for section in SECTIONS:
        result *= section_transfer(section, frequency_hz)
    return result


def magnitude_db(frequency_hz: float) -> float:
    magnitude = abs(filter_transfer(frequency_hz))
    return 20.0 * log10(magnitude)


def phase_degrees(frequency_hz: float) -> float:
    value = filter_transfer(frequency_hz)
    return atan2(value.imag, value.real) * 180.0 / pi


def attenuation_improvement_factor(frequency_hz: float) -> float:
    return 1.0 / abs(filter_transfer(frequency_hz))


def validate_rumble_filter() -> None:
    assert DESIGN_STATUS is RumbleFilterStatus.ELECTRICALLY_CLOSED
    assert FILTER_ORDER == 4
    assert len(SECTIONS) == 2
    assert all(abs(section.realised_f0_hz - TARGET_CUTOFF_HZ) < 0.15 for section in SECTIONS)
    assert all(abs(section.realised_q - section.target_q) < 0.01 for section in SECTIONS)

    # Wanted-band preservation and infrasonic rejection.
    assert magnitude_db(20.0) > -0.50
    assert magnitude_db(30.0) > -0.05
    assert magnitude_db(10.0) < -14.0
    assert magnitude_db(5.0) < -38.0
    assert magnitude_db(0.55) < -110.0
