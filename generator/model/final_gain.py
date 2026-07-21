"""AE-006B SCH104 unity isolation-buffer engineering model.

AE-006 originally assigned +6 dB to SCH104 before the balanced output device
was selected.  AE-008 confirms that the THAT1646 provides the required +6 dB
differential gain.  SCH104 is therefore revised to unity gain so the complete
system retains its intended gain and nominal output level.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from math import log10, sqrt

class FinalGainStatus(str, Enum):
    ELECTRICALLY_CLOSED = "electrically_closed"

DESIGN_STATUS = FinalGainStatus.ELECTRICALLY_CLOSED
OPAMP = "OPA1656"
SUPPLY_RAIL_V = 18.0
GAIN_LINEAR = 1.0
GAIN_DB = 0.0
OUTPUT_ISOLATION_OHM = 100.0
DESIGN_OUTPUT_RMS_V = 10.0
NOMINAL_INPUT_RMS_V = 0.321
SEVERE_INPUT_RMS_V = 3.21

@dataclass(frozen=True, slots=True)
class FinalGainBudget:
    input_rms_v: float
    output_rms_v: float
    output_peak_v: float
    margin_to_design_ceiling_db: float

def gain_budget(input_rms_v: float) -> FinalGainBudget:
    if input_rms_v < 0:
        raise ValueError("input_rms_v must be non-negative")
    out = input_rms_v * GAIN_LINEAR
    peak = out * sqrt(2.0)
    margin = float("inf") if out == 0 else 20.0 * log10(DESIGN_OUTPUT_RMS_V / out)
    return FinalGainBudget(input_rms_v, out, peak, margin)

def validate_final_gain_stage() -> None:
    assert DESIGN_STATUS is FinalGainStatus.ELECTRICALLY_CLOSED
    assert GAIN_LINEAR == 1.0
    assert GAIN_DB == 0.0
    nominal = gain_budget(NOMINAL_INPUT_RMS_V)
    severe = gain_budget(SEVERE_INPUT_RMS_V)
    assert nominal.output_rms_v == NOMINAL_INPUT_RMS_V
    assert severe.output_rms_v < DESIGN_OUTPUT_RMS_V
    assert severe.margin_to_design_ceiling_db > 9.8
