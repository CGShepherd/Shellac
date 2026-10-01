# AE-076B current Shellac control/service-module architecture contract.
from __future__ import annotations
from dataclasses import dataclass

ARCHITECTURE_RECORD="AE-076B"
ENCLOSURE_MPN="M5502119"
ENCLOSURE_INTERNAL_COVER_HEIGHT_MM=86.2
TOP_COVER_NOMINAL_MM=2.0
TOP_COVER_TOLERANCE_MM=None

NKK_SWITCH_DEPTH_BEHIND_PANEL_MM=10.5
NKK_INSTALLED_PANEL_TO_PCB_MM=12.3
KNOWN_MAIN_BOARD_COMPONENT_HEIGHT_MM=11.0

CARRIER_PRESENT_IN_SELECTED_ARCHITECTURE=False
CARRIER_THICKNESS_MM=None
MAIN_PCB_CARRIER_STANDOFF_MM=None

CONTROL_BOARD_OWNERSHIP="ONE_MAIN_AUDIO_PCB_ALL_SEVEN_CONTROLS_DIRECT_SELECTED_PHYSICAL_MIGRATION_PENDING"
EQ_CONTROL_OWNERSHIP="MAIN_AUDIO_PCB_DIRECT_LOCAL_TO_CHANNEL_REGIONS_SELECTED"
SHARED_CK_CONTROL_OWNERSHIP="MAIN_AUDIO_PCB_DIRECT_SELECTED"
CONTROL_MODULE_PARTITION=("MAIN_AUDIO_PCB",)
SHARED_CK_CONTROL_PCB_PARTITION="NONE_SINGLE_MAIN_AUDIO_PCB"
CONTROL_INTERCONNECT_ARCHITECTURE="NO_CONTROL_INTERBOARD_HARNESSES"
CONTROL_CONNECTOR_FAMILY=None
CONTROL_CONNECTOR_HEADER_SERIES=()
CONTROL_CONNECTOR_HOUSING_SERIES=None
CONTROL_CONNECTOR_CRIMP_MPN=None
RUMBLE_EXTERNAL_NET_COUNT=0
MATRIX_MUTE_EXTERNAL_NET_COUNT=0
EQ_PASSIVE_PARTITION="NO_MEZZANINE_PARTITION_SELECTED_RUN10_PARASITIC_ACCEPTANCE_OPEN"
RIGID_BOARD_TO_BOARD_CONTROL_INTERCONNECT_ALLOWED=False
DIRECT_MAIN_PCB_CONTROL_MOUNTING_ALLOWED=True
CENTRAL_REMOTE_CONTROL_STRIP_ALLOWED=False

MAIN_PCB_SUPPORT_COUNT=6
SUPPORT_ARCHITECTURE="PCB_TO_REMOVABLE_UPPER_COVER_PRIMARY_DATUM_SUPPORTS"
SUPPORT_XY_FROZEN=False
SUPPORT_Z_TOLERANCE_STACK_FROZEN=False
CONTROL_XY_FROZEN=False
CK_INSTALLED_PCB_PLANE_VERIFIED=False
PHYSICAL_CAD_MIGRATION_COMPLETE=False
MCAD_DIGITAL_MOCKUP_REQUIRED=True
COMMON_MAIN_PCB_CONTROL_PLANE_MM=None

B03_STATUS="SINGLE_MAIN_PCB_SERVICE_MODULE_SELECTED_MCAD_Z_XY_FOOTPRINT_MIGRATION_OPEN"

@dataclass(frozen=True, slots=True)
class ControlStackPart:
    function:str
    quantity:int
    mpn:str
    panel_registration:str
    pcb_mounting:str

