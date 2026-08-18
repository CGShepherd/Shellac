"""G3-023 replacement PSU enclosure freeze.

Selects the next larger black METCASE UNICASE after G3-022 rejected UNICASE 1.
The decision uses explicit packaging and passive-thermal *reserve* metrics rather
than inventing a closed-box temperature prediction from missing load/Rth data.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field

from .psu_fit import build_psu_fit_closure
from .psu_release import ReleaseDecision, build_psu_release_decision


@dataclass(frozen=True, slots=True)
class ReplacementEnclosure:
    manufacturer: str
    family: str
    order_code: str
    colour: str
    external_width_mm: float
    external_depth_mm: float
    external_height_mm: float
    usable_inside_width_mm: float
    usable_inside_depth_mm: float
    usable_inside_height_mm: float
    panel_thickness_mm: float
    source_reference: str


@dataclass(frozen=True, slots=True)
class PassiveThermalReserve:
    internal_volume_ratio_vs_rejected: float
    external_surface_area_ratio_vs_rejected: float
    residual_width_after_known_components_mm: float
    residual_depth_after_known_components_and_mains_mm: float
    transformer_headroom_mm: float
    regulator_headroom_mm: float
    temperature_prediction_available: bool
    verification_rule: str


@dataclass(slots=True)
class PsuEnclosureFreeze:
    identifier: str
    revision: str
    enclosure: ReplacementEnclosure
    mains_entry_order_code: str
    known_component_geometry_fits: bool
    historical_size_gate_satisfied: bool
    passive_thermal_reserve: PassiveThermalReserve
    decision: ReleaseDecision
    findings: list[str] = field(default_factory=list)
    remaining_verification: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["decision"] = self.decision.value
        return payload


def _surface_area_mm2(width: float, depth: float, height: float) -> float:
    return 2.0 * (width * depth + width * height + depth * height)


def build_psu_enclosure_freeze() -> PsuEnclosureFreeze:
    old_fit = build_psu_fit_closure()
    old_release = build_psu_release_decision()
    enclosure = ReplacementEnclosure(
        manufacturer="METCASE",
        family="UNICASE 2",
        order_code="M5502119",
        colour="Black RAL 9005",
        external_width_mm=260.0,
        external_depth_mm=250.0,
        external_height_mm=90.2,
        usable_inside_width_mm=256.0,
        usable_inside_depth_mm=236.0,
        usable_inside_height_mm=86.2,
        panel_thickness_mm=2.0,
        source_reference="METCASE M5502119 manufacturer drawing/product data",
    )

    occupied_width = old_fit.side_by_side_fit.occupied_width_mm
    occupied_depth = old_fit.side_by_side_fit.occupied_depth_mm
    mains_depth = old_release.mains_entry.behind_panel_depth_mm
    residual_width = enclosure.usable_inside_width_mm - occupied_width
    residual_depth = enclosure.usable_inside_depth_mm - occupied_depth - mains_depth
    transformer_headroom = enclosure.usable_inside_height_mm - old_fit.transformer.height_mm
    regulator_headroom = enclosure.usable_inside_height_mm - old_fit.regulator.height_mm

    old_volume = old_fit.floor.width_mm * old_fit.floor.depth_mm * old_fit.floor.usable_height_mm
    new_volume = enclosure.usable_inside_width_mm * enclosure.usable_inside_depth_mm * enclosure.usable_inside_height_mm
    old_surface = _surface_area_mm2(185.0, 180.0, 65.0)
    new_surface = _surface_area_mm2(
        enclosure.external_width_mm,
        enclosure.external_depth_mm,
        enclosure.external_height_mm,
    )
    reserve = PassiveThermalReserve(
        internal_volume_ratio_vs_rejected=new_volume / old_volume,
        external_surface_area_ratio_vs_rejected=new_surface / old_surface,
        residual_width_after_known_components_mm=residual_width,
        residual_depth_after_known_components_and_mains_mm=residual_depth,
        transformer_headroom_mm=transformer_headroom,
        regulator_headroom_mm=regulator_headroom,
        temperature_prediction_available=False,
        verification_rule=(
            "Freeze the enclosure from explicit geometric/thermal reserve; verify closed-box "
            "temperatures on the first powered prototype at worst credible load. A failed "
            "temperature test reopens the regulator thermal path before it reopens enclosure size."
        ),
    )

    geometry_fits = (
        residual_width >= 50.0
        and residual_depth >= 75.0
        and transformer_headroom >= 40.0
        and regulator_headroom >= 40.0
    )
    historical_gate = (
        enclosure.usable_inside_width_mm >= 120.0
        and enclosure.usable_inside_depth_mm >= 180.0
        and enclosure.usable_inside_height_mm >= 80.0
    )
    thermal_reserve_is_explicit = (
        reserve.internal_volume_ratio_vs_rejected >= 2.5
        and reserve.external_surface_area_ratio_vs_rejected >= 1.75
        and min(reserve.transformer_headroom_mm, reserve.regulator_headroom_mm) >= 40.0
    )
    decision = (
        ReleaseDecision.FROZEN
        if geometry_fits and historical_gate and thermal_reserve_is_explicit
        else ReleaseDecision.REJECTED
    )

    findings = [
        "M5502119 is the next larger black UNICASE after the rejected M5501119 and is already frozen for the audio enclosure, reducing enclosure-family and procurement variation.",
        f"Its 256 x 236 x 86.2 mm usable envelope leaves {residual_width:.1f} mm width and {residual_depth:.1f} mm depth after the conservative transformer/regulator overlay plus the frozen SCHURTER KMF mains-entry depth.",
        f"Vertical reserve is {transformer_headroom:.1f} mm above the conservative transformer envelope and {regulator_headroom:.1f} mm above the existing regulator-module envelope.",
        f"Relative to rejected M5501119, usable internal volume rises by {reserve.internal_volume_ratio_vs_rejected:.2f}x and nominal external surface area by {reserve.external_surface_area_ratio_vs_rejected:.2f}x.",
        "No junction or enclosure temperature is invented: controlled rail-current and regulator thermal-resistance data remain unavailable, so prototype temperature verification is retained as a verification activity rather than an enclosure-selection blocker.",
        "G3-023 therefore freezes black M5502119 for the PSU enclosure; both Shellac boxes now use the same UNICASE 2 order code.",
    ]
    return PsuEnclosureFreeze(
        identifier="G3-MECH-023",
        revision="Rev A0",
        enclosure=enclosure,
        mains_entry_order_code=old_release.mains_entry.order_code,
        known_component_geometry_fits=geometry_fits,
        historical_size_gate_satisfied=historical_gate,
        passive_thermal_reserve=reserve,
        decision=decision,
        findings=findings,
        remaining_verification=[
            "measure closed-box transformer/regulator temperatures on the first powered prototype at worst credible operating load",
            "retain the toroid anti-shorted-turn mounting rule and rear-mains/front-SELV segregation in detailed layout",
            "confirm current distributor availability at procurement; stock and price are not design invariants",
        ],
    )


def validate_psu_enclosure_freeze(model: PsuEnclosureFreeze) -> list[str]:
    issues: list[str] = []
    if model.enclosure.order_code != "M5502119":
        issues.append("G3-023 must assess and freeze M5502119")
    if model.mains_entry_order_code != "KMF1.1121.11":
        issues.append("frozen SCHURTER KMF mains-entry variant must carry forward")
    if not model.known_component_geometry_fits:
        issues.append("known PSU component/mains envelopes do not preserve required reserve")
    if not model.historical_size_gate_satisfied:
        issues.append("replacement enclosure does not satisfy the established 120 x 180 x 80 mm PSU gate")
    reserve = model.passive_thermal_reserve
    if reserve.internal_volume_ratio_vs_rejected < 2.5:
        issues.append("replacement enclosure lacks explicit internal-volume reserve")
    if reserve.external_surface_area_ratio_vs_rejected < 1.75:
        issues.append("replacement enclosure lacks explicit external-area reserve")
    if reserve.temperature_prediction_available:
        issues.append("temperature prediction must not be claimed without controlled load/Rth evidence")
    if "prototype" not in reserve.verification_rule.lower():
        issues.append("prototype closed-box thermal verification rule is missing")
    if model.decision is not ReleaseDecision.FROZEN:
        issues.append("G3-023 replacement enclosure did not reach the required binary FROZEN decision")
    return issues
