"""Foundry's CAD-independent engineering model.

This module deliberately contains no KiCad concepts such as pages, coordinates,
symbols, wires or sheet filenames.  Those belong to renderer/adaptor layers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable


class Direction(str, Enum):
    INPUT = "input"
    OUTPUT = "output"
    BIDIRECTIONAL = "bidirectional"
    POWER = "power"
    GROUND = "ground"


class SignalKind(str, Enum):
    ANALOG = "analog"
    CONTROL = "control"
    POWER = "power"
    GROUND = "ground"


@dataclass(frozen=True, slots=True)
class Signal:
    """A named project-level electrical or logical connection."""

    name: str
    kind: SignalKind
    description: str = ""

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Signal name must not be empty.")


@dataclass(frozen=True, slots=True)
class Interface:
    """One externally visible connection on a functional block."""

    name: str
    signal: str
    direction: Direction
    description: str = ""

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Interface name must not be empty.")
        if not self.signal.strip():
            raise ValueError("Interface signal must not be empty.")


@dataclass(frozen=True, slots=True)
class Constraint:
    """A concise engineering requirement attached to a block or project."""

    identifier: str
    statement: str
    rationale: str = ""
    verification: str = ""

    def __post_init__(self) -> None:
        if not self.identifier.strip():
            raise ValueError("Constraint identifier must not be empty.")
        if not self.statement.strip():
            raise ValueError("Constraint statement must not be empty.")


@dataclass(frozen=True, slots=True)
class PowerDomain:
    name: str
    nominal_voltage: str
    description: str = ""


@dataclass(frozen=True, slots=True)
class GroundDomain:
    name: str
    description: str = ""


@dataclass(slots=True)
class FunctionalBlock:
    """The principal unit of engineering intent in Foundry."""

    identifier: str
    name: str
    purpose: str
    interfaces: list[Interface] = field(default_factory=list)
    constraints: list[Constraint] = field(default_factory=list)
    children: list["FunctionalBlock"] = field(default_factory=list)
    implementation_ref: str | None = None

    def add_interface(self, interface: Interface) -> Interface:
        self.interfaces.append(interface)
        return interface

    def add_constraint(self, constraint: Constraint) -> Constraint:
        self.constraints.append(constraint)
        return constraint

    def add_child(self, child: "FunctionalBlock") -> "FunctionalBlock":
        self.children.append(child)
        return child

    def walk(self) -> Iterable["FunctionalBlock"]:
        yield self
        for child in self.children:
            yield from child.walk()


@dataclass(slots=True)
class ProjectModel:
    """Single authoritative architecture model for one hardware product."""

    identifier: str
    name: str
    revision: str
    purpose: str
    blocks: list[FunctionalBlock] = field(default_factory=list)
    signals: list[Signal] = field(default_factory=list)
    power_domains: list[PowerDomain] = field(default_factory=list)
    ground_domains: list[GroundDomain] = field(default_factory=list)
    constraints: list[Constraint] = field(default_factory=list)

    def add_block(self, block: FunctionalBlock) -> FunctionalBlock:
        self.blocks.append(block)
        return block

    def all_blocks(self) -> Iterable[FunctionalBlock]:
        for block in self.blocks:
            yield from block.walk()
