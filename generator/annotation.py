"""Project-wide deterministic reference validation."""

from __future__ import annotations

from collections.abc import Iterable
import re


_ANNOTATED_REFERENCE = re.compile(r"^[A-Za-z#]+[0-9]+$")


def duplicate_references(sheets: Iterable[tuple[str, object]]) -> dict[str, tuple[str, ...]]:
    owners: dict[str, list[str]] = {}
    for block_id, sheet in sheets:
        for component in sheet.components:
            owners.setdefault(component.ref, []).append(block_id)
    return {
        reference: tuple(block_ids)
        for reference, block_ids in sorted(owners.items())
        if len(block_ids) > 1
    }


def invalid_references(sheets: Iterable[tuple[str, object]]) -> dict[str, str]:
    invalid: dict[str, str] = {}
    for block_id, sheet in sheets:
        for component in sheet.components:
            if not _ANNOTATED_REFERENCE.fullmatch(component.ref):
                invalid[component.ref] = block_id
    return dict(sorted(invalid.items()))


def validate_unique_references(sheets: Iterable[tuple[str, object]]) -> None:
    sheets = tuple(sheets)
    duplicates = duplicate_references(sheets)
    invalid = invalid_references(sheets)
    errors = []
    if duplicates:
        errors.append(
            "duplicates " + "; ".join(
                f"{reference}: {', '.join(block_ids)}"
                for reference, block_ids in duplicates.items()
            )
        )
    if invalid:
        errors.append(
            "invalid " + "; ".join(
                f"{reference}: {block_id}"
                for reference, block_id in invalid.items()
            )
        )
    if errors:
        raise ValueError("Project annotation errors: " + " | ".join(errors))
