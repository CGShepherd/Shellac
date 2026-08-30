"""SR-042 native-KiCad routing bootstrap contract."""
from __future__ import annotations
from dataclasses import asdict, dataclass
from pathlib import Path
import csv, json

from generator.layout.constraints import build_layout_baseline
from generator.layout.footprint_contract import build_footprint_contract
from generator.layout.preliminary_placement import build_preliminary_placement_baseline
from generator.layout.sr041_routing_release import build_sr041_routing_release
from generator.mechanical.sr040_audio_freeze import frozen_audio_board_outline

@dataclass(frozen=True, slots=True)
class NativeRoutingBootstrap:
    identifier: str
    revision: str
    status: str
    board_width_mm: float
    board_depth_mm: float
    footprint_count: int
    mounting_hole_count: int
    critical_manual_net_count: int
    native_board_owner: str
    source_schematic: str
    target_board: str
    handoff_steps: tuple[str,...]

    def to_dict(self)->dict:
        return asdict(self)

def build_native_routing_bootstrap()->NativeRoutingBootstrap:
    release=build_sr041_routing_release()
    if release.status!="ROUTING_RELEASED":
        raise ValueError("SR-041 routing release is not closed")
    outline=frozen_audio_board_outline()
    placement=build_preliminary_placement_baseline(
        width_mm=outline.outline.width_mm,depth_mm=outline.outline.depth_mm)
    layout=build_layout_baseline()
    manual=sum(n.routing_policy.value=="manual_only" for n in layout.critical_nets)
    return NativeRoutingBootstrap(
        identifier="SR-042",
        revision="Rev A0",
        status="READY_FOR_NATIVE_KICAD_BOARD_CREATION",
        board_width_mm=outline.outline.width_mm,
        board_depth_mm=outline.outline.depth_mm,
        footprint_count=len(placement.proposals),
        mounting_hole_count=len(outline.mounting_holes),
        critical_manual_net_count=manual,
        native_board_owner="KiCad .kicad_pcb updated from ProjectShellac.kicad_sch",
        source_schematic="out/kicad/ProjectShellac.kicad_sch",
        target_board="out/kicad/ProjectShellac.kicad_pcb",
        handoff_steps=(
            "Open out/kicad/ProjectShellac.kicad_sch in KiCad 9.",
            "Use Tools > Update PCB from Schematic (F8) to create/update the native ProjectShellac.kicad_pcb.",
            "Keep all generated real footprints and nets; do not route yet.",
            "Use out/sr042/placement_manifest.csv and ProjectShellac_PlacementReference.kicad_pcb to place real footprints by reference.",
            "Add the four frozen NPTH mounting holes from out/sr042/mounting_holes.csv.",
            "Save the native board and run KiCad DRC before the first copper route.",
        ),
    )

def write_native_routing_bootstrap(out: Path)->NativeRoutingBootstrap:
    out.mkdir(parents=True,exist_ok=True)
    gate=build_native_routing_bootstrap()
    outline=frozen_audio_board_outline()
    placement=build_preliminary_placement_baseline(
        width_mm=outline.outline.width_mm,depth_mm=outline.outline.depth_mm)
    contract=build_footprint_contract()
    by_ref={e.ref:e for e in contract.entries}

    (out/"native_routing_bootstrap.json").write_text(
        json.dumps(gate.to_dict(),indent=2)+"\n",encoding="utf-8")
    with (out/"placement_manifest.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f)
        w.writerow(["reference","sheet","cluster","x_mm","y_mm","rotation_deg","footprint","value"])
        for p in placement.proposals:
            e=by_ref[p.ref]
            w.writerow([p.ref,p.sheet_id,p.cluster_id,p.x_mm,p.y_mm,p.rotation_deg,p.footprint,e.value])
    with (out/"mounting_holes.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f)
        w.writerow(["reference","x_mm","y_mm","drill_mm","copper_keepout_mm"])
        for h in outline.mounting_holes:
            w.writerow([h.identifier,h.centre.x_mm,h.centre.y_mm,h.finished_diameter_mm,h.copper_keepout_diameter_mm])
    return gate
