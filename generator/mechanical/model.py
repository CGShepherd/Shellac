"""Gate 3 mechanical datum and enclosure trade-study model.

The model deliberately separates fixed project intent from catalogue-specific
coordinates.  A candidate enclosure may be scored and admitted only after its
usable internal dimensions and access architecture are known.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum


class EnclosureRole(str, Enum):
    AUDIO = "audio"
    PSU = "psu"


class AccessArchitecture(str, Enum):
    VERTICAL_LID = "vertical_lid_or_base"
    DETACHABLE_PANELS = "detachable_panels"
    SLIDING_COVER = "sliding_cover"
    DIECAST_LID = "diecast_vertical_lid"
    TOTAL_ACCESS = "removable_top_base_and_end_panels"


class CandidateStatus(str, Enum):
    PLAUSIBLE = "plausible"
    CONDITIONAL = "conditional"
    REJECTED = "rejected"
    DATA_REQUIRED = "data_required"


@dataclass(frozen=True, slots=True)
class Datum:
    identifier: str
    name: str
    definition: str
    verification: str


@dataclass(frozen=True, slots=True)
class CarrierPlate:
    enabled: bool
    minimum_edge_margin_mm: float
    pcb_standoff_height_mm: float
    plate_thickness_mm: float
    removable_as_module: bool
    rationale: str


@dataclass(frozen=True, slots=True)
class EnclosureRequirement:
    role: EnclosureRole
    minimum_internal_width_mm: float
    minimum_internal_depth_mm: float
    minimum_internal_height_mm: float
    maximum_external_width_mm: float | None
    sliding_cover_allowed: bool
    conductive_metal_required: bool
    carrier_plate: CarrierPlate
    hard_gates: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class EnclosureCandidate:
    identifier: str
    manufacturer: str
    family: str
    role: EnclosureRole
    access: AccessArchitecture
    internal_width_mm: float | None
    internal_depth_mm: float | None
    internal_height_mm: float | None
    external_width_mm: float | None
    material: str
    status: CandidateStatus
    construction_score: int
    service_score: int
    robustness_score: int
    machining_score: int
    notes: str

    @property
    def weighted_score(self) -> int:
        # Service and construction receive the highest weighting because they
        # directly affect prototype build and commissioning risk.
        return (
            3 * self.construction_score
            + 3 * self.service_score
            + 2 * self.robustness_score
            + 2 * self.machining_score
        )


@dataclass(slots=True)
class MechanicalBaseline:
    identifier: str
    revision: str
    status: str
    audio_requirement: EnclosureRequirement
    psu_requirement: EnclosureRequirement
    datums: list[Datum] = field(default_factory=list)
    candidates: list[EnclosureCandidate] = field(default_factory=list)
    open_inputs: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        payload = asdict(self)
        for candidate, raw in zip(self.candidates, payload["candidates"]):
            raw["weighted_score"] = candidate.weighted_score
        return payload


def evaluate_candidate(candidate: EnclosureCandidate, requirement: EnclosureRequirement) -> list[str]:
    failures: list[str] = []
    if candidate.role is not requirement.role:
        failures.append("candidate role does not match requirement")
    if requirement.conductive_metal_required and "metal" not in candidate.material.lower() and "aluminium" not in candidate.material.lower():
        failures.append("conductive metal construction not demonstrated")
    if not requirement.sliding_cover_allowed and candidate.access is AccessArchitecture.SLIDING_COVER:
        failures.append("audio enclosure may not use a trapped sliding cover")
    dimensions = (
        ("width", candidate.internal_width_mm, requirement.minimum_internal_width_mm),
        ("depth", candidate.internal_depth_mm, requirement.minimum_internal_depth_mm),
        ("height", candidate.internal_height_mm, requirement.minimum_internal_height_mm),
    )
    for name, actual, required in dimensions:
        if actual is None:
            failures.append(f"usable internal {name} requires drawing confirmation")
        elif actual < required:
            failures.append(f"usable internal {name} {actual:.1f} mm is below {required:.1f} mm")
    if requirement.maximum_external_width_mm is not None:
        if candidate.external_width_mm is None:
            failures.append("external width requires drawing confirmation")
        elif candidate.external_width_mm > requirement.maximum_external_width_mm:
            failures.append("external width exceeds project limit")
    return failures


def build_mechanical_baseline() -> MechanicalBaseline:
    carrier = CarrierPlate(
        enabled=True,
        minimum_edge_margin_mm=5.0,
        pcb_standoff_height_mm=8.0,
        plate_thickness_mm=2.0,
        removable_as_module=True,
        rationale="A removable aluminium carrier decouples PCB mounting from arbitrary enclosure bosses and supports assembly, probing, and Revision B reuse.",
    )
    audio = EnclosureRequirement(
        role=EnclosureRole.AUDIO,
        minimum_internal_width_mm=230.0,
        minimum_internal_depth_mm=145.0,
        minimum_internal_height_mm=60.0,
        maximum_external_width_mm=300.0,
        sliding_cover_allowed=False,
        conductive_metal_required=True,
        carrier_plate=carrier,
        hard_gates=(
            "Top or base remains removable after PCB-mounted controls and front/rear XLRs are fitted.",
            "Main PCB and all component-side test points remain accessible with enclosure open.",
            "PCB-mounted switch/potentiometer bushings may support the upper cover but must not force PCB alignment.",
            "Front input and rear output/DC panel harnesses disconnect without desoldering.",
            "Operator switches and potentiometers use no flying leads; indicators use PCB light pipes where practical.",
        ),
    )
    psu = EnclosureRequirement(
        role=EnclosureRole.PSU,
        minimum_internal_width_mm=120.0,
        minimum_internal_depth_mm=180.0,
        minimum_internal_height_mm=80.0,
        maximum_external_width_mm=None,
        sliding_cover_allowed=True,
        conductive_metal_required=True,
        carrier_plate=carrier,
        hard_gates=(
            "Protective-earth stud adjacent to the rear IEC entry.",
            "Rear mains and front regulated-DC panel hardware remain serviceable.",
            "Transformer fastener cannot create a chassis shorted turn.",
            "Mains wiring remains confined to the rear entry zone of the enclosure.",
            "Top/base clamshell panels remain unmachined where the selected size permits the complete PSU layout.",
        ),
    )
    datums = [
        Datum("DAT-001", "Carrier-plate origin", "Lower-left corner of the removable carrier plate viewed from the component side.", "Mechanical drawing and assembly jig."),
        Datum("DAT-002", "Audio front/input plane", "Front end-panel plane carrying the cartridge input XLRs; board front edge lies immediately behind this plane.", "Manufacturer drawing and enclosure/PCB overlay review."),
        Datum("DAT-003", "Audio rear/output plane", "Rear end-panel plane carrying balanced output XLRs.", "Manufacturer drawing and enclosure/PCB overlay review."),
        Datum("DAT-004", "Audio upper-cover control plane", "Removable upper cover through which PCB-mounted switch/potentiometer bushings and indicator light pipes register.", "PCB-to-cover stack-up and drilling-template review."),
        Datum("DAT-005", "Audio rear-centre DC entry", "Rear-panel regulated-DC inlet near the enclosure centreline with local serviceable 0VA/CHASSIS bond region.", "Connector-clearance and continuity/isolation review."),
        Datum("DAT-006", "PSU rear protective-earth point", "Dedicated fastener immediately adjacent to the rear filtered IEC inlet.", "Protective-earth resistance test."),
        Datum("DAT-007", "PSU front DC-output plane", "Front end-panel plane carrying only the regulated low-voltage output interface.", "Panel drawing and segregation review."),
    ]
    candidates = [
        EnclosureCandidate("ENC-A04", "METCASE", "UNICASE 2 / black RAL 9005 (M5502119)", EnclosureRole.AUDIO, AccessArchitecture.TOTAL_ACCESS, 241.0, 229.0, 86.2, 260.0, "Aluminium metal instrument enclosure", CandidateStatus.PLAUSIBLE, 5, 5, 4, 5, "Exact audio enclosure frozen by G3-MECH-020. Manufacturer drawing gives 241 x 229 mm base-PCB envelope, 256 x 236 mm inside-face envelope and 86.2 mm internal cover height; control-hole release remains part-gated."),
        EnclosureCandidate("ENC-P04", "METCASE", "UNICASE 1 / black RAL 9005 (M5501119)", EnclosureRole.PSU, AccessArchitecture.TOTAL_ACCESS, 166.0, 159.0, 65.0, 185.0, "Aluminium metal instrument enclosure", CandidateStatus.REJECTED, 5, 5, 4, 5, "Rejected by G3-MECH-022 binary release gate: exact SCHURTER KMF mains-entry geometry fits, but passive thermal release evidence cannot be established from the controlled worst-case load and thermal-resistance data currently available."),
        EnclosureCandidate("ENC-A01", "Takachi", "Large AL die-cast family", EnclosureRole.AUDIO, AccessArchitecture.DIECAST_LID, None, None, None, None, "Die-cast aluminium", CandidateStatus.DATA_REQUIRED, 4, 5, 5, 3, "Retained as the rugged audio candidate; exact part and boss-to-boss dimensions remain to be frozen."),
        EnclosureCandidate("ENC-A02", "Takachi", "Detachable-top T/project-box family", EnclosureRole.AUDIO, AccessArchitecture.VERTICAL_LID, 239.0, 133.0, 57.0, 250.0, "Aluminium metal project box", CandidateStatus.CONDITIONAL, 5, 5, 3, 5, "Example compact size is too shallow/depth-limited against the current hard envelope; larger family member remains credible."),
        EnclosureCandidate("ENC-A03", "Custom/Takachi", "Custom detachable-cover aluminium", EnclosureRole.AUDIO, AccessArchitecture.VERTICAL_LID, 250.0, 160.0, 70.0, 280.0, "Aluminium metal instrument case", CandidateStatus.PLAUSIBLE, 5, 5, 4, 5, "Reference geometry only, not an ordered part. Demonstrates the target envelope for supplier comparison."),
        EnclosureCandidate("ENC-P01", "Hammond", "1590Z large die-cast", EnclosureRole.PSU, AccessArchitecture.DIECAST_LID, 206.7, 105.8, 65.0, 221.0, "Die-cast aluminium", CandidateStatus.CONDITIONAL, 4, 4, 5, 3, "Robust, but candidate orientation and transformer height must be assessed against the actual PSU module."),
        EnclosureCandidate("ENC-P02", "Generic/Hammond/Takachi", "Extruded aluminium with removable end panels", EnclosureRole.PSU, AccessArchitecture.SLIDING_COVER, 140.0, 200.0, 90.0, 160.0, "Extruded aluminium metal enclosure", CandidateStatus.PLAUSIBLE, 5, 4, 4, 5, "Sliding cover is acceptable for the PSU. Dimensions are a target envelope pending exact part selection."),
        EnclosureCandidate("ENC-P03", "Takachi", "DWH rugged heatsink die-cast", EnclosureRole.PSU, AccessArchitecture.DIECAST_LID, 123.0, 203.0, 86.0, 140.0, "Die-cast aluminium", CandidateStatus.PLAUSIBLE, 4, 5, 5, 3, "Strong premium candidate where regulator thermal margin and internal mounting plate justify cost."),
    ]
    return MechanicalBaseline(
        identifier="G3-MECH-003",
        revision="Rev A1",
        status="AUDIO ENCLOSURE FROZEN — M5502119; PSU M5501119 REJECTED by G3-022 release gate",
        audio_requirement=audio,
        psu_requirement=psu,
        datums=datums,
        candidates=candidates,
        open_inputs=[
            "Audio M5502119 is frozen; exact upper-cover control stack remains gated by selected control parts.",
            "M5501119 rejected; assess the next larger black UNICASE PSU candidate with explicit passive-thermal margin.",
            "Exact PCB-mounted switch/potentiometer parts, anti-rotation features, and bushing-to-upper-cover stack-up.",
            "SCHURTER KMF1.1121.11 mains-entry architecture selected; freeze exact procurement variant/availability with the replacement PSU enclosure.",
            "Released datum-based 1:1 PDF/DXF drilling templates after PCB/control coordinates freeze.",
        ],
    )
