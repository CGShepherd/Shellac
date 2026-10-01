from pathlib import Path

import yaml

from generator.blocks.balanced_output import add_balanced_output
from generator.blocks.replay_eq import add_replay_equalisation
from generator.core.pins import pin_position
from generator.core.sheet import Sheet
from generator.dispatch import build_project_from_model, shellac_builder_registry
from generator.model.core import Direction
from generator.model.shellac import build_shellac_model
from generator.layout.footprint_contract import build_footprint_contract
from generator.layout.placement_clusters import build_cluster_placement_baseline

ROOT = Path(__file__).resolve().parents[1]
HOLD = ROOT / "config/release/ae071_prerouting_hold.yaml"
OLD_RELEASE = ROOT / "config/release/sr041_routing_release.yaml"
BOM = ROOT / "config/bom/shellac_bom.yaml"
DECISION_INDEX = ROOT / "config/decisions/current_decision_index.yaml"
DOCUMENT_AUTHORITY = ROOT / "config/decisions/document_authority.yaml"
DESIGN_PACK_INDEX = ROOT / "docs/knowledge/DESIGN_PACK_INDEX.md"
AE071_RECORD = ROOT / "docs/design_pack/AE-071_PreRouting_Integrity_Reconciliation_Rev_A0.md"
WRITER = ROOT / "generator/writers/kicad9.py"

def _connected_label_names(sheet, start):
    point = (start.x, start.y)
    adjacency = {}
    for wire in sheet.wires:
        a = (wire.x1, wire.y1); b = (wire.x2, wire.y2)
        adjacency.setdefault(a, set()).add(b)
        adjacency.setdefault(b, set()).add(a)
    labels_by_point = {}
    for label in sheet.labels:
        labels_by_point.setdefault((label.x, label.y), set()).add(label.name)
    seen = {point}; stack = [point]; labels = set()
    while stack:
        current = stack.pop()
        labels |= labels_by_point.get(current, set())
        for nxt in adjacency.get(current, ()):
            if nxt not in seen:
                seen.add(nxt); stack.append(nxt)
    return labels

def _sheet(builder, title, filename):
    sheet = Sheet(title=title, filename=filename); builder(sheet); return sheet

def test_sch103_negative_bulk_electrolytics_have_positive_terminal_at_0va():
    sheet = _sheet(add_replay_equalisation, "SCH103", "ProjectShellac_SCH103.kicad_sch")
    components = {component.ref: component for component in sheet.components}
    for ref in ("C30053", "C35053"):
        cap = components[ref]
        assert "Low-ESR electrolytic" in cap.fields["Dielectric"]
        assert "0VA" in _connected_label_names(sheet, pin_position(cap, "1"))
        assert "-17V" in _connected_label_names(sheet, pin_position(cap, "2"))

def test_sch108_negative_bulk_electrolytics_have_positive_terminal_at_0va():
    sheet = _sheet(add_balanced_output, "SCH108", "ProjectShellac_SCH108.kicad_sch")
    components = {component.ref: component for component in sheet.components}
    for ref in ("C80043", "C90043"):
        cap = components[ref]
        assert "Low-ESR electrolytic" in cap.fields["Dielectric"]
        assert "0VA" in _connected_label_names(sheet, pin_position(cap, "1"))
        assert "-17V" in _connected_label_names(sheet, pin_position(cap, "2"))

def test_generated_footprint_table_exposes_capacitor_tht():
    assert '"Capacitor_THT"' in WRITER.read_text(encoding="utf-8")

def test_lt5400_bom_no_longer_claims_nonexistent_a_grade_minus7():
    data = yaml.safe_load(BOM.read_text(encoding="utf-8"))
    item = next(x for x in data["items"] if x["id"] == "BOM-SCH101-LT5400")
    assert item["mpn"] == "LT5400BIMS8E-7#PBF"
    assert item["available_grade"] == "B"
    assert item["status"] == "EXACT_MPN_SELECTED_EP_IMPLEMENTED_RUN10_OPEN"
    assert item["candidate_mpns"] == ["LT5400BCMS8E-7#PBF", "LT5400BIMS8E-7#PBF"]
    assert item["exposed_pad"] == "QUIET_0VA"
    assert item["network_only_cmrr_floor_db"] == 84.44

