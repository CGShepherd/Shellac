from __future__ import annotations
from dataclasses import dataclass
import re

@dataclass(frozen=True,slots=True)
class CopperPreflight:
    net_count:int
    zero_va_net_id:int|None
    zero_va_name:str|None
    copper_layers:tuple[str,...]
    segment_count:int
    via_count:int
    zone_count:int
    edge_line_count:int
    issues:tuple[str,...]

def inspect_native_board(text:str)->CopperPreflight:
    nets={int(n):name for n,name in re.findall(r'\(net\s+(\d+)\s+"([^"]*)"\)',text)}
    candidates=[(n,name) for n,name in nets.items() if name.upper() in {'0VA','0V','GND','AGND'}]
    exact=[x for x in candidates if x[1].upper()=='0VA']
    chosen=exact[0] if len(exact)==1 else (candidates[0] if len(candidates)==1 else None)
    layers=tuple(x for x in ('F.Cu','In1.Cu','In2.Cu','B.Cu') if f'"{x}"' in text)
    issues=[]
    if len(layers)!=4: issues.append('native board is not four-layer')
    if chosen is None: issues.append('cannot uniquely identify analogue 0VA net')
    if text.count('(layer "Edge.Cuts")')<4: issues.append('frozen rectangular board outline not evident')
    return CopperPreflight(len(nets),chosen[0] if chosen else None,chosen[1] if chosen else None,layers,text.count('(segment '),text.count('(via '),text.count('(zone '),text.count('(layer "Edge.Cuts")'),tuple(issues))

def validate_preflight(x:CopperPreflight):
    assert x.net_count>0
    assert x.copper_layers==('F.Cu','In1.Cu','In2.Cu','B.Cu')
    assert x.zero_va_net_id is not None and x.zero_va_name is not None
