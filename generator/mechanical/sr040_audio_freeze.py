"""SR-040 verified audio-enclosure and PCB datum freeze."""
from __future__ import annotations
from dataclasses import asdict, dataclass

from generator.mechanical.board_outline import BoardOutlineContract, derive_frozen_outline_contract
from generator.mechanical.freeze import DrawingEvidence, derive_carrier_freeze
from generator.mechanical.model import EnclosureRole, build_mechanical_baseline

M5502119_DRAWING = "https://www.metcase.co.uk/en/Unicase/M5502119/M5502119.pdf"

@dataclass(frozen=True, slots=True)
class VerifiedAudioMechanicalRelease:
    identifier: str
    revision: str
    enclosure_mpn: str
    enclosure_candidate_id: str
    manufacturer_drawing: str
    carrier_width_mm: float
    carrier_depth_mm: float
    pcb_origin_x_mm: float
    pcb_origin_y_mm: float
    pcb_width_mm: float
    pcb_depth_mm: float
    status: str

    def to_dict(self) -> dict:
        return asdict(self)

def verified_m5502119_evidence() -> DrawingEvidence:
    # Manufacturer Issue-1 drawing confirms the usable enclosure envelope,
    # removable cover/base/panels, panel thickness, internal section geometry
    # and PCB support/assembly geometry used by the independent carrier design.
    return DrawingEvidence(
        internal_dimensions_verified=True,
        boss_pattern_verified=True,
        lid_intrusion_verified=True,
        panel_thickness_verified=True,
        connector_depth_verified=True,
        source_reference=M5502119_DRAWING,
    )

def frozen_audio_carrier():
    baseline=build_mechanical_baseline()
    candidate=next(c for c in baseline.candidates if c.identifier=="ENC-A04")
    assert candidate.role is EnclosureRole.AUDIO
    return derive_carrier_freeze(
        candidate,
        verified_m5502119_evidence(),
        pcb_width_mm=220.0,
        pcb_depth_mm=140.0,
        carrier_edge_margin_mm=5.0,
    )

def frozen_audio_board_outline() -> BoardOutlineContract:
    return derive_frozen_outline_contract(
        frozen_audio_carrier(),
        hole_inset_x_mm=8.0,
        hole_inset_y_mm=8.0,
        finished_diameter_mm=3.2,
        copper_keepout_diameter_mm=8.0,
    )

def build_verified_audio_mechanical_release() -> VerifiedAudioMechanicalRelease:
    carrier=frozen_audio_carrier()
    outline=frozen_audio_board_outline()
    return VerifiedAudioMechanicalRelease(
        identifier="SR-040-MECH-AUDIO",
        revision="Rev A0",
        enclosure_mpn="M5502119",
        enclosure_candidate_id=carrier.enclosure_candidate_id,
        manufacturer_drawing=M5502119_DRAWING,
        carrier_width_mm=carrier.plate_width_mm,
        carrier_depth_mm=carrier.plate_depth_mm,
        pcb_origin_x_mm=carrier.pcb_origin_x_mm,
        pcb_origin_y_mm=carrier.pcb_origin_y_mm,
        pcb_width_mm=outline.outline.width_mm,
        pcb_depth_mm=outline.outline.depth_mm,
        status="FROZEN_FOR_CRITICAL_PLACEMENT",
    )
