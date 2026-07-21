"""Structural validation for the Foundry engineering model."""

from __future__ import annotations

from dataclasses import dataclass

from .core import Direction, ProjectModel, SignalKind


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    code: str
    location: str
    message: str


class ModelValidationError(ValueError):
    def __init__(self, issues: list[ValidationIssue]):
        self.issues = issues
        super().__init__(
            "Engineering model validation failed:\n"
            + "\n".join(
                f"- {issue.code} at {issue.location}: {issue.message}"
                for issue in issues
            )
        )


def _duplicates(values: list[str]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates


def validate_project(project: ProjectModel, *, raise_on_error: bool = True) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    blocks = list(project.all_blocks())
    signal_by_name = {signal.name: signal for signal in project.signals}

    for duplicate in sorted(_duplicates([block.identifier for block in blocks])):
        issues.append(
            ValidationIssue("FM001", "project.blocks", f"Duplicate block identifier {duplicate!r}.")
        )

    for duplicate in sorted(_duplicates([signal.name for signal in project.signals])):
        issues.append(
            ValidationIssue("FM002", "project.signals", f"Duplicate signal name {duplicate!r}.")
        )

    for duplicate in sorted(_duplicates([item.name for item in project.power_domains])):
        issues.append(
            ValidationIssue("FM003", "project.power_domains", f"Duplicate power domain {duplicate!r}.")
        )

    for duplicate in sorted(_duplicates([item.name for item in project.ground_domains])):
        issues.append(
            ValidationIssue("FM004", "project.ground_domains", f"Duplicate ground domain {duplicate!r}.")
        )

    for block in blocks:
        location = f"block[{block.identifier}]"
        if not block.purpose.strip():
            issues.append(ValidationIssue("FM010", location, "Purpose must not be empty."))

        for duplicate in sorted(_duplicates([item.name for item in block.interfaces])):
            issues.append(
                ValidationIssue("FM011", location, f"Duplicate interface name {duplicate!r}.")
            )

        for interface in block.interfaces:
            signal = signal_by_name.get(interface.signal)
            if signal is None:
                issues.append(
                    ValidationIssue(
                        "FM012",
                        f"{location}.interface[{interface.name}]",
                        f"Unknown signal {interface.signal!r}.",
                    )
                )
                continue

            if interface.direction is Direction.POWER and signal.kind is not SignalKind.POWER:
                issues.append(
                    ValidationIssue(
                        "FM013",
                        f"{location}.interface[{interface.name}]",
                        "POWER interface must reference a power signal.",
                    )
                )

            if interface.direction is Direction.GROUND and signal.kind is not SignalKind.GROUND:
                issues.append(
                    ValidationIssue(
                        "FM014",
                        f"{location}.interface[{interface.name}]",
                        "GROUND interface must reference a ground signal.",
                    )
                )

    used_signals = {
        interface.signal
        for block in blocks
        for interface in block.interfaces
    }
    for signal in project.signals:
        if signal.name not in used_signals:
            issues.append(
                ValidationIssue(
                    "FM020",
                    f"signal[{signal.name}]",
                    "Signal is declared but unused.",
                )
            )

    if issues and raise_on_error:
        raise ModelValidationError(issues)
    return issues
