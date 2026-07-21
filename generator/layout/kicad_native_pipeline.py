"""KiCad-native PCB placement-intent export for Gate 3.

The engineering model owns design intent: footprint assignments, proposed
coordinates, cluster membership, placement authority, keep-outs and review
status.  KiCad owns the native ``.kicad_pcb`` document, netlist, pads, zones,
routing and edit history.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import json

from generator.layout.constraints import build_layout_baseline
from generator.layout.footprint_contract import build_footprint_contract
from generator.layout.preliminary_placement import build_preliminary_placement_baseline
from generator.mechanical.board_outline import build_provisional_outline_contract


@dataclass(frozen=True, slots=True)
class NativePipelineBaseline:
    status: str
    pcb_owner: str
    intent_owner: str
    board_width_mm: float
    board_depth_mm: float
    footprint_count: int
    accepted_count: int
    review_count: int
    manufacturing_holes_frozen: bool
    placement_items: tuple[dict, ...]
    critical_net_classes: tuple[dict, ...]
    keepouts: tuple[dict, ...]
    import_contract: tuple[str, ...]


def build_kicad_native_pipeline_baseline() -> NativePipelineBaseline:
    placement = build_preliminary_placement_baseline()
    footprint = build_footprint_contract()
    layout = build_layout_baseline()
    outline = build_provisional_outline_contract()
    value_by_ref = {entry.ref: entry.value for entry in footprint.entries}

    items = tuple(
        {
            "reference": p.ref,
            "value": value_by_ref.get(p.ref, ""),
            "footprint": p.footprint,
            "cluster_id": p.cluster_id,
            "x_mm": p.x_mm,
            "y_mm": p.y_mm,
            "rotation_deg": p.rotation_deg,
            "placement_authority": p.placement_authority,
            "accepted": p.accepted,
            "rationale": p.rationale,
        }
        for p in placement.proposals
    )
    nets = tuple(asdict(n) for n in layout.critical_nets)
    keepouts = tuple(
        {
            "identifier": name,
            "clearance_mm": clearance,
            "status": "intent_only_until_native_board_import",
        }
        for name, clearance in (
            ("board_edge", layout.envelope.board_edge_clearance_mm),
            ("mounting_hole", layout.envelope.mounting_hole_keepout_mm),
            ("input_noise_exclusion", 15.0),
            ("harness_extraction", 12.0),
            ("test_point_probe_access", 8.0),
        )
    )
    return NativePipelineBaseline(
        status="PROVISIONAL_KICAD_NATIVE_IMPORT",
        pcb_owner="KiCad native document",
        intent_owner="Project Shellac engineering model",
        board_width_mm=outline.outline.width_mm,
        board_depth_mm=outline.outline.depth_mm,
        footprint_count=len(items),
        accepted_count=sum(1 for item in items if item["accepted"]),
        review_count=sum(1 for item in items if not item["accepted"]),
        manufacturing_holes_frozen=False,
        placement_items=items,
        critical_net_classes=nets,
        keepouts=keepouts,
        import_contract=(
            "Create or retain the PCB as a native KiCad document.",
            "Import/update footprints from the accepted schematic using KiCad tools.",
            "Apply proposed coordinates by reference without replacing native footprint definitions.",
            "Do not move manual-authority clusters to accepted state without Gate 3A review.",
            "Do not emit manufacturing holes until the enclosure/carrier freeze is approved.",
            "Run native KiCad DRC after every import or placement update.",
        ),
    )


def validate_kicad_native_pipeline_baseline(b: NativePipelineBaseline) -> list[str]:
    issues: list[str] = []
    refs = [item["reference"] for item in b.placement_items]
    if len(refs) != len(set(refs)):
        issues.append("placement references must be unique")
    if b.footprint_count != len(b.placement_items):
        issues.append("footprint count does not match placement items")
    if b.accepted_count + b.review_count != b.footprint_count:
        issues.append("placement acceptance counts do not reconcile")
    if b.pcb_owner != "KiCad native document":
        issues.append("native PCB ownership contract is missing")
    if b.manufacturing_holes_frozen:
        issues.append("manufacturing holes must remain unfrozen before enclosure decision")
    for item in b.placement_items:
        if not item["footprint"]:
            issues.append(f"{item['reference']} has no footprint identity")
    return issues


def write_kicad_native_pipeline_baseline(path: Path) -> NativePipelineBaseline:
    baseline = build_kicad_native_pipeline_baseline()
    issues = validate_kicad_native_pipeline_baseline(baseline)
    if issues:
        raise ValueError("invalid KiCad-native pipeline baseline: " + "; ".join(issues))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(baseline), indent=2) + "\n", encoding="utf-8")
    return baseline
