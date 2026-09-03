from pathlib import Path
import sys
_REPO=Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:sys.path.insert(0,str(_REPO))
from generator.layout.native_four_layer import audit,configure_layers
BOARD=_REPO/"out/kicad/ProjectShellac.kicad_pcb"
def main():
    text=BOARD.read_text(encoding="utf-8"); new=configure_layers(text); issues=audit(new)
    if issues:raise SystemExit("AE-033 failed: "+"; ".join(issues))
    if new!=text:BOARD.write_text(new,encoding="utf-8")
    print("AE-033 configured F.Cu / In1.Cu / In2.Cu / B.Cu; board remains unrouted.")
    return 0
if __name__=="__main__":raise SystemExit(main())
