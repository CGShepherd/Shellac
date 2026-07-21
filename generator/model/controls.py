"""AE-009 SCH109 controls and user-interface engineering model."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ControlsStatus(str, Enum):
    DEFINED = "defined"
    ELECTRICALLY_CLOSED = "electrically_closed"


DESIGN_STATUS = ControlsStatus.ELECTRICALLY_CLOSED
LED_SERIES_RESISTANCE_OHM = 8_200.0
NOMINAL_RAIL_VOLTAGE_V = 18.0
ASSUMED_LED_FORWARD_V = 2.0
LED_CURRENT_A = (NOMINAL_RAIL_VOLTAGE_V - ASSUMED_LED_FORWARD_V) / LED_SERIES_RESISTANCE_OHM


@dataclass(frozen=True, slots=True)
class ControlDefinition:
    identifier: str
    name: str
    control_type: str
    positions: tuple[str, ...]
    electrical_function: str
    mounting: str = "Top-panel mounted"
    switching: str = "Break-before-make"


@dataclass(frozen=True, slots=True)
class IndicatorDefinition:
    identifier: str
    name: str
    rail: str
    resistor_ohm: float
    nominal_current_a: float
    mounting: str = "Top-panel mounted"


CONTROLS: tuple[ControlDefinition, ...] = (
    ControlDefinition(
        "SW901",
        "Bass characteristic",
        "2P5 rotary",
        ("FLAT", "200 Hz", "400 Hz", "500 Hz 78", "TRUE RIAA"),
        "Linked stereo selection of the complete SCH103 bass RS+C branches.",
    ),
    ControlDefinition(
        "SW902",
        "Treble characteristic",
        "2P5 rotary",
        ("FLAT", "1600 Hz", "2121 Hz RIAA", "3400 Hz", "5800 Hz"),
        "Linked stereo selection of the SCH103 passive treble networks.",
    ),
    ControlDefinition(
        "SW903",
        "Channel mode",
        "4P4T rotary",
        ("STEREO", "DUAL LEFT", "DUAL RIGHT", "L+R MONO"),
        "Controls the SCH105 passive routing and mono-averaging matrix.",
    ),
    ControlDefinition(
        "SW904",
        "Rumble filter",
        "2P2T toggle",
        ("FILTER", "BYPASS"),
        "Selects the filtered or direct SCH103 output for both channels.",
    ),
    ControlDefinition(
        "SW905",
        "Output mute",
        "2P2T toggle",
        ("PLAY", "MUTE"),
        "Selects MODE_L/R or 0VA at the THAT1646 inputs.",
    ),
)

INDICATORS: tuple[IndicatorDefinition, ...] = (
    IndicatorDefinition("LED901", "+18 V", "+18V", LED_SERIES_RESISTANCE_OHM, LED_CURRENT_A),
    IndicatorDefinition("LED902", "-18 V", "-18V", LED_SERIES_RESISTANCE_OHM, LED_CURRENT_A),
)


def validate_controls() -> None:
    assert DESIGN_STATUS is ControlsStatus.ELECTRICALLY_CLOSED
    assert len(CONTROLS) == 5
    assert len(INDICATORS) == 2
    assert [len(item.positions) for item in CONTROLS] == [5, 5, 4, 2, 2]
    assert CONTROLS[0].control_type == "2P5 rotary"
    assert CONTROLS[1].control_type == "2P5 rotary"
    assert CONTROLS[2].control_type == "4P4T rotary"
    assert 0.0018 < LED_CURRENT_A < 0.0021
