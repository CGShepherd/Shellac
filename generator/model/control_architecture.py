"""Current Project Shellac control and matrix architecture authority."""
from dataclasses import dataclass
from typing import Tuple

ARCHITECTURE_RECORD="AE-041"
ARCHITECTURE_REVISION="A1"
HARDWARE_RECONCILIATION_RECORD="AE-076B"
MANUFACTURING_COORDINATES_RELEASED=False
CONTROL_STACK_STATUS="SINGLE_MAIN_PCB_SERVICE_MODULE_SELECTED_MCAD_PHYSICAL_MIGRATION_OPEN"

SIGNAL_FLOW=("INPUT","BASS","TREBLE","RUMBLE","MATRIX","MUTE","OUTPUT")
TOP_COVER_DIRECTION="FRONT_TO_REAR"
CONTROL_SURFACE="REMOVABLE_TOP_COVER"
REG08_ROLE="DISTRIBUTED_TOP_COVER_MECHANICAL_REGISTRATION_AUTHORITY_NO_CENTRAL_ANALOGUE_STRIP"
CONTROL_BOARD_OWNERSHIP="ONE_MAIN_AUDIO_PCB_ALL_SEVEN_CONTROLS_DIRECT"
CONTROL_SERVICE_MODULE="UPPER_COVER_PLUS_MAIN_PCB_PLUS_CONTROLS_REMOVABLE_ASSEMBLY"
CONTROL_INTERBOARD_HARNESSES_SELECTED=False
ALUMINIUM_CARRIER_SELECTED=False
MAIN_PCB_SUPPORT_COUNT=6
SUPPORT_XY_Z_FROZEN=False
PHYSICAL_CAD_MIGRATION_COMPLETE=False

@dataclass(frozen=True)
class RotaryControlAuthority:
    function:str
    channel:str
    manufacturer:str
    family_or_mpn:str
    knob_colour:str
    local_to_channel:bool
    panel_registration:str

@dataclass(frozen=True)
class ToggleAuthority:
    reference:str
    function:str
    manufacturer:str
    mpn:str
    left_label:str
    right_label:str
    actuation_axis:str="TRANSVERSE_LEFT_RIGHT"

@dataclass(frozen=True)
class MatrixAuthority:
    manufacturer:str
    mpn:str
    fallback_mpn:str
    poles:int
    positions:int
    switching:str
    contacts:str
    mounting:str
    mode_order_ccw_to_cw:Tuple[str,...]
    averaging_resistance_ohm:float
    averaging_tolerance_percent:float
    averaging_resistor_count:int
    summing_node:str
    switched_leg_node:str
    switched_leg_mode:str
    isolation_resistor_ohm:float

EQ_CONTROLS=(
    RotaryControlAuthority("BASS","L","NKK","NR01105ANG13-2C","RED",True,"AT3009 flange beneath panel; no threaded bushing"),
    RotaryControlAuthority("BASS","R","NKK","NR01105ANG13-2C","RED",True,"AT3009 flange beneath panel; no threaded bushing"),
    RotaryControlAuthority("TREBLE","L","NKK","NR01105ANG13-2A","BLACK",True,"AT3009 flange beneath panel; no threaded bushing"),
    RotaryControlAuthority("TREBLE","R","NKK","NR01105ANG13-2A","BLACK",True,"AT3009 flange beneath panel; no threaded bushing"),
)

RUMBLE=ToggleAuthority("SW904","RUMBLE","C&K","7201SYCBE","BYPASS","IN")
MUTE=ToggleAuthority("SW905","MUTE","C&K","7201SYCBE","RUN","MUTE")
MATRIX=MatrixAuthority(
    "C&K","A30403RNCB","TE/Alcoswitch MRJE3404",
    3,4,"BBM_NON_SHORTING","GOLD","THT_PCB_PLUS_3/8-32_BUSHING",
    ("DUAL L","STEREO","L+R","DUAL R"),
    4700.0,0.1,2,"MONO_AVG","MONO_R_LEG","L+R",100.0)

MATRIX_KNOB={
    "manufacturer":"TE/Alcoswitch",
    "mpn":"KN900B1/4",
    "diameter_mm":24.1,
    "finish":"black knurled aluminium",
    "indicator":"line",
}

RELATIVE_GEOMETRY={
    "treble_to_rumble_min_pitch_mm":25.0,
    "rumble_to_matrix_min_pitch_mm":32.0,
    "matrix_to_mute_min_pitch_mm":35.0,
    "matrix_operator_envelope_diameter_mm":40.0,
    "status":"ERGONOMIC_TARGET_NOT_MANUFACTURING_RELEASE",
}

OPEN_QUALIFICATION=(
    "matrix_switching_transients_spice_and_bench",
    "matrix_mono_accuracy_spice_and_bench",
    "production_switch_detent_terminal_continuity_confirmation",
    "ae076b2_dimensionally_controlled_mcad_digital_mockup",
    "nkk_12p3mm_constrained_main_pcb_plane_to_ck_fit_and_tolerance_stack",
    "six_support_xy_z_hardware_and_tolerance_stack",
    "exact_part_footprints_pin_mapping_courtyards_and_3d_envelopes",
    "control_xy_and_upper_cover_apertures",
    "run10_switch_local_parasitic_and_stability_acceptance",
    "native_pcb_control_and_support_migration",
    "manual_placement_reconciliation_after_mcad_freeze",
)

def validate_control_architecture()->None:
    assert SIGNAL_FLOW==("INPUT","BASS","TREBLE","RUMBLE","MATRIX","MUTE","OUTPUT")
    assert len(EQ_CONTROLS)==4 and all(c.local_to_channel for c in EQ_CONTROLS)
    assert [c.family_or_mpn for c in EQ_CONTROLS]==[
        "NR01105ANG13-2C","NR01105ANG13-2C",
        "NR01105ANG13-2A","NR01105ANG13-2A"]
    assert all("no threaded bushing" in c.panel_registration for c in EQ_CONTROLS)
    assert RUMBLE.mpn==MUTE.mpn=="7201SYCBE"
    assert MATRIX.mpn=="A30403RNCB" and MATRIX.poles==3 and MATRIX.positions==4
    assert MATRIX.fallback_mpn=="TE/Alcoswitch MRJE3404"
    assert MATRIX.mode_order_ccw_to_cw==("DUAL L","STEREO","L+R","DUAL R")
    assert MATRIX.switched_leg_node=="MONO_R_LEG" and MATRIX.switched_leg_mode=="L+R"
    assert MATRIX.averaging_resistor_count==2 and MATRIX.averaging_resistance_ohm==4700.0
    assert CONTROL_STACK_STATUS=="SINGLE_MAIN_PCB_SERVICE_MODULE_SELECTED_MCAD_PHYSICAL_MIGRATION_OPEN"
    assert CONTROL_BOARD_OWNERSHIP=="ONE_MAIN_AUDIO_PCB_ALL_SEVEN_CONTROLS_DIRECT"
    assert CONTROL_INTERBOARD_HARNESSES_SELECTED is False
    assert ALUMINIUM_CARRIER_SELECTED is False
    assert MAIN_PCB_SUPPORT_COUNT==6
    assert SUPPORT_XY_Z_FROZEN is False
    assert PHYSICAL_CAD_MIGRATION_COMPLETE is False
    assert MANUFACTURING_COORDINATES_RELEASED is False
