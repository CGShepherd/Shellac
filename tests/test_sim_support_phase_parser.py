import pytest
from simulation.scripts.sim_support import parse_measure

def test_phase_parser_uses_second_ltspice_tuple_member():
    text = """
vph20: ph(V(VP,VM)/V(IN)) =(-31.9204746918dB,180°) at 20
sph20: ph(V(SP,SM)/V(IN)) =(-79.2015286906dB,180°) at 20
"""
    assert parse_measure(text, "VPH20") == pytest.approx(180.0)
    assert parse_measure(text, "SPH20") == pytest.approx(180.0)

def test_phase_parser_preserves_signed_tuple_phase():
    text = """
PNEG: ph(V(OUT)/V(IN)) =(-1.234dB,-47.125°) at 1000
PPOS: ph(V(OUT)/V(IN)) =(+0.125dB,+12.500°) at 20000
"""
    assert parse_measure(text, "PNEG") == pytest.approx(-47.125)
    assert parse_measure(text, "PPOS") == pytest.approx(12.5)

def test_phase_parser_accepts_scalar_degree_form():
    text = "PHASE: ph(V(OUT)/V(IN)) = -89.75deg\n"
    assert parse_measure(text, "PHASE") == pytest.approx(-89.75)

def test_magnitude_tuple_parsing_is_unchanged():
    text = "GAIN: mag(V(OUT))=(-6.020599913dB,0°) at 1000\n"
    assert parse_measure(text, "GAIN") == pytest.approx(0.5, rel=1e-10)
