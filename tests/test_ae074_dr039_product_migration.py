from pathlib import Path

import yaml

from generator.blocks.replay_eq import add_replay_equalisation
from generator.blocks.rumble_filter import add_rumble_filter
from generator.core.sheet import Sheet
from generator.layout.footprint_contract import build_footprint_contract


ROOT = Path(__file__).resolve().parents[1]


def _refs(builder, name):
    sheet = Sheet(name, f"{name}.kicad_sch")
    builder(sheet)
    return {component.ref for component in sheet.components}


def test_ae074_moves_stable_dr039_identities_from_sch103_to_sch107():
    sch103 = _refs(add_replay_equalisation, "SCH103")
    sch107 = _refs(add_rumble_filter, "SCH107")
    moved = {"C30060", "R30060", "C35060", "R35060"}
    assert moved.isdisjoint(sch103)
    assert moved <= sch107


def test_ae074_footprint_contract_preserves_four_stable_physical_identities():
    contract = build_footprint_contract()
    by_ref = {entry.ref: entry for entry in contract.entries}
    moved = {"C30060", "R30060", "C35060", "R35060"}
    assert moved <= set(by_ref)
    assert all(by_ref[ref].sheet_id == "SCH107" for ref in moved)
    assert by_ref["C30060"].footprint == "Capacitor_THT:C_Rect_L7.2mm_W5.0mm_P5.00mm"
    assert by_ref["C35060"].footprint == "Capacitor_THT:C_Rect_L7.2mm_W5.0mm_P5.00mm"


def test_ae074_authority_records_native_board_reconciliation_but_keeps_qualification_gates_open():
    decisions = yaml.safe_load(
        (ROOT / "config/decisions/current_decision_index.yaml").read_text(encoding="utf-8")
    )
    dr039 = decisions["decisions"]["DR-039"]
    assert dr039["status"] == "CURRENT_ARCHITECTURE_QUALIFICATION_OPEN"
    assert "AE-074_DR039_Branch_Local_Product_Migration_Rev_A0.md" in "\n".join(
        dr039["evidence"]
    )

    hold = yaml.safe_load(
        (ROOT / "config/release/ae071_prerouting_hold.yaml").read_text(encoding="utf-8")
    )
    resolved = {item["id"]: item for item in hold["resolved_after_ae074"]}
    assert resolved["AE071-B02"]["resolution"] == (
        "AE074_NATIVE_PCB_F8_REFERENCE_RELINK_NET_AND_METADATA_RECONCILIATION_COMPLETE"
    )
    blockers = {item["id"] for item in hold["routing_blockers"]}
    assert "AE071-B02" not in blockers
    assert {"AE071-B03", "AE071-B04", "AE071-B06", "AE071-B08"} <= blockers
    assert "AE071-B05" not in blockers
    assert "AE071-B07" not in blockers
    resolved_ae075 = {item["id"]: item for item in hold["resolved_after_ae075"]}
    assert resolved_ae075["AE071-B07"]["native_validation"] == "PASS"
    assert hold["permissions"]["final_routing"] is False
    assert hold["permissions"]["layout_freeze"] is False
    assert hold["permissions"]["bom_freeze"] is False
    assert hold["permissions"]["manufacturing_release"] is False
