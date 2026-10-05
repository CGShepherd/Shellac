"""Historical SR-041 snapshot adapter, quarantined by AE-076D."""
from dataclasses import dataclass
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[2]; SNAPSHOT=ROOT/'config/release/sr041_routing_release.yaml'; HOLD=ROOT/'config/release/ae071_prerouting_hold.yaml'
@dataclass(frozen=True,slots=True)
class RoutingRelease:
 identifier:str; revision:str; status:str; historical_status:str; base_commit:str; current_authority:bool; current_routing_authorized:bool; current_hold_authority:str; observed_current_hold_final_routing:bool; controlled_frozen_items:tuple[str,...]; routing_method:dict[str,str]
def build_sr041_routing_release():
 s=yaml.safe_load(SNAPSHOT.read_text(encoding='utf-8')); h=yaml.safe_load(HOLD.read_text(encoding='utf-8'))
 return RoutingRelease(s['release_gate'],s['revision'],'HISTORICAL_SNAPSHOT_ONLY_DO_NOT_USE_FOR_CURRENT_RELEASE',s['status'],s['base_commit'],False,False,h['authority'],bool(h['permissions']['final_routing']),tuple(s['controlled_frozen_items']),dict(s['routing_method']))
