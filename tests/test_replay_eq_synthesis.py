import pytest

from generator.model.replay_eq import (
    BASS_NETWORKS,
    DESIGN_STATUS,
    P06_RF_OHM,
    P06_RG_OHM,
    P91_SOURCE_BASS_NETWORKS,
    RIAA_BASS_NETWORK,
    EqValueStatus,
    validate_replay_eq_data,
)
from generator.model.replay_eq_synthesis import active_synthesis_rows, exact_riaa_solution
from generator.model.replay_eq_transfer import active_network_response, frequency_response, logarithmic_frequencies


def test_curve_networks_are_optimised():
    assert DESIGN_STATUS is EqValueStatus.ELECTRICALLY_CLOSED
    validate_replay_eq_data()


def test_published_p91_source_networks_remain_traceable():
    expected = {
        "200 Hz SOURCE": (25.83684, 225.04148),
        "400 Hz SOURCE": (53.58752, 466.75270),
        "500 Hz SOURCE": (65.76651, 572.83285),
    }
    for row in active_synthesis_rows(source=True):
        pole, zero = expected[row.selection]
        assert row.pole_hz == pytest.approx(pole, rel=1e-6)
        assert row.zero_hz == pytest.approx(zero, rel=1e-6)


def test_final_historical_networks_hold_20_hz_lower_break():
    targets = {"200 Hz": 200.0, "400 Hz": 400.0, "500 Hz 78": 500.0}
    for row in active_synthesis_rows()[:3]:
        assert row.pole_hz == pytest.approx(20.0, rel=8e-4)
        assert row.zero_hz == pytest.approx(targets[row.selection], rel=2e-3)


def test_exact_riaa_solution_matches_3180_and_318_microseconds():
    rs, capacitance_nf = exact_riaa_solution()
    response = active_network_response(P06_RF_OHM, rs, P06_RG_OHM, capacitance_nf * 1e-9)
    assert rs == pytest.approx(8190.0819, rel=2e-5)
    assert capacitance_nf == pytest.approx(29.3917, rel=2e-5)
    assert response.pole_hz == pytest.approx(50.05, rel=1e-9)
    assert response.zero_hz == pytest.approx(500.5, rel=1e-9)


def test_selected_riaa_preferred_values_are_close_to_target():
    response = active_network_response(
        RIAA_BASS_NETWORK.rf_ohm,
        RIAA_BASS_NETWORK.rs_ohm,
        RIAA_BASS_NETWORK.rg_ohm,
        RIAA_BASS_NETWORK.capacitance_nf * 1e-9,
    )
    assert abs(response.pole_hz / 50.05 - 1.0) < 0.002
    assert abs(response.zero_hz / 500.5 - 1.0) < 0.002


def test_simple_14k3_bass_model_has_been_removed():
    import generator.model.replay_eq as model
    assert not hasattr(model, "BASS_FIXED_RESISTANCE_OHM")


def test_response_and_frequency_grid_are_numerically_sane():
    magnitude_db, phase_deg = frequency_response(1000.0, P06_RF_OHM, 1430.0, P06_RG_OHM, 78.47e-9)
    assert magnitude_db > 0
    assert -90.0 < phase_deg < 0.0
    grid = logarithmic_frequencies()
    assert len(grid) == 401
    assert grid[0] == pytest.approx(10.0)
    assert grid[-1] == pytest.approx(50_000.0)
