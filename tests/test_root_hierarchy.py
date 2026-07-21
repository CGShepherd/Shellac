from pathlib import Path
import json
import re

from generator.dispatch import build_project_from_model, shellac_builder_registry
from generator.hierarchy import (
    GLOBAL_POWER_DOMAINS,
    deterministic_uuid,
    root_instance_path,
    sheet_instance_path,
    sheet_instance_uuid,
)
from generator.model.shellac import build_shellac_model


def _build(out_dir: Path) -> str:
    build_project_from_model(
        build_shellac_model(),
        shellac_builder_registry(),
        out_dir=out_dir,
        project_name="ProjectShellac",
    )
    return (out_dir / "ProjectShellac.kicad_sch").read_text(encoding="utf-8")


def test_uuid_derivation_is_stable_and_identity_sensitive():
    assert deterministic_uuid("sheet", "SCH101") == deterministic_uuid("sheet", "SCH101")
    assert deterministic_uuid("sheet", "SCH101") != deterministic_uuid("sheet", "SCH103")


def test_root_contains_all_sheet_instances_and_files(tmp_path: Path):
    text = _build(tmp_path)
    project = build_shellac_model()
    for block in project.blocks:
        assert f'(uuid "{sheet_instance_uuid("ProjectShellac", block.identifier)}")' in text
        assert f'ProjectShellac_{block.identifier}.kicad_sch' in text
    assert text.count(f'(path "{root_instance_path("ProjectShellac")}"') == 8
    assert text.count("  (sheet (at ") == 8


def test_root_sheet_instances_table_contains_only_the_root_page(tmp_path: Path):
    text = _build(tmp_path)
    table = text.split("  (sheet_instances", 1)[1]
    assert table.count('(path "/" (page "1"))') == 1
    assert "sheet-instance" not in table


def test_root_pins_cover_every_model_interface_and_labels_only_singletons(
    tmp_path: Path,
):
    text = _build(tmp_path)
    project = build_shellac_model()
    counts = {}
    for block in project.blocks:
        for interface in block.interfaces:
            if interface.signal in GLOBAL_POWER_DOMAINS:
                assert f'(pin "{interface.signal}" ' not in text
                continue
            assert f'(pin "{interface.signal}" ' in text
            counts[interface.signal] = counts.get(interface.signal, 0) + 1

    for signal, count in counts.items():
        if count == 1:
            assert text.count(f'(label "{signal}" ') == 1
        else:
            assert f'(label "{signal}" ' not in text


def test_child_sheets_contain_matching_hierarchical_labels(tmp_path: Path):
    _build(tmp_path)
    for block in build_shellac_model().blocks:
        child = (tmp_path / f"ProjectShellac_{block.identifier}.kicad_sch").read_text(
            encoding="utf-8"
        )
        for interface in block.interfaces:
            if interface.signal in GLOBAL_POWER_DOMAINS:
                assert f'(hierarchical_label "{interface.signal}" ' not in child
                assert f'(label "{interface.signal}" ' not in child
            else:
                assert f'(hierarchical_label "{interface.signal}" ' in child
        assert f'(path "{sheet_instance_path("ProjectShellac", block.identifier)}"' in child


def test_root_hierarchy_is_byte_deterministic(tmp_path: Path):
    first = _build(tmp_path / "one")
    second = _build(tmp_path / "two")
    assert first == second


def test_root_has_deterministic_wire_and_label_uuids(tmp_path: Path):
    text = _build(tmp_path)
    uuids = re.findall(r'\(uuid "([0-9a-f-]{36})"\)', text)
    assert len(uuids) == len(set(uuids))


def test_generated_project_contains_kicad_schematic_sections(tmp_path: Path):
    _build(tmp_path)
    project = json.loads((tmp_path / "ProjectShellac.kicad_pro").read_text(encoding="utf-8"))
    required = {
        "board", "boards", "cvpcb", "erc", "legacy", "libraries", "meta",
        "net_settings", "pcbnew", "schematic", "sheets", "text_variables",
    }
    assert required.issubset(project)


def test_generated_project_has_local_symbol_and_footprint_tables(tmp_path: Path):
    _build(tmp_path)
    symbol_table = (tmp_path / "sym-lib-table").read_text(encoding="utf-8")
    footprint_table = (tmp_path / "fp-lib-table").read_text(encoding="utf-8")
    custom_library = (tmp_path / "ProjectShellac.kicad_sym").read_text(encoding="utf-8")
    assert '${KIPRJMOD}/Device.kicad_sym' in symbol_table
    assert '${KIPRJMOD}/ProjectShellac.kicad_sym' in symbol_table
    assert '${KICAD9_FOOTPRINT_DIR}/Package_SO.pretty' in footprint_table
    assert '(symbol "OpAmp_NonInv_Block" ' in custom_library
    assert '(symbol "DIP_Switch_Block" ' in custom_library
    assert '(symbol "R" ' in (tmp_path / "Device.kicad_sym").read_text(encoding="utf-8")


def test_root_sheet_geometry_is_on_254_mm_grid(tmp_path: Path):
    text = _build(tmp_path)
    coordinates = re.findall(
        r'\(sheet \(at ([0-9.]+) ([0-9.]+)\) \(size ([0-9.]+) ([0-9.]+)\)',
        text,
    )
    assert len(coordinates) == 8
    for values in coordinates:
        for value in values:
            grid_units = float(value) / 2.54
            assert abs(grid_units - round(grid_units)) < 1e-9


def test_root_uses_one_stub_per_interface_and_global_labels_for_shared_signals(
    tmp_path: Path,
):
    text = _build(tmp_path)
    counts = {}
    for block in build_shellac_model().blocks:
        for interface in block.interfaces:
            if interface.signal not in GLOBAL_POWER_DOMAINS:
                counts[interface.signal] = counts.get(interface.signal, 0) + 1

    expected_wires = sum(counts.values())
    expected_local_labels = sum(1 for count in counts.values() if count == 1)
    expected_global_labels = sum(count for count in counts.values() if count > 1)

    assert text.count('  (wire (pts ') == expected_wires
    assert text.count('  (label "') == expected_local_labels
    assert text.count('  (global_label "') == expected_global_labels

    for signal, count in counts.items():
        if count == 1:
            assert text.count(f'(label "{signal}" ') == 1
            assert f'(global_label "{signal}" ' not in text
        else:
            root_name = f"ROOT__{signal}"
            assert text.count(f'(global_label "{root_name}" ') == count
            assert f'(global_label "{signal}" ' not in text
            assert f'(label "{signal}" ' not in text


def test_repeated_root_signals_use_global_labels_not_direct_wires(tmp_path: Path):
    text = _build(tmp_path)

    assert '(global_label "ROOT__+18V"' not in text
    assert '(global_label "ROOT__0VA"' not in text
    assert '(pin "+18V" ' not in text
    assert '(pin "0VA" ' not in text
    assert '(global_label "OUTPUT_L_POS"' not in text
    assert '(label "OUTPUT_L_POS"' in text
    assert 'root-net-wire' not in text



def test_power_domains_are_global_not_hierarchical_or_local(tmp_path: Path):
    _build(tmp_path)
    combined = ""
    for block in build_shellac_model().blocks:
        child = (tmp_path / f"ProjectShellac_{block.identifier}.kicad_sch").read_text(
            encoding="utf-8"
        )
        combined += child
        for signal in GLOBAL_POWER_DOMAINS:
            assert f'(hierarchical_label "{signal}" ' not in child
            assert f'(label "{signal}" ' not in child
    for signal in ("+18V", "-18V", "0VA"):
        assert f'(global_label "{signal}" ' in combined
