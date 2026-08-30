"""Internal electrical-integrity audit for generated schematic sheets.

This checker complements native KiCad ERC.  It validates the in-memory design
before serialization and detects three failure classes that previously escaped
basic builder tests:

* off-grid electrical geometry;
* required symbol pins without a conductor or explicit no-connect;
* incompatible net labels joined by generated conductor geometry.

Components are intentionally *not* treated as conductive between their pins.
Only wires and labels form nets.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from generator.core.geometry import Point
from generator.core.grid import is_aligned_point
from generator.core.pins import SYMBOL_PIN_CONTRACTS, pin_position


def _key(point: Point) -> tuple[float, float]:
    return (round(float(point.x), 8), round(float(point.y), 8))


def _point_on_segment(point: Point, wire) -> bool:
    x, y = _key(point)
    x1, y1 = round(wire.x1, 8), round(wire.y1, 8)
    x2, y2 = round(wire.x2, 8), round(wire.y2, 8)
    cross = (x - x1) * (y2 - y1) - (y - y1) * (x2 - x1)
    if abs(cross) > 1e-7:
        return False
    return (
        min(x1, x2) - 1e-8 <= x <= max(x1, x2) + 1e-8
        and min(y1, y2) - 1e-8 <= y <= max(y1, y2) + 1e-8
    )


@dataclass(frozen=True, slots=True)
class PinIssue:
    reference: str
    pin_name: str
    point: Point


@dataclass(frozen=True, slots=True)
class NetNameConflict:
    names: tuple[str, ...]
    pin_references: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SheetElectricalAudit:
    sheet_name: str
    off_grid_items: tuple[str, ...]
    unterminated_pins: tuple[PinIssue, ...]
    net_name_conflicts: tuple[NetNameConflict, ...]
    zero_length_wires: int

    @property
    def passed(self) -> bool:
        return not (
            self.off_grid_items
            or self.unterminated_pins
            or self.net_name_conflicts
            or self.zero_length_wires
        )


class _DisjointSet:
    def __init__(self, items):
        self.parent = {item: item for item in items}

    def find(self, item):
        parent = self.parent[item]
        if parent != item:
            self.parent[item] = self.find(parent)
        return self.parent[item]

    def union(self, left, right):
        left_root, right_root = self.find(left), self.find(right)
        if left_root != right_root:
            self.parent[right_root] = left_root


def audit_sheet_electrical(sheet) -> SheetElectricalAudit:
    off_grid: list[str] = []
    zero_length = 0

    for component in sheet.components:
        if not is_aligned_point(component.at):
            off_grid.append(f"component {component.ref} origin")
        for pin_name in SYMBOL_PIN_CONTRACTS.get(component.lib_id, {}):
            if not is_aligned_point(pin_position(component, pin_name)):
                off_grid.append(f"component {component.ref} pin {pin_name}")

    for index, wire in enumerate(sheet.wires):
        start, end = Point(wire.x1, wire.y1), Point(wire.x2, wire.y2)
        if not is_aligned_point(start) or not is_aligned_point(end):
            off_grid.append(f"wire {index}")
        if _key(start) == _key(end):
            zero_length += 1

    for index, label in enumerate(sheet.labels):
        if not is_aligned_point(Point(label.x, label.y)):
            off_grid.append(f"label {index}:{label.name}")
    for index, point in enumerate(sheet.no_connects):
        if not is_aligned_point(point):
            off_grid.append(f"no-connect {index}")

    # Nodes include every conductor endpoint and every semantic object that may
    # intentionally sit on the middle of a conductor.
    node_keys: set[tuple[float, float]] = set()
    for wire in sheet.wires:
        node_keys.add(_key(Point(wire.x1, wire.y1)))
        node_keys.add(_key(Point(wire.x2, wire.y2)))
    node_keys.update(_key(Point(label.x, label.y)) for label in sheet.labels)
    node_keys.update(_key(point) for point in sheet.no_connects)
    for component in sheet.components:
        for pin_name in SYMBOL_PIN_CONTRACTS.get(component.lib_id, {}):
            node_keys.add(_key(pin_position(component, pin_name)))

    dsu = _DisjointSet(node_keys)
    node_points = [Point(*item) for item in node_keys]
    for wire in sheet.wires:
        points = [point for point in node_points if _point_on_segment(point, wire)]
        if abs(wire.x2 - wire.x1) >= abs(wire.y2 - wire.y1):
            points.sort(key=lambda item: (item.x, item.y))
        else:
            points.sort(key=lambda item: (item.y, item.x))
        for left, right in zip(points, points[1:]):
            dsu.union(_key(left), _key(right))

    # KiCad local labels with the same name on one sheet are electrically
    # equivalent even when they are not joined by drawn conductor geometry.
    label_keys_by_name: dict[str, list[tuple[float, float]]] = defaultdict(list)
    for label in sheet.labels:
        label_keys_by_name[label.name].append(_key(Point(label.x, label.y)))
    for keys in label_keys_by_name.values():
        if len(keys) < 2:
            continue
        anchor = keys[0]
        for other in keys[1:]:
            dsu.union(anchor, other)

    no_connect_keys = {_key(point) for point in sheet.no_connects}
    unterminated: list[PinIssue] = []
    pin_refs_by_root: dict[tuple[float, float], set[str]] = defaultdict(set)
    for component in sheet.components:
        for pin_name in SYMBOL_PIN_CONTRACTS.get(component.lib_id, {}):
            point = pin_position(component, pin_name)
            point_key = _key(point)
            pin_refs_by_root[dsu.find(point_key)].add(f"{component.ref}.{pin_name}")
            if point_key in no_connect_keys:
                continue
            if not any(_point_on_segment(point, wire) for wire in sheet.wires):
                unterminated.append(PinIssue(component.ref, pin_name, point))

    labels_by_root: dict[tuple[float, float], set[str]] = defaultdict(set)
    for label in sheet.labels:
        label_key = _key(Point(label.x, label.y))
        labels_by_root[dsu.find(label_key)].add(label.name)

    conflicts: list[NetNameConflict] = []
    for root, names in labels_by_root.items():
        if len(names) > 1:
            conflicts.append(NetNameConflict(
                tuple(sorted(names)),
                tuple(sorted(pin_refs_by_root.get(root, set()))),
            ))

    return SheetElectricalAudit(
        sheet_name=sheet.filename,
        off_grid_items=tuple(sorted(set(off_grid))),
        unterminated_pins=tuple(sorted(
            unterminated, key=lambda item: (item.reference, item.pin_name)
        )),
        net_name_conflicts=tuple(sorted(conflicts, key=lambda item: item.names)),
        zero_length_wires=zero_length,
    )
