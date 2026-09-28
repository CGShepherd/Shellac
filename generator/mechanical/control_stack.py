"""Current Shellac control-stack mechanical contract for routing blocker B03."""
from __future__ import annotations
from dataclasses import dataclass

ENCLOSURE_MPN="M5502119"
ENCLOSURE_INTERNAL_COVER_HEIGHT_MM=86.2
UNICASE_GUIDE_PCB_THICKNESS_MM=1.6
CARRIER_THICKNESS_MM=2.0
CARRIER_GUIDE_RAIL_COMPATIBLE=False
MAIN_PCB_CARRIER_STANDOFF_MM=8.0

NKK_SWITCH_DEPTH_BEHIND_PANEL_MM=10.5
NKK_INSTALLED_PANEL_TO_PCB_MM=12.3
KNOWN_MAIN_BOARD_COMPONENT_HEIGHT_MM=11.0
NKK_NOMINAL_CLEARANCE_TO_KNOWN_11MM_PART_MM=round(
    NKK_INSTALLED_PANEL_TO_PCB_MM-KNOWN_MAIN_BOARD_COMPONENT_HEIGHT_MM, 1
)

TOP_COVER_THICKNESS_MM=None
CARRIER_OR_CONTROL_PLANE_Z_MM=None

EQ_CONTROL_OWNERSHIP="TWO_CHANNEL_LOCAL_EQ_MEZZANINES_SELECTED"
SHARED_CK_CONTROL_OWNERSHIP="DISTRIBUTED_LOCAL_CONTROL_PCB_SELECTED"
CONTROL_BOARD_OWNERSHIP="FOUR_LOCAL_CONTROL_PCBS_SELECTED_SUPPORT_FOOTPRINT_XY_OPEN"
CONTROL_MODULE_PARTITION=("EQ_L","EQ_R","RUMBLE","MATRIX_MUTE")
SHARED_CK_CONTROL_PCB_PARTITION="RUMBLE_LOCAL_PLUS_MATRIX_MUTE_DOWNSTREAM_SELECTED"
CONTROL_INTERCONNECT_ARCHITECTURE="SHORT_DETACHABLE_WIRE_HARNESSES_SELECTED"
CONTROL_CONNECTOR_FAMILY="MOLEX_MICRO_LOCK_PLUS_2MM_SELECTED"
CONTROL_CONNECTOR_HEADER_SERIES=("505575","505578")
CONTROL_CONNECTOR_HOUSING_SERIES="505570"
CONTROL_CONNECTOR_CRIMP_MPN="5055721200"
RUMBLE_EXTERNAL_NET_COUNT=6
MATRIX_MUTE_EXTERNAL_NET_COUNT=7
EQ_PASSIVE_PARTITION="OPEN_PENDING_B03_PARASITIC_RUN10_DISCRIMINATOR"
RIGID_BOARD_TO_BOARD_CONTROL_INTERCONNECT_ALLOWED=False
DIRECT_MAIN_PCB_CONTROL_MOUNTING_ALLOWED=False
CENTRAL_REMOTE_CONTROL_STRIP_ALLOWED=False
B03_STATUS="MODULE_PARTITION_AND_HARNESS_FAMILY_SELECTED_Z_SUPPORT_PASSIVES_FOOTPRINT_XY_OPEN"

@dataclass(frozen=True, slots=True)
class ControlStackPart:
    function:str
    quantity:int
    mpn:str
    panel_registration:str
    pcb_mounting:str

PARTS=(
    ControlStackPart("BASS",2,"NR01105ANG13-2C",
        "AT3009 flanged knob beneath panel; installed panel-to-PCB plane 12.3 mm",
        "channel-local EQ mezzanine; REG-08 mechanical registration; THT straight PC with support bracket"),
    ControlStackPart("TREBLE",2,"NR01105ANG13-2A",
        "AT3009 flanged knob beneath panel; installed panel-to-PCB plane 12.3 mm",
        "channel-local EQ mezzanine; REG-08 mechanical registration; THT straight PC with support bracket"),
    ControlStackPart("CHANNEL",1,"A30403RNCB",
        "3/8-32 threaded bushing and nut; exact PCB-plane stack still to freeze",
        "THT PC pins; local module partition selected; short detachable harness family selected; exact support/Z/connector variant open"),
    ControlStackPart("RUMBLE",1,"7201SYCBE",
        "1/4-40 threaded bushing and nut; exact PCB-plane stack still to freeze",
        "THT PC pins; local module partition selected; short detachable harness family selected; exact support/Z/connector variant open"),
    ControlStackPart("MUTE",1,"7201SYCBE",
        "1/4-40 threaded bushing and nut; exact PCB-plane stack still to freeze",
        "THT PC pins; local module partition selected; short detachable harness family selected; exact support/Z/connector variant open"),
)

