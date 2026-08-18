"""G3-020 exact UNICASE sizing and mechanical fit evidence.

This module records only dimensions supported by manufacturer drawings or
component datasheets.  It deliberately distinguishes a frozen enclosure from
a preferred-but-not-yet-releasable candidate.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum


class FitStatus(str, Enum):
    FROZEN = "FROZEN"
    CONDITIONAL = "CONDITIONAL"
    REJECTED = "REJECTED"


@dataclass(frozen=True, slots=True)
class VerifiedEnclosure:
    role: str
    manufacturer: str
    family: str
    order_code: str
    colour: str
    external_width_mm: float
    external_depth_mm: float
    external_height_mm: float
    base_pcb_width_mm: float
    base_pcb_depth_mm: float
    panel_thickness_mm: float
    usable_inside_width_mm: float | None
    usable_inside_depth_mm: float | None
    usable_inside_height_mm: float | None
    source_reference: str


@dataclass(frozen=True, slots=True)
class ComponentEnvelope:
    identifier: str
    width_mm: float
    depth_mm: float
    height_mm: float
    source_reference: str


@dataclass(frozen=True, slots=True)
class ControlStackContract:
    pcb_mounting_datum: str
    upper_cover_datum: str
    panel_thickness_mm: float | None
    minimum_free_thread_mm: float
    radial_hole_clearance_mm: float
    alignment_rule: str
    release_inputs: tuple[str, ...]


@dataclass(slots=True)
class UnicaseFitDecision:
    identifier: str
    revision: str
    audio: VerifiedEnclosure
    psu: VerifiedEnclosure
    transformer: ComponentEnvelope
    control_stack: ControlStackContract
    audio_status: FitStatus
    psu_status: FitStatus
    findings: list[str] = field(default_factory=list)
    open_items: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["audio_status"] = self.audio_status.value
        payload["psu_status"] = self.psu_status.value
        return payload


def build_unicase_fit_decision() -> UnicaseFitDecision:
    audio = VerifiedEnclosure(
        role="audio", manufacturer="METCASE", family="UNICASE 2",
        order_code="M5502119", colour="Black RAL 9005",
        external_width_mm=260.0, external_depth_mm=250.0, external_height_mm=90.2,
        base_pcb_width_mm=241.0, base_pcb_depth_mm=229.0,
        panel_thickness_mm=2.0,
        usable_inside_width_mm=256.0, usable_inside_depth_mm=236.0,
        usable_inside_height_mm=86.2,
        source_reference="METCASE M5502119 manufacturer drawing",
    )
    psu = VerifiedEnclosure(
        role="psu", manufacturer="METCASE", family="UNICASE 1",
        order_code="M5501119", colour="Black RAL 9005",
        external_width_mm=185.0, external_depth_mm=180.0, external_height_mm=65.0,
        base_pcb_width_mm=166.0, base_pcb_depth_mm=159.0,
        panel_thickness_mm=2.0,
        usable_inside_width_mm=None, usable_inside_depth_mm=None,
        usable_inside_height_mm=None,
        source_reference="METCASE M5501119 manufacturer product data/drawing set",
    )
    transformer = ComponentEnvelope(
        identifier="TI-69043-ME / TA030-15",
        width_mm=78.0, depth_mm=78.0, height_mm=36.0,
        source_reference="Toroid International TA range 30 VA datasheet: 73 mm diameter and 31 mm height, each with 5 mm allowance",
    )
    controls = ControlStackContract(
        pcb_mounting_datum="PCB component-side Z=0 established by its chassis/standoff mounting; controls are soldered without panel preload",
        upper_cover_datum="inside face of fitted UNICASE upper cover",
        panel_thickness_mm=None,
        minimum_free_thread_mm=1.5,
        radial_hole_clearance_mm=0.25,
        alignment_rule="PCB/standoffs establish XY and Z first; cover holes provide clearance; control nuts may locate/support but shall never pull the PCB or cover into alignment",
        release_inputs=(
            "exact switch and potentiometer manufacturer part numbers",
            "bushing diameter, threaded length and shoulder height for every control",
            "verified upper-cover sheet thickness and inside-face Z datum",
            "final PCB control-centre coordinates",
            "selected washer/nut stack and knob shaft-engagement requirement",
        ),
    )
    findings = [
        "Audio M5502119 is frozen: 220 x 140 mm PCB fits the manufacturer 241 x 229 mm base-PCB envelope with 21 mm and 89 mm total margin respectively.",
        "A 230 x 150 mm carrier also fits within the 241 x 229 mm base envelope when oriented 230 mm across the 241 mm dimension.",
        "Audio usable internal envelope from the manufacturer drawing is compatible with the current 60 mm height gate.",
        "PSU M5501119 remains conditional rather than frozen: its 166 x 159 mm base envelope can plausibly package the 78 x 78 mm conservative transformer envelope and existing regulator module, but exact IEC/filter, regulator-board and segregation geometry is not yet frozen.",
        "The historical PSU 80 mm minimum-height gate is not relaxed by this increment; it is superseded only if a component-level fit and thermal/clearance review proves the 65 mm UNICASE 1 architecture.",
        "Drilling-template coordinates remain unreleased until exact control parts close the bushing stack.",
    ]
    return UnicaseFitDecision(
        identifier="G3-MECH-020", revision="Rev A0",
        audio=audio, psu=psu, transformer=transformer, control_stack=controls,
        audio_status=FitStatus.FROZEN, psu_status=FitStatus.CONDITIONAL,
        findings=findings,
        open_items=[
            "select exact filtered IEC/fuse/switch hardware and verify rear-panel depth in M5501119",
            "verify regulator PCB 75 x 85 x 31 mm envelope and mounting orientation against the M5501119 drawing",
            "complete mains/SELV segregation and transformer-fastener clearance overlay for M5501119",
            "complete passive thermal check before accepting the lower 65 mm PSU enclosure",
            "select exact PCB-mounted pots/switches and close upper-cover bushing stack",
        ],
    )


def validate_unicase_fit_decision(model: UnicaseFitDecision) -> list[str]:
    issues: list[str] = []
    if model.audio.order_code != "M5502119" or model.audio_status is not FitStatus.FROZEN:
        issues.append("audio enclosure must remain frozen as black M5502119")
    if model.audio.base_pcb_width_mm < 230.0 or model.audio.base_pcb_depth_mm < 150.0:
        issues.append("audio enclosure does not preserve the 230 x 150 mm carrier envelope")
    if model.audio.usable_inside_height_mm is None or model.audio.usable_inside_height_mm < 60.0:
        issues.append("audio usable height does not meet the project gate")
    if model.psu.order_code == "M5501119" and model.psu_status is FitStatus.FROZEN:
        issues.append("M5501119 PSU may not be frozen before component/thermal/segregation closure")
    if model.control_stack.panel_thickness_mm is not None:
        issues.append("control panel thickness must remain open until verified from the exact cover drawing")
    if "never pull" not in model.control_stack.alignment_rule.lower():
        issues.append("control stack must prohibit nut-forced alignment")
    return issues
