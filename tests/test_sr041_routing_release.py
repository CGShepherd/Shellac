from pathlib import Path
import yaml
from generator.layout.sr041_routing_release import build_sr041_routing_release
def test_sr041_executable_is_historical_only_and_fail_closed():
 g=build_sr041_routing_release(); assert g.status=='HISTORICAL_SNAPSHOT_ONLY_DO_NOT_USE_FOR_CURRENT_RELEASE' and g.historical_status=='ROUTING_RELEASED' and g.base_commit=='56c74250507a2f4d4b4dc04641096c7883512740' and not g.current_authority and not g.current_routing_authorized and not g.observed_current_hold_final_routing and g.current_hold_authority=='AE-076D'
def test_sr041_immutable_snapshot_remains_historically_released():
 c=yaml.safe_load(Path('config/release/sr041_routing_release.yaml').read_text(encoding='utf-8')); assert c['status']=='ROUTING_RELEASED' and c['base_commit']=='56c74250507a2f4d4b4dc04641096c7883512740' and 'four_layer_stackup' in c['controlled_frozen_items']
def test_sr041_historical_routing_methods_are_provenance_only():
 g=build_sr041_routing_release(); assert g.routing_method['critical_analogue']=='MANUAL_ONLY' and not g.current_authority
