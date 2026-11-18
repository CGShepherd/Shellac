"""S35B-P14: user-reported static switch evidence; NOT timing or footprint qualification."""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT/'config/decisions/current_spec_manifest.yaml'
REPORT = 'docs/design_pack/AE-076F7H_S35B_P14_TE_Matrix_Physical_Continuity_Rev_A0.md'

def test_p14_static_evidence_is_indexed_but_footprint_is_open():
    m = yaml.safe_load(MANIFEST.read_text(encoding='utf-8'))
    c = m['channel_matrix']
    assert c['physical_continuity_evidence'] == REPORT
    assert c['physical_continuity'] == 'USER_REPORTED_STATIC_SEQUENCE_AND_ISOLATION_PASS'
    assert c['physical_detent_throw_map_ccw_cw'] == [1,2,3,4]
    assert c['physical_common_banks'] == ['C1','C2','C3']
    assert c['physical_bbm_timing'] == 'MANUFACTURER_SPECIFIED_NOT_BENCH_MEASURED'
    assert c['control_pin_mapping'] == 'OPEN_BEFORE_FAB'
    assert (ROOT/REPORT).is_file()

def test_p14_never_opens_mcad_or_manufacturing_gates():
    m = yaml.safe_load(MANIFEST.read_text(encoding='utf-8'))
    assert m['assurance']['te_physical_continuity'] == 'STATIC_ACCEPTED_PAD_ORIENTATION_OPEN'
    assert m['assurance']['mcad_complete_seven_control_assembly'] == 'OPEN'
    assert m['channel_matrix']['dynamic_switching'] == 'RUN12_OPEN'
    assert m['next_engineering_transaction'] == 'TE_FOOTPRINT_15_PAD_ANTIMIRROR_AND_SEVEN_CONTROL_NATIVE_MCAD'
    hold = yaml.safe_load((ROOT/'config/release/ae071_prerouting_hold.yaml').read_text(encoding='utf-8'))
    for x in ('final_routing','layout_freeze','bom_freeze','manufacturing_release'):
        assert m['system_invariants'][x] is False
        assert hold['permissions'][x] is False
