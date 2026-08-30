import pytest

from generator.core.components import Component, capacitor, resistor
from generator.core.geometry import Point
from generator.core.grid import align_point
from generator.core.pins import pin_position
from generator.core.sheet import Sheet
from generator.blocks.final_gain import add_final_gain


def test_named_pin_position_uses_semantic_contract():
    component = Component(
        "U1",
        "ProjectShellac:OpAmp_Buffer_Block",
        "BUFFER",
        Point(100.0, 50.0),
    )
    origin = align_point(component.at)
    assert pin_position(component, "IN") == align_point(Point(origin.x - 11.43, origin.y))
    assert pin_position(component, "OUT") == align_point(Point(origin.x + 11.43, origin.y))


def test_named_pin_position_rotates_with_component():
    component = resistor("R1", "100", Point(10.0, 10.0), rotation=90.0)
    pin1 = pin_position(component, "1")
    pin2 = pin_position(component, "2")
    origin = align_point(component.at)
    assert pin1 == align_point(Point(origin.x, origin.y + 2.54))
    assert pin2 == align_point(Point(origin.x, origin.y - 2.54))


def test_vertical_two_pin_helper_keeps_opposite_nets_separate():
    sheet = Sheet("stub", "stub.kicad_sch")
    cap = sheet.add_component(capacitor("C1", "100n", Point(50.0, 50.0)))
    sheet.connect_vertical_two_pin(cap, "+18V", "0VA")
    first, second = sheet.wires
    assert max(first.y1, first.y2) > min(second.y1, second.y2)
    assert min(first.y1, first.y2) > max(second.y1, second.y2)


def test_sch104_builder_emits_real_connectivity():
    sheet = Sheet("SCH104", "SCH104.kicad_sch")
    add_final_gain(sheet)
    assert len(sheet.wires) >= 20
    labels = {label.name for label in sheet.labels}
    assert {"FILTERED_L", "FILTERED_R", "BUFFERED_L", "BUFFERED_R", "+18V", "-18V", "0VA"}.issubset(labels)


def test_mode_switch_named_pin_contract():
    component = Component(
        "SW1", "ProjectShellac:Mode_Switch_Block", "MODE", Point(100.0, 100.0)
    )
    origin = align_point(component.at)
    assert pin_position(component, "L_IN") == align_point(Point(origin.x - 15.24, origin.y + 7.62))
    assert pin_position(component, "R_OUT") == align_point(Point(origin.x + 15.24, origin.y - 5.08))


def test_sch105_builder_emits_real_connectivity():
    from generator.blocks.mode_matrix import add_mode_matrix
    sheet = Sheet("SCH105", "SCH105.kicad_sch")
    add_mode_matrix(sheet)
    assert len(sheet.wires) >= 30
    labels = {label.name for label in sheet.labels}
    assert {
        "BUFFERED_L", "BUFFERED_R", "MONO_AVG", "MODE_L", "MODE_R",
        "+18V", "-18V", "0VA",
    }.issubset(labels)



def test_rumble_bypass_switch_named_pin_contract():
    component = Component(
        "SW1", "ProjectShellac:Switch_Bypass_Block", "BYPASS", Point(100.0, 100.0)
    )
    origin = align_point(component.at)
    assert pin_position(component, "L_DIRECT") == align_point(Point(origin.x - 15.24, origin.y + 7.62))
    assert pin_position(component, "R_OUT") == align_point(Point(origin.x + 15.24, origin.y - 3.81))


def test_sch107_builder_emits_real_connectivity():
    from generator.blocks.rumble_filter import add_rumble_filter

    sheet = Sheet("SCH107", "SCH107.kicad_sch")
    add_rumble_filter(sheet)

    assert len(sheet.wires) >= 70
    labels = {label.name for label in sheet.labels}
    assert {
        "POST_EQ_L", "POST_EQ_R", "FILTERED_L", "FILTERED_R",
        "+18V", "-18V", "0VA",
    }.issubset(labels)
    assert {
        "L_HP1_OUT", "R_HP1_OUT", "L_HP2_OUT", "R_HP2_OUT",
        "L_FILTER_BRANCH", "R_FILTER_BRANCH",
    }.isdisjoint(labels)