PARTS=(
    ControlStackPart("BASS",2,"NR01105ANG13-2C",
        "AT3009 flanged knob beneath panel; controlled panel-to-PCB relationship 12.3 mm",
        "direct main audio PCB; local to corresponding SCH103 channel; exact footprint/XY migration open"),
    ControlStackPart("TREBLE",2,"NR01105ANG13-2A",
        "AT3009 flanged knob beneath panel; controlled panel-to-PCB relationship 12.3 mm",
        "direct main audio PCB; local to corresponding SCH103 channel; exact footprint/XY migration open"),
    ControlStackPart("CHANNEL",1,"A30403RNCB",
        "3/8-32 threaded bushing; installed PCB plane must be proven in MCAD/tolerance stack",
        "direct main audio PCB; bushing secondary only after six-support PCB datum is established"),
    ControlStackPart("RUMBLE",1,"7201SYCBE",
        "1/4-40 threaded bushing; installed PCB plane must be proven in MCAD/tolerance stack",
        "direct main audio PCB local to SCH107; bushing secondary only"),
    ControlStackPart("MUTE",1,"7201SYCBE",
        "1/4-40 threaded bushing; installed PCB plane must be proven in MCAD/tolerance stack",
        "direct main audio PCB immediately before THAT1646; bushing secondary only"),
)

REQUIRED_BEFORE_B03_CLOSURE=(
    "governed dimensionally accurate MCAD assembly of M5502119, panels, PCB, major connectors and controls",
    "prove C&K A30403RNCB and 7201SYCBE fit at the rigid PCB plane constrained by NKK 12.3 mm installation evidence",
    "freeze six PCB-to-upper-cover support XY, Z, hardware and tolerance stack",
    "freeze exact control footprints, pin maps, courtyards and 3D/body envelopes",
    "freeze control XY coordinates, upper-cover apertures and keep-outs",
    "close RUN10 switch-local parasitic/stability obligations",
    "migrate physical control footprints/support geometry only after MCAD acceptance",
    "reconcile manual placement only after MCAD/support datum freeze",
)

def validate_control_stack()->None:
    assert ARCHITECTURE_RECORD=="AE-076B"
    assert ENCLOSURE_MPN=="M5502119"
    assert TOP_COVER_NOMINAL_MM==2.0
    assert NKK_INSTALLED_PANEL_TO_PCB_MM==12.3
    assert CARRIER_PRESENT_IN_SELECTED_ARCHITECTURE is False
    assert CARRIER_THICKNESS_MM is None
    assert MAIN_PCB_CARRIER_STANDOFF_MM is None
    assert CONTROL_BOARD_OWNERSHIP=="ONE_MAIN_AUDIO_PCB_ALL_SEVEN_CONTROLS_DIRECT_SELECTED_PHYSICAL_MIGRATION_PENDING"
    assert EQ_CONTROL_OWNERSHIP=="MAIN_AUDIO_PCB_DIRECT_LOCAL_TO_CHANNEL_REGIONS_SELECTED"
    assert SHARED_CK_CONTROL_OWNERSHIP=="MAIN_AUDIO_PCB_DIRECT_SELECTED"
    assert CONTROL_MODULE_PARTITION==("MAIN_AUDIO_PCB",)
    assert CONTROL_INTERCONNECT_ARCHITECTURE=="NO_CONTROL_INTERBOARD_HARNESSES"
    assert CONTROL_CONNECTOR_FAMILY is None
    assert DIRECT_MAIN_PCB_CONTROL_MOUNTING_ALLOWED is True
    assert CENTRAL_REMOTE_CONTROL_STRIP_ALLOWED is False
    assert MAIN_PCB_SUPPORT_COUNT==6
    assert SUPPORT_XY_FROZEN is False
    assert SUPPORT_Z_TOLERANCE_STACK_FROZEN is False
    assert CONTROL_XY_FROZEN is False
    assert CK_INSTALLED_PCB_PLANE_VERIFIED is False
    assert PHYSICAL_CAD_MIGRATION_COMPLETE is False
    assert MCAD_DIGITAL_MOCKUP_REQUIRED is True
    assert COMMON_MAIN_PCB_CONTROL_PLANE_MM is None
    assert sum(part.quantity for part in PARTS)==7
    assert all("direct main audio PCB" in part.pcb_mounting for part in PARTS)
    assert B03_STATUS=="SINGLE_MAIN_PCB_SERVICE_MODULE_SELECTED_MCAD_Z_XY_FOOTPRINT_MIGRATION_OPEN"
