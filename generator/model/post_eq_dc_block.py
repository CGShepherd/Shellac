"""DR-039 branch-local DIRECT/BYPASS DC-block contract."""
from __future__ import annotations
from math import log10, pi

CAPACITANCE_F = 1.0e-6
CAPACITANCE_VALUE = "1u"
BIAS_RESISTANCE_OHM = 330_000.0
BIAS_RESISTANCE_VALUE = "330k"
CAPACITOR_DIELECTRIC = "PET film"
CAPACITOR_VOLTAGE = "63V"
CAPACITOR_FOOTPRINT = "Capacitor_THT:C_Rect_L7.2mm_W5.0mm_P5.00mm"
DIRECT_BRANCH_REFS = {
    "L": ("C30060", "R30060"),
    "R": ("C35060", "R35060"),
}

def cutoff_hz() -> float:
    return 1.0/(2*pi*BIAS_RESISTANCE_OHM*CAPACITANCE_F)

def magnitude(f_hz: float) -> float:
    if f_hz <= 0:
        return 0.0
    x=2*pi*f_hz*BIAS_RESISTANCE_OHM*CAPACITANCE_F
    return x/(1+x*x)**0.5

def magnitude_db(f_hz: float) -> float:
    return 20*log10(magnitude(f_hz))

def validate_post_eq_dc_block():
    assert 0.4 < cutoff_hz() < 0.6
    assert magnitude_db(20.0) > -0.01
    assert set(DIRECT_BRANCH_REFS) == {"L", "R"}
    assert len({ref for pair in DIRECT_BRANCH_REFS.values() for ref in pair}) == 4
