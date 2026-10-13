# AE-076B upper-cover/control-stack evidence.
from __future__ import annotations
from dataclasses import dataclass

TOP_COVER_NOMINAL_MM=2.0
TOP_COVER_TOLERANCE_MM=None

@dataclass(frozen=True, slots=True)
class ControlStackEvidence:
    identifier:str
    mpn:str
    registration:str
    installed_panel_to_pcb_mm:float|None
    bushing_thread:str|None
    bushing_length_mm:float|None
    final_hardware_stack_verified:bool=False
    machining_released:bool=False

NKK_EQ_STACK=ControlStackEvidence(
    "STACK-SW901L-R-SW902L-R","NR01105ANG13-2C / NR01105ANG13-2A",
    "AT3009 flange beneath panel; no threaded bushing",12.3,None,None)
TE_MATRIX_STACK=ControlStackEvidence(
    "STACK-SW903","MRJE3404",
    "independent three-pillar plate; exact TE bushing, nut and lid seating OPEN",None,None,None)
CK_TOGGLE_STACK=ControlStackEvidence(
    "STACK-SW904-905","7201SYCBE",
    "1/4-40 threaded bushing; PCB/support datum primary",None,"1/4-40",8.89)

DIRECT_MAIN_PCB_SELECTED=True
MAIN_PCB_SUPPORT_COUNT=6
SUPPORT_XY_FROZEN=False
SUPPORT_Z_TOLERANCE_STACK_FROZEN=False
MCAD_STACK_PROOF_REQUIRED=True

def validate_top_cover_stack()->None:
    assert TOP_COVER_NOMINAL_MM==2.0
    assert TOP_COVER_TOLERANCE_MM is None
    assert NKK_EQ_STACK.installed_panel_to_pcb_mm==12.3
    assert TE_MATRIX_STACK.installed_panel_to_pcb_mm is None
    assert TE_MATRIX_STACK.bushing_thread is None and not TE_MATRIX_STACK.final_hardware_stack_verified
    assert CK_TOGGLE_STACK.installed_panel_to_pcb_mm is None
    assert CK_TOGGLE_STACK.bushing_length_mm==8.89
    assert DIRECT_MAIN_PCB_SELECTED is True
    assert MAIN_PCB_SUPPORT_COUNT==6
    assert SUPPORT_XY_FROZEN is False
    assert SUPPORT_Z_TOLERANCE_STACK_FROZEN is False
    assert MCAD_STACK_PROOF_REQUIRED is True
    assert not NKK_EQ_STACK.final_hardware_stack_verified
    assert not TE_MATRIX_STACK.final_hardware_stack_verified
    assert not CK_TOGGLE_STACK.final_hardware_stack_verified