def test_ae071_and_follow_on_resolutions_preserve_historical_release_provenance():
    hold = yaml.safe_load(HOLD.read_text(encoding="utf-8"))
    assert hold["historical_release"]["record"] == "config/release/sr041_routing_release.yaml"
    assert hold["historical_release"]["current_authority"] is False
    assert hold["resolved_after_ae071"][0]["id"] == "AE071-B01"
    assert hold["resolved_after_ae071a"] == [{
        "id": "AE071-M01",
        "item": "NATIVE_PCB_MOUNTING_HOLE_BOARD_ONLY_OWNERSHIP",
        "resolution": "AE071B_MH1_MH4_BOARD_ONLY_LOCKED_AND_BOM_POS_EXCLUDED",
    }]
    assert hold["resolved_after_ae074"] == [{
        "id": "AE071-B02",
        "item": "AE074_DR039_NATIVE_PCB_F8_RECONCILIATION_AND_NET_AUDIT",
        "resolution": "AE074_NATIVE_PCB_F8_REFERENCE_RELINK_NET_AND_METADATA_RECONCILIATION_COMPLETE",
    }]
    resolved_ae075 = {item["id"]: item for item in hold["resolved_after_ae075"]}
    assert set(resolved_ae075) == {"AE071-B07", "AE071-B05"}
    assert resolved_ae075["AE071-B07"]["native_validation"] == "PASS"
    assert resolved_ae075["AE071-B05"]["mpn"] == "ECEA1VN100U"
    assert hold["resolved_after_ae075b"][0]["id"] == "AE071-B06"

    historical = yaml.safe_load(OLD_RELEASE.read_text(encoding="utf-8"))
    assert historical["base_commit"] == "56c74250507a2f4d4b4dc04641096c7883512740"
    assert historical["status"] == "ROUTING_RELEASED"

def test_ae071_record_and_registration_remain_controlled_provenance():
    decisions = yaml.safe_load(DECISION_INDEX.read_text(encoding="utf-8"))
    ae071_rel = "docs/design_pack/AE-071_PreRouting_Integrity_Reconciliation_Rev_A0.md"
    assert decisions["pre_spice_assurance"]["AE-071"] == ae071_rel

    authority = yaml.safe_load(DOCUMENT_AUTHORITY.read_text(encoding="utf-8"))
    assert ae071_rel in authority["pre_spice_assurance_evidence"]

    index_text = DESIGN_PACK_INDEX.read_text(encoding="utf-8")
    assert "AE-071A migrates SCH101" in index_text
    assert "74 hierarchical pins / 23 cross-sheet signals" in index_text

    record_text = AE071_RECORD.read_text(encoding="utf-8")
    assert "BASS_L_SELECT" in record_text
    assert "MONO_R_LEG" in record_text
    assert "a103d9c34573f492" in record_text


def test_ae071_hold_records_hierarchy_and_placement_reconciliation_as_resolved():
    hold = yaml.safe_load(HOLD.read_text(encoding="utf-8"))
    resolved = set(hold["resolved_in_ae071"])
    assert {
        "ROOT_HIERARCHY_DUAL_MONO_CONTROL_AND_MONO_AVERAGING_CONNECTIVITY",
        "SCH101_LOCAL_BYPASS_PLACEMENT_AUTHORITY_RECONCILIATION",
    } <= resolved


def test_ae071_record_preserves_that1646_semantics_as_historical_nondecision():
    record_text = AE071_RECORD.read_text(encoding="utf-8")
    assert "correct the THAT1646 25-ohm-per-leg / 50-ohm-balanced model semantics" in record_text


