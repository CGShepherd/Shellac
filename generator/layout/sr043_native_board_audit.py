"""SR-043 native-board integrity audit, extended by AE-071B.

This module deliberately separates:
- native-board structural/integrity readiness; from
- configuration authority to perform final routing.

A board may be structurally coherent while final routing remains explicitly held.
SR-040 mounting-hole coordinates are board-local; native KiCad pose is therefore
checked against Edge.Cuts lower-left + the SR-040 board-local hole centre.
"""
from __future__ import annotations

from pathlib import Path
import sys

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import json
import re
from dataclasses import asdict, dataclass

import yaml

from generator.layout.preliminary_placement import build_preliminary_placement_baseline
from generator.mechanical.sr040_audio_freeze import frozen_audio_board_outline

BOARD = Path("out/kicad/ProjectShellac.kicad_pcb")
ROUTING_HOLD = Path("config/release/ae071_prerouting_hold.yaml")


@dataclass(frozen=True)
class NativeBoardAudit:
    footprint_population_ok: bool
    board_outline_ok: bool
    mounting_holes_ok: bool
    mounting_holes_pose_ok: bool
    mounting_holes_board_only_ok: bool
    mounting_holes_locked_ok: bool
    mounting_holes_output_excluded_ok: bool
    unrouted_ok: bool
    four_layer_ok: bool
    inner1_present: bool
    inner2_present: bool
    native_board_integrity_ok: bool
    routing_authorized: bool


def _extract_balanced(text: str, start: int) -> str:
    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    raise ValueError("unterminated KiCad S-expression")


def _footprint_by_ref(text: str, ref: str) -> str | None:
    marker = f'(property "Reference" "{ref}"'
    pos = text.find(marker)
    if pos < 0:
        return None
    if text.find(marker, pos + 1) >= 0:
        raise ValueError(f"duplicate footprint reference {ref}")
    start = text.rfind("(footprint ", 0, pos)
    if start < 0:
        return None
    block = _extract_balanced(text, start)
    return block if marker in block else None


def _attr_tokens(block: str) -> set[str]:
    match = re.search(r"\(attr\s+([^\)]*)\)", block)
    return set(match.group(1).split()) if match else set()


def _footprint_pose(block: str) -> tuple[float, float, float]:
    match = re.search(
        r"(?m)^\s*\(at\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)"
        r"(?:\s+(-?\d+(?:\.\d+)?))?\)\s*$",
        block,
    )
    if not match:
        raise ValueError("footprint pose not found")
    return (
        float(match.group(1)),
        float(match.group(2)),
        float(match.group(3) or 0.0),
    )


def _edgecuts_rectangle(text: str) -> tuple[float, float, float, float, int]:
    points: list[tuple[float, float]] = []
    count = 0
    start = 0
    while True:
        pos = text.find("(gr_line", start)
        if pos < 0:
            break
        block = _extract_balanced(text, pos)
        start = pos + len(block)
        if '(layer "Edge.Cuts")' not in block:
            continue
        count += 1
        p1 = re.search(
            r"\(start\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\)",
            block,
        )
        p2 = re.search(
            r"\(end\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\)",
            block,
        )
        if not p1 or not p2:
            raise ValueError("Edge.Cuts line lacks start/end coordinates")
        points.extend(
            [
                (float(p1.group(1)), float(p1.group(2))),
                (float(p2.group(1)), float(p2.group(2))),
            ]
        )

    if not points:
        raise ValueError("no Edge.Cuts gr_line geometry found")

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return min(xs), min(ys), max(xs), max(ys), count


def _same_pose(
    actual: tuple[float, float, float],
    expected: tuple[float, float, float],
    tol: float = 1e-9,
) -> bool:
    return all(abs(a - e) <= tol for a, e in zip(actual, expected))


def _routing_authorized() -> bool:
    hold = yaml.safe_load(ROUTING_HOLD.read_text(encoding="utf-8"))
    permissions = hold.get("permissions", {})
    return bool(permissions.get("final_routing", False))


def audit_native_board() -> NativeBoardAudit:
    text = BOARD.read_text(encoding="utf-8")
    outline = frozen_audio_board_outline()
    placement = build_preliminary_placement_baseline(
        width_mm=outline.outline.width_mm,
        depth_mm=outline.outline.depth_mm,
    )

    refs = set(re.findall(r'\(property\s+"Reference"\s+"([^"]+)"', text))
    population_ok = all(p.ref in refs for p in placement.proposals)

    edge_min_x, edge_min_y, edge_max_x, edge_max_y, edge_count = _edgecuts_rectangle(text)
    board_outline_ok = (
        edge_count == 4
        and abs((edge_max_x - edge_min_x) - outline.outline.width_mm) <= 1e-9
        and abs((edge_max_y - edge_min_y) - outline.outline.depth_mm) <= 1e-9
    )

    hole_blocks = {
        h.identifier: _footprint_by_ref(text, h.identifier)
        for h in outline.mounting_holes
    }
    holes_ok = all(block is not None for block in hole_blocks.values())

    expected_by_ref = {h.identifier: h for h in outline.mounting_holes}
    pose_ok = holes_ok and board_outline_ok and all(
        _same_pose(
            _footprint_pose(hole_blocks[ref] or ""),
            (
                edge_min_x + expected_by_ref[ref].centre.x_mm,
                edge_min_y + expected_by_ref[ref].centre.y_mm,
                0.0,
            ),
        )
        for ref in expected_by_ref
    )

    required_attrs = {"board_only", "exclude_from_pos_files", "exclude_from_bom"}
    board_only_ok = holes_ok and all(
        "board_only" in _attr_tokens(block or "")
        for block in hole_blocks.values()
    )
    output_excluded_ok = holes_ok and all(
        required_attrs <= _attr_tokens(block or "")
        for block in hole_blocks.values()
    )
    locked_ok = holes_ok and all(
        re.search(r"(?m)^\s*\(locked yes\)\s*$", block or "") is not None
        for block in hole_blocks.values()
    )

    unrouted = "(segment " not in text and "(via " not in text
    inner1 = '"In1.Cu"' in text
    inner2 = '"In2.Cu"' in text
    four = inner1 and inner2

    integrity_ok = all(
        (
            population_ok,
            board_outline_ok,
            holes_ok,
            pose_ok,
            board_only_ok,
            locked_ok,
            output_excluded_ok,
            unrouted,
            four,
        )
    )

    return NativeBoardAudit(
        footprint_population_ok=population_ok,
        board_outline_ok=board_outline_ok,
        mounting_holes_ok=holes_ok,
        mounting_holes_pose_ok=pose_ok,
        mounting_holes_board_only_ok=board_only_ok,
        mounting_holes_locked_ok=locked_ok,
        mounting_holes_output_excluded_ok=output_excluded_ok,
        unrouted_ok=unrouted,
        four_layer_ok=four,
        inner1_present=inner1,
        inner2_present=inner2,
        native_board_integrity_ok=integrity_ok,
        routing_authorized=_routing_authorized(),
    )


def main():
    result = audit_native_board()
    print(json.dumps(asdict(result), indent=2))
    if not result.four_layer_ok:
        print("\nACTION REQUIRED: configure the KiCad board as 4 copper layers.")
        print("Required: F.Cu / In1.Cu / In2.Cu / B.Cu")
        print("In1.Cu = continuous 0VA; In2.Cu = power rails / rail spine.")
        raise SystemExit(2)
    if not result.native_board_integrity_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
