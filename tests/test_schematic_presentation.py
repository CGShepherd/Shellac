from generator.core.sheet import Sheet
from generator.dispatch import shellac_builder_registry
from generator.hierarchy import child_hierarchical_ports
from generator.model.shellac import build_shellac_model


def _built_sheets():
    project = build_shellac_model()
    registry = shellac_builder_registry()
    for block in project.blocks:
        registration = registry.resolve(block.identifier)
        sheet = Sheet(registration.title, f"{block.identifier}.kicad_sch")
        registration.builder(sheet)
        child_hierarchical_ports(sheet, block)
        yield block.identifier, sheet


def test_physical_sheet_content_stays_clear_of_a3_title_block():
    offenders = []
    for block_id, sheet in _built_sheets():
        for component in sheet.components:
            if component.at.y > 255.0:
                offenders.append((block_id, component.ref, component.at.y))
    assert offenders == []


def test_mode_matrix_uses_only_orthogonal_signal_wires():
    sheet = dict(_built_sheets())["SCH105"]
    assert all(wire.x1 == wire.x2 or wire.y1 == wire.y2 for wire in sheet.wires)
