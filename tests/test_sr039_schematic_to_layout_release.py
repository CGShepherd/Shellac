from pathlib import Path
import yaml
from generator.layout.schematic_release_gate import build_schematic_to_layout_release_gate
def test_sr039_executable_is_historical_snapshot_not_current_release():
 g=build_schematic_to_layout_release_gate(); assert g.status=='HISTORICAL_SNAPSHOT_ONLY_DO_NOT_USE_FOR_CURRENT_RELEASE' and g.validated_design_commit=='dce5c0ec36e12f979338d8c46106c44a79c7a023'; assert g.historical_disposition.schematic_release=='RELEASED' and g.historical_disposition.routing_release=='BLOCKED_PENDING_MECHANICAL_DATUM_FREEZE'; assert not g.current_authority and not g.current_routing_authorized and not g.observed_current_hold_final_routing and g.current_hold_authority=='AE-076D'
def test_sr039_controlled_historical_validation_evidence():
 c=yaml.safe_load(Path('config/release/sr039_schematic_to_layout.yaml').read_text(encoding='utf-8')); assert c['validation']['pytest']=={'passed':374,'failed':0} and c['validation']['native_kicad_erc']['errors']==0 and c['validation']['native_kicad_erc']['warnings']==0
def test_sr039_historical_and_current_dr038_dr039_are_separated():
 g=build_schematic_to_layout_release_gate(); assert not g.current_authority; d38=Path('docs/decisions/DR-038_SCH101_Precision_Architecture_SELECTED.md').read_text(encoding='utf-8'); assert '**Historical implementation closure:** SR-039' in d38 and 'selected-next' in d38.lower(); d39=Path('docs/decisions/DR-039_Branch_Local_DC_Block_SELECTED.md').read_text(encoding='utf-8'); assert 'CURRENT_ARCHITECTURE_QUALIFICATION_OPEN' in d39 and 'BRANCH_LOCAL_DIRECT_BYPASS_BLOCK' in d39
def test_current_layout_contract_retains_critical_manual_nets():
 from generator.layout.constraints import build_layout_baseline
 ids={x.identifier for x in build_layout_baseline().critical_nets}; assert {'NET-011','NET-012','NET-013'}<=ids
