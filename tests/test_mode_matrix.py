import pytest

from generator.model.mode_matrix import (
    ChannelMode,
    DESIGN_STATUS,
    MODE_TABLE,
    ModeMatrixStatus,
    mono_average_error_db,
    mono_average_gain_for_equal_inputs,
    mono_source_impedance_ohm,
    output_margin_db,
    validate_mode_matrix,
)
from generator.model.mode_matrix_analysis import analyse_mode_matrix


def test_mode_matrix_is_electrically_closed():
    assert DESIGN_STATUS is ModeMatrixStatus.ELECTRICALLY_CLOSED
    validate_mode_matrix()


def test_truth_table_is_frozen():
    assert [row.mode for row in MODE_TABLE] == [
        ChannelMode.STEREO,
        ChannelMode.DUAL_LEFT,
        ChannelMode.DUAL_RIGHT,
        ChannelMode.MONO_SUM,
    ]
    assert MODE_TABLE[0].left_output_expression == "L"
    assert MODE_TABLE[0].right_output_expression == "R"
    assert MODE_TABLE[1].left_output_expression == "L"
    assert MODE_TABLE[1].right_output_expression == "L"
    assert MODE_TABLE[2].left_output_expression == "R"
    assert MODE_TABLE[2].right_output_expression == "R"
    assert MODE_TABLE[3].left_output_expression == "(L+R)/2"
    assert MODE_TABLE[3].right_output_expression == "(L+R)/2"


def test_summing_network_is_connected_only_in_mono_sum():
    connected = [row.mode for row in MODE_TABLE if row.summing_network_connected]
    assert connected == [ChannelMode.MONO_SUM]


def test_mono_average_level_is_effectively_unity_for_equal_inputs():
    assert mono_average_gain_for_equal_inputs() == pytest.approx(0.997868, rel=1e-5)
    assert abs(mono_average_error_db()) < 0.03


def test_mono_source_impedance_and_headroom():
    assert mono_source_impedance_ohm() == pytest.approx(2350.0)
    assert output_margin_db() > 3.8


def test_analysis_summary_matches_model():
    result = analyse_mode_matrix()
    assert result.mono_gain == pytest.approx(mono_average_gain_for_equal_inputs())
    assert result.mono_source_impedance_ohm == pytest.approx(2350.0)
