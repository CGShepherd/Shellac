"""AE-007 SCH105 channel-mode matrix engineering model.

The approved implementation uses a mechanically linked 4-pole, 4-position,
break-before-make rotary switch followed by one dual OPA1656 unity buffer.

Pole allocation:
- pole A selects the left output-buffer input;
- pole B selects the right output-buffer input;
- pole C connects left through its summing resistor only in L+R mode;
- pole D connects right through its summing resistor only in L+R mode.

This avoids a permanent resistor bridge between channels in stereo mode.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import log10, sqrt


class ModeMatrixStatus(str, Enum):
    DESIGNED = "designed"
    ELECTRICALLY_CLOSED = "electrically_closed"


class ChannelMode(str, Enum):
    STEREO = "stereo"
    DUAL_LEFT = "dual_left"
    DUAL_RIGHT = "dual_right"
    MONO_SUM = "mono_sum"


DESIGN_STATUS = ModeMatrixStatus.ELECTRICALLY_CLOSED
SWITCH_TYPE = "4P4T break-before-make rotary"
OPAMP = "OPA1656"
SUM_RESISTOR_OHM = 4_700.0
INPUT_BIAS_RESISTOR_OHM = 2_200_000.0
OUTPUT_ISOLATION_OHM = 100.0
BUFFER_GAIN = 1.0
DESIGN_OUTPUT_RMS_V = 10.0
SEVERE_INPUT_RMS_V = 6.42


@dataclass(frozen=True, slots=True)
class ModeTruth:
    mode: ChannelMode
    left_output_expression: str
    right_output_expression: str
    summing_network_connected: bool


MODE_TABLE: tuple[ModeTruth, ...] = (
    ModeTruth(ChannelMode.STEREO, "L", "R", False),
    ModeTruth(ChannelMode.DUAL_LEFT, "L", "L", False),
    ModeTruth(ChannelMode.DUAL_RIGHT, "R", "R", False),
    ModeTruth(ChannelMode.MONO_SUM, "(L+R)/2", "(L+R)/2", True),
)


def mono_average_gain_for_equal_inputs() -> float:
    """Account for two buffer-input bias resistors loading the averaging node."""
    source_thevenin = SUM_RESISTOR_OHM / 2.0
    load = INPUT_BIAS_RESISTOR_OHM / 2.0
    return load / (source_thevenin + load)


def mono_average_error_db() -> float:
    return 20.0 * log10(mono_average_gain_for_equal_inputs())


def mono_source_impedance_ohm() -> float:
    return SUM_RESISTOR_OHM / 2.0


def output_margin_db(input_rms_v: float = SEVERE_INPUT_RMS_V) -> float:
    if input_rms_v <= 0:
        raise ValueError("input_rms_v must be positive")
    return 20.0 * log10(DESIGN_OUTPUT_RMS_V / (input_rms_v * BUFFER_GAIN))


def resistor_noise_nv_per_rt_hz(resistance_ohm: float, temperature_k: float = 300.0) -> float:
    if resistance_ohm <= 0 or temperature_k <= 0:
        raise ValueError("resistance and temperature must be positive")
    k = 1.380649e-23
    return sqrt(4.0 * k * temperature_k * resistance_ohm) * 1e9


def validate_mode_matrix() -> None:
    assert DESIGN_STATUS is ModeMatrixStatus.ELECTRICALLY_CLOSED
    assert len(MODE_TABLE) == 4
    assert [item.mode for item in MODE_TABLE] == [
        ChannelMode.STEREO,
        ChannelMode.DUAL_LEFT,
        ChannelMode.DUAL_RIGHT,
        ChannelMode.MONO_SUM,
    ]
    assert sum(item.summing_network_connected for item in MODE_TABLE) == 1
    assert abs(mono_average_error_db()) < 0.03
    assert output_margin_db() > 3.8
