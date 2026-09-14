import math

from simulation.scripts.analytical_correlation import (
    build_report,
    equal_resistor_average,
    gain_db,
    high_pass_fc,
    high_pass_mag_db,
)


def test_dr039_direct_rc_corner_matches_expected():
    fc = high_pass_fc(330000.0, 1.0e-6)
    assert math.isclose(fc, 0.4822877063390768, rel_tol=0.0, abs_tol=1e-12)


def test_dr039_direct_rc_20hz_loss_is_negligible():
    loss = high_pass_mag_db(20.0, 330000.0, 1.0e-6)
    assert -0.003 < loss < -0.002


def test_selected_sch101_nominal_converter_gain_is_12db_class():
    db = gain_db(4.0)
    assert math.isclose(db, 12.041199826559248, rel_tol=0.0, abs_tol=1e-12)


def test_equal_4k7_mono_average_truth():
    assert equal_resistor_average(1.0, 0.0, 4700.0, 4700.0) == 0.5
    assert equal_resistor_average(0.0, 1.0, 4700.0, 4700.0) == 0.5
    assert equal_resistor_average(1.0, 1.0, 4700.0, 4700.0) == 1.0
    assert equal_resistor_average(1.0, -1.0, 4700.0, 4700.0) == 0.0


def test_controlled_report_contains_all_three_early_correlation_cases():
    report = build_report()
    assert set(report["cases"]) == {
        "dr039_direct_rc",
        "sch101_nominal_gain",
        "matrix_mono_average",
    }
    assert report["authority"]["architecture"] == "AE-053"
    assert report["authority"]["execution"] == "AE-050"
    assert report["authority"]["acceptance"] == "AE-049"
