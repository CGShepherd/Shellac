from pathlib import Path
import yaml

from generator.blocks.balanced_input import add_sch101_rf_slice
from generator.core.sheet import Sheet
from generator.electrical_audit import audit_sheet_electrical
from generator.layout.footprint_contract import build_footprint_contract
from generator.layout.placement_clusters import build_cluster_placement_baseline
from generator.model.balanced_input import (
    AT_VM95SP,GAIN_SETTINGS,SERVICE_CAPACITANCE_PF,validate_balanced_input
)
from generator.writers.kicad9 import embedded_symbol_ids

ROOT=Path(__file__).resolve().parents[1]

def _sheet():
    s=Sheet(title="SCH101",filename="ProjectShellac_SCH101.kicad_sch")
    add_sch101_rf_slice(s)
    return s

def test_ae071a_product_migration_values_and_refs_are_live():
    validate_balanced_input()
    by_ref={c.ref:c for c in _sheet().components}
    assert [round(x.realised_total_db,4) for x in GAIN_SETTINGS] == [13.9737,18.0575,22.0145]
    assert SERVICE_CAPACITANCE_PF == {"BASE":0.0,"PLUS_47":47.0,"PLUS_100":100.0}
    assert AT_VM95SP.inductance_h == 0.55
    for old in ("R115","R116","R125","R126","R215","R216","R225","R226"):
        assert old not in by_ref

def test_service_header_symbol_and_footprint_support_is_embedded():
    ids=embedded_symbol_ids()
    assert "ProjectShellac:Service_Header_4Gang" in ids
    assert "ProjectShellac:Service_Header_2Gang" in ids
    text=(ROOT/"generator/writers/kicad9.py").read_text(encoding="utf-8")
    assert '"Connector_PinHeader_2.54mm"' in text

def test_population_remains_255_but_new_service_hardware_is_owned():
    contract=build_footprint_contract()
    assert len(contract.board_population_refs)==255
    population=set(contract.board_population_refs)
    assert {"H110","H111","H112","H120","H121","H122","C104","C204"} <= population
    assert not {"R115","R116","R125","R126","R215","R216","R225","R226"} & population
    owners={}
    for cluster in build_cluster_placement_baseline().clusters:
        for ref in cluster.member_refs:
            owners.setdefault(ref,[]).append(cluster.identifier)
    for ref in ("H110","H111","H112"):
        assert owners[ref]==["CLU-101-E"]
    for ref in ("H120","H121","H122"):
        assert owners[ref]==["CLU-101-F"]
    assert owners["C104"]==["CLU-101-A"]
    assert owners["C204"]==["CLU-101-C"]

def test_governance_closes_migration_but_not_routing():
    hold=yaml.safe_load((ROOT/"config/release/ae071_prerouting_hold.yaml").read_text(encoding="utf-8"))
    assert hold["authority"]=="AE-071A"
    assert {x["id"] for x in hold["resolved_after_ae071"]}=={"AE071-B01"}
    blockers={x["id"] for x in hold["routing_blockers"]}
    assert "AE071-B01" not in blockers
    assert "AE071-B02" in blockers
    assert "AE071-B08" in blockers
    assert hold["permissions"]["final_routing"] is False

def test_service_capacitors_do_not_short_programming_branches():
    audit = audit_sheet_electrical(_sheet())
    assert audit.net_name_conflicts == ()
    assert audit.unterminated_pins == ()
    assert audit.zero_length_wires == 0
    assert audit.passed


def test_sch101_internal_label_anchors_clear_kicad_multiwire_geometry():
    sheet = _sheet()
    offenders = []
    checked = 0
    for label in sheet.labels:
        if not label.name.startswith("SCH101_"):
            continue
        checked += 1
        point = (label.x, label.y)
        passing = []
        for index, wire in enumerate(sheet.wires):
            a = (wire.x1, wire.y1)
            b = (wire.x2, wire.y2)
            if point == a or point == b:
                continue
            if (
                min(wire.x1, wire.x2) <= label.x <= max(wire.x1, wire.x2)
                and min(wire.y1, wire.y2) <= label.y <= max(wire.y1, wire.y2)
            ):
                passing.append(index)
        if len(passing) > 1:
            offenders.append((label.name, point, tuple(passing)))
    assert checked > 0
    assert offenders == []


def test_dr039_product_generator_is_deliberately_untouched():
    replay=(ROOT/"generator/blocks/replay_eq.py").read_text(encoding="utf-8")
    assert "DR-039: common post-EQ DC block before SCH107 FILTER/BYPASS." in replay
