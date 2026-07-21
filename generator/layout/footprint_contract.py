"""Schematic-to-PCB footprint contract for Project Shellac Gate 3.

The contract audits every generated schematic component, distinguishes true PCB
members from panel interfaces, and prevents mechanically unresolved connectors
from being emitted into a preliminary board population.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum

from generator.core.sheet import Sheet
from generator.dispatch import shellac_builder_registry
from generator.model.shellac import build_shellac_model


class PopulationStatus(str, Enum):
    APPROVED = "approved"
    PANEL_EXCLUDED = "panel_excluded"
    MECHANICAL_ECO_REQUIRED = "mechanical_eco_required"


@dataclass(frozen=True, slots=True)
class FootprintEntry:
    ref: str
    sheet_id: str
    value: str
    lib_id: str
    footprint: str
    schematic_on_board: bool
    population_status: PopulationStatus
    package_family: str
    placement_authority: str
    rationale: str


@dataclass(slots=True)
class FootprintContract:
    identifier: str
    revision: str
    status: str
    entries: list[FootprintEntry] = field(default_factory=list)
    board_population_refs: list[str] = field(default_factory=list)
    panel_interface_refs: list[str] = field(default_factory=list)
    mechanical_eco_refs: list[str] = field(default_factory=list)
    freeze_blockers: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


# These connectors are electrically correct in the frozen schematic but their
# current horizontal PCB footprints conflict with the accepted panel-harness
# mechanical architecture.  Keep the discrepancy visible until a controlled
# ECO changes the schematic ownership/footprint fields.
_MECHANICAL_ECO: dict[str, str] = {}



def _package_family(footprint: str, lib_id: str) -> str:
    if not footprint:
        return "panel_or_virtual"
    if "SOIC-8" in footprint:
        return "SOIC-8"
    if "0805" in footprint:
        return "0805"
    if "SOD-123" in footprint:
        return "SOD-123"
    if "SMA" in footprint:
        return "SMA"
    if "DIP" in footprint or "SW_DIP" in footprint:
        return "THT_DIP_or_switch"
    if "TestPoint" in footprint:
        return "test_point"
    if "XLR" in footprint:
        return "XLR_interface"
    if lib_id.startswith("Device:R"):
        return "resistor"
    if lib_id.startswith("Device:C"):
        return "capacitor"
    return "other"


def _placement_authority(ref: str, package: str) -> str:
    if ref.startswith("TP"):
        return "manual_probe_access"
    if package in {"SOIC-8", "0805", "SOD-123", "SMA", "test_point"}:
        return "cluster_contract"
    return "manual_review"


def build_footprint_contract() -> FootprintContract:
    model = build_shellac_model()
    registry = shellac_builder_registry()
    entries: list[FootprintEntry] = []

    for block in model.blocks:
        registration = registry.resolve(block.identifier)
        if registration is None:
            continue
        sheet = Sheet(registration.title, f"{block.identifier}.kicad_sch")
        registration.builder(sheet)
        for component in sheet.components:
            if component.ref in _MECHANICAL_ECO:
                status = PopulationStatus.MECHANICAL_ECO_REQUIRED
                rationale = _MECHANICAL_ECO[component.ref]
            elif not component.on_board:
                status = PopulationStatus.PANEL_EXCLUDED
                rationale = "Schematic explicitly declares panel/virtual ownership."
            else:
                status = PopulationStatus.APPROVED
                rationale = "PCB-owned component with an assigned schematic footprint."
            package = _package_family(component.footprint, component.lib_id)
            entries.append(FootprintEntry(
                ref=component.ref,
                sheet_id=block.identifier,
                value=component.value,
                lib_id=component.lib_id,
                footprint=component.footprint,
                schematic_on_board=component.on_board,
                population_status=status,
                package_family=package,
                placement_authority=_placement_authority(component.ref, package),
                rationale=rationale,
            ))

    entries.sort(key=lambda item: (item.sheet_id, item.ref))
    board_refs = [e.ref for e in entries if e.population_status is PopulationStatus.APPROVED]
    panel_refs = [e.ref for e in entries if e.population_status is PopulationStatus.PANEL_EXCLUDED]
    eco_refs = [e.ref for e in entries if e.population_status is PopulationStatus.MECHANICAL_ECO_REQUIRED]
    blockers = [
        f"{ref}: {_MECHANICAL_ECO[ref]}" for ref in sorted(eco_refs)
    ]
    return FootprintContract(
        identifier="G3-009-FPC",
        revision="A1",
        status="PRELIMINARY_BLOCKED" if blockers else "PRELIMINARY_READY",
        entries=entries,
        board_population_refs=board_refs,
        panel_interface_refs=panel_refs,
        mechanical_eco_refs=eco_refs,
        freeze_blockers=blockers,
    )


def validate_footprint_contract(contract: FootprintContract) -> list[str]:
    issues: list[str] = []
    refs = [entry.ref for entry in contract.entries]
    if len(refs) != len(set(refs)):
        issues.append("duplicate reference in footprint contract")
    for entry in contract.entries:
        if entry.population_status is PopulationStatus.APPROVED:
            if not entry.schematic_on_board:
                issues.append(f"{entry.ref} approved despite panel ownership")
            if not entry.footprint:
                issues.append(f"{entry.ref} approved without footprint")
        if entry.population_status is PopulationStatus.PANEL_EXCLUDED and entry.footprint:
            issues.append(f"{entry.ref} panel excluded but still carries PCB footprint")
        if entry.population_status is PopulationStatus.MECHANICAL_ECO_REQUIRED:
            if entry.ref not in _MECHANICAL_ECO:
                issues.append(f"{entry.ref} has undocumented mechanical ECO")
            if entry.ref in contract.board_population_refs:
                issues.append(f"{entry.ref} ECO blocker leaked into board population")
    if sorted(contract.mechanical_eco_refs) != sorted(_MECHANICAL_ECO):
        issues.append("mechanical ECO reference set is incomplete")
    if bool(contract.freeze_blockers) != (contract.status == "PRELIMINARY_BLOCKED"):
        issues.append("contract status does not match blocker state")
    return issues
