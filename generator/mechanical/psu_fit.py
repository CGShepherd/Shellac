"""G3-021 PSU UNICASE 1 component-fit closure.

The assessment deliberately separates geometric evidence from release evidence.
It may prove that the known transformer and regulator envelopes can coexist
without pretending that an unselected IEC inlet or an unperformed thermal
check has been closed.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum

from .unicase_fit import ComponentEnvelope, build_unicase_fit_decision


class ClosureState(str, Enum):
    GEOMETRY_PROVEN = "GEOMETRY_PROVEN"
    RELEASE_BLOCKED = "RELEASE_BLOCKED"
    REJECTED = "REJECTED"


@dataclass(frozen=True, slots=True)
class FloorEnvelope:
    width_mm: float
    depth_mm: float
    usable_height_mm: float
    source_reference: str


@dataclass(frozen=True, slots=True)
class RectangularFit:
    component_a: str
    component_b: str
    occupied_width_mm: float
    occupied_depth_mm: float
    residual_width_mm: float
    residual_depth_mm: float
    fits: bool
    rule: str


@dataclass(slots=True)
class PsuFitClosure:
    identifier: str
    revision: str
    enclosure_order_code: str
    floor: FloorEnvelope
    transformer: ComponentEnvelope
    regulator: ComponentEnvelope
    side_by_side_fit: RectangularFit
    state: ClosureState
    findings: list[str] = field(default_factory=list)
    release_blockers: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["state"] = self.state.value
        return payload


def build_psu_fit_closure() -> PsuFitClosure:
    base = build_unicase_fit_decision()
    floor = FloorEnvelope(
        width_mm=181.0,
        depth_mm=161.01,
        usable_height_mm=61.2,
        source_reference=(
            "METCASE M5501119 manufacturer drawing: 181.00 mm inside face-to-inside "
            "face, 161.01 mm internal floor dimension, 61.20 mm internal height"
        ),
    )
    regulator = ComponentEnvelope(
        identifier="existing LM317/LM337 regulator module",
        width_mm=75.0,
        depth_mm=85.0,
        height_mm=31.0,
        source_reference="Project Shellac measured/current module envelope",
    )
    occupied_width = base.transformer.width_mm + regulator.width_mm
    occupied_depth = max(base.transformer.depth_mm, regulator.depth_mm)
    fit = RectangularFit(
        component_a=base.transformer.identifier,
        component_b=regulator.identifier,
        occupied_width_mm=occupied_width,
        occupied_depth_mm=occupied_depth,
        residual_width_mm=floor.width_mm - occupied_width,
        residual_depth_mm=floor.depth_mm - occupied_depth,
        fits=occupied_width <= floor.width_mm and occupied_depth <= floor.depth_mm,
        rule=(
            "Conservative orthogonal-envelope test only: transformer and regulator are "
            "placed side-by-side on the internal floor with no overlap. Residual space is "
            "not allocated to mains hardware until its exact part geometry is selected."
        ),
    )
    blockers = [
        "select the exact filtered IEC/fuse/DPST-switch hardware and prove its rear-panel depth, terminals, touch protection, mains/SELV segregation and wiring bend space",
        "complete passive thermal calculation/measurement for transformer plus LM317/LM337 dissipation in the closed 65 mm enclosure",
    ]
    findings = [
        "The manufacturer drawing closes the previously missing M5501119 internal envelope at 181.00 x 161.01 x 61.20 mm for this fit model.",
        "The conservative 78 x 78 x 36 mm transformer and 75 x 85 x 31 mm regulator envelopes fit side-by-side within that floor envelope.",
        f"The simple side-by-side overlay consumes {occupied_width:.0f} x {occupied_depth:.0f} mm, leaving {floor.width_mm - occupied_width:.0f} mm lateral and {floor.depth_mm - occupied_depth:.2f} mm depth residual before allocation of IEC hardware and segregation zones.",
        "Transformer and regulator heights individually fit below the 61.20 mm internal-height datum; this is not a substitute for fastener, terminal or thermal clearance review.",
        "M5501119 is therefore not rejected on known component geometry, but it is not frozen: exact mains-entry hardware and passive thermal evidence remain release blockers.",
        "No arbitrary IEC inlet, fuse holder, switch, heatsink or drilling coordinate is selected by this increment.",
    ]
    return PsuFitClosure(
        identifier="G3-MECH-021",
        revision="Rev A0",
        enclosure_order_code="M5501119",
        floor=floor,
        transformer=base.transformer,
        regulator=regulator,
        side_by_side_fit=fit,
        state=ClosureState.RELEASE_BLOCKED,
        findings=findings,
        release_blockers=blockers,
    )


def validate_psu_fit_closure(model: PsuFitClosure) -> list[str]:
    issues: list[str] = []
    if model.enclosure_order_code != "M5501119":
        issues.append("PSU fit closure must assess M5501119")
    if model.floor.width_mm != 181.0 or model.floor.depth_mm != 161.01 or model.floor.usable_height_mm != 61.2:
        issues.append("M5501119 internal envelope must remain tied to the manufacturer drawing")
    if not model.side_by_side_fit.fits:
        issues.append("known transformer/regulator envelopes do not fit the assessed floor")
    if model.transformer.height_mm > model.floor.usable_height_mm or model.regulator.height_mm > model.floor.usable_height_mm:
        issues.append("known component height exceeds M5501119 internal height")
    if model.state is not ClosureState.RELEASE_BLOCKED:
        issues.append("M5501119 must remain release-blocked until exact mains hardware and thermal evidence close")
    blocker_text = " ".join(model.release_blockers).lower()
    if "iec" not in blocker_text or "thermal" not in blocker_text:
        issues.append("release blockers must preserve exact IEC and thermal closure")
    return issues
