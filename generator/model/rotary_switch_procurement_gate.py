"""AE-075C exact procurement gate for the current NKK NR01 EQ controls.

Historical AE-026/AE-027 Lorlin PT records remain provenance only. This live
module follows AE-041 A1 and AE-075C current control authority.
"""

FAMILY="NKK NR01"
BASE_SWITCH_MPN="NR01105ANG13"
BASS_MPN="NR01105ANG13-2C"
TREBLE_MPN="NR01105ANG13-2A"

ELECTRICAL={
    "poles":1,
    "positions":5,
    "index_deg":45,
    "action":"BBM_NON_SHORTING",
    "contact_finish":"gold",
    "rating_va":0.4,
    "rating_v":28,
}

MECHANICAL={
    "mount":"PCB_THT_STRAIGHT_PC_WITH_BRACKET",
    "threaded_bushing":False,
    "body_xy_mm":(10.7,10.7),
    "depth_behind_panel_mm":10.5,
    "knob_family":"AT3009",
    "knob_mount":"FLANGE_BENEATH_PANEL",
}

BASS_KNOB_COLOUR="RED"
TREBLE_KNOB_COLOUR="BLACK"
VERTICAL_STACK_STATUS="OPEN_BEFORE_B03_CLOSURE"
FOOTPRINT_STATUS="OPEN_BEFORE_B03_CLOSURE"

def validate_procurement_gate():
    assert FAMILY=="NKK NR01"
    assert BASE_SWITCH_MPN=="NR01105ANG13"
    assert BASS_MPN=="NR01105ANG13-2C"
    assert TREBLE_MPN=="NR01105ANG13-2A"
    assert ELECTRICAL["poles"]==1
    assert ELECTRICAL["positions"]==5
    assert ELECTRICAL["action"]=="BBM_NON_SHORTING"
    assert ELECTRICAL["contact_finish"]=="gold"
    assert MECHANICAL["threaded_bushing"] is False
    assert MECHANICAL["knob_mount"]=="FLANGE_BENEATH_PANEL"
    assert VERTICAL_STACK_STATUS.startswith("OPEN")
    assert FOOTPRINT_STATUS.startswith("OPEN")
