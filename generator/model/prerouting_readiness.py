"""Current pre-routing preparation contract reconciled by AE-076D. Not release authority."""
from dataclasses import dataclass
@dataclass(frozen=True)
class PreRoutingRule:
 identifier:str; requirement:str; control_dependent:bool; release_blocking:bool
RULES=(
 PreRoutingRule('LAYER-COUNT','Four copper layers: F.Cu / In1.Cu / In2.Cu / B.Cu',False,True),
 PreRoutingRule('IN1-0VA','In1.Cu reserved as substantially continuous 0VA reference plane',False,True),
 PreRoutingRule('IN2-POWER','In2.Cu used for controlled power distribution / rail spine',False,True),
 PreRoutingRule('INPUT-SYMMETRY','SCH101 differential input/RF paths routed as a symmetric matched pair',False,True),
 PreRoutingRule('LT5400-LOCAL','LT5400 ratio-network connections remain short and local; no autorouting',False,True),
 PreRoutingRule('EQ-LOCAL','EQ timing components and selector nets kept local and away from output/rail switching loops',True,True),
 PreRoutingRule('OUTPUT-BALANCE','THAT1646 balanced-output legs and return paths kept symmetric',False,True),
 PreRoutingRule('NO-PLANE-SPLIT','No high-impedance or precision analogue route crosses a 0VA-plane discontinuity',False,True),
 PreRoutingRule('DECOUPLING','Every active device decoupled to the local reference with minimum loop area',False,True),
 PreRoutingRule('CONTROL-GEOMETRY','Exact NKK/C&K B.Cu footprints, pin/pad orientation, keep-outs, upper-cover apertures and six-support service-module stack remain gated by current AE071-B03',True,True),
 PreRoutingRule('PERSONALITY-LOCAL','Future H120/H220 per-channel personality sockets remain local to differential load nodes with short symmetric shunt geometry; exact interface parasitics remain RUN10-open',False,True),)
def independent_rules(): return tuple(r for r in RULES if not r.control_dependent)
def control_dependent_rules(): return tuple(r for r in RULES if r.control_dependent)
def validate_prerouting_contract():
 assert len(RULES)>=10 and independent_rules() and control_dependent_rules() and all(r.release_blocking for r in RULES)
 r=next(r for r in RULES if r.identifier=='CONTROL-GEOMETRY')
 assert 'AE071-B03' in r.requirement and 'AE-027' not in r.requirement and 'AE-028' not in r.requirement
