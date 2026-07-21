"""Analysis helpers for AE-007 SCH105."""

from __future__ import annotations

from dataclasses import dataclass

from .mode_matrix import (
    MODE_TABLE,
    INPUT_BIAS_RESISTOR_OHM,
    SUM_RESISTOR_OHM,
    mono_average_error_db,
    mono_average_gain_for_equal_inputs,
    mono_source_impedance_ohm,
    output_margin_db,
    resistor_noise_nv_per_rt_hz,
)


@dataclass(frozen=True, slots=True)
class MatrixAnalysis:
    mono_gain: float
    mono_error_db: float
    mono_source_impedance_ohm: float
    severe_output_margin_db: float
    summing_resistor_noise_nv_per_rt_hz: float


def analyse_mode_matrix() -> MatrixAnalysis:
    return MatrixAnalysis(
        mono_gain=mono_average_gain_for_equal_inputs(),
        mono_error_db=mono_average_error_db(),
        mono_source_impedance_ohm=mono_source_impedance_ohm(),
        severe_output_margin_db=output_margin_db(),
        summing_resistor_noise_nv_per_rt_hz=resistor_noise_nv_per_rt_hz(
            mono_source_impedance_ohm()
        ),
    )
