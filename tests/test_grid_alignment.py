from pathlib import Path

from generator.core.components import Component
from generator.core.geometry import Point
from generator.core.pins import pin_position
from generator.core.sheet import Sheet
from generator.writers.kicad9 import write_schematic


def test_serialized_symbol_and_wire_preserve_same_aligned_pin_coordinate(
    tmp_path: Path,
):
    sheet = Sheet("Alignment", "Alignment.kicad_sch")
    component = sheet.add_component(Component(
        "U1",
        "ProjectShellac:OpAmp_Buffer_Block",
        "BUFFER",
        Point(190.0, 95.0),
    ))
    pin = pin_position(component, "IN")
    sheet.connect_points(Point(125.0, pin.y), pin)

    out = tmp_path / "Alignment.kicad_sch"
    write_schematic(sheet, out)
    text = out.read_text(encoding="utf-8")

    # Sheet.add_component() is the canonical alignment boundary.  The writer
    # must preserve the already-aligned component origin and named-pin endpoint.
    assert component.at == Point(190.50, 95.25)
    assert pin == Point(179.07, 95.25)
    assert (
        f'(symbol (lib_id "ProjectShellac:OpAmp_Buffer_Block") '
        f'(at {component.at.x:.2f} {component.at.y:.2f} 0)'
    ) in text
    assert f'(xy {pin.x:.2f} {pin.y:.2f})' in text


def test_aligned_coordinate_serialization_is_deterministic(tmp_path: Path):
    def build(path: Path) -> bytes:
        sheet = Sheet("Alignment", "Alignment.kicad_sch")
        component = sheet.add_component(Component(
            "U1",
            "ProjectShellac:OpAmp_Buffer_Block",
            "BUFFER",
            Point(190.0, 95.0),
        ))
        pin = pin_position(component, "IN")
        sheet.connect_points(Point(125.0, pin.y), pin)
        write_schematic(sheet, path)
        return path.read_bytes()

    assert build(tmp_path / "one.kicad_sch") == build(tmp_path / "two.kicad_sch")
