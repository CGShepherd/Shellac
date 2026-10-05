from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
def test_delta_maps_current_conditions_without_rewriting_history():
 c=yaml.safe_load((ROOT/'config/decisions/ae076d_qualification_delta.yaml').read_text(encoding='utf-8')); assert c['authority']=='AE-076D' and c['parent_baseline']=='46bfd380193fc6008cdcb2f7ae8acece597f8f80' and c['historical_methodology']['records_immutable'] and not c['historical_methodology']['performance_criteria_relaxed']; r=c['current_conditions']['regulated_rails']; assert (r['plus_v'],r['zero_v'],r['minus_v'])==(17.0,0.0,-17.0); assert c['current_conditions']['primary_cartridge']['identity']=='Grado Prestige 78C'; s=c['current_conditions']['sch101_personality']['electrical_states']; assert (s['BASE']['added_differential_capacitance_pf'],s['PLUS_47']['added_differential_capacitance_pf'],s['PLUS_100']['added_differential_capacitance_pf'])==(0,47,100); assert c['qualification_interpretation']['ae076d_does_not_claim_any_run08_run14_execution']
def test_runs_and_release_remain_open_false():
 c=yaml.safe_load((ROOT/'config/decisions/ae076d_qualification_delta.yaml').read_text(encoding='utf-8')); assert set(c['remaining_campaign'])=={'RUN08','RUN09','RUN10','RUN11','RUN12','RUN13','RUN14','hardware_bench_correlation'} and not any(c['release'].values())
def test_live_hold_advances_fail_closed():
 h=yaml.safe_load((ROOT/'config/release/ae071_prerouting_hold.yaml').read_text(encoding='utf-8')); assert h['authority']=='AE-076D' and h['previous_authority']=='AE-076C' and h['baseline_commit']=='46bfd380193fc6008cdcb2f7ae8acece597f8f80'; assert h['final_design_assurance']['authority']=='AE-076D' and h['final_design_assurance']['status']=='OPEN_REQUIRED_BEFORE_FREEZE' and h['final_design_assurance']['independent_review_required']; assert not any(h['permissions'][k] for k in ('final_routing','layout_freeze','bom_freeze','manufacturing_release'))
def test_historical_release_records_keep_historical_values():
 a=yaml.safe_load((ROOT/'config/release/sr039_schematic_to_layout.yaml').read_text(encoding='utf-8'))
 b=yaml.safe_load((ROOT/'config/release/sr041_routing_release.yaml').read_text(encoding='utf-8'))
 c=yaml.safe_load((ROOT/'config/release/sr042_native_kicad_bootstrap.yaml').read_text(encoding='utf-8'))
 assert a['validated_design_commit']=='dce5c0ec36e12f979338d8c46106c44a79c7a023'
 assert b['status']=='ROUTING_RELEASED' and b['base_commit']=='56c74250507a2f4d4b4dc04641096c7883512740'
 assert c['status']=='READY_FOR_NATIVE_KICAD_BOARD_CREATION' and c['base_commit']=='47f7c01e639f85ebc28d77f7eb2d84718a8caf4b'
