from pathlib import Path
from generator.blocks.power_entry import add_power_entry
from generator.core.geometry import Point
from generator.core.grid import align_coordinate
from generator.core.pins import pin_position
from generator.core.sheet import Sheet

def test_power_entry_contains_required_components_and_labels():
    sheet = Sheet(title="Power Entry Test", filename="PowerEntryTest.kicad_sch")
    add_power_entry(sheet)
    refs = {c.ref for c in sheet.components}
    labels = {l.name for l in sheet.labels}
    assert {"J901", "TP901", "TP902", "TP903", "TP904", "R909", "C909", "D901", "D902"}.issubset(refs)
    assert {"+18V", "-18V", "0VA", "CHASSIS"}.issubset(labels)

def test_ground_clamp_diodes_are_dnp_initially():
    sheet = Sheet(title="Power Entry Test", filename="PowerEntryTest.kicad_sch")
    add_power_entry(sheet)
    by_ref = {c.ref: c for c in sheet.components}
    assert by_ref["D901"].dnp is True
    assert by_ref["D902"].dnp is True
    assert by_ref["R909"].value == "0R"


def test_power_entry_emits_semantic_pin_connectivity():
    sheet = Sheet(title="Power Entry Test", filename="PowerEntryTest.kicad_sch")
    add_power_entry(sheet)
    assert len(sheet.wires) >= 70
    labels = {label.name for label in sheet.labels}
    assert {"+18VA_IN", "-18VA_IN", "+18V", "-18V", "0VA", "CHASSIS"}.issubset(labels)
    assert "NC_RESERVED" not in labels
    assert len(sheet.no_connects) == 1
    by_ref = {component.ref: component for component in sheet.components}
    assert by_ref["PWR901"].lib_id == "ProjectShellac:Power_Rail_Source"
    assert by_ref["PWR902"].lib_id == "ProjectShellac:Power_Rail_Source"


def test_power_entry_uses_continuous_visible_domain_rails():
    sheet = Sheet(title="Power Entry Test", filename="PowerEntryTest.kicad_sch")
    add_power_entry(sheet)
    endpoints = {
        frozenset(((wire.x1, wire.y1), (wire.x2, wire.y2)))
        for wire in sheet.wires
    }

    # Each post-entry domain reaches its hierarchy label through visible,
    # segmented conductors; the segments also expose intentional branch nodes
    # to the deterministic-junction writer.
    for requested_y in (60, 90, 120, 160):
        y = align_coordinate(requested_y)
        assert frozenset(((align_coordinate(340), y), (align_coordinate(365), y))) in endpoints

    by_ref = {component.ref: component for component in sheet.components}
    assert frozenset((
        (pin_position(by_ref["R901"], "2").x, align_coordinate(60)),
        (align_coordinate(120), align_coordinate(60)),
    )) in endpoints
    assert frozenset((
        (pin_position(by_ref["R902"], "2").x, align_coordinate(120)),
        (align_coordinate(120), align_coordinate(120)),
    )) in endpoints


def test_power_entry_bond_options_are_drawn_between_0va_and_chassis():
    sheet = Sheet(title="Power Entry Test", filename="PowerEntryTest.kicad_sch")
    add_power_entry(sheet)
    by_ref = {component.ref: component for component in sheet.components}

    expected_pins = {
        "R909": ("1", "2"),
        "C909": ("1", "2"),
        "D901": ("K", "A"),
        "D902": ("A", "K"),
    }
    endpoints = {
        frozenset(((wire.x1, wire.y1), (wire.x2, wire.y2)))
        for wire in sheet.wires
    }
    for ref, (upper_pin, lower_pin) in expected_pins.items():
        component = by_ref[ref]
        upper = pin_position(component, upper_pin)
        lower = pin_position(component, lower_pin)
        assert frozenset(((upper.x, align_coordinate(90)), (upper.x, upper.y))) in endpoints
        assert frozenset(((lower.x, lower.y), (lower.x, align_coordinate(160)))) in endpoints

    assert by_ref["R909"].value == "0R"
    assert by_ref["D901"].dnp is True
    assert by_ref["D902"].dnp is True


def test_psu_input_connector_is_passive_and_rail_flags_own_power_source_role(tmp_path: Path):
    from generator.blocks.power_entry import add_power_entry
    from generator.core.sheet import Sheet
    from generator.writers.kicad9 import write_schematic

    sheet = Sheet("SCH106", "SCH106.kicad_sch")
    add_power_entry(sheet)
    out = tmp_path / "SCH106.kicad_sch"
    write_schematic(sheet, out)
    text = out.read_text(encoding="utf-8")

    connector = text.split('(symbol "Connector_Generic:Conn_01x05"', 1)[1].split('(symbol "Connector_Generic:Conn_01x06"', 1)[0]
    assert connector.count('(pin passive line') == 5
    assert '(pin power_out line' not in connector
    assert '(symbol "ProjectShellac:Power_Rail_Source"' in text
