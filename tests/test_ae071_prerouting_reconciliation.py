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
        assert "-18V" in _connected_label_names(sheet, pin_position(cap, "2"))

def test_sch108_negative_bulk_electrolytics_have_positive_terminal_at_0va():
    sheet = _sheet(add_balanced_output, "SCH108", "ProjectShellac_SCH108.kicad_sch")
    components = {component.ref: component for component in sheet.components}
    for ref in ("C80043", "C90043"):
        cap = components[ref]
        assert "Low-ESR electrolytic" in cap.fields["Dielectric"]
        assert "0VA" in _connected_label_names(sheet, pin_position(cap, "1"))
        assert "-18V" in _connected_label_names(sheet, pin_position(cap, "2"))

def test_generated_footprint_table_exposes_capacitor_tht():
    assert '"Capacitor_THT"' in WRITER.read_text(encoding="utf-8")

def test_lt5400_bom_no_longer_claims_nonexistent_a_grade_minus7():
    data = yaml.safe_load(BOM.read_text(encoding="utf-8"))
    item = next(x for x in data["items"] if x["id"] == "BOM-SCH101-LT5400")
    assert item["mpn"] == "OPEN_B_GRADE_-7"
    assert item["available_grade"] == "B"
    assert item["status"] == "GRADE_RATIO_SELECTED_RUN10_AND_EXACT_MPN_OPEN"
    assert item["candidate_mpns"] == ["LT5400BCMS8E-7#PBF", "LT5400BIMS8E-7#PBF"]

def test_current_routing_authority_is_fail_closed_and_sr041_is_historical():
    hold = yaml.safe_load(HOLD.read_text(encoding="utf-8"))
    assert hold["authority"] == "AE-071"
    assert hold["baseline_commit"] == "67b2101474bc1db10deb7784a0cc7131ed20e2ef"
    assert hold["status"] == "ROUTING_HELD_PENDING_PRODUCT_RECONCILIATION"
    assert hold["historical_release"]["record"] == "config/release/sr041_routing_release.yaml"
    assert hold["historical_release"]["current_authority"] is False
    assert hold["permissions"]["final_routing"] is False
    assert hold["permissions"]["layout_freeze"] is False
    assert hold["permissions"]["bom_freeze"] is False
    assert hold["permissions"]["manufacturing_release"] is False
    assert hold["final_design_assurance"]["authority"] == "AE-072_PENDING"
    assert {x["id"] for x in hold["routing_blockers"]} == {
        "AE071-B01","AE071-B02","AE071-B03","AE071-B04",
        "AE071-B05","AE071-B06","AE071-B07",
    }
    historical = yaml.safe_load(OLD_RELEASE.read_text(encoding="utf-8"))
    assert historical["base_commit"] == "56c74250507a2f4d4b4dc04641096c7883512740"
    assert historical["status"] == "ROUTING_RELEASED"

def test_ae071_is_registered_in_current_authority_and_dr038_uses_b_grade_identity():
    decisions = yaml.safe_load(DECISION_INDEX.read_text(encoding="utf-8"))
    dr038 = decisions["decisions"]["DR-038"]
    assert "B-grade procurement candidate" in dr038["implementation"]["network"]
    assert "A-grade -7 procurement identity" in dr038["implementation"]["note"]
    assert (
        "docs/design_pack/AE-071_PreRouting_Integrity_Reconciliation_Rev_A0.md"
        in dr038["evidence"]
    )
    assert decisions["pre_spice_assurance"]["AE-071"] == (
        "docs/design_pack/AE-071_PreRouting_Integrity_Reconciliation_Rev_A0.md"
    )

    authority = yaml.safe_load(DOCUMENT_AUTHORITY.read_text(encoding="utf-8"))
    assert (
        "docs/design_pack/AE-071_PreRouting_Integrity_Reconciliation_Rev_A0.md"
        in authority["pre_spice_assurance_evidence"]
    )

    index_text = DESIGN_PACK_INDEX.read_text(encoding="utf-8")
    assert "AE-042 through AE-071" in index_text
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


def test_that1646_output_impedance_semantics_are_explicitly_pre_run08_open():
    hold = yaml.safe_load(HOLD.read_text(encoding="utf-8"))
    assert hold["pre_run08_prerequisites"] == [{
        "id":"AE071-S01",
        "item":"THAT1646_OUTPUT_IMPEDANCE_MODEL_SEMANTICS_25OHM_PER_LEG_50OHM_BALANCED",
        "status":"OPEN",
    }]


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
    assert len(contract.board_population_refs) == 255
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
