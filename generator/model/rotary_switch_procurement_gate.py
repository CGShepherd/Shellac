"""AE-027 exact procurement gate for the preferred Lorlin PT platform."""

FAMILY = "Lorlin PT"
STANDARD_BASS_TREBLE_MPN = "PT6004"
STANDARD_BASS_TREBLE = {
    "mount": "PCB",
    "metric": True,
    "poles": 2,
    "positions": 5,
    "index_deg": 30,
    "action": "BBM",
    "contact_finish": "standard silver",
}

STOCKED_PROXY_MPN = "PT6422/BMH"
STOCKED_PROXY_CONTACT_FINISH = "silver / Ag-plated standard construction"

PRODUCTION_CONTACT_FINISH = "gold plated preferred"
PRODUCTION_BASS_TREBLE_MPN = "OPEN — Lorlin non-standard order code required"

CHANNEL = {
    "architecture": "two synchronised 2-pole PT wafers",
    "positions": 4,
    "action": "BBM",
    "contact_finish": "gold plated preferred",
    "mpn": "OPEN — Lorlin multi-wafer order code required",
}

CONTACT_RESISTANCE_INITIAL_MAX_MOHM = 20.0
INSULATION_RESISTANCE_INITIAL_MIN_MOHM = 999.0
LIFE_MIN_CYCLES = 10_000
PANEL_HOLE_MM = 10.0
PCB_TERMINAL_PITCH_MM = 2.54

def validate_procurement_gate():
    assert STANDARD_BASS_TREBLE_MPN == "PT6004"
    assert STANDARD_BASS_TREBLE["poles"] == 2
    assert STANDARD_BASS_TREBLE["positions"] == 5
    assert STANDARD_BASS_TREBLE["action"] == "BBM"
    assert "gold" in PRODUCTION_CONTACT_FINISH
    assert PRODUCTION_BASS_TREBLE_MPN.startswith("OPEN")
    assert CHANNEL["mpn"].startswith("OPEN")
    assert CONTACT_RESISTANCE_INITIAL_MAX_MOHM == 20.0
