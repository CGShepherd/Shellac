from pathlib import Path
import sys,json
_REPO=Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path: sys.path.insert(0,str(_REPO))
from generator.layout.native_copper_preflight import inspect_native_board
BOARD=_REPO/'out/kicad/ProjectShellac.kicad_pcb'
def main():
    x=inspect_native_board(BOARD.read_text(encoding='utf-8'))
    payload={'net_count':x.net_count,'zero_va_net_id':x.zero_va_net_id,'zero_va_name':x.zero_va_name,'copper_layers':x.copper_layers,'segment_count':x.segment_count,'via_count':x.via_count,'zone_count':x.zone_count,'edge_line_count':x.edge_line_count,'issues':x.issues}
    print(json.dumps(payload,indent=2))
    out=_REPO/'docs/design_pack/AE-034_Generated_Native_Copper_Preflight.json'; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
    print(f'Wrote {out}')
    return 1 if x.issues else 0
if __name__=='__main__': raise SystemExit(main())
