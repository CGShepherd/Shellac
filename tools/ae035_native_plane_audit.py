from pathlib import Path
import json,sys
REPO=Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path: sys.path.insert(0,str(REPO))
from generator.layout.native_plane import audit_in1_zone,discover_power_nets,deterministic_uuid
BOARD=REPO/"out/kicad/ProjectShellac.kicad_pcb"
def main():
    t=BOARD.read_text(encoding="utf-8"); p=discover_power_nets(t); issues=audit_in1_zone(t)
    payload={"zero_va":p.zero_va,"positive_rail":p.positive_rail,"negative_rail":p.negative_rail,"in1_zone_present":deterministic_uuid("In1_0VA_zone") in t,"zone_count":t.count("(zone "),"segment_count":t.count("(segment "),"via_count":t.count("(via "),"issues":issues}
    print(json.dumps(payload,indent=2))
    out=REPO/"docs/design_pack/AE-035_Generated_Native_Plane_Audit.json"; out.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
    return 1 if issues else 0
if __name__=="__main__": raise SystemExit(main())
