"""Historical SR-042 native-KiCad bootstrap snapshot adapter, quarantined by AE-076D.

The immutable SR-042 YAML records readiness at its own historical baseline. This
adapter cannot grant current routing/native-creation authority and cannot
regenerate historical bootstrap artefacts from the mutable current design.
"""
from dataclasses import asdict, dataclass
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[2]
SNAPSHOT=ROOT/'config/release/sr042_native_kicad_bootstrap.yaml'
HOLD=ROOT/'config/release/ae071_prerouting_hold.yaml'
@dataclass(frozen=True,slots=True)
class NativeRoutingBootstrap:
    identifier:str
    revision:str
    status:str
    historical_status:str
    base_commit:str
    current_authority:bool
    current_routing_authorized:bool
    current_hold_authority:str
    observed_current_hold_final_routing:bool
    source_schematic:str
    target_board:str
    reference_board:str
    placement_count:int
    mounting_hole_count:int
    critical_manual_net_count:int
    native_board_owner:str
    def to_dict(self): return asdict(self)
def build_native_routing_bootstrap():
    s=yaml.safe_load(SNAPSHOT.read_text(encoding='utf-8'))
    h=yaml.safe_load(HOLD.read_text(encoding='utf-8'))
    return NativeRoutingBootstrap(
        s['release_gate'],s['revision'],'HISTORICAL_SNAPSHOT_ONLY_DO_NOT_USE_FOR_CURRENT_RELEASE',
        s['status'],s['base_commit'],False,False,h['authority'],bool(h['permissions']['final_routing']),
        s['source_schematic'],s['target_native_board'],s['reference_board'],int(s['placement_count']),
        int(s['mounting_hole_count']),int(s['manual_critical_net_count']),s['native_board_owner'])
def write_native_routing_bootstrap(out):
    raise RuntimeError('SR-042 is immutable historical bootstrap evidence; regeneration from the current mutable product state is disabled. Use current native-board and routing-hold authority instead.')
