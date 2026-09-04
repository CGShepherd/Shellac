from generator.layout.footprint_contract import build_footprint_contract
from generator.layout.sr042_native_routing_bootstrap import build_native_routing_bootstrap
from generator.mechanical.released_placement_board import (
    render_released_placement_reference_board,
    validate_released_placement_reference_board,
)

def test_sr042_native_bootstrap_is_released_from_sr041():
    gate=build_native_routing_bootstrap()
    assert gate.status=="READY_FOR_NATIVE_KICAD_BOARD_CREATION"
    assert gate.board_width_mm==220.0
    assert gate.board_depth_mm==140.0
    assert gate.footprint_count==len(build_footprint_contract().board_population_refs)
    assert gate.mounting_hole_count==4
    assert gate.critical_manual_net_count==10

def test_sr042_reference_board_has_holes_and_all_placement_envelopes():
    text=render_released_placement_reference_board()
    assert validate_released_placement_reference_board(text)==[]
    assert text.count('(footprint "ProjectShellac:MountingHole"')==4
    assert text.count('(footprint "ProjectShellac:PlacementReference"')==len(build_footprint_contract().board_population_refs)
    assert '(segment ' not in text
