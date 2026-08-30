"""Named-pin contracts for generated schematic symbols.

The contract is renderer-facing CAD data: it maps a semantic pin name to the
symbol pin number and local symbol coordinate.  Builders use semantic names
and never hard-code KiCad pin coordinates.

Coordinates are in millimetres relative to the symbol origin at zero rotation.
Positive x is right and positive y is down in the generated-sheet coordinate
system.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, radians, sin

from .geometry import Point
from .grid import align_point


@dataclass(frozen=True, slots=True)
class PinContract:
    number: str
    offset: Point


SYMBOL_PIN_CONTRACTS: dict[str, dict[str, PinContract]] = {
    "ProjectShellac:OpAmp_NonInv_Block": {
        "IN+": PinContract("1", Point(-11.43, 0.0)),
        "FB-": PinContract("2", Point(-2.54, -10.16)),
        "OUT": PinContract("3", Point(11.43, 0.0)),
        "+V": PinContract("4", Point(2.54, 10.16)),
        "-V": PinContract("5", Point(2.54, -10.16)),
    },
    "ProjectShellac:OpAmp_Buffer_Block": {
        "IN": PinContract("1", Point(-11.43, 0.0)),
        "OUT": PinContract("2", Point(11.43, 0.0)),
        "+V": PinContract("3", Point(2.54, -10.16)),
        "-V": PinContract("4", Point(2.54, 10.16)),
        "0VA": PinContract("5", Point(-2.54, 10.16)),
    },
    "ProjectShellac:DiffAmp_Block": {"IN+": PinContract("1", Point(-11.43, 2.54)), "IN-": PinContract("2", Point(-11.43, -2.54)), "OUT": PinContract("3", Point(11.43, 0.0)), "+V": PinContract("4", Point(2.54, 10.16)), "-V": PinContract("5", Point(2.54, -10.16))},
    "ProjectShellac:LT5400_Network": {
        "1": PinContract("1", Point(-12.70, -7.62)),
        "2": PinContract("2", Point(-12.70, -2.54)),
        "3": PinContract("3", Point(-12.70, 2.54)),
        "4": PinContract("4", Point(-12.70, 7.62)),
        "5": PinContract("5", Point(12.70, 7.62)),
        "6": PinContract("6", Point(12.70, 2.54)),
        "7": PinContract("7", Point(12.70, -2.54)),
        "8": PinContract("8", Point(12.70, -7.62)),
        "9": PinContract("9", Point(0.0, 12.70)),
    },
    "ProjectShellac:TestPoint": {
        "TP": PinContract("1", Point(0.0, -5.08)),
    },
    "ProjectShellac:Mode_Switch_Block": {
        "L_IN": PinContract("1", Point(-15.24, -7.62)),
        "R_IN": PinContract("2", Point(-15.24, 7.62)),
        "SUM_L": PinContract("3", Point(-5.08, -12.70)),
        "SUM_R": PinContract("4", Point(5.08, -12.70)),
        "MONO": PinContract("5", Point(0.0, 12.70)),
        "L_OUT": PinContract("6", Point(15.24, -5.08)),
        "R_OUT": PinContract("7", Point(15.24, 5.08)),
    },
    "ProjectShellac:Switch_Bypass_Block": {
        "L_DIRECT": PinContract("1", Point(-15.24, -7.62)),
        "L_FILTER": PinContract("2", Point(-15.24, -2.54)),
        "R_DIRECT": PinContract("3", Point(-15.24, 2.54)),
        "R_FILTER": PinContract("4", Point(-15.24, 7.62)),
        "L_OUT": PinContract("5", Point(15.24, -3.81)),
        "R_OUT": PinContract("6", Point(15.24, 3.81)),
    },
    "ProjectShellac:Balanced_Line_Driver_Block": {
        "OUT-": PinContract("1", Point(15.24, 5.08)),
        "SNS-": PinContract("2", Point(0.0, 12.70)),
        "GND": PinContract("3", Point(-5.08, 12.70)),
        "IN": PinContract("4", Point(-15.24, 0.0)),
        "-V": PinContract("5", Point(-5.08, -12.70)),
        "+V": PinContract("6", Point(5.08, -12.70)),
        "SNS+": PinContract("7", Point(5.08, 12.70)),
        "OUT+": PinContract("8", Point(15.24, -5.08)),
    },
    "ProjectShellac:Switch_Mute_Block": {
        "L_SIGNAL": PinContract("1", Point(-15.24, -7.62)),
        "L_MUTE": PinContract("2", Point(-15.24, -2.54)),
        "R_SIGNAL": PinContract("3", Point(-15.24, 2.54)),
        "R_MUTE": PinContract("4", Point(-15.24, 7.62)),
        "L_OUT": PinContract("5", Point(15.24, -3.81)),
        "R_OUT": PinContract("6", Point(15.24, 3.81)),
    },
    "ProjectShellac:Panel_Control_Block": {
        "CONTROL": PinContract("1", Point(0.0, 10.16)),
    },
    "ProjectShellac:Hierarchy_Port_Anchor": {
        "PORT": PinContract("1", Point(-5.08, 0.0)),
    },
    "ProjectShellac:Power_Rail_Source": {
        "POWER_OUT": PinContract("1", Point(-5.08, 0.0)),
    },
    "ProjectShellac:Panel_LED_Block": {
        "A": PinContract("1", Point(0.0, -8.89)),
        "K": PinContract("2", Point(0.0, 8.89)),
    },
    "ProjectShellac:Bass_Select_Block": {
        "COMMON": PinContract("1", Point(15.24, 0.0)),
        "OUT": PinContract("2", Point(-15.24, -10.16)),
        "B200": PinContract("3", Point(-15.24, -5.08)),
        "B400": PinContract("4", Point(-15.24, 0.0)),
        "B500": PinContract("5", Point(-15.24, 5.08)),
        "RIAA": PinContract("6", Point(-15.24, 10.16)),
    },
    "ProjectShellac:Treble_Select_Block": {
        "COMMON": PinContract("1", Point(-15.24, 0.0)),
        "T1600": PinContract("2", Point(15.24, -7.62)),
        "T2121": PinContract("3", Point(15.24, -2.54)),
        "T3400": PinContract("4", Point(15.24, 2.54)),
        "T5800": PinContract("5", Point(15.24, 7.62)),
    },
    "Connector_Generic:Conn_01x03": {
        "1": PinContract("1", Point(-5.08, -2.54)),
        "2": PinContract("2", Point(-5.08, 0.0)),
        "3": PinContract("3", Point(-5.08, 2.54)),
    },
    "Connector_Generic:Conn_01x06": {
        "1": PinContract("1", Point(-5.08, -6.35)),
        "2": PinContract("2", Point(-5.08, -3.81)),
        "3": PinContract("3", Point(-5.08, -1.27)),
        "4": PinContract("4", Point(-5.08, 1.27)),
        "5": PinContract("5", Point(-5.08, 3.81)),
        "6": PinContract("6", Point(-5.08, 6.35)),
    },
    "Connector_Generic:Conn_01x05": {"1": PinContract("1", Point(-5.08, -5.08)), "2": PinContract("2", Point(-5.08, -2.54)), "3": PinContract("3", Point(-5.08, 0.0)), "4": PinContract("4", Point(-5.08, 2.54)), "5": PinContract("5", Point(-5.08, 5.08))},
    "Device:Ferrite_Bead": {
        "1": PinContract("1", Point(-2.54, 0.0)),
        "2": PinContract("2", Point(2.54, 0.0)),
    },
    "Device:D": {
        "K": PinContract("1", Point(-2.54, 0.0)),
        "A": PinContract("2", Point(2.54, 0.0)),
    },
    "Device:R": {
        "1": PinContract("1", Point(-2.54, 0.0)),
        "2": PinContract("2", Point(2.54, 0.0)),
    },
    "Device:C": {
        "1": PinContract("1", Point(0.0, -2.54)),
        "2": PinContract("2", Point(0.0, 2.54)),
    },
}

_DIP_Y = (-8.89, -6.35, -3.81, -1.27, 1.27, 3.81, 6.35, 8.89)
SYMBOL_PIN_CONTRACTS["ProjectShellac:DIP_Switch_Block"] = {
    name: contract
    for index, y in enumerate(_DIP_Y, start=1)
    for name, contract in (
        (f"{index}A", PinContract(str(index), Point(-17.78, y))),
        (f"{index}B", PinContract(str(17 - index), Point(17.78, y))),
    )
}


def pin_contract(lib_id: str, pin_name: str) -> PinContract:
    try:
        return SYMBOL_PIN_CONTRACTS[lib_id][pin_name]
    except KeyError as exc:
        raise KeyError(f"No named-pin contract for {lib_id!r} pin {pin_name!r}.") from exc


def pin_position(component, pin_name: str) -> Point:
    contract = pin_contract(component.lib_id, pin_name)
    angle = radians(component.rotation)
    x = contract.offset.x * cos(angle) - contract.offset.y * sin(angle)
    # KiCad library-symbol Y coordinates use the opposite sign to sheet Y.
    # Positive instance rotation also rotates a left-pointing local pin down.
    y = -(contract.offset.x * sin(angle) + contract.offset.y * cos(angle))
    return align_point(Point(component.at.x + x, component.at.y + y))


def pin_number(lib_id: str, pin_name: str) -> str:
    return pin_contract(lib_id, pin_name).number
