"""Gate 3 real-footprint readiness audit.

This audit separates footprint identities that are mechanically credible from
schematic value/package combinations that still need a controlled ECO before a
manufacturable KiCad board can be populated.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field

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
        elif entry.lib_id.startswith("Device:C") and entry.value == "10u NP":
            findings.append(FootprintAuditFinding(
                ref=entry.ref,
                sheet_id=entry.sheet_id,
                severity="BLOCKER",
                category="non_polar_10u_0805_unresolved",
                value=entry.value,
                footprint=entry.footprint,
                finding=(
                    "A non-polar 10 uF signal capacitor is assigned to a generic 0805 "
                    "footprint without an approved dielectric, voltage or derating basis."
                ),
                required_action=(
                    "Select the physical capacitor technology and rated voltage, then "
                    "assign the corresponding real footprint before placement acceptance."
                ),
            ))
        elif entry.lib_id.startswith("Device:C") and entry.value == "10u":
            findings.append(FootprintAuditFinding(
                ref=entry.ref,
                sheet_id=entry.sheet_id,
                severity="REVIEW",
                category="10u_0805_derating_review",
                value=entry.value,
                footprint=entry.footprint,
                finding=(
                    "10 uF in 0805 may be electrically viable only with a specific MLCC "
                    "voltage rating and acceptable DC-bias derating."
                ),
                required_action=(
                    "Confirm rail exposure, dielectric, rated voltage and effective "
                    "capacitance before freezing the footprint."
                ),
            ))

    blockers = sum(f.severity == "BLOCKER" for f in findings)
    reviews = sum(f.severity == "REVIEW" for f in findings)
    accepted = len(entries) - blockers - reviews
    return RealFootprintAudit(
        identifier="G3-FPA-016",
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
    np10 = [f for f in audit.findings if f.category == "non_polar_10u_0805_unresolved"]
    if len(np10) != 4:
        issues.append(f"expected 4 non-polar 10 uF blockers, found {len(np10)}")
    return issues
