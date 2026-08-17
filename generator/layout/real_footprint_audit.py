"""Gate 3 real-footprint readiness audit.

This audit separates footprint identities that are mechanically credible from
schematic value/package combinations that still need a controlled ECO before a
manufacturable KiCad board can be populated.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field

from generator.component_selection import (
    BULK_DECOUPLING_10UF_SMD,
    NONPOLAR_FEEDBACK_10UF_THT,
)
from generator.layout.footprint_contract import build_footprint_contract


@dataclass(frozen=True, slots=True)
class FootprintAuditFinding:
    ref: str
    sheet_id: str
    severity: str
    category: str
    value: str
    footprint: str
    finding: str
    required_action: str


@dataclass(slots=True)
class RealFootprintAudit:
    identifier: str
    revision: str
    status: str
    board_population_count: int
    accepted_identity_count: int
    review_count: int
    blocker_count: int
    findings: list[FootprintAuditFinding] = field(default_factory=list)
    invariants: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def _is_compound_capacitor_value(value: str) -> bool:
    return "+" in value and any(unit in value.lower() for unit in ("p", "n", "u"))


def build_real_footprint_audit() -> RealFootprintAudit:
    contract = build_footprint_contract()
    entries = [e for e in contract.entries if e.ref in contract.board_population_refs]
    findings: list[FootprintAuditFinding] = []

    for entry in entries:
        if entry.lib_id.startswith("Device:C") and _is_compound_capacitor_value(entry.value):
            findings.append(FootprintAuditFinding(
                ref=entry.ref,
                sheet_id=entry.sheet_id,
                severity="BLOCKER",
                category="compound_capacitor_not_physical",
                value=entry.value,
                footprint=entry.footprint,
                finding=(
                    "One schematic reference encodes multiple parallel capacitor values "
                    "but owns only one PCB footprint."
                ),
                required_action=(
                    "Decompose into individually referenced physical capacitors while "
                    "preserving the synthesised aggregate value and channel symmetry."
                ),
            ))
        elif (
            entry.lib_id.startswith("Device:C")
            and entry.value == "10u NP"
            and entry.footprint != NONPOLAR_FEEDBACK_10UF_THT
        ):
            findings.append(FootprintAuditFinding(
                ref=entry.ref,
                sheet_id=entry.sheet_id,
                severity="BLOCKER",
                category="non_polar_10u_physical_unresolved",
                value=entry.value,
                footprint=entry.footprint,
                finding=(
                    "A non-polar 10 uF signal capacitor does not use the controlled "
                    "common-mode feedback footprint policy."
                ),
                required_action=(
                    "Apply the controlled 10 uF non-polar feedback requirements before "
                    "placement acceptance."
                ),
            ))
        elif (
            entry.lib_id.startswith("Device:C")
            and entry.value == "10u"
            and entry.footprint != BULK_DECOUPLING_10UF_SMD
        ):
            findings.append(FootprintAuditFinding(
                ref=entry.ref,
                sheet_id=entry.sheet_id,
                severity="REVIEW",
                category="10u_bulk_physical_identity_review",
                value=entry.value,
                footprint=entry.footprint,
                finding=(
                    "A 10 uF bulk decoupling capacitor does not use the controlled "
                    "35 V low-ESR electrolytic footprint policy."
                ),
                required_action=(
                    "Apply the controlled 10 uF bulk-decoupling requirements before "
                    "freezing the footprint."
                ),
            ))

    blockers = sum(f.severity == "BLOCKER" for f in findings)
    reviews = sum(f.severity == "REVIEW" for f in findings)
    accepted = len(entries) - blockers - reviews
    return RealFootprintAudit(
        identifier="G3-FPA-017",
        revision="Rev A0",
        status=("BLOCKED — schematic-to-physical capacitor ECO required" if blockers else "READY"),
        board_population_count=len(entries),
        accepted_identity_count=accepted,
        review_count=reviews,
        blocker_count=blockers,
        findings=sorted(findings, key=lambda f: (f.severity, f.sheet_id, f.ref)),
        invariants=[
            "No compound electrical value may be represented by one physical footprint.",
            "Signal-path capacitor technology and voltage rating must be explicit.",
            "Mirrored channels must retain identical physical decomposition.",
            "Only conventional solderable terminations are permitted; conductive-epoxy-only parts are prohibited.",
            "No footprint audit action authorises routing or manufacturing release.",
        ],
    )


def validate_real_footprint_audit(audit: RealFootprintAudit) -> list[str]:
    issues: list[str] = []
    if audit.board_population_count != (
        audit.accepted_identity_count + audit.review_count + audit.blocker_count
    ):
        issues.append("audit population accounting does not balance")
    refs = [f.ref for f in audit.findings]
    if len(refs) != len(set(refs)):
        issues.append("duplicate footprint audit finding")
    compound = [f for f in audit.findings if f.category == "compound_capacitor_not_physical"]
    if compound:
        issues.append(f"compound-capacitor blockers remain: {len(compound)}")
    np10 = [f for f in audit.findings if f.category == "non_polar_10u_physical_unresolved"]
    if np10:
        issues.append(f"non-polar 10 uF blockers remain: {len(np10)}")
    bulk10 = [f for f in audit.findings if f.category == "10u_bulk_physical_identity_review"]
    if bulk10:
        issues.append(f"10 uF bulk footprint reviews remain: {len(bulk10)}")
    return issues
