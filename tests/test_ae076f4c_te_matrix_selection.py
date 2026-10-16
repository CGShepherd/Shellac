"""AE-076F4C: matrix identity migrated; holds and historical evidence retained."""
from pathlib import Path
import yaml
from generator.model.control_architecture import MATRIX
from generator.model.controls import CONTROLS, MATRIX_MPN, MATRIX_FALLBACK_MPN
from generator.mechanical.control_hardware import (
    CK_A30403RNCB, CURRENT_ROTARY_EVIDENCE, TE_MRJE3404, ROTARY_PLATFORM_AUTHORITY
)
from generator.mechanical.control_stack import PARTS
from generator.mechanical.top_cover_stack import TE_MATRIX_STACK

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))

def test_f4c_selected_matrix_is_coherent_in_all_live_models():
    assert MATRIX.mpn == MATRIX_MPN == CONTROLS[4].mpn == "MRJE3404"
    assert MATRIX.fallback_mpn is MATRIX_FALLBACK_MPN is None
    assert PARTS[2].mpn == TE_MATRIX_STACK.mpn == "MRJE3404"
    assert TE_MRJE3404 in CURRENT_ROTARY_EVIDENCE
    assert CK_A30403RNCB not in CURRENT_ROTARY_EVIDENCE
    assert ROTARY_PLATFORM_AUTHORITY["matrix_mpn"] == "MRJE3404"
    assert all(c.mpn == "7201SYCBE" for c in CONTROLS[-2:])

def test_f4c_no_unintended_release_or_native_change():
    idx = load("config/decisions/current_decision_index.yaml")
    f4c = idx["decisions"]["AE-076F4C"]
    assert f4c["status"] == "CURRENT_SELECTED_PENDING_IMPLEMENTATION"
    assert f4c["selected_mpn"] == "MRJE3404"
    assert f4c["fallback"] == "NONE_SELECTED"
    assert f4c["manufacturing_release"] is False
    bom = load("config/bom/shellac_bom.yaml")
    matrix = next(x for x in bom["items"] if x["id"] == "BOM-CTRL-CHANNEL")
    assert matrix["mpn"] == "MRJE3404"
    assert matrix["knob_mpn"] == "OPEN"
    hold = load("config/release/ae071_prerouting_hold.yaml")
    b03 = next(x for x in hold["routing_blockers"] if x["id"] == "AE071-B03")
    assert b03["exact_parts"]["channel"] == "TE_MRJE3404_1825537_3_QTY1"
    assert hold["permissions"] == {"analysis_and_nonbinding_placement_work":True,
        "final_routing":False,"layout_freeze":False,"bom_freeze":False,"manufacturing_release":False}
    mech = load("config/mechanical/ae076b_control_service_module.yaml")
    assert mech["selected_architecture"]["aluminium_carrier"] == "NOT_SELECTED"
    assert mech["permissions"]["native_pcb_mechanical_migration"] is False

def test_f4w_sch105_live_generator_identity_no_historical_fallback():
    from generator.model.mode_matrix import (
        SWITCH_TYPE, SWITCH_PREFERRED_MPN, SWITCH_FALLBACK_MPN,
    )
    from generator.blocks.mode_matrix import _mode_switch
    from generator.core.geometry import Point

    assert SWITCH_TYPE == "TE/Alcoswitch MRJE3404 3P4T break-before-make"
    assert SWITCH_PREFERRED_MPN == "MRJE3404"
    assert SWITCH_FALLBACK_MPN is None
    sw = _mode_switch("SW501", Point(215.0, 150.0))
    assert sw.value == "MODE 3P4T — MRJE3404"
    assert sw.fields["Type"] == SWITCH_TYPE
    # No phantom physical switch is allowed before the numbered-pin migration.
    assert sw.on_board is False
    assert sw.footprint == ""
