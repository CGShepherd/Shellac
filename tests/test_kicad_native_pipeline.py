from generator.layout.kicad_native_pipeline import (
    build_kicad_native_pipeline_baseline,
    validate_kicad_native_pipeline_baseline,
)


def test_kicad_native_pipeline_assigns_document_ownership_cleanly():
    baseline = build_kicad_native_pipeline_baseline()
    assert baseline.pcb_owner == "KiCad native document"
    assert baseline.intent_owner == "Project Shellac engineering model"
    assert baseline.manufacturing_holes_frozen is False
    assert validate_kicad_native_pipeline_baseline(baseline) == []


def test_kicad_native_pipeline_covers_all_preliminary_footprints():
    baseline = build_kicad_native_pipeline_baseline()
    assert baseline.footprint_count == 250
    assert baseline.accepted_count + baseline.review_count == 250
    assert len({item["reference"] for item in baseline.placement_items}) == 250


def test_kicad_native_pipeline_preserves_manual_review_boundary():
    baseline = build_kicad_native_pipeline_baseline()
    manual = [i for i in baseline.placement_items if not i["accepted"]]
    assert manual
    assert any("manual" in i["placement_authority"].lower() for i in manual)
