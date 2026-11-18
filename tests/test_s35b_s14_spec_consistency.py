"""S35B-S14: selected-next source/status consistency, NOT physical acceptance."""
from pathlib import Path
import yaml
from generator.model import mode_matrix
from generator.model.controls import CONTROLS

ROOT = Path(__file__).resolve().parents[1]

def read_yaml(rel):
    return yaml.safe_load((ROOT / rel).read_text(encoding='utf-8'))

SPEC = 'docs/specifications/SHELLAC_CURRENT_TECHNICAL_SPEC_Rev_A0.md'
MANIFEST = 'config/decisions/current_spec_manifest.yaml'

def test_spec_is_indexed_and_previous_mechanical_candidate_superseded():
    m = read_yaml(MANIFEST)
    idx = read_yaml('config/decisions/current_decision_index.yaml')['decisions']
    doc = read_yaml('config/decisions/document_authority.yaml')
    assert m['record'] == 'S35B-S14'
    assert m['specification'] == SPEC
    assert idx['AE-076F7H-S14']['primary_record'] == SPEC
    assert idx['AE-076F7H-S14']['status'] == 'CURRENT_SELECTED_PENDING_IMPLEMENTATION'
    assert idx['AE-076F4T']['status'] == 'SUPERSEDED'
    assert idx['AE-076F4T']['superseded_by'] == 'AE-076F7H-S14'
    assert SPEC in doc['current_authority']
    assert MANIFEST in doc['current_authority']
    assert 'docs/design_pack/AE-076F4T_Switch_Mounting_Selection_Rev_A0.md' in doc['historical_state_evidence']
    assert (ROOT / SPEC).is_file()

def test_current_matrix_identity_and_truth_table_are_consistent():
    m = read_yaml(MANIFEST)
    cm = m['channel_matrix']
    assert cm['selected_mpn'] == 'MRJE3404'
    assert cm['te_order_number'] == '1825537-3'
    assert (cm['poles'], cm['positions']) == (3, 4)
    assert cm['operator_order_ccw_cw'] == ['DUAL_L', 'STEREO', 'L_PLUS_R', 'DUAL_R']
    assert cm['control_pin_mapping'] == 'OPEN_BEFORE_FAB'
    assert cm['physical_continuity'] == 'USER_REPORTED_STATIC_SEQUENCE_AND_ISOLATION_PASS'
    assert mode_matrix.SWITCH_PREFERRED_MPN == cm['selected_mpn']
    assert '3P4T' in mode_matrix.SWITCH_TYPE
    assert [p.mono_right_leg_connected for p in mode_matrix.MODE_TABLE] == [False, False, True, False]
    idx = read_yaml('config/decisions/current_decision_index.yaml')['decisions']
    assert idx['AE-076F4C']['selected_mpn'] == cm['selected_mpn']
    bom = read_yaml('config/bom/shellac_bom.yaml')
    channel = next(x for x in bom['items'] if x['id']=='BOM-CTRL-CHANNEL')
    assert channel['mpn'] == cm['selected_mpn']

def test_implemented_vs_selected_next_mute_rumble_are_explicitly_different():
    m = read_yaml(MANIFEST)
    assert m['baseline']['implemented_mute_rumble_mpn_in_generator_and_bom'] == '7201SYCBE'
    assert m['mechanical_selected_next']['mute_rumble_mpn'] == 'UB226SKG03N-5C'
    assert m['mechanical_selected_next']['ub2_mount'] == 'DIRECT_PCB_NO_RAISER'
    assert m['mechanical_selected_next']['pcb_supports']['height_mm_nominal'] == 16.0
    assert m['mechanical_selected_next']['main_pcb']['implemented'] is False
    assert m['mechanical_selected_next']['pcb_supports']['height_frozen'] is False
    assert m['mechanical_selected_next']['h802_candidate_implemented'] is False
    assert all(x.mpn == '7201SYCBE' for x in CONTROLS[-2:])
    bom = read_yaml('config/bom/shellac_bom.yaml')
    for k in ('BOM-CTRL-MUTE','BOM-CTRL-RUMBLE'):
        assert next(x['mpn'] for x in bom['items'] if x['id'] == k) == '7201SYCBE'
    hold = read_yaml('config/release/ae071_prerouting_hold.yaml')
    assert hold['routing_blockers'][0]['id'] == 'AE071-B03'
    assert hold['routing_blockers'][0]['aluminium_carrier_selected'] is False

def test_never_relabel_open_release_and_validation_gates_as_passed():
    m = read_yaml(MANIFEST)
    permissions = read_yaml('config/release/ae071_prerouting_hold.yaml')['permissions']
    for gate in ('final_routing','layout_freeze','bom_freeze','manufacturing_release'):
        assert m['system_invariants'][gate] is False
        assert permissions[gate] is False
    assert m['assurance']['mcad_complete_seven_control_assembly'] == 'OPEN'
    assert m['assurance']['te_physical_continuity'] == 'STATIC_ACCEPTED_PAD_ORIENTATION_OPEN'
    assert m['channel_matrix']['dynamic_switching'] == 'RUN12_OPEN'
    spec_text = (ROOT / SPEC).read_text(encoding='utf-8')
    assert 'NOT FOR FABRICATION' in spec_text
    assert 'No complete seven-control installed 3D qualification has passed.' in spec_text
    assert m['next_engineering_transaction'] == 'TE_FOOTPRINT_15_PAD_ANTIMIRROR_AND_SEVEN_CONTROL_NATIVE_MCAD'
