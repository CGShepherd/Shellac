"""G3-022 binary PSU enclosure release decision.

Closes the mains-entry package with an exact integrated power-entry module and
refuses to freeze a 65 mm passive enclosure without an authoritative thermal
load/thermal-resistance model.  The gate is intentionally binary: an enclosure
that cannot be released from available evidence is rejected rather than left
indefinitely conditional.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum

from .psu_fit import build_psu_fit_closure


class ReleaseDecision(str, Enum):
    FROZEN = "FROZEN"
    REJECTED = "REJECTED"


@dataclass(frozen=True, slots=True)
class MainsEntryModule:
    manufacturer: str
    series: str
    order_code: str
    inlet: str
    filter: str
    fuseholder: str
    switch: str
    body_width_mm: float
    behind_panel_depth_mm: float
    front_height_mm: float
    panel_cutout_width_mm: float
    panel_cutout_height_mm: float
    accepted_panel_thickness_mm: tuple[float, ...]
    terminals: str
    source_reference: str


@dataclass(slots=True)
class PsuReleaseDecision:
    identifier: str
    revision: str
    enclosure_order_code: str
    mains_entry: MainsEntryModule
    mains_geometry_fits: bool
    residual_depth_after_mains_mm: float
    thermal_evidence_complete: bool
    decision: ReleaseDecision
    findings: list[str] = field(default_factory=list)
    next_action: str = ""

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["decision"] = self.decision.value
        return payload


def build_psu_release_decision() -> PsuReleaseDecision:
    fit = build_psu_fit_closure()
    mains = MainsEntryModule(
        manufacturer="SCHURTER",
        series="KMF",
        order_code="KMF1.1121.11",
        inlet="IEC C14, Protection Class I",
        filter="standard integrated line filter, 2 A",
        fuseholder="2-pole, 5 x 20 mm",
        switch="2-pole non-illuminated line switch",
        body_width_mm=30.4,
        behind_panel_depth_mm=40.4,
        front_height_mm=50.0,
        panel_cutout_width_mm=28.8,
        panel_cutout_height_mm=47.8,
        accepted_panel_thickness_mm=(1.0, 1.5, 2.0, 2.5),
        terminals="4.8 x 0.8 mm quick-connect",
        source_reference="SCHURTER KMF manufacturer datasheet, KMF1.1121.11 variant table and dimension drawing",
    )
    residual = fit.floor.depth_mm - fit.side_by_side_fit.occupied_depth_mm - mains.behind_panel_depth_mm
    geometry_fits = (
        mains.front_height_mm <= fit.floor.usable_height_mm
        and mains.behind_panel_depth_mm <= fit.side_by_side_fit.residual_depth_mm
        and 2.0 in mains.accepted_panel_thickness_mm
        and residual > 0.0
    )
    findings = [
        "Exact mains-entry family/variant is now selected: SCHURTER KMF1.1121.11 integrates C14 inlet, standard 2 A filter, 2-pole 5 x 20 mm fuseholder and 2-pole switch.",
        "The manufacturer KMF drawing gives 40.4 mm behind-panel depth, 50 mm front height, 28.8 x 47.8 mm nominal cut-out and explicitly accepts a 2.0 mm panel.",
        f"Against the G3-021 conservative transformer/regulator overlay, the KMF depth leaves {residual:.2f} mm nominal depth before wiring-bend and segregation allowances; mains hardware therefore does not force geometric rejection by itself.",
        "A release-grade passive thermal proof cannot be calculated from the project baseline: authoritative worst-case DC rail current and regulator-to-ambient thermal resistance/heatsink data are not frozen.",
        "G3-022 is a binary release gate. Because passive thermal viability cannot be demonstrated for the closed 65 mm M5501119 from controlled evidence, M5501119 is rejected rather than carried forward as another conditional enclosure.",
        "This rejection does not assert that a prototype must overheat; it asserts that the enclosure lacks sufficient release evidence at the design-freeze gate.",
    ]
    return PsuReleaseDecision(
        identifier="G3-MECH-022",
        revision="Rev A0",
        enclosure_order_code="M5501119",
        mains_entry=mains,
        mains_geometry_fits=geometry_fits,
        residual_depth_after_mains_mm=residual,
        thermal_evidence_complete=False,
        decision=ReleaseDecision.REJECTED,
        findings=findings,
        next_action="Evaluate the next larger black UNICASE PSU candidate with explicit passive-thermal margin; do not reopen M5501119 without measured/calculated thermal evidence.",
    )


def validate_psu_release_decision(model: PsuReleaseDecision) -> list[str]:
    issues: list[str] = []
    if model.enclosure_order_code != "M5501119":
        issues.append("G3-022 release gate must close M5501119")
    if model.mains_entry.order_code != "KMF1.1121.11":
        issues.append("exact SCHURTER KMF mains-entry variant must remain frozen")
    if not model.mains_geometry_fits:
        issues.append("selected mains-entry geometry must fit the assessed M5501119 envelope")
    if model.thermal_evidence_complete:
        issues.append("thermal evidence must not be invented without load and thermal-resistance inputs")
    if model.decision is not ReleaseDecision.REJECTED:
        issues.append("binary G3-022 gate must reject M5501119 when thermal release evidence is incomplete")
    return issues
