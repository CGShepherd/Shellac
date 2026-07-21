"""Project Shellac Gate 3 interconnect and harness architecture.

This module records mechanical ownership, connector families, cable classes,
shield termination, crimp-tool compatibility and harness verification rules.
It does not modify the frozen electrical topology.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum


class HarnessClass(str, Enum):
    MICROVOLT_ANALOGUE = "microvolt_analogue"
    LINE_LEVEL_ANALOGUE = "line_level_analogue"
    CONTROL = "control"
    INDICATOR = "indicator"
    REGULATED_POWER = "regulated_power"


class ConnectorFamily(str, Enum):
    JST_VH = "JST_VH_3.96mm"
    MINI_FIT_JR = "Molex_Mini-Fit_Jr_4.2mm"
    NEUTRIK_XLR5 = "Neutrik_XLR5"


@dataclass(frozen=True, slots=True)
class CrimpToolContract:
    tool: str
    nominal_wire_range_awg: tuple[int, int]
    terminal_families: tuple[ConnectorFamily, ...]
    qualification_required: bool
    acceptance_samples: int
    acceptance_checks: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class HarnessPin:
    position: int
    signal: str
    colour: str
    populated: bool = True


@dataclass(frozen=True, slots=True)
class HarnessContract:
    identifier: str
    harness_class: HarnessClass
    connector_family: ConnectorFamily
    ways: int
    wire_awg: int
    cable_type: str
    nominal_length_mm: int | None
    length_tolerance_mm: int | None
    service_loop_mm: int
    minimum_bend_radius_mm: int
    panel_end: str
    pcb_end: str
    shield_termination: str
    separation_rule: str
    pins: tuple[HarnessPin, ...]
    status: str = "PROVISIONAL"


@dataclass(slots=True)
class InterconnectArchitecture:
    identifier: str
    revision: str
    status: str
    crimp_tool: CrimpToolContract
    harnesses: list[HarnessContract] = field(default_factory=list)
    eco_refs: list[str] = field(default_factory=list)
    open_items: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


SN58B = CrimpToolContract(
    tool="SN-58B ratchet open-barrel crimper",
    nominal_wire_range_awg=(24, 16),
    terminal_families=(ConnectorFamily.JST_VH, ConnectorFamily.MINI_FIT_JR),
    qualification_required=True,
    acceptance_samples=5,
    acceptance_checks=(
        "conductor wings fully capture all strands",
        "insulation wings support without cutting insulation",
        "terminal locks into housing",
        "manual pull test passes",
        "successful die cavity and wire gauge recorded",
    ),
)


def _balanced_input(identifier: str, side: str) -> HarnessContract:
    colours = ("white", "grey") if side == "L" else ("yellow", "orange")
    return HarnessContract(
        identifier=identifier,
        harness_class=HarnessClass.MICROVOLT_ANALOGUE,
        connector_family=ConnectorFamily.JST_VH,
        ways=4,
        wire_awg=24,
        cable_type="shielded twisted pair or star-quad",
        nominal_length_mm=None,
        length_tolerance_mm=None,
        service_loop_mm=25,
        minimum_bend_radius_mm=20,
        panel_end=f"panel XLR input {side}",
        pcb_end=f"4-way JST VH input header {side}",
        shield_termination="shield/chassis bonded at panel entry; signal pair remains isolated from chassis",
        separation_rule="minimum 25 mm from power/control harnesses; crossings near 90 degrees",
        pins=(
            HarnessPin(1, f"INPUT_{side}_POS", colours[0]),
            HarnessPin(2, f"INPUT_{side}_NEG", colours[1]),
            HarnessPin(3, "CHASSIS_DRAIN", "bare/drain"),
            HarnessPin(4, "SPARE", "unpopulated", populated=False),
        ),
    )


def _balanced_output(identifier: str, side: str) -> HarnessContract:
    colours = ("white", "grey") if side == "L" else ("yellow", "orange")
    return HarnessContract(
        identifier=identifier,
        harness_class=HarnessClass.LINE_LEVEL_ANALOGUE,
        connector_family=ConnectorFamily.JST_VH,
        ways=4,
        wire_awg=22,
        cable_type="twisted pair with separate chassis drain where required",
        nominal_length_mm=None,
        length_tolerance_mm=None,
        service_loop_mm=25,
        minimum_bend_radius_mm=20,
        panel_end=f"panel XLR output {side}",
        pcb_end=f"4-way JST VH output header {side}",
        shield_termination="XLR shell bonds to chassis at panel; signal pair does not use chassis as return",
        separation_rule="keep clear of cartridge-input harnesses; shared output-side loom permitted",
        pins=(
            HarnessPin(1, f"OUTPUT_{side}_POS", colours[0]),
            HarnessPin(2, f"OUTPUT_{side}_NEG", colours[1]),
            HarnessPin(3, "CHASSIS_DRAIN", "bare/drain"),
            HarnessPin(4, "SPARE", "unpopulated", populated=False),
        ),
    )


def _dc_harness() -> HarnessContract:
    return HarnessContract(
        identifier="H-DC-01",
        harness_class=HarnessClass.REGULATED_POWER,
        connector_family=ConnectorFamily.MINI_FIT_JR,
        ways=5,
        wire_awg=18,
        cable_type="individual stranded conductors, twisted +18V/0VA and -18V/0VA where practical",
        nominal_length_mm=None,
        length_tolerance_mm=None,
        service_loop_mm=35,
        minimum_bend_radius_mm=25,
        panel_end="panel-mounted Neutrik 5-pin XLR DC inlet",
        pcb_end="5-way Mini-Fit Jr locking header",
        shield_termination="XLR shell bonds directly to chassis; dedicated chassis conductor retained",
        separation_rule="route only within output/high-level region; prohibited from input island",
        pins=(
            HarnessPin(1, "+18V", "red"),
            HarnessPin(2, "0VA", "black"),
            HarnessPin(3, "-18V", "blue"),
            HarnessPin(4, "CHASSIS", "green/yellow"),
            HarnessPin(5, "SPARE", "violet"),
        ),
    )


def build_interconnect_architecture() -> InterconnectArchitecture:
    harnesses = [
        _balanced_input("H-IN-L", "L"),
        _balanced_input("H-IN-R", "R"),
        _balanced_output("H-OUT-L", "L"),
        _balanced_output("H-OUT-R", "R"),
        _dc_harness(),
    ]
    return InterconnectArchitecture(
        identifier="G3-010-ICA",
        revision="A1",
        status="PRELIMINARY_READY",
        crimp_tool=SN58B,
        harnesses=harnesses,
        eco_refs=[],
        open_items=[
            "freeze exact JST VH housing/header/terminal part numbers after sample-crimp qualification",
            "freeze exact Mini-Fit Jr housing/header/terminal part numbers after sample-crimp qualification",
            "derive final harness lengths from selected enclosure and panel datums",
            "define selector, mute, bypass and LED harness pin counts from final panel architecture",
        ],
    )


def validate_interconnect_architecture(model: InterconnectArchitecture) -> list[str]:
    issues: list[str] = []
    ids = [h.identifier for h in model.harnesses]
    if len(ids) != len(set(ids)):
        issues.append("duplicate harness identifier")
    if model.eco_refs:
        issues.append("closed panel-interface ECO still reports unresolved references")
    if ConnectorFamily.JST_VH not in model.crimp_tool.terminal_families:
        issues.append("JST VH not qualified against selected crimp tool")
    if ConnectorFamily.MINI_FIT_JR not in model.crimp_tool.terminal_families:
        issues.append("Mini-Fit Jr not qualified against selected crimp tool")
    for harness in model.harnesses:
        if harness.wire_awg < 16 or harness.wire_awg > 24:
            issues.append(f"{harness.identifier}: wire gauge outside SN-58B nominal range")
        if len(harness.pins) != harness.ways:
            issues.append(f"{harness.identifier}: pin count does not match housing ways")
        if len({pin.position for pin in harness.pins}) != harness.ways:
            issues.append(f"{harness.identifier}: duplicate or missing pin positions")
        if harness.harness_class is HarnessClass.MICROVOLT_ANALOGUE:
            if harness.connector_family is not ConnectorFamily.JST_VH:
                issues.append(f"{harness.identifier}: low-level signal must use JST VH")
            if "25 mm" not in harness.separation_rule:
                issues.append(f"{harness.identifier}: missing low-level separation rule")
        if harness.harness_class is HarnessClass.REGULATED_POWER:
            if harness.connector_family is not ConnectorFamily.MINI_FIT_JR:
                issues.append("regulated power must use Mini-Fit Jr")
            if "locking" not in harness.pcb_end.lower():
                issues.append("regulated power connector must use a polarised locking housing")
    return issues
