"""AE-008 SCH108 balanced-output and mute engineering model."""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from math import log10, sqrt

class OutputDriverStatus(str, Enum):
    ELECTRICALLY_CLOSED = "electrically_closed"

DESIGN_STATUS = OutputDriverStatus.ELECTRICALLY_CLOSED
DRIVER = "THAT1646"
PACKAGE = "SOIC-8"
SUPPLY_RAIL_V = 18.0
DIFFERENTIAL_GAIN_LINEAR = 2.0
DIFFERENTIAL_GAIN_DB = 20.0 * log10(DIFFERENTIAL_GAIN_LINEAR)
INPUT_IMPEDANCE_TYP_OHM = 5_000.0
OUTPUT_IMPEDANCE_PER_LEG_OHM = 50.0
DATASHEET_MAX_OUTPUT_RMS_V = 18.0
DESIGN_OUTPUT_RMS_V = 10.0
NOMINAL_INPUT_RMS_V = 0.321
SEVERE_INPUT_RMS_V = 3.21
MUTE_SWITCH = "2PDT break-before-make toggle"
COMMON_MODE_CAPACITANCE_UF = 10.0
RFI_CAPACITANCE_PF = 100.0
SURGE_DIODE = "1N4004"
DECOUPLING_HF_NF = 100.0
DECOUPLING_BULK_UF = 10.0

@dataclass(frozen=True, slots=True)
class OutputBudget:
    input_rms_v: float
    differential_output_rms_v: float
    differential_output_peak_v: float
    margin_to_design_ceiling_db: float

def output_budget(input_rms_v: float) -> OutputBudget:
    if input_rms_v < 0:
        raise ValueError("input_rms_v must be non-negative")
    output = input_rms_v * DIFFERENTIAL_GAIN_LINEAR
    peak = output * sqrt(2.0)
    margin = float("inf") if output == 0 else 20.0 * log10(DESIGN_OUTPUT_RMS_V / output)
    return OutputBudget(input_rms_v, output, peak, margin)

def validate_output_driver() -> None:
    assert DESIGN_STATUS is OutputDriverStatus.ELECTRICALLY_CLOSED
    assert DIFFERENTIAL_GAIN_LINEAR == 2.0
    nominal = output_budget(NOMINAL_INPUT_RMS_V)
    severe = output_budget(SEVERE_INPUT_RMS_V)
    assert abs(nominal.differential_output_rms_v - 0.642) < 1e-12
    assert abs(severe.differential_output_rms_v - 6.42) < 1e-12
    assert severe.margin_to_design_ceiling_db > 3.8
    assert severe.differential_output_rms_v < DATASHEET_MAX_OUTPUT_RMS_V
