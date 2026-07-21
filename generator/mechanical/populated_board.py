"""G3-013 populated provisional KiCad board export.

The exporter combines the accepted board skeleton with G3-012 coordinate
proposals.  It is deliberately review-only: footprint envelopes are rendered
as simple generated placeholders carrying the authoritative footprint identity,
reference and value.  No pads/nets/routing or manufacturing holes are emitted.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from generator.layout.footprint_contract import build_footprint_contract
from generator.layout.preliminary_placement import (
    PlacementProposal,
    build_preliminary_placement_baseline,
)
from generator.mechanical.board_skeleton import render_board_skeleton


@dataclass(frozen=True, slots=True)
class PopulatedBoardResult:
    path: Path
    footprint_count: int
    accepted_count: int
    manual_review_count: int
    routing_count: int
    mounting_hole_count: int
    status: str


def _q(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def _placeholder_footprint(p: PlacementProposal, value: str) -> str:
    # Board skeleton origin is 20,20 mm. Proposal coordinates are board-local.
    x = 20.0 + p.x_mm
    y = 20.0 + p.y_mm
    hw = max(p.width_mm / 2.0, 1.0)
    hd = max(p.depth_mm / 2.0, 1.0)
    review = "ACCEPTED" if p.accepted else "GATE3A_REVIEW"
    return (
        f'  (footprint "ProjectShellac:ReviewPlaceholder" (layer "F.Cu") '
        f'(at {x:.3f} {y:.3f} {p.rotation_deg:.1f})\n'
        f'    (property "Reference" "{_q(p.ref)}" (at 0 {-hd-1.5:.3f} {p.rotation_deg:.1f}) '
        f'(layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))\n'
        f'    (property "Value" "{_q(value)}" (at 0 {hd+1.5:.3f} {p.rotation_deg:.1f}) '
        f'(layer "F.Fab") hide (effects (font (size 1 1) (thickness 0.15))))\n'
        f'    (property "Shellac_Footprint" "{_q(p.footprint)}" (at 0 0) (layer "F.Fab") hide)\n'
        f'    (property "Shellac_Cluster" "{_q(p.cluster_id)}" (at 0 0) (layer "F.Fab") hide)\n'
        f'    (property "Shellac_Status" "{review}" (at 0 0) (layer "F.Fab") hide)\n'
        f'    (attr exclude_from_pos_files exclude_from_bom)\n'
        f'    (fp_rect (start {-hw:.3f} {-hd:.3f}) (end {hw:.3f} {hd:.3f}) '
        f'(stroke (width 0.2) (type default)) (fill none) (layer "F.CrtYd"))\n'
        f'    (fp_rect (start {-hw+0.3:.3f} {-hd+0.3:.3f}) (end {hw-0.3:.3f} {hd-0.3:.3f}) '
        f'(stroke (width 0.18) (type default)) (fill none) (layer "F.SilkS"))\n'
        f'    (fp_text user "{review}" (at 0 0 {p.rotation_deg:.1f}) (layer "Dwgs.User") '
        f'(effects (font (size 0.7 0.7) (thickness 0.12))))\n'
        f'  )\n'
    )


def render_populated_board() -> str:
    base = render_board_skeleton()
    if not base.endswith(')\n'):
        raise ValueError("unexpected board skeleton termination")
    placement = build_preliminary_placement_baseline()
    contract = build_footprint_contract()
    values = {entry.ref: entry.value for entry in contract.entries}

    content = base[:-2]
    content += (
        '  (gr_text "G3-013 POPULATED REVIEW BOARD — UNROUTED — PLACEHOLDERS ONLY" '
        '(at 20 10) (layer "Cmts.User") '
        '(effects (font (size 1.5 1.5) (thickness 0.25)) (justify left)))\n'
    )
    for proposal in placement.proposals:
        content += _placeholder_footprint(proposal, values.get(proposal.ref, ""))
    content += ')\n'
    return content


def validate_populated_board_text(text: str) -> list[str]:
    placement = build_preliminary_placement_baseline()
    issues: list[str] = []
    count = text.count('(footprint "ProjectShellac:ReviewPlaceholder"')
    if count != len(placement.proposals):
        issues.append(f"expected {len(placement.proposals)} review footprints, found {count}")
    if '(segment ' in text or '(via ' in text or '(zone ' in text:
        issues.append("review board must remain unrouted")
    if '(footprint "ProjectShellac:MountingHole"' in text:
        issues.append("provisional board must not contain manufacturing holes")
    if "UNROUTED — PLACEHOLDERS ONLY" not in text:
        issues.append("review-only warning is missing")
    for proposal in placement.proposals:
        if f'(property "Reference" "{proposal.ref}"' not in text:
            issues.append(f"missing footprint proposal {proposal.ref}")
    return issues


def write_populated_board(path: Path) -> PopulatedBoardResult:
    text = render_populated_board()
    issues = validate_populated_board_text(text)
    if issues:
        raise ValueError("invalid populated review board: " + "; ".join(issues))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    placement = build_preliminary_placement_baseline()
    return PopulatedBoardResult(
        path=path,
        footprint_count=len(placement.proposals),
        accepted_count=sum(1 for p in placement.proposals if p.accepted),
        manual_review_count=sum(1 for p in placement.proposals if not p.accepted),
        routing_count=0,
        mounting_hole_count=0,
        status="PROVISIONAL — GATE 3A VISUAL REVIEW ONLY",
    )
