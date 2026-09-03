from pathlib import Path
import sys,json
_REPO=Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:sys.path.insert(0,str(_REPO))
from generator.layout.native_four_layer import CONTRACT,audit,copper_layers
BOARD=_REPO/"out/kicad/ProjectShellac.kicad_pcb"
def main():
    t=BOARD.read_text(encoding="utf-8"); issues=audit(t); print(json.dumps({"copper_layers":copper_layers(t),"in1_role":CONTRACT.in1_role,"in2_role":CONTRACT.in2_role,"stack_policy":CONTRACT.fabrication_stack_policy,"issues":issues},indent=2)); return 1 if issues else 0
if __name__=="__main__":raise SystemExit(main())
