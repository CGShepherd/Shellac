"""AE-026 Lorlin PT rotary-switch platform contract."""

PT_FAMILY = "Lorlin PT"
MOUNTING = "PCB vertical / shaft normal to PCB / panel bush support"
SHAFT_DIAMETER_MM = 6.0
STANDARD_SHAFT_LENGTH_MM = 50.0
BUSH_THREAD = "M10 x 0.75"
PANEL_HOLE_MM = 10.0
PCB_TERMINAL_PITCH_MM = 2.54
STANDARD_INDEX_DEG = 30
CONTACT_ACTION = "BBM / non-shorting"
CONTACT_FINISH_REQUIRED = "gold plated preferred; gold flash acceptable only by explicit review"
INITIAL_CONTACT_RESISTANCE_MAX_MOHM = 20.0
INSULATION_RESISTANCE_MIN_MOHM = 999.0
MECHANICAL_LIFE_MIN_CYCLES = 10_000

BASS_TREBLE = {
    "poles": 2,
    "positions": 5,
    "wafer_count": 1,
    "reference_standard_metric_bbm": "PT6004",
    "stocked_geometry_proxy": "PT6422/BMH",
    "production_mpn_status": "GOLD CONTACT ORDER CODE TO BE CONFIRMED BY LORLIN",
}

CHANNEL = {
    "poles": 4,
    "positions": 4,
    "wafer_count": 2,
    "architecture": "two synchronised 2-pole wafers, stopped at four positions",
    "production_mpn_status": "CUSTOM MULTIWAFER ORDER CODE TO BE CONFIRMED BY LORLIN",
}

WAFER_SPACING_OPTIONS_MM = (6.35, 7.63, 10.16)
PREFERRED_WAFER_SPACING_MM = 6.35

def validate_pt_platform_contract():
    assert BASS_TREBLE["poles"] == 2
    assert BASS_TREBLE["positions"] == 5
    assert CHANNEL["poles"] == 4
    assert CHANNEL["positions"] == 4
    assert CHANNEL["wafer_count"] == 2
    assert SHAFT_DIAMETER_MM == 6.0
    assert BUSH_THREAD == "M10 x 0.75"
    assert PANEL_HOLE_MM == 10.0
    assert PCB_TERMINAL_PITCH_MM == 2.54
    assert CONTACT_ACTION.startswith("BBM")
    assert PREFERRED_WAFER_SPACING_MM in WAFER_SPACING_OPTIONS_MM
