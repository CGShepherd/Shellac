from pathlib import Path
import yaml

from generator.mechanical.control_stack import (
    B03_STATUS, CONTROL_BOARD_OWNERSHIP, CARRIER_OR_CONTROL_PLANE_Z_MM,
    TOP_COVER_THICKNESS_MM, PARTS, validate_control_stack,
)
from generator.model.controls import CONTROLS, DESIGN_STATUS, ControlsStatus

ROOT=Path(__file__).resolve().parents[1]
HOLD=ROOT/"config/release/ae071_prerouting_hold.yaml"
BOM=ROOT/"config/bom/shellac_bom.yaml"
DECISIONS=ROOT/"config/decisions/current_decision_index.yaml"
AUTHORITY=ROOT/"config/decisions/document_authority.yaml"
GATE=ROOT/"generator/model/rotary_switch_procurement_gate.py"

def test_ae075c_exact_control_hardware_is_frozen():
    assert DESIGN_STATUS is ControlsStatus.PHYSICAL_HARDWARE_SELECTED
    assert [c.mpn for c in CONTROLS] == [
        "NR01105ANG13-2C","NR01105ANG13-2C",
        "NR01105ANG13-2A","NR01105ANG13-2A",
        "A30403RNCB","7201SYCBE","7201SYCBE",
    ]
    assert sum(p.quantity for p in PARTS)==7
    validate_control_stack()

def test_ae075c_live_rotary_gate_no_longer_encodes_lorlin():
    text=GATE.read_text(encoding="utf-8")
    assert "NKK NR01" in text
    assert "NR01105ANG13-2C" in text
    assert "NR01105ANG13-2A" in text
    assert "PT6004" not in text
    assert "Lorlin PT records remain provenance only" in text

def test_ae075c_record_captures_b03_vertical_stack_scope_without_premature_ownership():
    record=(ROOT/"docs/design_pack/AE-075C_Control_Hardware_and_Vertical_Stack_Reconciliation_Rev_A0.md").read_text(encoding="utf-8")
    assert "Freeze control-plane Z relative to the top cover" in record
    assert "Downselect direct-main-PCB versus REG-08 control-PCB ownership" in record
    assert "Create exact footprints/pin maps/courtyards/body envelopes" in record
    assert CARRIER_OR_CONTROL_PLANE_Z_MM is None
    assert TOP_COVER_THICKNESS_MM is None
    assert CONTROL_BOARD_OWNERSHIP.startswith("OPEN_")
    assert B03_STATUS.endswith("VERTICAL_STACK_AND_FOOTPRINTS_OPEN")

def test_ae075c_bom_exact_eq_variants_and_physical_gate():
    data=yaml.safe_load(BOM.read_text(encoding="utf-8"))
    bass=next(x for x in data["items"] if x["id"]=="BOM-CTRL-BASS")
    treble=next(x for x in data["items"] if x["id"]=="BOM-CTRL-TREBLE")
    assert bass["mpn"]=="NR01105ANG13-2C"
    assert treble["mpn"]=="NR01105ANG13-2A"
    assert bass["knob_colour"]=="red"
    assert treble["knob_colour"]=="black"
    assert bass["status"]==treble["status"]=="EXACT_PART_SELECTED_B03_PHYSICAL_IMPLEMENTATION_OPEN"
    assert bass["depth_behind_panel_mm"]==treble["depth_behind_panel_mm"]==10.5

def test_ae075c_authority_is_cross_registered_and_record_is_validated():
    decisions=yaml.safe_load(DECISIONS.read_text(encoding="utf-8"))
    authority=yaml.safe_load(AUTHORITY.read_text(encoding="utf-8"))
    rel="docs/design_pack/AE-075C_Control_Hardware_and_Vertical_Stack_Reconciliation_Rev_A0.md"
    assert decisions["pre_spice_assurance"]["AE-075C"]==rel
    assert rel in authority["pre_spice_assurance_evidence"]
    record=(ROOT/rel).read_text(encoding="utf-8")
    assert "**Status:** CLOSED — PRE-ROUTING DESIGN IMPLEMENTATION VALIDATED" in record
    assert "full regression suite: **689 passed**" in record
    assert "native hierarchical ERC: **0 violations**" in record

def test_ae075c_does_not_prematurely_claim_physical_pcb_ownership():
    source=(ROOT/"generator/blocks/controls.py").read_text(encoding="utf-8")
    assert "on_board=False" in source
    assert 'footprint=""' in source
