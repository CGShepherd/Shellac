from generator.model.control_architecture import MATRIX, MANUFACTURING_COORDINATES_RELEASED, validate_control_architecture

def test_control_architecture_validates(): validate_control_architecture()
def test_matrix_is_3p4t_switched_summing():
    assert MATRIX.mpn=="A30403RNCB"; assert MATRIX.poles==3; assert MATRIX.positions==4; assert MATRIX.switched_leg_node=="MONO_R_LEG"; assert MATRIX.switched_leg_mode=="L+R"
def test_manufacturing_coordinates_remain_open(): assert MANUFACTURING_COORDINATES_RELEASED is False
