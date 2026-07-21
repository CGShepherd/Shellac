from generator.core.components import jst_vh_3, minifit_6
from generator.core.geometry import Point
from generator.core.pins import pin_position

def test_jst_header_pin_order_matches_panel_xlr_when_unrotated():
    header = jst_vh_3("H101", "INPUT", Point(48, 85), rotation=0)
    assert pin_position(header, "1").y > pin_position(header, "2").y > pin_position(header, "3").y

def test_minifit_power_header_is_six_way_keyed_2x3():
    header = minifit_6("H901", "POWER", Point(48, 105), rotation=180)
    assert "5566-06A2_2x03" in header.footprint
    assert header.fields["Pin 6"] == "KEY/NC"
