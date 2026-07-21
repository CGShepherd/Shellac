"""Provisional KiCad PCB skeleton export for Gate 3.

The exporter deliberately emits a non-manufacturing board skeleton while the
enclosure decision remains provisional.  It contains the coordinate frame,
provisional outline, four-layer stack-up declaration, functional-region guides,
and design-intent notes.  Manufacturing mounting holes are emitted only when a
frozen :class:`BoardOutlineContract` supplies approved coordinates.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from generator.layout.constraints import build_layout_baseline
from generator.mechanical.board_outline import (
    BoardOutlineContract,
    OutlineStatus,
    build_provisional_outline_contract,
    validate_outline_contract,
)
from generator.mechanical.placement import build_placement_synthesis


@dataclass(frozen=True, slots=True)
class BoardSkeletonResult:
    path: Path
    state: str
    outline_width_mm: float
    outline_depth_mm: float
    mounting_hole_count: int
    region_count: int


def _q(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _line(x1: float, y1: float, x2: float, y2: float, layer: str, width: float = 0.2) -> str:
    return (
        f'  (gr_line (start {x1:.3f} {y1:.3f}) (end {x2:.3f} {y2:.3f}) '
        f'(stroke (width {width:.3f}) (type default)) (layer "{layer}"))\n'
    )


def _rect(x: float, y: float, w: float, h: float, layer: str, width: float = 0.2) -> str:
    return (
        f'  (gr_rect (start {x:.3f} {y:.3f}) (end {x+w:.3f} {y+h:.3f}) '
        f'(stroke (width {width:.3f}) (type default)) (fill none) (layer "{layer}"))\n'
    )


def _text(text: str, x: float, y: float, layer: str = "Dwgs.User", size: float = 1.4) -> str:
    return (
        f'  (gr_text "{_q(text)}" (at {x:.3f} {y:.3f}) (layer "{layer}")\n'
        f'    (effects (font (size {size:.3f} {size:.3f}) (thickness 0.220)) (justify left)))\n'
    )


def _mounting_hole(identifier: str, x: float, y: float, drill: float, keepout: float) -> str:
    pad = max(drill, drill + 0.4)
    return (
        f'  (footprint "ProjectShellac:MountingHole" (layer "F.Cu") (at {x:.3f} {y:.3f})\n'
        f'    (property "Reference" "{identifier}" (at 0 -3 0) (layer "F.SilkS"))\n'
        f'    (property "Value" "MountingHole_{drill:.1f}mm" (at 0 3 0) (layer "F.Fab") hide)\n'
        f'    (attr exclude_from_pos_files exclude_from_bom)\n'
        f'    (fp_circle (center 0 0) (end {keepout/2:.3f} 0) (stroke (width 0.2) (type default)) (fill none) (layer "Dwgs.User"))\n'
        f'    (pad "" np_thru_hole circle (at 0 0) (size {pad:.3f} {pad:.3f}) (drill {drill:.3f}) (layers "*.Cu" "*.Mask")))\n'
    )


def validate_board_skeleton_text(text: str, contract: BoardOutlineContract) -> list[str]:
    issues: list[str] = []
    if not text.startswith("(kicad_pcb"):
        issues.append("missing kicad_pcb root")
    if text.count('(layer "Edge.Cuts")') < 4:
        issues.append("board outline must contain four Edge.Cuts segments")
    required_layers = (
        '(0 "F.Cu" signal)',
        '(2 "In1.Cu" signal)',
        '(4 "In2.Cu" signal)',
        '(31 "B.Cu" signal)',
        '(40 "Dwgs.User" user "user.drawings")',
        '(41 "Cmts.User" user "user.comments")',
        '(44 "Edge.Cuts" user)',
    )
    for declaration in required_layers:
        if declaration not in text:
            issues.append(f"missing or malformed layer declaration: {declaration}")

    in_layers = False
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if stripped == "(layers":
            in_layers = True
            continue
        if in_layers and stripped == ")":
            break
        if in_layers and stripped.startswith("("):
            token = stripped[1:].split(maxsplit=1)[0]
            if not token.isdigit():
                issues.append(f"layer declaration requires numeric index: {stripped}")
    expected_holes = len(contract.mounting_holes) if contract.status is OutlineStatus.FROZEN else 0
    actual_holes = text.count('(footprint "ProjectShellac:MountingHole"')
    if actual_holes != expected_holes:
        issues.append(f"expected {expected_holes} mounting holes, found {actual_holes}")
    if contract.status is not OutlineStatus.FROZEN and "PROVISIONAL — NOT FOR MANUFACTURE" not in text:
        issues.append("provisional manufacturing warning is missing")
    return issues


def render_board_skeleton(contract: BoardOutlineContract | None = None) -> str:
    contract = contract or build_provisional_outline_contract()
    contract_issues = validate_outline_contract(contract)
    if contract_issues:
        raise ValueError("invalid board outline contract: " + "; ".join(contract_issues))

    layout = build_layout_baseline()
    placement = build_placement_synthesis(
        width_mm=contract.outline.width_mm,
        depth_mm=contract.outline.depth_mm,
    )
    ox, oy = 20.0, 20.0
    width, depth = contract.outline.width_mm, contract.outline.depth_mm

    out = [
        '(kicad_pcb (version 20240108) (generator "project_shellac_generator")\n',
        '  (general (thickness 1.6))\n',
        '  (paper "A3")\n',
        '  (layers\n',
        '    (0 "F.Cu" signal)\n',
        '    (2 "In1.Cu" signal)\n',
        '    (4 "In2.Cu" signal)\n',
        '    (31 "B.Cu" signal)\n',
        '    (36 "B.SilkS" user "b.silkscreen")\n',
        '    (37 "F.SilkS" user "f.silkscreen")\n',
        '    (44 "Edge.Cuts" user)\n',
        '    (46 "B.CrtYd" user "b.courtyard")\n',
        '    (47 "F.CrtYd" user "f.courtyard")\n',
        '    (48 "B.Fab" user)\n',
        '    (49 "F.Fab" user)\n',
        '    (40 "Dwgs.User" user "user.drawings")\n',
        '    (41 "Cmts.User" user "user.comments")\n',
        '  )\n',
        '  (setup (pad_to_mask_clearance 0))\n',
    ]

    # Closed provisional/frozen rectangular outline.
    out.extend([
        _line(ox, oy, ox + width, oy, "Edge.Cuts"),
        _line(ox + width, oy, ox + width, oy + depth, "Edge.Cuts"),
        _line(ox + width, oy + depth, ox, oy + depth, "Edge.Cuts"),
        _line(ox, oy + depth, ox, oy, "Edge.Cuts"),
    ])

    state_label = (
        "FROZEN MANUFACTURING OUTLINE"
        if contract.status is OutlineStatus.FROZEN
        else "PROVISIONAL — NOT FOR MANUFACTURE"
    )
    out.append(_text(f"PROJECT SHELLAC PCB — {state_label}", ox, oy - 6.0, "Cmts.User", 1.8))
    out.append(_text(f"Origin datum: lower-left board corner at ({ox:.1f}, {oy:.1f}) mm", ox, oy + depth + 6.0))
    out.append(_text("Right edge = cartridge inputs | Left edge = balanced outputs and DC entry", ox, oy + depth + 10.0))
    out.append(_text(f"Stack-up intent: {layout.stackup.top_role} / {layout.stackup.inner_1_role} / {layout.stackup.inner_2_role} / {layout.stackup.bottom_role}", ox, oy + depth + 14.0, size=1.0))

    # Placement regions are guides only, shown on Dwgs.User.
    for region in placement.regions:
        out.append(_rect(ox + region.x_mm, oy + region.y_mm, region.width_mm, region.depth_mm, "Dwgs.User", 0.15))
        out.append(_text(f"{region.identifier}: {region.name}", ox + region.x_mm + 1.0, oy + region.y_mm + 2.0, size=0.9))

    # Board-edge clearance contract, not a KiCad copper keepout yet.
    c = layout.envelope.board_edge_clearance_mm
    out.append(_rect(ox + c, oy + c, width - 2*c, depth - 2*c, "Cmts.User", 0.15))
    out.append(_text(f"{c:.1f} mm board-edge component clearance guide", ox + c + 1.0, oy + c + 2.0, "Cmts.User", 0.9))

    for hole in contract.mounting_holes:
        out.append(_mounting_hole(
            hole.identifier,
            ox + hole.centre.x_mm,
            oy + hole.centre.y_mm,
            hole.finished_diameter_mm,
            hole.copper_keepout_diameter_mm,
        ))

    out.append(')\n')
    text = "".join(out)
    issues = validate_board_skeleton_text(text, contract)
    if issues:
        raise ValueError("invalid board skeleton: " + "; ".join(issues))
    return text


def write_board_skeleton(
    out_path: Path,
    contract: BoardOutlineContract | None = None,
) -> BoardSkeletonResult:
    contract = contract or build_provisional_outline_contract()
    text = render_board_skeleton(contract)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    placement = build_placement_synthesis(
        width_mm=contract.outline.width_mm,
        depth_mm=contract.outline.depth_mm,
    )
    return BoardSkeletonResult(
        path=out_path,
        state=contract.status.value,
        outline_width_mm=contract.outline.width_mm,
        outline_depth_mm=contract.outline.depth_mm,
        mounting_hole_count=len(contract.mounting_holes),
        region_count=len(placement.regions),
    )
