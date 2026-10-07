from pathlib import Path

import yaml

from generator.blocks.balanced_input import add_sch101_rf_slice
from generator.core.components import cartridge_personality_socket
from generator.core.geometry import Point
from generator.core.pins import pin_number
from generator.core.sheet import Sheet
from generator.writers.kicad9 import (
    PIN_COUNTS,
    embedded_symbol_ids,
    local_symbol_library,
    write_project_library_tables,
)

ROOT = Path(__file__).resolve().parents[1]
FOOTPRINT = (
    ROOT
    / "generator"
    / "footprints"
    / "ProjectShellac.pretty"
    / "Samtec_SLW-102-01-G-D_2x02_P2.54mm_Vertical.kicad_mod"
)


def _live_sch101():
    sheet = Sheet(title="SCH101", filename="ProjectShellac_SCH101.kicad_sch")
    add_sch101_rf_slice(sheet)
    return sheet


def test_exact_component_identity_is_controlled():
    c = cartridge_personality_socket("H120", "L LOAD PERSONALITY", Point(0, 0))
    assert c.lib_id == "ProjectShellac:Cartridge_Personality_Socket"
    assert c.footprint == (
        "ProjectShellac:Samtec_SLW-102-01-G-D_2x02_P2.54mm_Vertical"
    )
    assert c.fields["Manufacturer"] == "Samtec"
    assert c.fields["MPN"] == "SLW-102-01-G-D"
    assert c.fields["Mating header"] == "TSW-102-07-G-D"
    assert c.fields["No-card state"] == "BASE"
    assert "no series audio path" in c.fields["Signal-path ownership"]


def test_diagonal_duplicate_node_pin_contract_is_180_degree_benign():
    assert PIN_COUNTS["ProjectShellac:Cartridge_Personality_Socket"] == 4
    assert pin_number("ProjectShellac:Cartridge_Personality_Socket", "POS_A") == "1"
    assert pin_number("ProjectShellac:Cartridge_Personality_Socket", "NEG_A") == "2"
    assert pin_number("ProjectShellac:Cartridge_Personality_Socket", "NEG_B") == "3"
    assert pin_number("ProjectShellac:Cartridge_Personality_Socket", "POS_B") == "4"

    node = {1: "POS", 2: "NEG", 3: "NEG", 4: "POS"}
    rotated = {1: 4, 2: 3, 3: 2, 4: 1}
    assert all(node[pin] == node[mate] for pin, mate in rotated.items())


def test_symbol_is_self_contained_in_generated_project_library():
    assert "ProjectShellac:Cartridge_Personality_Socket" in embedded_symbol_ids()
    text = local_symbol_library()
    assert '(symbol "ProjectShellac:Cartridge_Personality_Socket"' in text
    for name in ("POS_A", "NEG_A", "NEG_B", "POS_B"):
        assert f'(name "{name}"' in text


def test_exact_slw_footprint_has_manufacturer_hole_and_numbering_geometry():
    text = FOOTPRINT.read_text(encoding="utf-8")
    assert "Samtec SLW-102-01-G-D" in text
    assert text.count('(pad "') == 4
    assert '(pad "1" thru_hole rect (at 0 0)' in text
    assert '(pad "2" thru_hole circle (at 0 2.54)' in text
    assert '(pad "3" thru_hole circle (at 2.54 0)' in text
    assert '(pad "4" thru_hole circle (at 2.54 2.54)' in text
    assert text.count("(drill 0.86)") == 4
    assert "(model " not in text


def test_project_library_export_copies_controlled_footprint(tmp_path):
    write_project_library_tables(tmp_path)
    copied = (
        tmp_path
        / "ProjectShellac.pretty"
        / "Samtec_SLW-102-01-G-D_2x02_P2.54mm_Vertical.kicad_mod"
    )
    assert copied.is_file()
    assert copied.read_bytes() == FOOTPRINT.read_bytes()


def test_ea_does_not_prematurely_migrate_live_sch101():
    refs = {c.ref for c in _live_sch101().components}
    assert {"H120", "H121", "H122", "C103", "C104", "C203", "C204"} <= refs
    assert "H220" not in refs


def test_ae076c_live_migration_and_release_remain_fail_closed():
    cfg = yaml.safe_load(
        (ROOT / "config/decisions/ae076c_cartridge_personality.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert cfg["status"] == "CURRENT_SELECTED_PENDING_IMPLEMENTATION"
    q = cfg["qualification"]
    assert q["live_sch101_generator_migration"] == "OPEN"
    assert not q["routing_authority"]
    assert not q["layout_freeze"]
    assert not q["bom_freeze"]
    assert not q["manufacturing_release"]
