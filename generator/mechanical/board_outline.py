"""Board-outline and mounting-hole synthesis interface for Gate 3.

The module intentionally separates provisional architecture dimensions from
manufacturing datums.  Exact PCB and carrier-hole coordinates are emitted only
from a verified :class:`CarrierPlateFreeze` produced by the enclosure-decision
model.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum

from generator.mechanical.freeze import CarrierPlateFreeze


class OutlineStatus(str, Enum):
    PROVISIONAL = "PROVISIONAL"
    DECISION_READY = "DECISION_READY"
    FROZEN = "FROZEN"


@dataclass(frozen=True, slots=True)
class Point2D:
    x_mm: float
    y_mm: float


@dataclass(frozen=True, slots=True)
class MountingHole:
    identifier: str
    centre: Point2D
    finished_diameter_mm: float
    copper_keepout_diameter_mm: float
    plated: bool
    purpose: str


@dataclass(frozen=True, slots=True)
class BoardOutline:
    width_mm: float
    depth_mm: float
    corner_radius_mm: float
    origin: str
    datum_x: str
    datum_y: str


@dataclass(slots=True)
class BoardOutlineContract:
    identifier: str
    revision: str
    status: OutlineStatus
    outline: BoardOutline
    mounting_holes: list[MountingHole] = field(default_factory=list)
    carrier_plate_reference: str | None = None
    unresolved_inputs: list[str] = field(default_factory=list)
    invariants: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["status"] = self.status.value
        return payload


def _corner_holes(
    width_mm: float,
    depth_mm: float,
    *,
    inset_x_mm: float,
    inset_y_mm: float,
    finished_diameter_mm: float,
    copper_keepout_diameter_mm: float,
) -> list[MountingHole]:
    coordinates = (
        ("MH1", inset_x_mm, inset_y_mm),
        ("MH2", width_mm - inset_x_mm, inset_y_mm),
        ("MH3", width_mm - inset_x_mm, depth_mm - inset_y_mm),
        ("MH4", inset_x_mm, depth_mm - inset_y_mm),
    )
    return [
        MountingHole(
            identifier=identifier,
            centre=Point2D(round(x, 3), round(y, 3)),
            finished_diameter_mm=finished_diameter_mm,
            copper_keepout_diameter_mm=copper_keepout_diameter_mm,
            plated=False,
            purpose="PCB-to-carrier standoff",
        )
        for identifier, x, y in coordinates
    ]


def validate_outline_contract(contract: BoardOutlineContract) -> list[str]:
    issues: list[str] = []
    if contract.outline.width_mm <= 0 or contract.outline.depth_mm <= 0:
        issues.append("board dimensions must be positive")
    if contract.status is OutlineStatus.FROZEN and contract.unresolved_inputs:
        issues.append("frozen outline cannot contain unresolved inputs")
    if contract.status is OutlineStatus.FROZEN and len(contract.mounting_holes) != 4:
        issues.append("frozen Rev A outline must contain four PCB mounting holes")

    seen: set[tuple[float, float]] = set()
    for hole in contract.mounting_holes:
        point = (hole.centre.x_mm, hole.centre.y_mm)
        if point in seen:
            issues.append(f"duplicate mounting-hole coordinate at {point}")
        seen.add(point)
        radius = hole.copper_keepout_diameter_mm / 2
        if hole.centre.x_mm - radius < 0 or hole.centre.x_mm + radius > contract.outline.width_mm:
            issues.append(f"{hole.identifier} copper keep-out exceeds board width")
        if hole.centre.y_mm - radius < 0 or hole.centre.y_mm + radius > contract.outline.depth_mm:
            issues.append(f"{hole.identifier} copper keep-out exceeds board depth")
        if hole.copper_keepout_diameter_mm <= hole.finished_diameter_mm:
            issues.append(f"{hole.identifier} copper keep-out must exceed drill diameter")
    return issues


def build_provisional_outline_contract(
    *,
    width_mm: float = 220.0,
    depth_mm: float = 140.0,
) -> BoardOutlineContract:
    """Return the architecture contract before enclosure evidence is complete."""
    return BoardOutlineContract(
        identifier="G3-OUT-007",
        revision="Rev A0",
        status=OutlineStatus.PROVISIONAL,
        outline=BoardOutline(
            width_mm=width_mm,
            depth_mm=depth_mm,
            corner_radius_mm=2.0,
            origin="lower-left PCB corner, component-side view",
            datum_x="parallel to audio-enclosure front/rear panel axis",
            datum_y="parallel to audio-enclosure left/right side axis",
        ),
        mounting_holes=[],
        unresolved_inputs=[
            "exact audio-enclosure order code",
            "authoritative enclosure dimensional drawing",
            "verified carrier-plate mounting pattern",
            "verified lid and panel-hardware intrusion envelopes",
            "final carrier-to-panel harness corridors",
        ],
        invariants=[
            "No manufacturing mounting-hole coordinate is emitted before enclosure freeze.",
            "The board orientation remains front-to-rear: audio input region at front, output and DC-entry regions at rear.",
            "Board origin and coordinate handedness remain stable across provisional and frozen states.",
            "All PCB holes are non-plated mechanical holes with explicit copper keep-outs.",
        ],
    )


def derive_frozen_outline_contract(
    carrier: CarrierPlateFreeze,
    *,
    hole_inset_x_mm: float = 8.0,
    hole_inset_y_mm: float = 8.0,
    finished_diameter_mm: float = 3.2,
    copper_keepout_diameter_mm: float = 8.0,
) -> BoardOutlineContract:
    """Derive manufacturing board datums from a verified carrier freeze."""
    if carrier.status != "FROZEN":
        raise ValueError("carrier plate must be frozen before board outline synthesis")
    outline = BoardOutline(
        width_mm=carrier.pcb_width_mm,
        depth_mm=carrier.pcb_depth_mm,
        corner_radius_mm=2.0,
        origin="lower-left PCB corner, component-side view",
        datum_x=f"carrier X + {carrier.pcb_origin_x_mm:.3f} mm",
        datum_y=f"carrier Y + {carrier.pcb_origin_y_mm:.3f} mm",
    )
    contract = BoardOutlineContract(
        identifier="G3-OUT-007",
        revision="Rev A0",
        status=OutlineStatus.FROZEN,
        outline=outline,
        mounting_holes=_corner_holes(
            outline.width_mm,
            outline.depth_mm,
            inset_x_mm=hole_inset_x_mm,
            inset_y_mm=hole_inset_y_mm,
            finished_diameter_mm=finished_diameter_mm,
            copper_keepout_diameter_mm=copper_keepout_diameter_mm,
        ),
        carrier_plate_reference=carrier.enclosure_candidate_id,
        unresolved_inputs=[],
        invariants=[
            "Four mounting holes form a rectangular, datum-referenced pattern.",
            "Hole coordinates are measured from the stable PCB lower-left origin.",
            "Mounting holes are non-plated and isolated from all copper by explicit keep-outs.",
            "Carrier plate preserves at least 5 mm PCB clearance on every side.",
            "PCB remains vertically removable with the panel harnesses disconnected.",
        ],
    )
    issues = validate_outline_contract(contract)
    if issues:
        raise ValueError("invalid frozen board outline: " + "; ".join(issues))
    return contract
