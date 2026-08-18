"""Mechanical models with lazy imports to avoid layout/mechanical cycles."""
from .model import (
    AccessArchitecture,
    CandidateStatus,
    EnclosureCandidate,
    EnclosureRequirement,
    EnclosureRole,
    MechanicalBaseline,
    build_mechanical_baseline,
    evaluate_candidate,
)

__all__ = [
    "AccessArchitecture", "CandidateStatus", "EnclosureCandidate",
    "EnclosureRequirement", "EnclosureRole", "MechanicalBaseline",
    "PlacementSynthesis", "RegionBox", "build_mechanical_baseline",
    "build_placement_synthesis", "evaluate_candidate", "validate_synthesis",
    "CarrierPlateFreeze", "DrawingEvidence", "EnclosureDecision",
    "build_enclosure_decision_baseline", "decision_findings",
    "derive_carrier_freeze",
    "BoardOutline", "BoardOutlineContract", "MountingHole",
    "OutlineStatus", "Point2D", "build_provisional_outline_contract",
    "derive_frozen_outline_contract", "validate_outline_contract",
    "BoardSkeletonResult", "render_board_skeleton",
    "validate_board_skeleton_text", "write_board_skeleton",
    "EnclosureFace", "InterfaceKind", "MountingMode",
    "EnclosureFamilyFreeze", "PanelInterface", "DrillingTemplateContract",
    "InterfaceArchitecture", "build_interface_architecture",
    "validate_interface_architecture",
    "FitStatus", "VerifiedEnclosure", "ComponentEnvelope", "ControlStackContract", "UnicaseFitDecision", "build_unicase_fit_decision", "validate_unicase_fit_decision",
    "ClosureState", "FloorEnvelope", "RectangularFit", "PsuFitClosure", "build_psu_fit_closure", "validate_psu_fit_closure",
    ]


def __getattr__(name: str):
    if name in {"PlacementSynthesis", "RegionBox", "build_placement_synthesis", "validate_synthesis"}:
        from . import placement
        return getattr(placement, name)
    if name in {
        "BoardOutline", "BoardOutlineContract", "MountingHole",
        "OutlineStatus", "Point2D", "build_provisional_outline_contract",
        "derive_frozen_outline_contract", "validate_outline_contract",
    }:
        from . import board_outline
        return getattr(board_outline, name)
    if name in {
        "BoardSkeletonResult", "render_board_skeleton",
        "validate_board_skeleton_text", "write_board_skeleton",
    }:
        from . import board_skeleton
        return getattr(board_skeleton, name)
    if name in {
        "EnclosureFace", "InterfaceKind", "MountingMode",
        "EnclosureFamilyFreeze", "PanelInterface", "DrillingTemplateContract",
        "InterfaceArchitecture", "build_interface_architecture",
        "validate_interface_architecture",
    }:
        from . import interface_architecture
        return getattr(interface_architecture, name)
    if name in {
        "FitStatus", "VerifiedEnclosure", "ComponentEnvelope", "ControlStackContract",
        "UnicaseFitDecision", "build_unicase_fit_decision", "validate_unicase_fit_decision",
    }:
        from . import unicase_fit
        return getattr(unicase_fit, name)
    if name in {
        "ClosureState", "FloorEnvelope", "RectangularFit", "PsuFitClosure",
        "build_psu_fit_closure", "validate_psu_fit_closure",
    }:
        from . import psu_fit
        return getattr(psu_fit, name)
    if name in {
        "CarrierPlateFreeze", "DrawingEvidence", "EnclosureDecision",
        "build_enclosure_decision_baseline", "decision_findings",
        "derive_carrier_freeze",
    }:
        from . import freeze
        return getattr(freeze, name)
    raise AttributeError(name)

from .psu_release import ReleaseDecision, build_psu_release_decision, validate_psu_release_decision
