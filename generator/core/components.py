from dataclasses import dataclass, field
from typing import Dict
from .geometry import Point

@dataclass
class Component:
    ref: str
    lib_id: str
    value: str
    at: Point
    footprint: str = ""
    fields: Dict[str, str] = field(default_factory=dict)
    dnp: bool = False
    in_bom: bool = True
    on_board: bool = True
    rotation: float = 0.0

def resistor(ref, value, at, tolerance="", function="", rotation=0.0):
    fields = {}
    if tolerance: fields["Tolerance"] = tolerance
    if function: fields["Function"] = function
    return Component(ref, "Device:R", value, at, "Resistor_SMD:R_0805_2012Metric", fields, rotation=rotation)

def capacitor(ref, value, at, dielectric="", voltage="", function="", dnp=False, rotation=0.0, footprint="Capacitor_SMD:C_0805_2012Metric"):
    """Create a capacitor with an explicit, overridable physical footprint.

    The 0805 default preserves existing schematic behaviour, while bulk,
    film, and high-capacitance parts can declare their actual package at the
    source instead of being corrected downstream in PCB tooling.
    """
    fields = {}
    if dielectric: fields["Dielectric"] = dielectric
    if voltage: fields["Voltage"] = voltage
    if function: fields["Function"] = function
    if dnp: fields["DNP"] = "YES"
    return Component(ref, "Device:C", value, at, footprint, fields, dnp=dnp, rotation=rotation)

def testpoint(ref, label, at):
    return Component(ref, "ProjectShellac:TestPoint", label, at, "TestPoint:TestPoint_Pad_D1.5mm", in_bom=False)

def xlr3(ref, label, at, function="Balanced XLR input"):
    return Component(
        ref, "Connector_Generic:Conn_01x03", label, at, "",
        {"Function": function, "Pin 1": "CHASSIS", "Pin 2": "HOT/+",
         "Pin 3": "COLD/-", "Ownership": "Panel-mounted; harnessed to PCB"},
        on_board=False,
    )


def jst_vh_3(ref, label, at, function="Panel audio harness interface", rotation=0.0):
    return Component(
        ref, "Connector_Generic:Conn_01x03", label, at,
        "Connector_JST:JST_VH_B3P-VH_1x03_P3.96mm_Vertical",
        {"Function": function, "Connector family": "JST VH",
         "Pin 1": "CHASSIS/SHIELD", "Pin 2": "HOT/+", "Pin 3": "COLD/-"},
        rotation=rotation,
    )


def minifit_6(ref, label, at, function="Regulated DC harness interface", rotation=0.0):
    return Component(
        ref, "Connector_Generic:Conn_01x06", label, at,
        "Connector_Molex:Molex_Mini-Fit_Jr_5566-06A2_2x03_P4.20mm_Vertical",
        {"Function": function, "Connector family": "Molex Mini-Fit Jr",
         "Pin 1": "0VA", "Pin 2": "+18VA_IN", "Pin 3": "-18VA_IN",
         "Pin 4": "CHASSIS", "Pin 5": "RESERVED", "Pin 6": "KEY/NC"},
        rotation=rotation,
    )

def opa1656_gain_block(ref, label, at, function="JFET input non-inverting gain stage"):
    return Component(ref, "ProjectShellac:OpAmp_NonInv_Block", label, at,
        "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm",
        {"Function": function, "Intended Device": "OPA1656 / OPA1655 class",
         "Topology": "Non-inverting gain", "Gain": "4x / +12 dB"})

def diff_converter_block(ref, label, at, function="Precision differential converter"):
    return Component(ref, "ProjectShellac:DiffAmp_Block", label, at,
        "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm",
        {"Function": function, "Intended Device": "OPA1656 / OPA1655 class",
         "Topology": "Four-resistor precision differential amplifier",
         "Gain": "External LT5400 network defines gain",
         "Resistor Network": "LT5400-7 A-grade"})


def lt5400_network(ref,label,at):
    return Component(ref,"ProjectShellac:LT5400_Network",label,at,"Package_SO:MSOP-8-1EP_3x3mm_P0.65mm_EP1.68x1.88mm",{"Function":"DR-038 matched resistor network","Device":"LT5400-7 A-grade","R1/R4":"5k","R2/R3":"1.25k","EP":"Pin 9 floating"})
