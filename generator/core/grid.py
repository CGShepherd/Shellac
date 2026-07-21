"""Canonical electrical-grid services for generated KiCad schematics.

Electrical geometry is normalised when the in-memory Sheet is constructed.
The writer is a passive formatter and must not independently move connected
objects.  Project Shellac uses KiCad's 50-mil (1.27 mm) electrical grid.
"""
from __future__ import annotations

from .geometry import Point

ELECTRICAL_GRID_MM = 1.27
_EPSILON = 1e-9


def grid_index(value: float, grid: float = ELECTRICAL_GRID_MM) -> int:
    return round(float(value) / grid)


def align_coordinate(value: float, grid: float = ELECTRICAL_GRID_MM) -> float:
    aligned = grid_index(value, grid) * grid
    # Normalise binary floating-point noise while retaining exact 50-mil values.
    return round(aligned, 10)


def align_point(point: Point, grid: float = ELECTRICAL_GRID_MM) -> Point:
    return Point(align_coordinate(point.x, grid), align_coordinate(point.y, grid))


def is_aligned_coordinate(value: float, grid: float = ELECTRICAL_GRID_MM) -> bool:
    return abs(float(value) - align_coordinate(value, grid)) <= _EPSILON


def is_aligned_point(point: Point, grid: float = ELECTRICAL_GRID_MM) -> bool:
    return is_aligned_coordinate(point.x, grid) and is_aligned_coordinate(point.y, grid)
