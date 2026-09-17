from pathlib import Path
import re

from generator.layout.footprint_contract import build_footprint_contract, PopulationStatus
from generator.layout.sr043_native_board_audit import audit_native_board
from generator.mechanical.sr040_audio_freeze import frozen_audio_board_outline

BOARD = Path("out/kicad/ProjectShellac.kicad_pcb")
HOLD = Path("config/release/ae071_prerouting_hold.yaml")

MECHANICAL_REFS = {"MH1", "MH2", "MH3", "MH4"}
REQUIRED_ATTRS = {"board_only", "exclude_from_pos_files", "exclude_from_bom"}


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
    raise AssertionError("unterminated KiCad S-expression")


def _block(text: str, ref: str) -> str:
    marker = f'(property "Reference" "{ref}"'
    pos = text.find(marker)
    assert pos >= 0, ref
    assert text.find(marker, pos + 1) < 0, ref
    start = text.rfind("(footprint ", 0, pos)
    assert start >= 0, ref
    return _extract_balanced(text, start)


def _attrs(block: str) -> set[str]:
    m = re.search(r"\(attr\s+([^\)]*)\)", block)
    assert m
    return set(m.group(1).split())


def _pose(block: str) -> tuple[float, float, float]:
    m = re.search(
        r"(?m)^\s*\(at\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)"
        r"(?:\s+(-?\d+(?:\.\d+)?))?\)\s*$",
        block,
    )
    assert m
    return float(m.group(1)), float(m.group(2)), float(m.group(3) or 0.0)


def _edgecuts_origin_and_size(text: str) -> tuple[float, float, float, float, int]:
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
        assert p1 and p2
        points.extend(
            [
                (float(p1.group(1)), float(p1.group(2))),
                (float(p2.group(1)), float(p2.group(2))),
            ]
        )
    assert points
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    min_x, min_y, max_x, max_y = min(xs), min(ys), max(xs), max(ys)
    return min_x, min_y, max_x - min_x, max_y - min_y, count


def test_ae071b_mounting_holes_are_board_owned_locked_and_output_excluded():
    text = BOARD.read_text(encoding="utf-8")
    frozen = frozen_audio_board_outline()
    by_ref = {hole.identifier: hole for hole in frozen.mounting_holes}
    assert set(by_ref) == MECHANICAL_REFS

    origin_x, origin_y, board_w, board_h, edge_count = _edgecuts_origin_and_size(text)
    assert edge_count == 4
    assert board_w == frozen.outline.width_mm
    assert board_h == frozen.outline.depth_mm

    for ref in sorted(MECHANICAL_REFS):
        block = _block(text, ref)
        assert block.startswith('(footprint "MountingHole:MountingHole_3.2mm_M3"')
        assert REQUIRED_ATTRS <= _attrs(block)
        assert re.search(r"(?m)^\s*\(locked yes\)\s*$", block)

        hole = by_ref[ref]
        assert _pose(block) == (
            origin_x + hole.centre.x_mm,
            origin_y + hole.centre.y_mm,
            0.0,
        )


def test_ae071b_mounting_holes_are_not_product_contract_references():
    contract = build_footprint_contract()
    product_refs = {
        entry.ref
        for entry in contract.entries
        if entry.population_status is PopulationStatus.APPROVED
    }
    assert MECHANICAL_REFS.isdisjoint(product_refs)


def test_ae071b_native_audit_enforces_mechanical_ownership_and_pose():
    result = audit_native_board()
    assert result.mounting_holes_pose_ok
    assert result.mounting_holes_board_only_ok
    assert result.mounting_holes_locked_ok
    assert result.mounting_holes_output_excluded_ok


def test_ae071b_retains_routing_hold():
    text = HOLD.read_text(encoding="utf-8")
    assert "authority: AE-071B" in text
    assert "previous_authority: AE-071A" in text
    assert "status: ROUTING_HELD_PENDING_PRODUCT_RECONCILIATION" in text
    assert "  final_routing: false" in text