REQUIRED_BEFORE_B03_CLOSURE=(
    "freeze main PCB/carrier Z relative to upper-cover inner face",
    "freeze top-cover thickness and finished aperture/clearance stack",
    "freeze exact C&K installed PCB-plane stack and local-control PCB support/connector variant",
    "freeze exact short-harness connector order codes/orientation after support and XY are known",
    "freeze switch-local passive ownership and bound RUN10 parasitic/stability effect",
    "create and verify exact part footprints, pin maps, courtyards and 3D/body envelopes",
    "freeze control XY coordinates and keep-outs against adjacent components",
    "verify actuator/knob projection, tool access, anti-rotation features and service removal",
    "migrate physical switch instances only after ownership and Z stack are frozen",
)

def validate_control_stack()->None:
    assert ENCLOSURE_MPN=="M5502119"
    assert ENCLOSURE_INTERNAL_COVER_HEIGHT_MM==86.2
    assert UNICASE_GUIDE_PCB_THICKNESS_MM==1.6
    assert CARRIER_THICKNESS_MM==2.0
    assert CARRIER_GUIDE_RAIL_COMPATIBLE is False
    assert MAIN_PCB_CARRIER_STANDOFF_MM==8.0
    assert NKK_SWITCH_DEPTH_BEHIND_PANEL_MM==10.5
    assert NKK_INSTALLED_PANEL_TO_PCB_MM==12.3
    assert NKK_NOMINAL_CLEARANCE_TO_KNOWN_11MM_PART_MM==1.3
    assert TOP_COVER_THICKNESS_MM is None
    assert CARRIER_OR_CONTROL_PLANE_Z_MM is None
    assert EQ_CONTROL_OWNERSHIP=="TWO_CHANNEL_LOCAL_EQ_MEZZANINES_SELECTED"
    assert SHARED_CK_CONTROL_OWNERSHIP=="DISTRIBUTED_LOCAL_CONTROL_PCB_SELECTED"
    assert CONTROL_BOARD_OWNERSHIP=="FOUR_LOCAL_CONTROL_PCBS_SELECTED_SUPPORT_FOOTPRINT_XY_OPEN"
    assert CONTROL_MODULE_PARTITION==("EQ_L","EQ_R","RUMBLE","MATRIX_MUTE")
    assert SHARED_CK_CONTROL_PCB_PARTITION=="RUMBLE_LOCAL_PLUS_MATRIX_MUTE_DOWNSTREAM_SELECTED"
    assert CONTROL_INTERCONNECT_ARCHITECTURE=="SHORT_DETACHABLE_WIRE_HARNESSES_SELECTED"
    assert CONTROL_CONNECTOR_FAMILY=="MOLEX_MICRO_LOCK_PLUS_2MM_SELECTED"
    assert CONTROL_CONNECTOR_CRIMP_MPN=="5055721200"
    assert RUMBLE_EXTERNAL_NET_COUNT==6
    assert MATRIX_MUTE_EXTERNAL_NET_COUNT==7
    assert EQ_PASSIVE_PARTITION=="OPEN_PENDING_B03_PARASITIC_RUN10_DISCRIMINATOR"
    assert RIGID_BOARD_TO_BOARD_CONTROL_INTERCONNECT_ALLOWED is False
    assert DIRECT_MAIN_PCB_CONTROL_MOUNTING_ALLOWED is False
    assert CENTRAL_REMOTE_CONTROL_STRIP_ALLOWED is False
    assert len(PARTS)==5
    assert sum(part.quantity for part in PARTS)==7
    assert B03_STATUS=="MODULE_PARTITION_AND_HARNESS_FAMILY_SELECTED_Z_SUPPORT_PASSIVES_FOOTPRINT_XY_OPEN"
