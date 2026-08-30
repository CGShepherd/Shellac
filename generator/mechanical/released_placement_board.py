"""SR-042 released placement-reference board.

This remains a visual/reference board: it contains the frozen outline,
mounting holes and accepted component envelopes, but intentionally no electrical
pads or copper.  The authoritative routed PCB must be a native KiCad board
updated from the generated schematic.
"""
from __future__ import annotations
from pathlib import Path

from generator.layout.footprint_contract import build_footprint_contract
from generator.layout.preliminary_placement import build_preliminary_placement_baseline
from generator.mechanical.board_skeleton import render_board_skeleton
from generator.mechanical.sr040_audio_freeze import frozen_audio_board_outline

def _q(text: str) -> str:
    return text.replace("\\","\\\\").replace('"','\\"')

def _mounting_hole(hole) -> str:
    # Board skeleton origin is 20,20 mm.
    x=20.0+hole.centre.x_mm
    y=20.0+hole.centre.y_mm
    return (
        f'  (footprint "ProjectShellac:MountingHole" (layer "F.Cu") (at {x:.3f} {y:.3f})\n'
        f'    (property "Reference" "{hole.identifier}" (at 0 -4) (layer "F.SilkS") '
        f'(effects (font (size 1 1) (thickness 0.15))))\n'
        f'    (property "Value" "NPTH_{hole.finished_diameter_mm:.1f}mm" (at 0 4) '
        f'(layer "F.Fab") hide (effects (font (size 1 1) (thickness 0.15))))\n'
        f'    (attr exclude_from_pos_files exclude_from_bom)\n'
        f'    (fp_circle (center 0 0) (end {hole.copper_keepout_diameter_mm/2:.3f} 0) '
        f'(stroke (width 0.25) (type default)) (fill none) (layer "Dwgs.User"))\n'
        f'    (pad "" np_thru_hole circle (at 0 0) (size {hole.finished_diameter_mm:.3f} '
        f'{hole.finished_diameter_mm:.3f}) (drill {hole.finished_diameter_mm:.3f}) (layers "*.Cu" "*.Mask"))\n'
        f'  )\n'
    )

def _reference_envelope(p, value: str) -> str:
    x=20.0+p.x_mm
    y=20.0+p.y_mm
    hw=max(p.width_mm/2,1.0)
    hd=max(p.depth_mm/2,1.0)
    return (
        f'  (footprint "ProjectShellac:PlacementReference" (layer "F.Cu") '
        f'(at {x:.3f} {y:.3f} {p.rotation_deg:.1f})\n'
        f'    (property "Reference" "{_q(p.ref)}" (at 0 {-hd-1.5:.3f}) (layer "F.SilkS") '
        f'(effects (font (size 0.8 0.8) (thickness 0.12))))\n'
        f'    (property "Value" "{_q(value)}" (at 0 {hd+1.5:.3f}) (layer "F.Fab") hide '
        f'(effects (font (size 0.8 0.8) (thickness 0.12))))\n'
        f'    (property "Shellac_TargetFootprint" "{_q(p.footprint)}" (at 0 0) (layer "F.Fab") hide)\n'
        f'    (property "Shellac_Cluster" "{_q(p.cluster_id)}" (at 0 0) (layer "F.Fab") hide)\n'
        f'    (attr exclude_from_pos_files exclude_from_bom)\n'
        f'    (fp_rect (start {-hw:.3f} {-hd:.3f}) (end {hw:.3f} {hd:.3f}) '
        f'(stroke (width 0.15) (type default)) (fill none) (layer "Dwgs.User"))\n'
        f'  )\n'
    )

def render_released_placement_reference_board() -> str:
    base=render_board_skeleton()
    if not base.endswith(')\n'):
        raise ValueError("unexpected board skeleton termination")
    outline=frozen_audio_board_outline()
    placement=build_preliminary_placement_baseline(
        width_mm=outline.outline.width_mm, depth_mm=outline.outline.depth_mm)
    contract=build_footprint_contract()
    values={e.ref:e.value for e in contract.entries}
    text=base[:-2]
    text += ('  (gr_text "SR-042 PLACEMENT REFERENCE — DO NOT ROUTE THIS FILE" '
             '(at 20 10) (layer "Cmts.User") '
             '(effects (font (size 1.5 1.5) (thickness 0.25)) (justify left)))\n')
    for h in outline.mounting_holes:
        text += _mounting_hole(h)
    for p in placement.proposals:
        text += _reference_envelope(p,values.get(p.ref,""))
    text += ')\n'
    return text

def validate_released_placement_reference_board(text: str) -> list[str]:
    outline=frozen_audio_board_outline()
    placement=build_preliminary_placement_baseline(
        width_mm=outline.outline.width_mm, depth_mm=outline.outline.depth_mm)
    issues=[]
    if text.count('(footprint "ProjectShellac:MountingHole"') != 4:
        issues.append("expected four frozen mounting holes")
    if text.count('(footprint "ProjectShellac:PlacementReference"') != len(placement.proposals):
        issues.append("placement-reference count mismatch")
    if '(segment ' in text or '(via ' in text or '(zone ' in text:
        issues.append("placement reference board must remain unrouted")
    if "DO NOT ROUTE THIS FILE" not in text:
        issues.append("reference-board warning missing")
    return issues

def write_released_placement_reference_board(path: Path) -> Path:
    text=render_released_placement_reference_board()
    issues=validate_released_placement_reference_board(text)
    if issues:
        raise ValueError("; ".join(issues))
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text,encoding="utf-8")
    return path
