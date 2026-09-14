from simulation.scripts.ltspice_correlation import read_ltspice_text
from simulation.scripts.shellac_spice import parse_measurements


def test_read_ltspice_utf16_bom(tmp_path):
    p = tmp_path / "x.log"
    p.write_bytes("CORR_GAIN_DB: 12.0412\r\n".encode("utf-16"))
    assert parse_measurements(read_ltspice_text(p))["CORR_GAIN_DB"] == 12.0412


def test_read_ltspice_utf16le_without_bom(tmp_path):
    p = tmp_path / "x.log"
    p.write_bytes("CORR_RC_DB_20HZ: -0.00252\r\n".encode("utf-16-le"))
    assert parse_measurements(read_ltspice_text(p))["CORR_RC_DB_20HZ"] == -0.00252


def test_read_ltspice_utf8(tmp_path):
    p = tmp_path / "x.log"
    p.write_text("CORR_MATRIX_EQUAL = 1.0\n", encoding="utf-8")
    assert parse_measurements(read_ltspice_text(p))["CORR_MATRIX_EQUAL"] == 1.0