def test_balanced_driver_and_mute_named_pin_contracts():
    driver = Component(
        "U1", "ProjectShellac:Balanced_Line_Driver_Block", "THAT1646",
        Point(100.0, 100.0)
    )
    mute = Component(
        "SW1", "ProjectShellac:Switch_Mute_Block", "MUTE",
        Point(100.0, 100.0)
    )
    driver_origin = align_point(driver.at)
    mute_origin = align_point(mute.at)
    assert pin_position(driver, "IN") == align_point(Point(driver_origin.x - 15.24, driver_origin.y))
    assert pin_position(driver, "OUT+") == align_point(Point(driver_origin.x + 15.24, driver_origin.y + 5.08))
    assert pin_position(driver, "OUT-") == align_point(Point(driver_origin.x + 15.24, driver_origin.y - 5.08))
    assert pin_position(driver, "SNS-") == align_point(Point(driver_origin.x, driver_origin.y - 12.70))
    assert pin_position(driver, "SNS+") == align_point(Point(driver_origin.x + 5.08, driver_origin.y - 12.70))
    assert pin_position(driver, "SNS-") != pin_position(driver, "SNS+")
    assert pin_position(mute, "L_SIGNAL") == align_point(Point(mute_origin.x - 15.24, mute_origin.y + 7.62))
    assert pin_position(mute, "R_OUT") == align_point(Point(mute_origin.x + 15.24, mute_origin.y - 3.81))


def test_sch108_builder_emits_real_connectivity():
    from generator.blocks.balanced_output import add_balanced_output

    sheet = Sheet("SCH108", "SCH108.kicad_sch")
    add_balanced_output(sheet)

    assert len(sheet.wires) >= 90
    labels = {label.name for label in sheet.labels}
    assert {
        "MODE_L", "MODE_R", "+18V", "-18V", "0VA", "CHASSIS",
        "OUTPUT_L_POS", "OUTPUT_L_NEG",
        "OUTPUT_R_POS", "OUTPUT_R_NEG",
    }.issubset(labels)
    assert not {
        "L_DRIVER_IN", "R_DRIVER_IN",
        "L_DRV_OUT_POS", "L_DRV_OUT_NEG",
        "R_DRV_OUT_POS", "R_DRV_OUT_NEG",
    } & labels


def test_panel_control_and_led_named_pin_contracts():
    control=Component("SW1","ProjectShellac:Panel_Control_Block","CONTROL",Point(100.0,100.0)); led=Component("LED1","ProjectShellac:Panel_LED_Block","LED",Point(100.0,100.0))
    control_origin = align_point(control.at); led_origin = align_point(led.at)
    assert pin_position(control,"CONTROL") == align_point(Point(control_origin.x, control_origin.y - 10.16))
    assert pin_position(led,"A") == align_point(Point(led_origin.x, led_origin.y + 8.89))
    assert pin_position(led,"K") == align_point(Point(led_origin.x, led_origin.y - 8.89))
def test_sch109_builder_emits_real_connectivity():
    from generator.blocks.controls import add_controls
    sheet=Sheet("SCH109","SCH109.kicad_sch"); add_controls(sheet)
    assert len(sheet.wires)>=13
    assert {"BASS_SELECT","TREBLE_SELECT","MODE_SELECT","RUMBLE_BYPASS","MUTE_CONTROL","+18V","-18V","0VA"}.issubset({x.name for x in sheet.labels})


def test_sch103_builder_emits_real_connectivity():
    from generator.blocks.replay_eq import add_replay_equalisation
    sheet = Sheet("SCH103", "SCH103.kicad_sch")
    add_replay_equalisation(sheet)
    assert len(sheet.wires) >= 100
    labels = {label.name for label in sheet.labels}
    assert {
        "PRE_EQ_L", "PRE_EQ_R", "POST_EQ_L", "POST_EQ_R",
        "+18V", "-18V", "0VA",
    }.issubset(labels)


def test_sch101_dip_and_diffamp_named_pin_contracts():
    dip = Component("SW1", "ProjectShellac:DIP_Switch_Block", "GAIN", Point(100.0, 100.0))
    diff = Component("U1", "ProjectShellac:DiffAmp_Block", "DIFF", Point(100.0, 100.0))
    dip_origin = align_point(dip.at); diff_origin = align_point(diff.at)
    assert pin_position(dip, "1A") == align_point(Point(dip_origin.x - 17.78, dip_origin.y + 8.89))
    assert pin_position(dip, "8B") == align_point(Point(dip_origin.x + 17.78, dip_origin.y - 8.89))
    assert pin_position(diff, "IN+") == align_point(Point(diff_origin.x - 11.43, diff_origin.y - 2.54))
    assert pin_position(diff, "OUT") == align_point(Point(diff_origin.x + 11.43, diff_origin.y))


def test_sch101_builder_emits_real_connectivity():
    from generator.blocks.balanced_input import add_sch101_diff_converter_slice
    sheet = Sheet("SCH101", "SCH101.kicad_sch")
    add_sch101_diff_converter_slice(sheet)
    refs={component.ref for component in sheet.components}
    assert {"RN130","RN230","U103","U203"} <= refs
    assert len(sheet.wires) >= 90
    assert {"PRE_EQ_L", "PRE_EQ_R", "+18V", "-18V", "0VA", "CHASSIS"}.issubset({label.name for label in sheet.labels})
