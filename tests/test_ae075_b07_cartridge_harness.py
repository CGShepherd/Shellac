from pathlib import Path

from generator.core.components import molex_microlock_plus_3
from generator.core.geometry import Point
from generator.layout.footprint_contract import build_footprint_contract, PopulationStatus

HOLD = Path("config/release/ae071_prerouting_hold.yaml")
BOM = Path("config/bom/shellac_bom.yaml")
BALANCED_INPUT = Path("generator/blocks/balanced_input.py")

def test_ae075_b07_exact_molex_set_is_encoded():
    c = molex_microlock_plus_3("H101", "L INPUT HARNESS", Point(0, 0))
    assert c.fields["PCB header"] == "5055780321"
    assert c.fields["Harness housing"] == "5055700301"
    assert c.fields["Harness terminal"] == "5055721200"
    assert c.fields["Pin 1"] == "CHASSIS/SHIELD"
    assert c.fields["Pin 2"] == "HOT/+"
    assert c.fields["Pin 3"] == "COLD/-"
    assert c.footprint == "ProjectShellac:Molex_MicroLockPlus_5055780321_1x03_P2.00mm_Horizontal"

def test_ae075_b07_live_sch101_uses_microlock_helper():
    text = BALANCED_INPUT.read_text(encoding="utf-8")
    assert "molex_microlock_plus_3" in text
    assert "jst_vh_3(" not in text

def test_ae075_b07_is_closed_in_footprint_contract():
    contract = build_footprint_contract()
    assert contract.status == "PRELIMINARY_READY"
    assert contract.mechanical_eco_refs == []
    entries = {e.ref: e for e in contract.entries}
    for ref in ("H101", "H201"):
        assert entries[ref].population_status is PopulationStatus.APPROVED
        assert entries[ref].footprint == "ProjectShellac:Molex_MicroLockPlus_5055780321_1x03_P2.00mm_Horizontal"

def test_ae075_b07_bom_and_hold_encode_closed_selected_hardware():
    bom = BOM.read_text(encoding="utf-8")
    for mpn in ("5055780321", "5055700301", "5055721200"):
        assert mpn in bom
    assert "SELECTED_IMPLEMENTED_NATIVE_VALIDATED" in bom
    hold = HOLD.read_text(encoding="utf-8")
    assert "resolved_after_ae075:" in hold
    assert "id: AE071-B07" in hold
    assert "native_validation: PASS" in hold
    routing = hold.split("routing_blockers:", 1)[1].split("pre_run08_prerequisites:", 1)[0]
    assert "AE071-B07" not in routing
    for blocker in ("AE071-B03", "AE071-B04", "AE071-B08"):
        assert blocker in routing
    assert "AE071-B05" not in routing
    assert "AE071-B06" not in routing


def test_ae075_b07_exact_part_footprint_geometry_is_controlled():
    fp = Path("generator/footprints/ProjectShellac.pretty/Molex_MicroLockPlus_5055780321_1x03_P2.00mm_Horizontal.kicad_mod")
    text = fp.read_text(encoding="utf-8")
    assert '(pad "1" smd rect (at -2.000001 -4.3791) (size 1.0414 2.5908)' in text
    assert '(pad "2" smd rect (at 0 -4.3791) (size 1.0414 2.5908)' in text
    assert '(pad "3" smd rect (at 2.000001 -4.3791) (size 1.0414 2.5908)' in text
    assert '(pad "4" smd rect (at -4.399999 -0.2291) (size 1.905 3.9116)' in text
    assert '(pad "5" smd rect (at 4.399999 -0.2291) (size 1.905 3.9116)' in text
    assert text.count("(zone (net 0)") == 3


def test_ae075_b07_generated_project_registers_local_footprint_library():
    writer = Path("generator/writers/kicad9.py").read_text(encoding="utf-8")
    assert "ProjectShellac.pretty" in writer
    c = molex_microlock_plus_3("H101", "L INPUT HARNESS", Point(0, 0))
    assert c.footprint == "ProjectShellac:Molex_MicroLockPlus_5055780321_1x03_P2.00mm_Horizontal"

def test_ae075_b07_native_board_carries_closed_microlock_implementation():
    board = Path("out/kicad/ProjectShellac.kicad_pcb").read_text(encoding="utf-8")
    fp = "ProjectShellac:Molex_MicroLockPlus_5055780321_1x03_P2.00mm_Horizontal"
    assert board.count(f'(footprint "{fp}"') == 2
    for ref, nets in {
        "H101": ("CHASSIS", "/INPUT_L_POS", "/INPUT_L_NEG"),
        "H201": ("CHASSIS", "/INPUT_R_POS", "/INPUT_R_NEG"),
    }.items():
        marker = f'(property "Reference" "{ref}"'
        pos = board.index(marker)
        start = board.rfind("(footprint ", 0, pos)
        end = board.find("\n\t(footprint ", pos)
        block = board[start:end if end >= 0 else len(board)]
        assert block.count("(keepout") == 3
        assert '(pad "4" smd rect' in block
        assert '(pad "5" smd rect' in block
        for net in nets:
            assert f'"{net}"' in block