def test_hierarchy_carries_dual_mono_controls_and_switched_mono_nodes():
    model = build_shellac_model()
    signal_names = {signal.name for signal in model.signals}
    memberships = {}
    for block in model.blocks:
        for interface in block.interfaces:
            memberships.setdefault(interface.signal, []).append(
                (block.identifier, interface.direction)
            )

    expected = {
        "BASS_L_SELECT": [("SCH103", Direction.INPUT), ("SCH109", Direction.OUTPUT)],
        "BASS_R_SELECT": [("SCH103", Direction.INPUT), ("SCH109", Direction.OUTPUT)],
        "TREBLE_L_SELECT": [("SCH103", Direction.INPUT), ("SCH109", Direction.OUTPUT)],
        "TREBLE_R_SELECT": [("SCH103", Direction.INPUT), ("SCH109", Direction.OUTPUT)],
        "MONO_AVG": [("SCH104", Direction.OUTPUT), ("SCH105", Direction.INPUT)],
        "MONO_R_LEG": [("SCH104", Direction.OUTPUT), ("SCH105", Direction.INPUT)],
    }
    for signal, expected_membership in expected.items():
        assert signal in signal_names
        assert memberships[signal] == expected_membership

    assert "BASS_SELECT" not in signal_names
    assert "TREBLE_SELECT" not in signal_names


def test_sch101_local_bypasses_are_current_board_population_and_cluster_owned():
    expected_left = {"C191", "C192", "C193", "C194"}
    expected_right = {"C291", "C292", "C293", "C294"}
    expected = expected_left | expected_right

    contract = build_footprint_contract()
    population = set(contract.board_population_refs)
    assert "complete 255-reference current PCB population" in AE071_RECORD.read_text(encoding="utf-8")
    assert expected <= population

    clusters = build_cluster_placement_baseline()
    owners = {}
    for cluster in clusters.clusters:
        for ref in cluster.member_refs:
            owners.setdefault(ref, []).append(cluster.identifier)

    assert {ref: owners.get(ref) for ref in sorted(expected_left)} == {
        ref: ["CLU-101-B"] for ref in sorted(expected_left)
    }
    assert {ref: owners.get(ref) for ref in sorted(expected_right)} == {
        ref: ["CLU-101-D"] for ref in sorted(expected_right)
    }


def test_six_previously_dangling_signals_render_as_real_hierarchy_connections(tmp_path):
    build_project_from_model(
        build_shellac_model(),
        shellac_builder_registry(),
        out_dir=tmp_path,
        project_name="ProjectShellac",
    )

    sch103 = (tmp_path / "ProjectShellac_SCH103.kicad_sch").read_text(encoding="utf-8")
    sch104 = (tmp_path / "ProjectShellac_SCH104.kicad_sch").read_text(encoding="utf-8")
    sch105 = (tmp_path / "ProjectShellac_SCH105.kicad_sch").read_text(encoding="utf-8")
    sch109 = (tmp_path / "ProjectShellac_SCH109.kicad_sch").read_text(encoding="utf-8")
    root = (tmp_path / "ProjectShellac.kicad_sch").read_text(encoding="utf-8")

    control_signals = (
        "BASS_L_SELECT", "BASS_R_SELECT",
        "TREBLE_L_SELECT", "TREBLE_R_SELECT",
    )
    mono_signals = ("MONO_AVG", "MONO_R_LEG")

    for signal in control_signals:
        assert f'(hierarchical_label "{signal}"' in sch103
        assert f'(hierarchical_label "{signal}"' in sch109
        assert f'(label "{signal}"' not in sch109
        assert root.count(f'(global_label "ROOT__{signal}"') == 2

    for signal in mono_signals:
        assert f'(hierarchical_label "{signal}"' in sch104
        assert f'(hierarchical_label "{signal}"' in sch105
        assert f'(label "{signal}"' not in sch104
        assert root.count(f'(global_label "ROOT__{signal}"') == 2
