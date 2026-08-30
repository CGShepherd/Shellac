from __future__ import annotations
from pathlib import Path
import json,re
from dataclasses import asdict,dataclass

from generator.layout.preliminary_placement import build_preliminary_placement_baseline
from generator.mechanical.sr040_audio_freeze import frozen_audio_board_outline

BOARD=Path("out/kicad/ProjectShellac.kicad_pcb")

@dataclass(frozen=True)
class NativeBoardAudit:
    footprint_population_ok: bool
    board_outline_ok: bool
    mounting_holes_ok: bool
    unrouted_ok: bool
    four_layer_ok: bool
    inner1_present: bool
    inner2_present: bool
    routing_ready: bool

def audit_native_board()->NativeBoardAudit:
    text=BOARD.read_text(encoding="utf-8")
    outline=frozen_audio_board_outline()
    placement=build_preliminary_placement_baseline(
        width_mm=outline.outline.width_mm,depth_mm=outline.outline.depth_mm)
    refs=set(re.findall(r'\(property\s+"Reference"\s+"([^"]+)"',text))
    population_ok=all(p.ref in refs for p in placement.proposals)
    board_outline_ok=text.count('(layer "Edge.Cuts")')>=4
    holes_ok=all(h.identifier in refs for h in outline.mounting_holes)
    unrouted='(segment ' not in text and '(via ' not in text
    inner1='"In1.Cu"' in text
    inner2='"In2.Cu"' in text
    four=inner1 and inner2
    return NativeBoardAudit(
        population_ok,board_outline_ok,holes_ok,unrouted,four,inner1,inner2,
        population_ok and board_outline_ok and holes_ok and unrouted and four
    )

def main():
    result=audit_native_board()
    print(json.dumps(asdict(result),indent=2))
    if not result.four_layer_ok:
        print("\\nACTION REQUIRED: configure the KiCad board as 4 copper layers.")
        print("Required: F.Cu / In1.Cu / In2.Cu / B.Cu")
        print("In1.Cu = continuous 0VA; In2.Cu = power rails / rail spine.")
        raise SystemExit(2)
    if not result.routing_ready:
        raise SystemExit(1)

if __name__=="__main__":
    main()
