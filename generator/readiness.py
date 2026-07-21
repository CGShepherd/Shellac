"""Schematic-generation readiness audit for Project Shellac.

This audit separates two distinct states:

1. Electrical engineering closure: the intended circuit function and values are
   approved in the engineering model.
2. CAD schematic closure: the generated KiCad project contains pin-aware,
   electrically connected, resolvable schematic symbols.

A block is not CAD-ready merely because its builder emits components and notes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from generator.core.sheet import Sheet
from generator.dispatch import BuilderRegistry
from generator.model.core import ProjectModel
from generator.writers.kicad9 import embedded_symbol_ids
from generator.annotation import duplicate_references
from generator.hierarchy import connected_project_signals



@dataclass(frozen=True, slots=True)
class BlockReadiness:
    block_id: str
    name: str
    components: int
    wires: int
    labels: int
    unresolved_custom_symbols: tuple[str, ...] = ()
    blockers: tuple[str, ...] = ()
    human_reviewable: bool = False

    @property
    def cad_ready(self) -> bool:
        return not self.blockers


@dataclass(frozen=True, slots=True)
class ProjectReadiness:
    blocks: tuple[BlockReadiness, ...]
    project_blockers: tuple[str, ...] = ()
    hierarchical_sheets: int = 0
    hierarchical_pins: int = 0
    cross_sheet_signals: int = 0

    @property
    def cad_ready(self) -> bool:
        return not self.project_blockers and all(block.cad_ready for block in self.blocks)

    @property
    def ready_blocks(self) -> int:
        return sum(block.cad_ready for block in self.blocks)

    @property
    def human_reviewable_blocks(self) -> int:
        return sum(block.human_reviewable for block in self.blocks)

    @property
    def human_review_ready(self) -> bool:
        return bool(self.blocks) and all(block.human_reviewable for block in self.blocks)


def _symbol_ids(sheet: Sheet) -> set[str]:
    return {
        component.lib_id
        for component in sheet.components
    }


def audit_block(block, registration, *, human_reviewable: bool = False) -> BlockReadiness:
    sheet = Sheet(title=registration.title, filename=f"{block.identifier}.kicad_sch")
    registration.builder(sheet)

    blockers: list[str] = []
    unresolved = tuple(
        sorted(_symbol_ids(sheet) - embedded_symbol_ids())
    )

    if not sheet.components:
        blockers.append("Builder emits no components.")

    # A functional electronic block with multiple signal interfaces cannot be
    # considered connected when it emits no wires.
    signal_interfaces = [
        interface
        for interface in block.interfaces
        if interface.direction.value in {"input", "output", "bidirectional"}
    ]
    if len(signal_interfaces) >= 2 and not sheet.wires:
        blockers.append("No pin-level electrical wiring is emitted.")

    if unresolved:
        blockers.append(
            "Writer has no embedded definition for custom symbol(s): "
            + ", ".join(unresolved)
        )

    return BlockReadiness(
        block_id=block.identifier,
        name=block.name,
        components=len(sheet.components),
        wires=len(sheet.wires),
        labels=len(sheet.labels),
        unresolved_custom_symbols=unresolved,
        blockers=tuple(blockers),
        human_reviewable=human_reviewable,
    )


def audit_project(
    project: ProjectModel,
    registry: BuilderRegistry,
    erc_violations: int | None = None,
    human_reviewable_block_ids: Iterable[str] = (),
) -> ProjectReadiness:
    results: list[BlockReadiness] = []
    project_blockers: list[str] = []

    registered = registry.registered_ids()
    model_ids = {block.identifier for block in project.blocks}

    missing_builders = sorted(model_ids - registered)
    unexpected_builders = sorted(registered - model_ids)
    if missing_builders:
        project_blockers.append(
            "Missing registered builders: " + ", ".join(missing_builders)
        )
    if unexpected_builders:
        project_blockers.append(
            "Registered builders without model blocks: " + ", ".join(unexpected_builders)
        )

    human_reviewable_ids = frozenset(human_reviewable_block_ids)
    for block in project.blocks:
        registration = registry.resolve(block.identifier)
        if registration is None:
            continue
        results.append(audit_block(
            block,
            registration,
            human_reviewable=block.identifier in human_reviewable_ids,
        ))

    built_sheets = []
    for block in project.blocks:
        registration = registry.resolve(block.identifier)
        if registration is None:
            continue
        sheet = Sheet(title=registration.title, filename=f"{block.identifier}.kicad_sch")
        registration.builder(sheet)
        built_sheets.append((block.identifier, sheet))
    duplicates = duplicate_references(built_sheets)
    if duplicates:
        project_blockers.append(
            "Duplicate project references: " + ", ".join(duplicates)
        )

    if erc_violations is None:
        project_blockers.append(
            "Native KiCad hierarchical electrical-rules checking result was not supplied."
        )
    elif erc_violations:
        project_blockers.append(
            f"Native KiCad hierarchical electrical-rules checking reports {erc_violations} violation(s)."
        )

    signal_membership = connected_project_signals(project)
    return ProjectReadiness(
        tuple(results),
        tuple(project_blockers),
        hierarchical_sheets=len(results),
        hierarchical_pins=sum(len(block.interfaces) for block in project.blocks),
        cross_sheet_signals=sum(len(blocks) > 1 for blocks in signal_membership.values()),
    )
