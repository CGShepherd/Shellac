# Current and historical mechanical evidence for Shellac control hardware.
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class MechanicalEvidence:
    identifier:str
    manufacturer:str
    mpn:str
    function:str
    mounting:str
    behind_panel_depth_mm:float|None=None
    installed_panel_to_pcb_mm:float|None=None
    shaft_diameter_mm:float|None=None
    shaft_projection_mm:float|None=None
    bushing_thread:str|None=None
    bushing_length_mm:float|None=None
    panel_cutout_mm:float|None=None
    body_length_mm:float|None=None
    body_depth_mm:float|None=None
    body_height_mm:float|None=None
    evidence_grade:str="E1/E3"
    manufacturing_released:bool=False
    notes:str=""

GRAYHILL_1_DECK=MechanicalEvidence(
    "MECH-SW901-902-HISTORICAL","Grayhill","71BDF30-01-2-AJN",
    "Bass/Treble rotary — rejected historical candidate","panel + through-hole PC mount, right-angle",
    behind_panel_depth_mm=19.33,shaft_diameter_mm=6.35,shaft_projection_mm=9.53,
    bushing_thread="3/8-32 UNEF",bushing_length_mm=7.92,
    notes="REJECTED by AE-026; retained for traceability only.")
GRAYHILL_2_DECK=MechanicalEvidence(
    "MECH-SW903-HISTORICAL","Grayhill","71BDF30-02-2-AJN",
    "Channel Mode rotary — rejected historical candidate","panel + through-hole PC mount, right-angle",
    behind_panel_depth_mm=24.87,shaft_diameter_mm=6.35,shaft_projection_mm=9.53,
    bushing_thread="3/8-32 UNEF",bushing_length_mm=7.92,
    notes="REJECTED by AE-026; retained for traceability only.")

NKK_NR01=MechanicalEvidence(
    "MECH-SW901L-R-SW902L-R","NKK","NR01105ANG13-2C / NR01105ANG13-2A",
    "Independent L/R Bass and Treble selectors",
    "PCB through-hole straight-PC with support bracket; AT3009 flanged knob beneath top cover; no threaded mounting bushing",
    behind_panel_depth_mm=10.5,installed_panel_to_pcb_mm=12.3,
    evidence_grade="E1 exact production MPNs reconciled by AE-075C/AE-076B",
    notes="Bass uses -2C red AT3009; Treble uses -2A black AT3009. Four independent controls total.")

CK_A30403RNCB=MechanicalEvidence(
    "MECH-SW903-SUPERSEDED","C&K","A30403RNCB","Historical Channel-mode 3P4T rotary",
    "panel + through-hole PC mount; 3/8-32 threaded bushing; installed PCB plane not frozen",
    behind_panel_depth_mm=14.48,shaft_diameter_mm=6.35,shaft_projection_mm=9.53,
    body_length_mm=26.2,panel_cutout_mm=9.8,bushing_thread="3/8-32",
    evidence_grade="E1 exact-MPN/family evidence",
    notes="SUPERSEDED by AE-076F4C TE MRJE3404; immutable physical provenance, not production candidate.")

TE_MRJE3404=MechanicalEvidence(
    "MECH-SW903","TE Connectivity / Alcoswitch","MRJE3404","Selected Channel-mode 3P4T rotary",
    "PCB through-hole terminals, mechanically restrained by independent three-pillar aluminium plate; actual TE panel/shaft hardware OPEN",shaft_diameter_mm=3.17,
    evidence_grade="E1 genuine exact-part STEP evidence; terminal numbering/fit qualification OPEN",
    notes="Selected by AE-076F4C / part 1825537-3. C&K matrix superseded. No qualified panel-to-PCB stack, knob or drilled footprint.")

CK_7201SYCBE=MechanicalEvidence(
    "MECH-SW904-905","C&K / Littelfuse","7201SYCBE","Rumble/Mute common toggle",
    "PC pins + threaded panel bushing; installed PCB plane not frozen",
    shaft_projection_mm=10.67,bushing_thread="1/4-40",bushing_length_mm=8.89,
    panel_cutout_mm=6.35,body_length_mm=12.70,body_depth_mm=11.43,body_height_mm=8.89,
    evidence_grade="E1 exact product electrical + E3 exact-MPN dimensions",
    notes="DPDT ON-ON, gold contacts, epoxy-sealed terminals. MCAD must prove direct-main-PCB stack.")

LED_BEZEL=MechanicalEvidence(
    "MECH-LED901-902-BEZEL","Arcolectric / Bulgin","A104700BLACK",
    "3 mm rail-indicator bezel","panel-mounted brass holder",
    panel_cutout_mm=6.30,body_length_mm=13.90,body_depth_mm=7.60,
    evidence_grade="E3 authorised-distributor exact-MPN data")

ROTARY_PLATFORM_AUTHORITY={
    "eq_manufacturer":"NKK","eq_family":"NR01","eq_quantity":4,
    "eq_mpns":("NR01105ANG13-2C","NR01105ANG13-2A"),
    "eq_exact_mpn_status":"FROZEN_AE075C",
    "matrix_manufacturer":"TE Connectivity / Alcoswitch","matrix_mpn":"MRJE3404",
    "matrix_manufacturer_part_number":"1825537-3",
    "matrix_fallback_mpn":None,
    "matrix_superseded_historical_mpn":"A30403RNCB",
    "matrix_status":"SINGLE_PRODUCTION_PART_SELECTED_PHYSICAL_MIGRATION_OPEN",
    "authority":"AE-076F4C (part selection) + AE-041 A1 (electrical truth table)",
}
HISTORICAL_ROTARY_EVIDENCE=(GRAYHILL_1_DECK,GRAYHILL_2_DECK)
CURRENT_ROTARY_EVIDENCE=(NKK_NR01,TE_MRJE3404)
EXTERNAL_CONTROL_CONTRACTS=(NKK_NR01,CK_A30403RNCB,TE_MRJE3404,CK_7201SYCBE,LED_BEZEL)

def validate_control_mechanical_evidence()->None:
    assert all("REJECTED" in item.notes for item in HISTORICAL_ROTARY_EVIDENCE)
    assert NKK_NR01.installed_panel_to_pcb_mm==12.3
    assert "no threaded mounting bushing" in NKK_NR01.mounting
    assert ROTARY_PLATFORM_AUTHORITY["eq_mpns"]==("NR01105ANG13-2C","NR01105ANG13-2A")
    assert ROTARY_PLATFORM_AUTHORITY["eq_exact_mpn_status"]=="FROZEN_AE075C"
    assert ROTARY_PLATFORM_AUTHORITY["matrix_mpn"]=="MRJE3404"
    assert ROTARY_PLATFORM_AUTHORITY["matrix_fallback_mpn"] is None
    assert CK_A30403RNCB.installed_panel_to_pcb_mm is None
    assert CK_7201SYCBE.installed_panel_to_pcb_mm is None
    assert CK_7201SYCBE.bushing_length_mm==8.89
    assert LED_BEZEL.panel_cutout_mm==6.30
