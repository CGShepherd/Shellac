"""AE-002 transfer-function engine for P06/P91 replay networks."""

from __future__ import annotations

from dataclasses import dataclass
from math import atan2, log10, pi
import cmath


@dataclass(frozen=True, slots=True)
class ActiveNetworkResponse:
    pole_hz: float
    zero_hz: float
    dc_gain: float
    hf_gain: float
    shelf_db: float


def _positive(name: str, value: float) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be positive.")


def active_feedback_impedance(s: complex, rf_ohm: float, rs_ohm: float, capacitance_f: float) -> complex:
    _positive("rf_ohm", rf_ohm)
    _positive("rs_ohm", rs_ohm)
    _positive("capacitance_f", capacitance_f)
    series_branch = rs_ohm + 1.0 / (s * capacitance_f)
    return (rf_ohm * series_branch) / (rf_ohm + series_branch)


def active_stage_transfer(s: complex, rf_ohm: float, rs_ohm: float, rg_ohm: float, capacitance_f: float) -> complex:
    _positive("rg_ohm", rg_ohm)
    return 1.0 + active_feedback_impedance(s, rf_ohm, rs_ohm, capacitance_f) / rg_ohm


def active_network_response(rf_ohm: float, rs_ohm: float, rg_ohm: float, capacitance_f: float) -> ActiveNetworkResponse:
    for name, value in (("rf_ohm", rf_ohm), ("rs_ohm", rs_ohm), ("rg_ohm", rg_ohm), ("capacitance_f", capacitance_f)):
        _positive(name, value)

    pole_hz = 1.0 / (2.0 * pi * capacitance_f * (rf_ohm + rs_ohm))
    zero_tau = capacitance_f * (rg_ohm * (rf_ohm + rs_ohm) + rf_ohm * rs_ohm) / (rg_ohm + rf_ohm)
    zero_hz = 1.0 / (2.0 * pi * zero_tau)
    dc_gain = 1.0 + rf_ohm / rg_ohm
    hf_gain = 1.0 + ((rf_ohm * rs_ohm) / (rf_ohm + rs_ohm)) / rg_ohm
    shelf_db = 20.0 * log10(dc_gain / hf_gain)
    return ActiveNetworkResponse(pole_hz, zero_hz, dc_gain, hf_gain, shelf_db)


def frequency_response(frequency_hz: float, rf_ohm: float, rs_ohm: float, rg_ohm: float, capacitance_f: float) -> tuple[float, float]:
    _positive("frequency_hz", frequency_hz)
    value = active_stage_transfer(1j * 2.0 * pi * frequency_hz, rf_ohm, rs_ohm, rg_ohm, capacitance_f)
    return 20.0 * log10(abs(value)), atan2(value.imag, value.real) * 180.0 / pi


def solve_series_resistor_for_break_ratio(rf_ohm: float, rg_ohm: float, ratio_zero_to_pole: float) -> float:
    """Solve RS for a requested zero/pole frequency ratio.

    Derived from the exact P06/P91 non-inverting transfer function.
    """
    for name, value in (("rf_ohm", rf_ohm), ("rg_ohm", rg_ohm), ("ratio_zero_to_pole", ratio_zero_to_pole)):
        _positive(name, value)
    numerator = (rf_ohm + rg_ohm) * rf_ohm - ratio_zero_to_pole * rg_ohm * rf_ohm
    denominator = ratio_zero_to_pole * (rf_ohm + rg_ohm) - (rf_ohm + rg_ohm)
    rs = numerator / denominator
    if rs <= 0:
        raise ValueError("Requested break ratio is not realisable with positive RS.")
    return rs


def solve_capacitance_for_pole(rf_ohm: float, rs_ohm: float, pole_hz: float) -> float:
    for name, value in (("rf_ohm", rf_ohm), ("rs_ohm", rs_ohm), ("pole_hz", pole_hz)):
        _positive(name, value)
    return 1.0 / (2.0 * pi * pole_hz * (rf_ohm + rs_ohm))


def logarithmic_frequencies(start_hz: float = 10.0, stop_hz: float = 50_000.0, points: int = 401) -> tuple[float, ...]:
    _positive("start_hz", start_hz)
    _positive("stop_hz", stop_hz)
    if stop_hz <= start_hz:
        raise ValueError("stop_hz must exceed start_hz.")
    if points < 2:
        raise ValueError("points must be at least 2.")
    start_log = log10(start_hz)
    step = (log10(stop_hz) - start_log) / (points - 1)
    return tuple(10.0 ** (start_log + index * step) for index in range(points))
