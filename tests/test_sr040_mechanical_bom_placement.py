from generator.mechanical.sr040_audio_freeze import (
    build_verified_audio_mechanical_release,
    frozen_audio_board_outline,
    frozen_audio_carrier,
)
from generator.procurement.full_bom_census import build_full_bom_census
from generator.layout.sr040_routing_readiness import build_sr040_routing_readiness

def test_sr040_audio_mechanical_datums_are_frozen():
    carrier=frozen_audio_carrier()
    assert carrier.status=="FROZEN"
    assert carrier.plate_width_mm==231.0
    assert carrier.plate_depth_mm==219.0
    assert carrier.pcb_origin_x_mm==5.5
    assert carrier.pcb_origin_y_mm==39.5

def test_sr040_board_outline_is_manufacturing_deterministic():
    outline=frozen_audio_board_outline()
    assert outline.status.value=="FROZEN"
    assert outline.outline.width_mm==220.0
    assert outline.outline.depth_mm==140.0
    assert len(outline.mounting_holes)==4
    assert [(h.centre.x_mm,h.centre.y_mm) for h in outline.mounting_holes]==[
        (5.0,8.0),(215.0,8.0),(215.0,132.0),(5.0,132.0)
    ]

def test_sr040_full_bom_census_covers_footprint_contract():
    census=build_full_bom_census()
    assert census.board_item_count>0
    assert census.footprint_count>0
    assert census.procurement_pending_count>0

def test_sr040_routing_gate_has_only_post_datum_review_actions():
    gate=build_sr040_routing_readiness()
    assert gate.mechanical_frozen
    assert gate.board_outline_frozen
    assert gate.mounting_hole_count==4
    assert gate.status=="MECHANICAL_FROZEN__CRITICAL_PLACEMENT_REVIEW_REQUIRED"
