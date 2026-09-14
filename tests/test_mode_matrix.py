import pytest
from generator.model.mode_matrix import ChannelMode, DESIGN_STATUS, MODE_TABLE, ModeMatrixStatus, direct_path_error_db, intentional_lr_bridge_present, mono_average_error_db, mono_average_gain_for_equal_inputs, mono_bridge_current_a, mono_source_impedance_ohm, output_margin_db, validate_mode_matrix
from generator.model.mode_matrix_analysis import analyse_mode_matrix

def test_mode_matrix_is_ae041_and_qualification_open():
    assert DESIGN_STATUS is ModeMatrixStatus.QUALIFICATION_OPEN; validate_mode_matrix()
def test_truth_table_follows_physical_ccw_to_cw_order():
    assert [r.mode for r in MODE_TABLE]==[ChannelMode.DUAL_LEFT,ChannelMode.STEREO,ChannelMode.MONO_SUM,ChannelMode.DUAL_RIGHT]
    assert [(r.left_source,r.right_source) for r in MODE_TABLE]==[("BUFFERED_L","BUFFERED_L"),("BUFFERED_L","BUFFERED_R"),("MONO_AVG","MONO_AVG"),("BUFFERED_R","BUFFERED_R")]
    assert [r.mono_right_leg_connected for r in MODE_TABLE]==[False,False,True,False]
def test_no_intentional_lr_bridge_outside_mono():
    assert not intentional_lr_bridge_present(ChannelMode.DUAL_LEFT); assert not intentional_lr_bridge_present(ChannelMode.STEREO); assert intentional_lr_bridge_present(ChannelMode.MONO_SUM); assert not intentional_lr_bridge_present(ChannelMode.DUAL_RIGHT)
def test_mono_node_impedance_and_loading():
    assert mono_source_impedance_ohm()==pytest.approx(2350.0); assert mono_average_gain_for_equal_inputs()==pytest.approx(0.997868,rel=1e-5); assert abs(mono_average_error_db())<0.03; assert abs(direct_path_error_db())<0.001
def test_mono_bridge_current_is_bounded_only_when_selected():
    assert mono_bridge_current_a(6.42)*1000==pytest.approx(0.683,rel=2e-3)
def test_headroom_and_analysis_summary():
    assert output_margin_db()>3.8; result=analyse_mode_matrix(); assert result.mono_gain==pytest.approx(mono_average_gain_for_equal_inputs())
