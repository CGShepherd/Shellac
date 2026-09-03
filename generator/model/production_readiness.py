"""AE-030 production-readiness gate model for Project Shellac."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class GateState(str, Enum):
    CLOSED = "CLOSED"
    READY_FOR_NEXT_ACTIVITY = "READY_FOR_NEXT_ACTIVITY"
    BLOCKED = "BLOCKED"
    PROTOTYPE_EVIDENCE_REQUIRED = "PROTOTYPE_EVIDENCE_REQUIRED"


@dataclass(frozen=True, slots=True)
class ProductionGate:
    identifier: str
    area: str
    state: GateState
    release_blocker: bool
    evidence: str
    next_action: str


GATES = (
    ProductionGate(
        "ELEC-SIGNAL",
        "Electrical signal chain",
        GateState.CLOSED,
        False,
        "AE-023 + AE-029; DR-037/038/039/040 implemented; analytical acceptance matrix established.",
        "Do not reopen unless prototype evidence contradicts the controlled model.",
    ),
    ProductionGate(
        "ELEC-MEASURE",
        "Prototype electrical acceptance",
        GateState.PROTOTYPE_EVIDENCE_REQUIRED,
        True,
        "AE-029 defines measured CMRR/noise/DC/EQ/overload/transient acceptance.",
        "Build representative hardware and execute commissioning matrix.",
    ),
    ProductionGate(
        "MECH-ENCLOSURE",
        "Audio enclosure / carrier / PCB datum",
        GateState.CLOSED,
        False,
        "SR-040 freezes METCASE M5502119 evidence and 220 x 140 mm PCB datum.",
        "Retain frozen datum unless a production ECO is justified.",
    ),
    ProductionGate(
        "MECH-CONTROLS",
        "Rotary control mechanics",
        GateState.BLOCKED,
        True,
        "Grayhill 71BDF30 is rejected for right-angle geometry; AE-026/027/028 select Lorlin PT pending exact MPN/sample evidence.",
        "Close Lorlin exact-order-code and physical sample geometry gates, then perform control-hardware ECO.",
    ),
    ProductionGate(
        "MECH-TOP",
        "Top-panel machining",
        GateState.BLOCKED,
        True,
        "Current top-cover stack still encodes Grayhill geometry and explicitly withholds machining release.",
        "Regenerate top-cover stack from verified Lorlin PT + C&K hardware and panel thickness.",
    ),
    ProductionGate(
        "PCB-OUTLINE",
        "PCB outline and mounting",
        GateState.CLOSED,
        False,
        "SR-040 frozen outline / four mounting holes / keep-outs.",
        "Carry frozen outline into native board.",
    ),
    ProductionGate(
        "PCB-PLACEMENT",
        "Critical placement",
        GateState.READY_FOR_NEXT_ACTIVITY,
        False,
        "SR-041 accepts manual clusters as routing baseline with zero mounting collisions.",
        "Only local refinement within movement authority during routing.",
    ),
    ProductionGate(
        "PCB-NATIVE",
        "Native KiCad board setup",
        GateState.READY_FOR_NEXT_ACTIVITY,
        True,
        "SR-043 audit requires populated frozen outline, mounting holes, unrouted state and four copper layers.",
        "Confirm native board is four-layer: F.Cu/In1.Cu/In2.Cu/B.Cu before routing.",
    ),
    ProductionGate(
        "PCB-ROUTING",
        "Native PCB routing",
        GateState.BLOCKED,
        True,
        "Current native-board audit intentionally expects an unrouted board before routing release.",
        "Complete controlled manual routing, planes, return paths, then DRC/ERC/review.",
    ),
    ProductionGate(
        "PCB-FAB",
        "Fabrication release",
        GateState.BLOCKED,
        True,
        "No production-routed/DRC-closed fabrication baseline exists yet.",
        "After routing: run DRC/ERC, Gerber/drill inspection, fabrication manifest and release review.",
    ),
    ProductionGate(
        "BOM-CONTROLS",
        "Control-hardware BOM",
        GateState.BLOCKED,
        True,
        "Controlled BOM still contains rejected Grayhill rotary parts.",
        "Replace only after Lorlin PT production MPN/sample gate closes.",
    ),
    ProductionGate(
        "BOM-GENERAL",
        "General BOM/procurement",
        GateState.READY_FOR_NEXT_ACTIVITY,
        True,
        "Controlled partial BOM exists; procurement_complete is false.",
        "Run final BOM completeness, alternates, lifecycle and availability audit before production release.",
    ),
    ProductionGate(
        "DOC-AUTHORITY",
        "Decision/document authority",
        GateState.CLOSED,
        False,
        "AE-024/025 reconciliation: zero vocabulary findings and zero current-authority contradictions.",
        "Maintain authority classifications with future ECOs.",
    ),
    ProductionGate(
        "DOC-COMMISSION",
        "Commissioning / maintenance baseline",
        GateState.READY_FOR_NEXT_ACTIVITY,
        False,
        "AE-029 provides first-hardware acceptance matrix; maintenance structure exists.",
        "Populate measured results and fault-isolation guidance after prototype.",
    ),
    ProductionGate(
        "DOC-RELEASE",
        "Production design pack",
        GateState.BLOCKED,
        True,
        "Pack structure exists but fabrication release, measured acceptance, final BOM and release manifest remain incomplete.",
        "Assemble release pack after PCB/mechanical/prototype gates close.",
    ),
    ProductionGate(
        "REPRO-CLEANCLONE",
        "Clean-clone reproducibility",
        GateState.BLOCKED,
        True,
        "Not yet demonstrated from an empty clone against pinned tool/dependency versions.",
        "Perform clean-clone build and compare generated production artifacts before tag.",
    ),
    ProductionGate(
        "REPO-HYGIENE",
        "Repository production cleanup",
        GateState.READY_FOR_NEXT_ACTIVITY,
        False,
        "Cleanup deliberately deferred until production standard is known.",
        "Classify authoritative source, controlled evidence and release artifacts; archive/remove detritus after baseline freeze.",
    ),
    ProductionGate(
        "INFRA-EXTRACT",
        "Foundry / Generator extraction",
        GateState.READY_FOR_NEXT_ACTIVITY,
        False,
        "Planned post-production extraction; Shellac still informs generic/project-specific boundary.",
        "Extract Foundry and Generator only after production clean-clone baseline is proven.",
    ),
)


def gates_by_state(state: GateState):
    return tuple(g for g in GATES if g.state is state)


def release_blockers():
    return tuple(g for g in GATES if g.release_blocker)


def validate_production_gates():
    assert len({g.identifier for g in GATES}) == len(GATES)
    assert len(GATES) >= 15
    assert gates_by_state(GateState.CLOSED)
    assert gates_by_state(GateState.BLOCKED)
    assert gates_by_state(GateState.PROTOTYPE_EVIDENCE_REQUIRED)
    assert all(g.next_action for g in release_blockers())
