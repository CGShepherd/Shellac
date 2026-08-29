"""DR-039 common post-EQ DC block."""
from __future__ import annotations
from math import log10, pi

CAPACITANCE_F = 1.0e-6
BIAS_RESISTANCE_OHM = 330_000.0

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
