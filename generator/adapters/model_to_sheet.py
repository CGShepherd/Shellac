"""Minimal bridge from Foundry model objects to the existing Sheet API.

Revision A intentionally creates architecture-summary sheets only.  Detailed
circuit rendering remains with the existing proven block builders.
"""

from __future__ import annotations

from generator.core.sheet import Sheet
from generator.model.core import FunctionalBlock, ProjectModel


def block_summary_sheet(project: ProjectModel, block: FunctionalBlock, filename: str) -> Sheet:
    sheet = Sheet(
        title=f"{project.name} — {block.identifier} {block.name}",
        filename=filename,
    )
    sheet.add_note(f"Purpose: {block.purpose}")
    sheet.add_note(f"Engineering-model revision: {project.revision}")
    if block.implementation_ref:
        sheet.add_note(f"Detailed implementation: {block.implementation_ref}")

    sheet.add_note("Interfaces:")
    for interface in block.interfaces:
        sheet.add_note(
            f"  {interface.direction.value.upper():13s} "
            f"{interface.name} -> {interface.signal}"
        )

    if block.constraints:
        sheet.add_note("Constraints:")
        for constraint in block.constraints:
            sheet.add_note(f"  {constraint.identifier}: {constraint.statement}")

    return sheet
