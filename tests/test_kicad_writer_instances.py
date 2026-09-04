from pathlib import Path

from generator.core.components import resistor, capacitor, xlr3
from generator.core.geometry import Point
from generator.core.sheet import Sheet
from generator.writers.kicad9 import deterministic_uuid, write_schematic


def test_generated_symbols_have_instance_references(tmp_path: Path):
    sheet = Sheet(title="Reference Test", filename="ReferenceTest.kicad_sch")
    sheet.add_component(resistor("R102", "100R", Point(20, 20)))
    sheet.add_component(capacitor("C101", "1n", Point(30, 20)))
    sheet.add_component(xlr3("J101", "INPUT XLR", Point(10, 20)))

    output = tmp_path / "ReferenceTest.kicad_sch"
    write_schematic(sheet, output)
    text = output.read_text(encoding="utf-8")

    assert '(reference "R102")' in text
    assert '(reference "C101")' in text
    assert '(reference "J101")' in text
    assert '(reference "R?")' not in text
    assert '(reference "C?")' not in text
    assert '(reference "J?")' not in text


def test_instance_path_uses_root_schematic_uuid(tmp_path: Path):
    sheet = Sheet(title="UUID Test", filename="UUIDTest.kicad_sch")
    sheet.add_component(resistor("R1", "1k", Point(20, 20)))

    output = tmp_path / "UUIDTest.kicad_sch"
    write_schematic(sheet, output)
    text = output.read_text(encoding="utf-8")

    marker = '(uuid "'
    start = text.index(marker) + len(marker)
    end = text.index('"', start)
    root_uuid = text[start:end]

    assert f'(path "/{root_uuid}"' in text


def test_hierarchical_child_also_carries_standalone_instance_references(tmp_path: Path):
    """A child sheet must remain annotated when opened outside the hierarchy."""
    sheet = Sheet(title="Child Test", filename="ChildTest.kicad_sch")
    sheet.add_component(resistor("R42", "4k7", Point(20, 20)))

    output = tmp_path / "ChildTest.kicad_sch"
    hierarchy_path = "/root-uuid/sheet-uuid"
    write_schematic(sheet, output, instance_path=hierarchy_path)
    text = output.read_text(encoding="utf-8")
    standalone_path = f'/{deterministic_uuid("schematic-file", sheet.filename)}'

    assert f'(path "{hierarchy_path}"' in text
    assert f'(path "{standalone_path}"' in text
    assert text.count('(reference "R42")') == 2
    assert '(reference "R?")' not in text


def test_identical_schematic_input_produces_byte_identical_output(tmp_path: Path):
    sheet = Sheet(title="Determinism Test", filename="DeterminismTest.kicad_sch")
    sheet.add_component(resistor("R1", "1k", Point(20, 20)))
    sheet.add_component(capacitor("C1", "100n", Point(30, 20)))
    output = tmp_path / "DeterminismTest.kicad_sch"

    write_schematic(sheet, output)
    first = output.read_bytes()
    write_schematic(sheet, output)

    assert output.read_bytes() == first



def test_writer_embeds_dip_switch_symbol():
    from generator.writers.kicad9 import embedded_custom_symbol_ids, local_symbol_library
    assert "ProjectShellac:DIP_Switch_Block" in embedded_custom_symbol_ids()
    assert 'symbol "ProjectShellac:DIP_Switch_Block"' in local_symbol_library()


def test_writer_embeds_panel_control_and_led_symbols():
    from generator.writers.kicad9 import embedded_custom_symbol_ids,local_symbol_library
    e=embedded_custom_symbol_ids(); assert "ProjectShellac:Panel_Control_Block" in e; assert "ProjectShellac:Panel_LED_Block" in e
    l=local_symbol_library(); assert 'symbol "ProjectShellac:Panel_Control_Block"' in l; assert 'symbol "ProjectShellac:Panel_LED_Block"' in l


def test_writer_embeds_every_standard_symbol_used_by_shellac():
    from generator.writers.kicad9 import embedded_standard_symbol_ids, local_symbol_library
    expected = {
        "Device:R", "Device:C", "Device:D", "Device:Ferrite_Bead",
        "Connector_Generic:Conn_01x03", "Connector_Generic:Conn_01x05",
        "Connector_Generic:Conn_01x06",
    }
    assert embedded_standard_symbol_ids() == expected
    library = local_symbol_library()
    for symbol_id in expected:
        assert f'symbol "{symbol_id}"' in library


def test_real_opamp_symbols_have_no_synthetic_ground_pin():
    from generator.writers.kicad9 import local_symbol_library
    library = local_symbol_library()
    start=library.index('symbol "ProjectShellac:OpAmp_Buffer_Block"')
    end=library.index('symbol "ProjectShellac:TestPoint"',start)
    buffer=library[start:end]
    assert '(name "IN-"' in buffer
    assert '(name "0VA"' not in buffer
    assert '(number "8"' in buffer
    assert '(number "4"' in buffer
    assert '(pin passive line (at -5.08 12.70 270) (length 2.54) (name "GND"' in library
