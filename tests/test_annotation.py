import pytest

from generator.annotation import duplicate_references, invalid_references, validate_unique_references
from generator.core.components import resistor
from generator.core.geometry import Point
from generator.core.sheet import Sheet
from generator.dispatch import shellac_builder_registry
from generator.model.shellac import build_shellac_model


def _project_sheets():
    project = build_shellac_model()
    registry = shellac_builder_registry()
    result = []
    for block in project.blocks:
        sheet = Sheet(block.name, f"{block.identifier}.kicad_sch")
        registry.resolve(block.identifier).builder(sheet)
        result.append((block.identifier, sheet))
    return result


def test_all_generated_references_are_project_unique():
    sheets = _project_sheets()
    assert duplicate_references(sheets) == {}
    assert invalid_references(sheets) == {}
    validate_unique_references(sheets)


def test_duplicate_reference_validation_reports_both_owners():
    left = Sheet("left", "left.kicad_sch")
    right = Sheet("right", "right.kicad_sch")
    left.add_component(resistor("R1", "1k", Point(0, 0)))
    right.add_component(resistor("R1", "2k", Point(0, 0)))
    duplicates = duplicate_references((("A", left), ("B", right)))
    assert duplicates == {"R1": ("A", "B")}
    with pytest.raises(ValueError, match="R1: A, B"):
        validate_unique_references((("A", left), ("B", right)))


def test_non_numeric_suffix_is_rejected_as_unannotated():
    sheet = Sheet("bad", "bad.kicad_sch")
    sheet.add_component(resistor("R1A", "1k", Point(0, 0)))
    assert invalid_references((("SCHX", sheet),)) == {"R1A": "SCHX"}
    with pytest.raises(ValueError, match="R1A: SCHX"):
        validate_unique_references((("SCHX", sheet),))
