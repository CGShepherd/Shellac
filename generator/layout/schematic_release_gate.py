"""Historical SR-039 snapshot adapter, quarantined by AE-076D."""
from dataclasses import dataclass
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[2]; SNAPSHOT=ROOT/'config/release/sr039_schematic_to_layout.yaml'; HOLD=ROOT/'config/release/ae071_prerouting_hold.yaml'
@dataclass(frozen=True,slots=True)
class ReleaseDisposition: schematic_release:str; placement_release:str; routing_release:str; manufacturing_release:str
@dataclass(frozen=True,slots=True)
class SchematicToLayoutReleaseGate:
 identifier:str; revision:str; status:str; validated_design_commit:str; historical_disposition:ReleaseDisposition; current_authority:bool; current_routing_authorized:bool; current_hold_authority:str; observed_current_hold_final_routing:bool; historical_validation:dict; historical_blockers:tuple[str,...]
def build_schematic_to_layout_release_gate():
 s=yaml.safe_load(SNAPSHOT.read_text(encoding='utf-8')); h=yaml.safe_load(HOLD.read_text(encoding='utf-8'))
 return SchematicToLayoutReleaseGate(s['release_gate'],s['revision'],'HISTORICAL_SNAPSHOT_ONLY_DO_NOT_USE_FOR_CURRENT_RELEASE',s['validated_design_commit'],ReleaseDisposition(s['electrical_release'],s['placement_release'],s['routing_release'],s['manufacturing_release']),False,False,h['authority'],bool(h['permissions']['final_routing']),dict(s['validation']),tuple(s['controlled_blockers']))
