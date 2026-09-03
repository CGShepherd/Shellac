from __future__ import annotations
from dataclasses import dataclass
import re
@dataclass(frozen=True,slots=True)
class NativeFourLayerContract:
    copper_layers: tuple[str,...]=("F.Cu","In1.Cu","In2.Cu","B.Cu")
    in1_role:str="continuous_0VA_reference"
    in2_role:str="power_distribution_rail_spine"
    fabrication_stack_policy:str="manufacturer_standard_4_layer_stack"
    board_thickness_mm:float=1.6
    outer_copper_oz:float=1.0
    finish_policy:str="HASL_LEAD_FREE_DEFAULT_ENIG_ONLY_IF_JUSTIFIED"
CONTRACT=NativeFourLayerContract()
def copper_layers(text):
    return tuple(x for x in CONTRACT.copper_layers if f'"{x}"' in text)
def configure_layers(text):
    if '"In1.Cu"' in text and '"In2.Cu"' in text:return text
    marker='(31 "B.Cu" signal)'
    if marker not in text:raise ValueError("cannot locate B.Cu layer declaration")
    return text.replace(marker,'(2 "In1.Cu" power)\n\t\t(4 "In2.Cu" power)\n\t\t'+marker,1)
def audit(text):
    issues=[f"missing copper layer {x}" for x in CONTRACT.copper_layers if f'"{x}"' not in text]
    if '(segment ' in text or '(via ' in text:issues.append("board must remain unrouted at AE-033 gate")
    return issues
