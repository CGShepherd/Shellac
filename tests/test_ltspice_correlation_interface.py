import math

from simulation.scripts.ltspice_correlation import (
    _transform_actual,
    extract_measurement,
    parse_correlation_measurements,
)


def test_parse_scalar_expression_measurement():
    text = "corr_scalar: expression=0.999711\n"
    values = parse_correlation_measurements(text)
    assert values["CORR_SCALAR"] == 0.999711


def test_when_at_extraction_uses_trailing_crossing_value():
    text = "corr_rc_fc_hz: mag(V(OUT))=0.7071067812  AT 0.482295004676\n"
    assert extract_measurement(text, "CORR_RC_FC_HZ", {"extraction": "when_at"}) == 0.482295004676


def test_complex_db_extraction_uses_first_db_component_not_frequency():
    text = "corr_rc_db_20hz: mag(V(OUT)) =(-0.00252502730823dB,0°) at 20\n"
    assert extract_measurement(text, "CORR_RC_DB_20HZ", {"extraction": "complex_db"}) == -0.00252502730823


def test_complex_result_is_not_misparsed_as_scalar():
    text = "corr_rc_db_20hz: db(V(OUT)) =(-13.5dB,90deg) at 20\n"
    values = parse_correlation_measurements(text)
    assert "CORR_RC_DB_20HZ" not in values


def test_metric_specific_extraction_prevents_false_at_parse():
    text = "corr_rc_db_20hz: db(V(OUT)) =(-13.5dB,90deg) at 20\n"
    assert extract_measurement(text, "CORR_RC_DB_20HZ", {"extraction": "complex_db"}) == -13.5


def test_magnitude_to_db_transform_remains_available():
    value = _transform_actual(4.0, {"transform": "magnitude_to_db"})
    assert math.isclose(value, 12.041199826559248, abs_tol=1e-12)


def test_toolchain_uses_explicit_batch_run_contract():
    from simulation.scripts.ltspice_correlation import SIM, load_yaml
    cfg = load_yaml(SIM / "config" / "toolchain.yaml")
    assert cfg["batch_arguments"] == ["-b", "-run", "{netlist}"]


def test_native_log_identity_check_accepts_requested_circuit(tmp_path):
    from simulation.scripts.ltspice_correlation import _native_log_matches_netlist
    netlist = tmp_path / "case.cir"
    text = f"LTspice 26.0.2 for Windows\nCircuit: {netlist}\n"
    assert _native_log_matches_netlist(text, netlist)
