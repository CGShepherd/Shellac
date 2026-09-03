"""AE-032 four-layer native routing preparation contract.

This contract deliberately stops short of modifying the native KiCad board.
It defines the production routing intent that the real board must satisfy.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LayerIntent:
    layer: str
    role: str
    continuous_reference: bool = False


LAYERS = (
    LayerIntent("F.Cu", "components + short/local signal routing"),
    LayerIntent("In1.Cu", "substantially continuous 0VA analogue reference plane", True),
    LayerIntent("In2.Cu", "power-rail distribution / rail spine"),
    LayerIntent("B.Cu", "secondary signal routing + local returns where necessary"),
)

CRITICAL_MANUAL_NET_GROUPS = (
    "SCH101 balanced cartridge input pair",
    "SCH101 RF/common-mode network",
    "LT5400 precision ratio connections",
    "SCH101 gain feedback/service-link paths",
    "SCH103 EQ timing networks",
    "SCH105 channel summing/mode paths",
    "SCH108 THAT1646 balanced-output pair",
)

ROUTING_HOLDS = (
    "final Bass rotary footprint and terminal fanout",
    "final Treble rotary footprint and terminal fanout",
    "final Channel rotary footprint / second-wafer envelope",
    "top-cover rotary drilling datum",
)

RULES = (
    "Do not split In1.Cu beneath precision/high-impedance analogue routes.",
    "Do not route precision analogue traces across voids or discontinuities in In1.Cu.",
    "Keep cartridge-input pair length/geometry closely matched and physically adjacent.",
    "Keep LT5400-related ratio connections short, local and free of unrelated vias.",
    "Keep EQ timing components and their switch nodes compact and away from output-driver loops.",
    "Keep supply decoupling loops local to each active device.",
    "Keep THAT1646 output legs geometrically symmetric through the connector region.",
    "Keep noisy/current-carrying rail routes off the In1.Cu reference layer.",
    "Use In2.Cu for rail distribution without creating capacitive/return-path traps beneath sensitive input nodes.",
    "Autorouting is prohibited for critical analogue net groups.",
    "Local placement refinement is permitted only within SR-041 movement authority.",
    "Rotary-specific final routing remains held until AE-027/AE-028 close.",
)

def validate_production_routing_contract():
    assert [x.layer for x in LAYERS] == ["F.Cu", "In1.Cu", "In2.Cu", "B.Cu"]
    assert sum(x.continuous_reference for x in LAYERS) == 1
    assert next(x for x in LAYERS if x.layer == "In1.Cu").continuous_reference
    assert len(CRITICAL_MANUAL_NET_GROUPS) >= 7
    assert len(ROUTING_HOLDS) == 4
    assert any("Autorouting" in r for r in RULES)
    assert any("Rotary-specific" in r for r in RULES)
