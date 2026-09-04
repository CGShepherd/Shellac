"""G3-025 / AE-040B controlled mechanical evidence for control hardware."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MechanicalEvidence:
    identifier: str
    manufacturer: str
    mpn: str
    function: str
    mounting: str
    behind_panel_depth_mm: float | None = None
    shaft_diameter_mm: float | None = None
    shaft_projection_mm: float | None = None
    bushing_thread: str | None = None
    bushing_length_mm: float | None = None
    panel_cutout_mm: float | None = None
    body_length_mm: float | None = None
    body_depth_mm: float | None = None
    body_height_mm: float | None = None
    terminal_pitch_mm: float | None = None
    terminal_row_spacing_mm: float | None = None
    evidence_grade: str = "E1/E3"
    manufacturing_released: bool = False
    notes: str = ""


GRAYHILL_1_DECK = MechanicalEvidence(
    "MECH-SW901-902-HISTORICAL", "Grayhill", "71BDF30-01-2-AJN",
    "Bass/Treble rotary — rejected historical candidate", "panel + through-hole PC mount, right-angle",
    behind_panel_depth_mm=19.33, shaft_diameter_mm=6.35,
    shaft_projection_mm=9.53, bushing_thread="3/8-32 UNEF",
    bushing_length_mm=7.92,
    evidence_grade="E1 exact product + E3 dimensional cross-check",
    notes="REJECTED by AE-026 because right-angle geometry conflicts with the preferred vertical-PCB control architecture.",
)

GRAYHILL_2_DECK = MechanicalEvidence(
    "MECH-SW903-HISTORICAL", "Grayhill", "71BDF30-02-2-AJN",
    "Channel Mode rotary — rejected historical candidate", "panel + through-hole PC mount, right-angle",
    behind_panel_depth_mm=24.87, shaft_diameter_mm=6.35,
    shaft_projection_mm=9.53, bushing_thread="3/8-32 UNEF",
    bushing_length_mm=7.92,
    evidence_grade="E1 exact product + E3 dimensional cross-check",
    notes="REJECTED by AE-026 because right-angle geometry conflicts with the preferred vertical-PCB control architecture.",
)

CK_7201SYCBE = MechanicalEvidence(
    "MECH-SW904-905", "C&K / Littelfuse", "7201SYCBE",
    "Rumble/Mute common toggle", "PC pins + threaded panel bushing",
    shaft_projection_mm=10.67, bushing_thread="1/4-40",
    bushing_length_mm=8.89, panel_cutout_mm=6.35,
    body_length_mm=12.70, body_depth_mm=11.43, body_height_mm=8.89,
    terminal_pitch_mm=4.70, terminal_row_spacing_mm=4.83,
    evidence_grade="E1 exact product electrical + E3 exact-MPN dimensions",
    notes="DPDT ON-ON, gold contacts, epoxy-sealed terminals, 100k-cycle class.",
)

LED_BEZEL = MechanicalEvidence(
    "MECH-LED901-902-BEZEL", "Arcolectric / Bulgin", "A104700BLACK",
    "3 mm rail-indicator bezel", "panel-mounted brass holder",
    panel_cutout_mm=6.30, body_length_mm=13.90, body_depth_mm=7.60,
    evidence_grade="E3 authorised-distributor exact-MPN data",
    notes="Black-finish brass; common bezel for both rail LEDs.",
)

ROTARY_PLATFORM_AUTHORITY = {
    "manufacturer": "Lorlin",
    "family": "PT",
    "status": "PREFERRED_PLATFORM_EXACT_PRODUCTION_MPN_OPEN",
    "authority": "AE-026 / AE-027 / AE-040B",
    "bass_treble_requirement": "vertical PCB, metric, 2P5, BBM, gold plated preferred",
    "channel_requirement": "vertical PCB, metric, two synchronised 2-pole wafers, 4P4, BBM, gold plated preferred",
}

HISTORICAL_ROTARY_EVIDENCE = (GRAYHILL_1_DECK, GRAYHILL_2_DECK)
EXTERNAL_CONTROL_CONTRACTS = (CK_7201SYCBE, LED_BEZEL)


def validate_control_mechanical_evidence() -> None:
    assert GRAYHILL_2_DECK.behind_panel_depth_mm > GRAYHILL_1_DECK.behind_panel_depth_mm
    assert GRAYHILL_1_DECK.shaft_diameter_mm == GRAYHILL_2_DECK.shaft_diameter_mm == 6.35
    assert GRAYHILL_1_DECK.shaft_projection_mm == GRAYHILL_2_DECK.shaft_projection_mm == 9.53
    assert GRAYHILL_1_DECK.bushing_thread == GRAYHILL_2_DECK.bushing_thread == "3/8-32 UNEF"
    assert all("REJECTED" in item.notes for item in HISTORICAL_ROTARY_EVIDENCE)
    assert ROTARY_PLATFORM_AUTHORITY["manufacturer"] == "Lorlin"
    assert ROTARY_PLATFORM_AUTHORITY["family"] == "PT"
    assert "OPEN" in ROTARY_PLATFORM_AUTHORITY["status"]
    assert CK_7201SYCBE.panel_cutout_mm == 6.35
    assert LED_BEZEL.panel_cutout_mm == 6.30
    assert all(not item.manufacturing_released for item in HISTORICAL_ROTARY_EVIDENCE + EXTERNAL_CONTROL_CONTRACTS)
