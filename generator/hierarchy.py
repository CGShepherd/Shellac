"""Deterministic KiCad hierarchy derived from the Engineering Model.

This module is deliberately limited to CAD adaptation.  The engineering model
continues to own block identities, interfaces, directions and signal names;
layout coordinates and legacy sheet-label aliases remain renderer concerns.
"""

from __future__ import annotations

from dataclasses import dataclass
import uuid

from generator.model.core import Direction, FunctionalBlock, ProjectModel


FOUNDRY_UUID_NAMESPACE = uuid.UUID("d352ba17-42ae-5d8d-a71d-bf8b9f0f91a4")


GLOBAL_POWER_DOMAINS = frozenset({"+18V", "-18V", "0VA", "CHASSIS"})


def deterministic_uuid(*parts: object) -> str:
    """Return a stable UUID for one generated engineering identity."""

    key = "::".join(str(part) for part in parts)
    return str(uuid.uuid5(FOUNDRY_UUID_NAMESPACE, key))


def root_schematic_uuid(project_name: str) -> str:
    return deterministic_uuid("root-schematic", project_name)


def sheet_instance_uuid(project_name: str, block_id: str) -> str:
    return deterministic_uuid("sheet-instance", project_name, block_id)


def root_instance_path(project_name: str) -> str:
    """Return KiCad's parent path for sheet-symbol instances on the root."""

    return f"/{root_schematic_uuid(project_name)}"


def sheet_instance_path(project_name: str, block_id: str) -> str:
    """Return the full instance path used by symbols inside one child sheet."""

    return f"{root_instance_path(project_name)}/{sheet_instance_uuid(project_name, block_id)}"


def pin_shape(direction: Direction) -> str:
    if direction is Direction.INPUT:
        return "input"
    if direction is Direction.OUTPUT:
        return "output"
    if direction is Direction.BIDIRECTIONAL:
        return "bidirectional"
    return "passive"


@dataclass(frozen=True, slots=True)
class HierarchicalPort:
    name: str
    shape: str
    x: float
    y: float
    visible: bool = True


# Early builders used local descriptive net names before the Engineering Model
# became authoritative.  These aliases attach hierarchy labels to the proven
# electrical nodes without changing any validated analogue circuit.
_BLOCK_NET_ALIASES: dict[str, dict[str, str]] = {}


def child_hierarchical_ports(sheet, block: FunctionalBlock) -> tuple[HierarchicalPort, ...]:
    """Place child hierarchical labels on existing named electrical nodes.

    Mechanical control-state interfaces have no electrical switch-control pin
    in the functional symbols.  They are still represented as passive
    hierarchy ports for architecture traceability, at a deterministic margin
    position, without modifying the analogue switch contacts.
    """

    aliases = _BLOCK_NET_ALIASES.get(block.identifier, {})
    wire_endpoints = {
        (wire.x1, wire.y1) for wire in sheet.wires
    } | {
        (wire.x2, wire.y2) for wire in sheet.wires
    }
    label_positions: dict[str, tuple[float, float]] = {}
    for item in sheet.labels:
        position = (item.x, item.y)
        if position in wire_endpoints:
            label_positions.setdefault(item.name, position)

    fallback_input_y = 55.0
    fallback_output_y = 55.0
    ports: list[HierarchicalPort] = []
    for index, interface in enumerate(block.interfaces):
        if interface.signal in GLOBAL_POWER_DOMAINS:
            continue
        local_name = aliases.get(interface.signal, interface.signal)
        position = label_positions.get(local_name)
        if position is None:
            from generator.core.components import Component
            from generator.core.geometry import Point
            if interface.direction is Direction.OUTPUT:
                anchor_at = Point(375.0, fallback_output_y)
                fallback_output_y += 6.0
            else:
                anchor_at = Point(65.0, fallback_input_y)
                fallback_input_y += 6.0
            anchor = sheet.add_component(Component(
                ref=f"H{block.identifier[3:]}{index + 1:02d}",
                lib_id="ProjectShellac:Hierarchy_Port_Anchor",
                value=f"{interface.signal} HIERARCHY ANCHOR",
                at=anchor_at,
                in_bom=False,
                on_board=False,
                fields={"Function": "Non-physical hierarchy interface anchor"},
            ))
            end = sheet.connect_pin_to_net(anchor, "PORT", interface.signal, stub_dx=-8.0)
            position = (end.x, end.y)
        ports.append(
            HierarchicalPort(
                name=interface.signal,
                shape=pin_shape(interface.direction),
                x=position[0],
                y=position[1],
                visible=position in label_positions.values(),
            )
        )
    return tuple(ports)


def connected_project_signals(project: ProjectModel) -> dict[str, tuple[str, ...]]:
    """Return deterministic signal-to-block membership for root connectivity."""

    connections: dict[str, list[str]] = {}
    for block in project.blocks:
        for interface in block.interfaces:
            connections.setdefault(interface.signal, []).append(block.identifier)
    return {
        signal: tuple(blocks)
        for signal, blocks in sorted(connections.items())
    }
