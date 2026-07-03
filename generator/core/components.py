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

def resistor(ref, value, at, tolerance="", function=""):
    fields = {}
    if tolerance:
        fields["Tolerance"] = tolerance
    if function:
        fields["Function"] = function
    return Component(ref, "ProjectShellac:R", value, at, "Resistor_SMD:R_0805_2012Metric", fields)

def capacitor(ref, value, at, dielectric="", voltage="", function="", dnp=False):
    fields = {}
    if dielectric:
        fields["Dielectric"] = dielectric
    if voltage:
        fields["Voltage"] = voltage
    if function:
        fields["Function"] = function
    if dnp:
        fields["DNP"] = "YES"
    return Component(ref, "ProjectShellac:C", value, at, "Capacitor_SMD:C_0805_2012Metric", fields, dnp=dnp)

def testpoint(ref, label, at):
    return Component(ref, "ProjectShellac:TestPoint", label, at, "TestPoint:TestPoint_Pad_D1.5mm", in_bom=False)
