"""AE-075C control-stack mechanical contract for routing blocker B03."""
from __future__ import annotations
from dataclasses import dataclass

ENCLOSURE_MPN="M5502119"
ENCLOSURE_INTERNAL_COVER_HEIGHT_MM=86.2
MAIN_PCB_CARRIER_STANDOFF_MM=8.0
TOP_COVER_THICKNESS_MM=None
CARRIER_OR_CONTROL_PLANE_Z_MM=None
CONTROL_BOARD_OWNERSHIP="OPEN_DIRECT_MAIN_PCB_OR_REG08_CONTROL_PCB"
B03_STATUS="EXACT_PARTS_FROZEN_VERTICAL_STACK_AND_FOOTPRINTS_OPEN"

@dataclass(frozen=True, slots=True)
class ControlStackPart:
    function:str
    quantity:int
    mpn:str
    panel_registration:str
    pcb_mounting:str

PARTS=(
    ControlStackPart("BASS",2,"NR01105ANG13-2C",
        "AT3009 flanged knob beneath panel; no threaded bushing",
        "THT straight PC with support bracket"),
    ControlStackPart("TREBLE",2,"NR01105ANG13-2A",
        "AT3009 flanged knob beneath panel; no threaded bushing",
        "THT straight PC with support bracket"),
    ControlStackPart("CHANNEL",1,"A30403RNCB",
        "3/8-32 threaded bushing and nut",
        "THT PC pins"),
    ControlStackPart("RUMBLE",1,"7201SYCBE",
        "1/4-40 threaded bushing and nut",
        "THT PC pins"),
    ControlStackPart("MUTE",1,"7201SYCBE",
        "1/4-40 threaded bushing and nut",
        "THT PC pins"),
)

REQUIRED_BEFORE_B03_CLOSURE=(
    "freeze carrier/control PCB plane Z relative to upper-cover inner face",
    "freeze top-cover thickness and finished aperture/clearance stack",
    "downselect direct main PCB versus REG-08 control PCB ownership",
    "create and verify exact part footprints, pin maps, courtyards and 3D/body envelopes",
    "freeze control XY coordinates and keep-outs against adjacent components",
    "verify actuator/knob projection, tool access, anti-rotation features and service removal",
    "migrate physical switch instances from panel-excluded representation only after ownership is frozen",
)

def validate_control_stack()->None:
    assert ENCLOSURE_MPN=="M5502119"
    assert ENCLOSURE_INTERNAL_COVER_HEIGHT_MM==86.2
    assert MAIN_PCB_CARRIER_STANDOFF_MM==8.0
    assert TOP_COVER_THICKNESS_MM is None
    assert CARRIER_OR_CONTROL_PLANE_Z_MM is None
    assert CONTROL_BOARD_OWNERSHIP.startswith("OPEN_")
    assert len(PARTS)==5
    assert sum(part.quantity for part in PARTS)==7
    assert B03_STATUS=="EXACT_PARTS_FROZEN_VERTICAL_STACK_AND_FOOTPRINTS_OPEN"
