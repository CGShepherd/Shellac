"""Gate 3 enclosure-decision and carrier-plate freeze logic.

No catalogue enclosure is accepted without a complete manufacturer drawing.
The module therefore separates a *decision-ready* candidate from a merely
plausible candidate and derives carrier/PCB datums only from verified geometry.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field

from generator.mechanical.model import (
    CandidateStatus,
    EnclosureCandidate,
    EnclosureRole,
    MechanicalBaseline,
    build_mechanical_baseline,
    evaluate_candidate,
)


@dataclass(frozen=True, slots=True)
class DrawingEvidence:
    internal_dimensions_verified: bool
    boss_pattern_verified: bool
    lid_intrusion_verified: bool
    panel_thickness_verified: bool
    connector_depth_verified: bool
    source_reference: str | None = None

    @property
    def complete(self) -> bool:
        return all((
            self.internal_dimensions_verified,
            self.boss_pattern_verified,
            self.lid_intrusion_verified,
            self.panel_thickness_verified,
            self.connector_depth_verified,
            bool(self.source_reference),
        ))


@dataclass(frozen=True, slots=True)
class CarrierPlateFreeze:
    enclosure_candidate_id: str
    plate_width_mm: float
    plate_depth_mm: float
    plate_thickness_mm: float
    plate_origin: str
    pcb_origin_x_mm: float
    pcb_origin_y_mm: float
    pcb_width_mm: float
    pcb_depth_mm: float
    mounting_hole_strategy: str
    service_removal_direction: str
    status: str


@dataclass(slots=True)
class EnclosureDecision:
    identifier: str
    revision: str
    role: EnclosureRole
    candidate_id: str | None
    status: str
    gate_findings: list[str] = field(default_factory=list)
    required_evidence: list[str] = field(default_factory=list)
    carrier_freeze: CarrierPlateFreeze | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def decision_findings(
    candidate: EnclosureCandidate,
    baseline: MechanicalBaseline,
    evidence: DrawingEvidence,
) -> list[str]:
    requirement = (
        baseline.audio_requirement
        if candidate.role is EnclosureRole.AUDIO
        else baseline.psu_requirement
    )
    findings = evaluate_candidate(candidate, requirement)
    if candidate.status is CandidateStatus.REJECTED:
        findings.append("candidate is already rejected by the trade study")
    if not evidence.internal_dimensions_verified:
        findings.append("manufacturer drawing has not verified usable internal dimensions")
    if not evidence.boss_pattern_verified:
        findings.append("mounting boss pattern and usable carrier-plate area are unverified")
    if not evidence.lid_intrusion_verified:
        findings.append("lid intrusion and fitted-control clearance are unverified")
    if not evidence.panel_thickness_verified:
        findings.append("panel thickness is unverified for XLR and switch hardware")
    if not evidence.connector_depth_verified:
        findings.append("rearward connector and harness depth is unverified")
    if not evidence.source_reference:
        findings.append("authoritative manufacturer drawing reference is missing")
    return findings


def derive_carrier_freeze(
    candidate: EnclosureCandidate,
    evidence: DrawingEvidence,
    *,
    pcb_width_mm: float = 220.0,
    pcb_depth_mm: float = 140.0,
    carrier_edge_margin_mm: float = 5.0,
) -> CarrierPlateFreeze:
    if not evidence.complete:
        raise ValueError("carrier plate cannot be frozen without complete drawing evidence")
    if candidate.internal_width_mm is None or candidate.internal_depth_mm is None:
        raise ValueError("candidate internal dimensions are incomplete")
    plate_w = candidate.internal_width_mm - 2 * carrier_edge_margin_mm
    plate_d = candidate.internal_depth_mm - 2 * carrier_edge_margin_mm
    if plate_w < pcb_width_mm + 10.0 or plate_d < pcb_depth_mm + 10.0:
        raise ValueError("verified carrier plate does not preserve 5 mm PCB margin on all sides")
    return CarrierPlateFreeze(
        enclosure_candidate_id=candidate.identifier,
        plate_width_mm=round(plate_w, 3),
        plate_depth_mm=round(plate_d, 3),
        plate_thickness_mm=2.0,
        plate_origin="lower-left internal floor datum, component-side view",
        pcb_origin_x_mm=round((plate_w - pcb_width_mm) / 2, 3),
        pcb_origin_y_mm=round((plate_d - pcb_depth_mm) / 2, 3),
        pcb_width_mm=pcb_width_mm,
        pcb_depth_mm=pcb_depth_mm,
        mounting_hole_strategy="four carrier-plate fasteners plus four PCB standoffs; enclosure bosses used only where drawing confirms alignment",
        service_removal_direction="vertical",
        status="FROZEN",
    )


def build_enclosure_decision_baseline() -> list[EnclosureDecision]:
    baseline = build_mechanical_baseline()
    evidence = DrawingEvidence(False, False, False, False, False, None)
    decisions: list[EnclosureDecision] = []
    for role in (EnclosureRole.AUDIO, EnclosureRole.PSU):
        eligible = [candidate for candidate in baseline.candidates if candidate.role is role]
        ranked = sorted(eligible, key=lambda item: item.weighted_score, reverse=True)
        candidate = ranked[0] if ranked else None
        findings = decision_findings(candidate, baseline, evidence) if candidate else ["no candidate available"]
        decisions.append(EnclosureDecision(
            identifier=f"G3-ENC-006-{role.value.upper()}",
            revision="Rev A0",
            role=role,
            candidate_id=candidate.identifier if candidate else None,
            status="BLOCKED — authoritative drawing evidence required",
            gate_findings=findings,
            required_evidence=[
                "manufacturer dimensional drawing and order code",
                "verified usable internal width/depth/height",
                "mounting boss or baseplate pattern",
                "lid/base intrusion envelope",
                "panel thickness and flat machining zones",
                "connector and control body rearward depth",
            ],
        ))
    return decisions
