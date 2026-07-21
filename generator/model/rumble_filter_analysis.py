"""Analysis helpers for AE-005 SCH107."""

from __future__ import annotations

from dataclasses import dataclass
from math import pi
from typing import Iterable

from .rumble_filter import (
    SECTIONS,
    filter_transfer,
    magnitude_db,
    phase_degrees,
)


@dataclass(frozen=True, slots=True)
class ResponsePoint:
    frequency_hz: float
    magnitude_db: float
    phase_degrees: float


REPORT_FREQUENCIES_HZ: tuple[float, ...] = (
    0.55, 1.0, 5.0, 10.0, 15.0, 20.0, 30.0, 50.0, 100.0, 1000.0, 20_000.0
)


def response_points(
    frequencies_hz: Iterable[float] = REPORT_FREQUENCIES_HZ,
) -> tuple[ResponsePoint, ...]:
    return tuple(
        ResponsePoint(
            frequency_hz=f,
            magnitude_db=magnitude_db(f),
            phase_degrees=phase_degrees(f),
        )
        for f in frequencies_hz
    )


def approximate_group_delay_seconds(frequency_hz: float, fractional_step: float = 1e-4) -> float:
    """Numerically estimate -d(phi)/d(omega) around one frequency."""
    if frequency_hz <= 0:
        raise ValueError("frequency_hz must be positive")
    if fractional_step <= 0:
        raise ValueError("fractional_step must be positive")

    f1 = frequency_hz * (1.0 - fractional_step)
    f2 = frequency_hz * (1.0 + fractional_step)
    h1 = filter_transfer(f1)
    h2 = filter_transfer(f2)

    # Phase ratio avoids a 360-degree discontinuity for the small local step.
    local_phase_change = __import__("cmath").phase(h2 / h1)
    domega = 2.0 * pi * (f2 - f1)
    return -local_phase_change / domega
