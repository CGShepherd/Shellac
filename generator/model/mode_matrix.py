"""AE-041 SCH105 3P4T switched-summing channel-mode matrix engineering model.

The matrix eliminates the permanent L-R averaging bridge used by the superseded
DP4 architecture.  One 4.7 kOhm leg remains connected from the SCH104 left
OPA1656 output to MONO_AVG.  A third switch pole connects the right 4.7 kOhm leg
to MONO_AVG only in L+R mode.  Therefore no intentional conductive L-R path
exists in DUAL LEFT, STEREO or DUAL RIGHT.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from math import log10, sqrt

class ModeMatrixStatus(str, Enum):
    DESIGNED = "designed"
    ELECTRICALLY_CLOSED = "electrically_closed"
    QUALIFICATION_OPEN = "qualification_open"

class ChannelMode(str, Enum):
    DUAL_LEFT = "dual_left"
    STEREO = "stereo"
    MONO_SUM = "mono_sum"
    DUAL_RIGHT = "dual_right"

DESIGN_STATUS = ModeMatrixStatus.QUALIFICATION_OPEN
SWITCH_TYPE = "C&K A30403RNCB 3P4T break-before-make"
SWITCH_PREFERRED_MPN = "A30403RNCB"
SWITCH_FALLBACK_MPN = "TE/Alcoswitch MRJE3404"
OPAMP = "OPA1656"
SUM_RESISTOR_OHM = 4_700.0
SUM_RESISTOR_TOLERANCE_PERCENT = 0.1
INPUT_BIAS_RESISTOR_OHM = 2_200_000.0
DIRECT_SOURCE_ISOLATION_OHM = 100.0
BUFFER_GAIN = 1.0
DESIGN_OUTPUT_RMS_V = 10.0
SEVERE_INPUT_RMS_V = 6.42

@dataclass(frozen=True, slots=True)
class ModeTruth:
    mode: ChannelMode
    left_output_expression: str
    right_output_expression: str
    left_source: str
    right_source: str
    mono_right_leg_connected: bool

MODE_TABLE: tuple[ModeTruth, ...] = (
    ModeTruth(ChannelMode.DUAL_LEFT, "L", "L", "BUFFERED_L", "BUFFERED_L", False),
    ModeTruth(ChannelMode.STEREO, "L", "R", "BUFFERED_L", "BUFFERED_R", False),
    ModeTruth(ChannelMode.MONO_SUM, "(L+R)/2", "(L+R)/2", "MONO_AVG", "MONO_AVG", True),
    ModeTruth(ChannelMode.DUAL_RIGHT, "R", "R", "BUFFERED_R", "BUFFERED_R", False),
)

def mono_source_impedance_ohm() -> float:
    return SUM_RESISTOR_OHM / 2.0

def mono_load_ohm() -> float:
    return INPUT_BIAS_RESISTOR_OHM / 2.0

def mono_average_gain_for_equal_inputs() -> float:
    rs = mono_source_impedance_ohm()
    rl = mono_load_ohm()
    return rl / (rs + rl)

def mono_average_error_db() -> float:
    return 20.0 * log10(mono_average_gain_for_equal_inputs())

def direct_path_gain() -> float:
    return INPUT_BIAS_RESISTOR_OHM / (INPUT_BIAS_RESISTOR_OHM + DIRECT_SOURCE_ISOLATION_OHM)

def direct_path_error_db() -> float:
    return 20.0 * log10(direct_path_gain())

def mono_bridge_current_a(differential_rms_v: float) -> float:
    """RMS L-R current through the two 4.7 kOhm legs when L+R is selected."""
    if differential_rms_v < 0:
        raise ValueError("differential_rms_v must be non-negative")
    return differential_rms_v / (2.0 * SUM_RESISTOR_OHM)

def intentional_lr_bridge_present(mode: ChannelMode) -> bool:
    return next(row.mono_right_leg_connected for row in MODE_TABLE if row.mode is mode)

def output_margin_db(input_rms_v: float = SEVERE_INPUT_RMS_V) -> float:
    if input_rms_v <= 0:
        raise ValueError("input_rms_v must be positive")
    return 20.0 * log10(DESIGN_OUTPUT_RMS_V / (input_rms_v * BUFFER_GAIN))

def resistor_noise_nv_per_rt_hz(resistance_ohm: float, temperature_k: float = 300.0) -> float:
    if resistance_ohm <= 0 or temperature_k <= 0:
        raise ValueError("resistance and temperature must be positive")
    k = 1.380649e-23
    return sqrt(4.0*k*temperature_k*resistance_ohm)*1e9

def validate_mode_matrix() -> None:
    assert DESIGN_STATUS is ModeMatrixStatus.QUALIFICATION_OPEN
    assert SWITCH_TYPE.startswith("C&K A30403RNCB")
    assert [row.mode for row in MODE_TABLE] == [
        ChannelMode.DUAL_LEFT, ChannelMode.STEREO,
        ChannelMode.MONO_SUM, ChannelMode.DUAL_RIGHT,
    ]
    assert [row.mono_right_leg_connected for row in MODE_TABLE] == [False, False, True, False]
    assert not intentional_lr_bridge_present(ChannelMode.STEREO)
    assert abs(mono_average_error_db()) < 0.03
    assert abs(direct_path_error_db()) < 0.001
    assert output_margin_db() > 3.8
