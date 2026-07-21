from generator.core.grid import is_aligned_point
from generator.core.sheet import Sheet
from generator.dispatch import shellac_builder_registry
from generator.electrical_audit import audit_sheet_electrical
from generator.model.shellac import build_shellac_model


def _audits():
    registry = shellac_builder_registry()
    results = {}
    for block in build_shellac_model().blocks:
        sheet = Sheet(block.name, f"{block.identifier}.kicad_sch")
        registry.resolve(block.identifier).builder(sheet)
        results[block.identifier] = audit_sheet_electrical(sheet)
    return results


def test_every_block_passes_internal_electrical_integrity_gate():
    failures = {
        block_id: audit
        for block_id, audit in _audits().items()
        if not audit.passed
    }
    assert failures == {}


def test_canonical_grid_is_applied_before_serialisation():
    registry = shellac_builder_registry()
    for block in build_shellac_model().blocks:
        sheet = Sheet(block.name, f"{block.identifier}.kicad_sch")
        registry.resolve(block.identifier).builder(sheet)
        assert all(is_aligned_point(component.at) for component in sheet.components)
        assert all(
            is_aligned_point(type(component.at)(wire.x1, wire.y1))
            and is_aligned_point(type(component.at)(wire.x2, wire.y2))
            for component in sheet.components[:1]
            for wire in sheet.wires
        )
