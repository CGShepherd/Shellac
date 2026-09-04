from __future__ import annotations
from pathlib import Path
import json, shutil, subprocess, sys, tempfile
REPO=Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path: sys.path.insert(0,str(REPO))
from generator.layout.native_plane import add_in1_zone,audit_in1_zone,discover_power_nets
BOARD=REPO/"out/kicad/ProjectShellac.kicad_pcb"
BACKUP=REPO/"out/kicad/ProjectShellac.pre_AE035.kicad_pcb"
def find_kicad_cli():
    candidates=[shutil.which("kicad-cli"),r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe",r"C:\Program Files\KiCad\8.0\bin\kicad-cli.exe"]
    for c in candidates:
        if c and Path(c).exists(): return str(c)
    return None
def parse_check(cli):
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/"pos.csv"
        return subprocess.run([cli,"pcb","export","pos","-o",str(out),str(BOARD)],capture_output=True,text=True)
def main():
    cli=find_kicad_cli()
    if not cli: raise SystemExit("AE-035 requires kicad-cli; no board changes made.")
    original=BOARD.read_text(encoding="utf-8")
    nets=discover_power_nets(original)
    print(json.dumps({"0VA":nets.zero_va,"positive_rail":nets.positive_rail,"negative_rail":nets.negative_rail},indent=2))
    new=add_in1_zone(original); issues=audit_in1_zone(new)
    if issues: raise SystemExit("AE-035 pre-write audit failed: "+"; ".join(issues))
    BACKUP.write_text(original,encoding="utf-8"); BOARD.write_text(new,encoding="utf-8")
    r=parse_check(cli)
    if r.returncode!=0:
        BOARD.write_text(original,encoding="utf-8")
        raise SystemExit("KiCad rejected AE-035 board; original restored.\n"+r.stdout+"\n"+r.stderr)
    print(f"Applied In1.Cu 0VA zone using {nets.zero_va}.")
    print(f"KiCad parse validation passed via: {cli}")
    print(f"Rollback backup retained at: {BACKUP}")
    return 0
if __name__=="__main__": raise SystemExit(main())
