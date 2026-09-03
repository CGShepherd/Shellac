"""AE-031 production pre-routing contract, independent of rotary-switch dimensions."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class PreRoutingRule:
    identifier: str
    requirement: str
    control_dependent: bool
    release_blocking: bool

RULES=(
    PreRoutingRule("LAYER-COUNT","Four copper layers: F.Cu / In1.Cu / In2.Cu / B.Cu",False,True),
    PreRoutingRule("IN1-0VA","In1.Cu reserved as substantially continuous 0VA reference plane",False,True),
    PreRoutingRule("IN2-POWER","In2.Cu used for controlled power distribution / rail spine",False,True),
    PreRoutingRule("INPUT-SYMMETRY","SCH101 differential input/RF paths routed as a symmetric matched pair",False,True),
    PreRoutingRule("LT5400-LOCAL","LT5400 ratio-network connections remain short and local; no autorouting",False,True),
    PreRoutingRule("EQ-LOCAL","EQ timing components and selector nets kept local and away from output/rail switching loops",True,True),
    PreRoutingRule("OUTPUT-BALANCE","THAT1646 balanced-output legs and return paths kept symmetric",False,True),
    PreRoutingRule("NO-PLANE-SPLIT","No high-impedance or precision analogue route crosses a 0VA-plane discontinuity",False,True),
    PreRoutingRule("DECOUPLING","Every active device decoupled to the local reference with minimum loop area",False,True),
    PreRoutingRule("ROTARY-KEEP-OUT","Final rotary footprints/keep-outs remain gated by AE-027/AE-028",True,True),
)

def independent_rules():
    return tuple(r for r in RULES if not r.control_dependent)

def control_dependent_rules():
    return tuple(r for r in RULES if r.control_dependent)

def validate_prerouting_contract():
    assert len(RULES)>=10
    assert independent_rules()
    assert control_dependent_rules()
    assert all(r.release_blocking for r in RULES)
