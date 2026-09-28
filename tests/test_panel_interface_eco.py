from generator.core.sheet import Sheet
from generator.blocks.balanced_input import add_sch101_diff_converter_slice
from generator.blocks.power_entry import add_power_entry


def test_input_xlrs_are_panel_owned_and_microlock_headers_are_board_owned():
    sheet = Sheet("SCH101", "SCH101.kicad_sch")
    add_sch101_diff_converter_slice(sheet)
    parts = {c.ref: c for c in sheet.components}
    expected = "ProjectShellac:Molex_MicroLockPlus_5055780321_1x03_P2.00mm_Horizontal"
    for panel, header in (("J101", "H101"), ("J201", "H201")):
        assert parts[panel].on_board is False
        assert parts[panel].footprint == ""
        assert parts[header].on_board is True
        assert parts[header].footprint == expected
        assert parts[header].fields["PCB header"] == "5055780321"
        assert parts[header].fields["Footprint authority"] == (
            "AE-075 B07 exact-part EDA footprint and native-board migration validated"
        )


def test_dc_xlr_is_panel_owned_and_minifit_header_is_board_owned():
    sheet = Sheet("SCH106", "SCH106.kicad_sch")
    add_power_entry(sheet)
    parts = {c.ref: c for c in sheet.components}
    assert parts["J901"].on_board is False
    assert parts["J901"].footprint == ""
    assert parts["H901"].on_board is True
    assert "Mini-Fit" in parts["H901"].footprint
