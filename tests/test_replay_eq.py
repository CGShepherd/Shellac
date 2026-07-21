from generator.model.replay_eq import (
    BASS_NETWORKS,
    DESIGN_STATUS,
    RIAA_BASS_NETWORK,
    SOURCE_RETRIEVED,
    SOURCE_URL,
    TREBLE_NETWORKS,
    EqValueStatus,
    validate_replay_eq_data,
)


def test_replay_eq_sources_and_transfer_function_status_are_controlled():
    validate_replay_eq_data()
    assert DESIGN_STATUS is EqValueStatus.ELECTRICALLY_CLOSED
    assert SOURCE_URL == "https://sound-au.com/project91.htm"
    assert SOURCE_RETRIEVED == "2026-07-14"


def test_replay_eq_switch_structure_is_frozen():
    assert len(BASS_NETWORKS) == 4
    assert len(TREBLE_NETWORKS) == 5
    assert BASS_NETWORKS[0].switch_condition == "SHORT"
    assert TREBLE_NETWORKS[0].switch_condition == "OPEN"


def test_dedicated_true_riaa_branch_is_present():
    assert RIAA_BASS_NETWORK.target_pole_hz == 50.05
    assert RIAA_BASS_NETWORK.target_zero_hz == 500.5
    assert RIAA_BASS_NETWORK.capacitance_nf == 29.4
    assert any(item.target_hz == 2121.0 for item in TREBLE_NETWORKS)
