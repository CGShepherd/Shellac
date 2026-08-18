"""G3-019 enclosure and panel-interface architecture.

This module freezes the mechanical *direction* of the two Shellac enclosures
without pretending that exact METCASE order codes, hole coordinates, or control
parts have already been selected.  It is the contract that later PCB placement
and drilling-template generation must satisfy.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum


class EnclosureFace(str, Enum):
    FRONT = "front"
    REAR = "rear"
    UPPER_COVER = "upper_cover"
    LOWER_CHASSIS = "lower_chassis"


class InterfaceKind(str, Enum):
    AUDIO_INPUT = "audio_input"
    AUDIO_OUTPUT = "audio_output"
    DC_INPUT = "dc_input"
    MAINS_INPUT = "mains_input"
    DC_OUTPUT = "dc_output"
    OPERATOR_CONTROL = "operator_control"
    INDICATOR = "indicator"


class MountingMode(str, Enum):
    PANEL_HARNESS = "panel_mounted_with_removable_harness"
    PCB_BUSHING = "pcb_mounted_threaded_bushing_through_cover"
    PCB_PLAIN_SHAFT = "pcb_mounted_plain_shaft_through_cover"
    PCB_LIGHT_PIPE = "pcb_mounted_indicator_with_light_pipe"
    FLYING_INDICATOR = "panel_indicator_with_flying_leads"


@dataclass(frozen=True, slots=True)
class EnclosureFamilyFreeze:
    manufacturer: str
    family: str
    finish: str
    colour_standard: str
    construction: str
    family_status: str
    exact_audio_order_code: str | None
    exact_psu_order_code: str | None
    source_reference: str


@dataclass(frozen=True, slots=True)
class PanelInterface:
    identifier: str
    enclosure: str
    kind: InterfaceKind
    face: EnclosureFace
    mounting: MountingMode
    preferred_location: str
    wiring_rule: str
    structural_rule: str


@dataclass(frozen=True, slots=True)
class DrillingTemplateContract:
    scale: str
    primary_format: str
    machine_format: str
    coordinate_origin: str
    required_datums: tuple[str, ...]
    required_features: tuple[str, ...]
    tolerance_rule: str
    verification_rule: str
    release_gate: str


@dataclass(slots=True)
class InterfaceArchitecture:
    identifier: str
    revision: str
    status: str
    enclosure_family: EnclosureFamilyFreeze
    signal_flow_rule: str
    psu_flow_rule: str
    interfaces: list[PanelInterface] = field(default_factory=list)
    drilling_template: DrillingTemplateContract | None = None
    invariants: list[str] = field(default_factory=list)
    open_items: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def build_interface_architecture() -> InterfaceArchitecture:
    family = EnclosureFamilyFreeze(
        manufacturer="METCASE",
        family="UNICASE",
        finish="Black",
        colour_standard="RAL 9005",
        construction="aluminium total-access instrument enclosure with removable top/base and anodised front/rear panels",
        family_status="PARTIAL SIZE FREEZE — audio M5502119 frozen; PSU M5501119 remains component-fit gated",
        exact_audio_order_code="M5502119",
        exact_psu_order_code=None,
        source_reference="METCASE UNICASE manufacturer catalogue/product drawings",
    )

    interfaces = [
        PanelInterface(
            "IF-A-IN", "audio", InterfaceKind.AUDIO_INPUT, EnclosureFace.FRONT,
            MountingMode.PANEL_HARNESS, "front panel; left/right XLR inputs arranged symmetrically",
            "short removable shielded harnesses to the front edge of the PCB",
            "XLR shells bond locally to chassis; connector loads are carried by the front panel",
        ),
        PanelInterface(
            "IF-A-OUT", "audio", InterfaceKind.AUDIO_OUTPUT, EnclosureFace.REAR,
            MountingMode.PANEL_HARNESS, "rear panel; left/right XLR outputs",
            "short removable output harnesses from the rear/output PCB region",
            "connector loads are carried by the rear panel",
        ),
        PanelInterface(
            "IF-A-DC", "audio", InterfaceKind.DC_INPUT, EnclosureFace.REAR,
            MountingMode.PANEL_HARNESS, "rear panel near enclosure centreline and separated from output XLR signal pairs",
            "locking removable regulated-power harness to rear-centre PCB power entry",
            "DC connector shell/chassis bond remains serviceable",
        ),
        PanelInterface(
            "IF-A-CTRL", "audio", InterfaceKind.OPERATOR_CONTROL, EnclosureFace.UPPER_COVER,
            MountingMode.PCB_BUSHING, "top cover above authoritative PCB control coordinates",
            "no flying switch or potentiometer leads",
            "threaded bushings locate/support controls through the cover; nuts must never pull a misaligned PCB into position",
        ),
        PanelInterface(
            "IF-A-IND", "audio", InterfaceKind.INDICATOR, EnclosureFace.UPPER_COVER,
            MountingMode.PCB_LIGHT_PIPE, "top cover aligned to PCB-mounted indicators",
            "prefer PCB LED/light-pipe construction; flying leads permitted only as an explicit fallback",
            "indicator aperture must not constrain PCB alignment",
        ),
        PanelInterface(
            "IF-P-MAINS", "psu", InterfaceKind.MAINS_INPUT, EnclosureFace.REAR,
            MountingMode.PANEL_HARNESS, "rear panel mains-entry zone",
            "mains remains confined to the rear entry zone before transformer transition",
            "IEC/filter/switch hardware is panel-supported and protective earth bonds immediately adjacent",
        ),
        PanelInterface(
            "IF-P-DC", "psu", InterfaceKind.DC_OUTPUT, EnclosureFace.FRONT,
            MountingMode.PANEL_HARNESS, "front panel low-voltage output zone",
            "regulated DC progresses forward from transformer/regulator section",
            "output connector is panel-supported and physically segregated from mains wiring",
        ),
    ]

    template = DrillingTemplateContract(
        scale="1:1",
        primary_format="PDF",
        machine_format="DXF",
        coordinate_origin="manufacturer-defined enclosure/panel datum; never chained hole-to-hole dimensions",
        required_datums=(
            "front edge",
            "rear edge",
            "left/right enclosure centreline",
            "PCB mounting origin",
            "upper-cover seating datum",
        ),
        required_features=(
            "switch and potentiometer bushing centres and finished-hole diameters",
            "anti-rotation flats/tabs where selected hardware requires them",
            "indicator or light-pipe apertures",
            "front/rear XLR and DC connector cut-outs",
            "PSU IEC/filter/switch and DC-output cut-outs",
            "reference centre-lines and check dimensions",
            "100 x 100 mm print calibration box",
            "PRINT AT 100% / ACTUAL SIZE — DO NOT FIT TO PAGE notice",
        ),
        tolerance_rule="hole coordinates derive from the same authoritative PCB/enclosure coordinate model; panel holes must provide assembly clearance without using control nuts as alignment force",
        verification_rule="verify calibration box, edge datums, PCB-to-cover stack-up, bushing thread engagement, and all cut-out clearances before drilling",
        release_gate="do not release manufacturing templates until exact UNICASE order codes, PCB coordinates, control part numbers, panel thickness and enclosure drawings are frozen",
    )

    return InterfaceArchitecture(
        identifier="G3-MECH-019",
        revision="Rev A0",
        status="ARCHITECTURE_FROZEN — audio M5502119 frozen; PSU size and drilling coordinates remain open",
        enclosure_family=family,
        signal_flow_rule="main audio signal flow is front-to-rear: input XLRs at front, PCB processing inward, output XLRs at rear; regulated DC enters at rear near the centreline",
        psu_flow_rule="PSU flow is rear-to-front: mains entry at rear, transformer transition, rectification/regulation, regulated DC output at front",
        interfaces=interfaces,
        drilling_template=template,
        invariants=[
            "Main-audio switches and potentiometers are PCB mounted; no flying control harness is permitted.",
            "Threaded control bushings are preferred where electrically/mechanically suitable and provide secondary support only after PCB alignment is established by its own mounting datums.",
            "PCB-mounted LEDs/light pipes are preferred so the audio upper cover can be electrically passive.",
            "Audio XLR and DC panel connections remain removable harnesses because they terminate on detachable end panels.",
            "PSU clamshell top/base should remain unmachined; rear/front panels carry mains and DC interfaces.",
            "No drilling template may be generated from hand-measured chained dimensions.",
        ],
        open_items=[
            "audio black UNICASE 2 M5502119 frozen by G3-MECH-020; preserve its manufacturer datums",
            "prove or reject black UNICASE 1 M5501119 for PSU from IEC/regulator layout, segregation and thermal fit",
            "select exact PCB-mount switch/potentiometer families and verify threaded-bushing stack-up",
            "decide whether every indicator can use PCB mounting/light pipes or whether any flying indicator lead is genuinely required",
            "generate released 1:1 PDF and DXF drilling templates only after exact PCB/control coordinates are frozen",
        ],
    )


def validate_interface_architecture(model: InterfaceArchitecture) -> list[str]:
    issues: list[str] = []
    ids = [item.identifier for item in model.interfaces]
    if len(ids) != len(set(ids)):
        issues.append("duplicate panel-interface identifier")
    if model.enclosure_family.finish != "Black" or model.enclosure_family.colour_standard != "RAL 9005":
        issues.append("selected UNICASE finish must remain black RAL 9005")

    by_id = {item.identifier: item for item in model.interfaces}
    required_faces = {
        "IF-A-IN": EnclosureFace.FRONT,
        "IF-A-OUT": EnclosureFace.REAR,
        "IF-A-DC": EnclosureFace.REAR,
        "IF-A-CTRL": EnclosureFace.UPPER_COVER,
        "IF-P-MAINS": EnclosureFace.REAR,
        "IF-P-DC": EnclosureFace.FRONT,
    }
    for identifier, face in required_faces.items():
        if identifier not in by_id or by_id[identifier].face is not face:
            issues.append(f"{identifier} violates frozen enclosure-face assignment")

    controls = by_id.get("IF-A-CTRL")
    if controls and controls.mounting not in {MountingMode.PCB_BUSHING, MountingMode.PCB_PLAIN_SHAFT}:
        issues.append("audio operator controls must be PCB mounted")
    if controls and "no flying" not in controls.wiring_rule.lower():
        issues.append("audio operator controls must prohibit flying leads")

    template = model.drilling_template
    if template is None:
        issues.append("drilling-template contract is missing")
    else:
        if template.scale != "1:1":
            issues.append("drilling template must be released at 1:1")
        if "100 x 100" not in " ".join(template.required_features):
            issues.append("drilling template lacks print calibration feature")
        if "do not release" not in template.release_gate.lower():
            issues.append("drilling-template release gate is not explicit")
    return issues
