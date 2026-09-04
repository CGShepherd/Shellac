"""AE-040B / AE-009 SCH109 controls and user-interface engineering model."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class ControlsStatus(str, Enum):
    DEFINED = "defined"
    ELECTRICALLY_CLOSED = "electrically_closed"
    PLATFORM_SELECTED_PROCUREMENT_OPEN = "platform_selected_procurement_open"
    PHYSICAL_HARDWARE_SELECTED = "physical_hardware_selected"

DESIGN_STATUS = ControlsStatus.PLATFORM_SELECTED_PROCUREMENT_OPEN
LED_SERIES_RESISTANCE_OHM = 8_200.0
NOMINAL_RAIL_VOLTAGE_V = 18.0
ASSUMED_LED_FORWARD_V = 2.4
LED_CURRENT_A = (NOMINAL_RAIL_VOLTAGE_V - ASSUMED_LED_FORWARD_V) / LED_SERIES_RESISTANCE_OHM
ROTARY_MANUFACTURER = "Lorlin"
ROTARY_PLATFORM = "PT"
ROTARY_BASS_TREBLE_MPN = "OPEN — Lorlin PT gold-contact 2P5 BBM order code required"
ROTARY_MODE_MPN = "OPEN — Lorlin PT gold-contact two-wafer 4P4 BBM order code required"
TOGGLE_MANUFACTURER = "C&K"
TOGGLE_MPN = "7201SYCBE"
LED_MANUFACTURER = "Vishay"
LED_MPN = "TLLG4401"
LED_BEZEL_MANUFACTURER = "Arcolectric / Bulgin"
LED_BEZEL_MPN = "A104700BLACK"

@dataclass(frozen=True, slots=True)
class ControlDefinition:
    identifier: str
    name: str
    control_type: str
    positions: tuple[str, ...]
    electrical_function: str
    manufacturer: str
    mpn: str
    mounting: str = ("PCB through-hole with threaded bushing through top cover; "
                     "PCB/standoffs define geometry and bushing is a secondary structural connection")
    switching: str = "Break-before-make"

@dataclass(frozen=True, slots=True)
class IndicatorDefinition:
    identifier: str
    name: str
    rail: str
    resistor_ohm: float
    nominal_current_a: float
    manufacturer: str = LED_MANUFACTURER
    mpn: str = LED_MPN
    bezel_manufacturer: str = LED_BEZEL_MANUFACTURER
    bezel_mpn: str = LED_BEZEL_MPN
    mounting: str = ("Audio-chassis top cover, central longitudinal spine, "
                     "panel-mounted black brass bezel, short flying leads")

CONTROLS = (
    ControlDefinition("SW901", "Bass characteristic", "2P5 rotary",
        ("FLAT", "200 Hz", "400 Hz", "500 Hz 78", "TRUE RIAA"),
        "Linked stereo selection of the complete SCH103 bass RS+C branches.", ROTARY_MANUFACTURER, ROTARY_BASS_TREBLE_MPN),
    ControlDefinition("SW902", "Treble characteristic", "2P5 rotary",
        ("FLAT", "1600 Hz", "2121 Hz RIAA", "3400 Hz", "5800 Hz"),
        "Linked stereo selection of the SCH103 passive treble networks.", ROTARY_MANUFACTURER, ROTARY_BASS_TREBLE_MPN),
    ControlDefinition("SW903", "Channel mode", "4P4 rotary realised as two synchronised 2-pole PT wafers",
        ("STEREO", "DUAL LEFT", "DUAL RIGHT", "L+R MONO"),
        "Controls the SCH105 passive routing and mono-averaging matrix.", ROTARY_MANUFACTURER, ROTARY_MODE_MPN),
    ControlDefinition("SW904", "Rumble filter", "2P2T toggle", ("FILTER", "BYPASS"),
        "Selects the filtered or direct SCH103 output for both channels.", TOGGLE_MANUFACTURER, TOGGLE_MPN),
    ControlDefinition("SW905", "Output mute", "2P2T toggle", ("PLAY", "MUTE"),
        "Selects MODE_L/R or 0VA at the THAT1646 inputs.", TOGGLE_MANUFACTURER, TOGGLE_MPN),
)
INDICATORS = (
    IndicatorDefinition("LED901", "+18 V", "+18V", LED_SERIES_RESISTANCE_OHM, LED_CURRENT_A),
    IndicatorDefinition("LED902", "-18 V", "-18V", LED_SERIES_RESISTANCE_OHM, LED_CURRENT_A),
)

def validate_controls() -> None:
    assert DESIGN_STATUS is ControlsStatus.PLATFORM_SELECTED_PROCUREMENT_OPEN
    assert len(CONTROLS) == 5 and len(INDICATORS) == 2
    assert [len(x.positions) for x in CONTROLS] == [5,5,4,2,2]
    assert CONTROLS[0].mpn == CONTROLS[1].mpn == ROTARY_BASS_TREBLE_MPN
    assert CONTROLS[2].mpn == ROTARY_MODE_MPN
    assert all(x.manufacturer == ROTARY_MANUFACTURER for x in CONTROLS[:3])
    assert all(x.mpn.startswith("OPEN") for x in CONTROLS[:3])
    assert CONTROLS[3].mpn == CONTROLS[4].mpn == TOGGLE_MPN
    assert all("secondary structural connection" in x.mounting for x in CONTROLS)
    assert 0.0018 < LED_CURRENT_A < 0.0020
    assert all(x.mpn == LED_MPN and x.bezel_mpn == LED_BEZEL_MPN for x in INDICATORS)
