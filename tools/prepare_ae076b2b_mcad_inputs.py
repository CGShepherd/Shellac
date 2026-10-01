#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, http.cookiejar, json, os, shutil, subprocess, urllib.request
import yaml

ROOT=Path(__file__).resolve().parents[1]
CFG=ROOT/"config/mechanical/ae076b2b_mcad_sources.yaml"
CACHE=ROOT/"mechanical/mcad/vendor/cache"
PCB_DIR=ROOT/"mechanical/mcad/pcb/generated"
BOARD=ROOT/"out/kicad/ProjectShellac.kicad_pcb"

def sha(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
    return h.hexdigest()

def step_ok(path,min_bytes=4096):
    path=Path(path)
    if not path.is_file() or path.stat().st_size<min_bytes: raise RuntimeError(f"STEP missing/too small: {path}")
    if "ISO-10303-21;" not in path.read_bytes()[:128].decode("ascii","ignore"): raise RuntimeError(f"not STEP: {path}")

def pdf_ok(path,min_bytes=4096):
    path=Path(path)
    if not path.is_file() or path.stat().st_size<min_bytes: raise RuntimeError(f"PDF missing/too small: {path}")
    if not path.read_bytes()[:5].startswith(b"%PDF-"): raise RuntimeError(f"not PDF: {path}")

def opener():
    jar=http.cookiejar.CookieJar()
    op=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    op.addheaders=[("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/154 Safari/537.36"),("Accept","*/*")]
    return op

def download(url,dest,referer=None):
    op=opener()
    if referer:
        try:
            with op.open(referer,timeout=30) as r: r.read(2048)
        except Exception:
            pass
    req=urllib.request.Request(url,headers={"Referer":referer} if referer else {})
    with op.open(req,timeout=75) as r: data=r.read()
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes(data)

def find_kicad():
    c=[]
    if os.environ.get("KICAD_CLI"): c.append(Path(os.environ["KICAD_CLI"]))
    w=shutil.which("kicad-cli")
    if w: c.append(Path(w))
    c.append(Path(r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"))
    for x in c:
        if x.is_file(): return x
    raise RuntimeError("KiCad 9 kicad-cli not found")

def export_pcb(cfg):
    cli=find_kicad()
    out=PCB_DIR/cfg["pcb_step"]["filename"]
    out.parent.mkdir(parents=True,exist_ok=True)
    cmd=[str(cli),"pcb","export","step","--force","--subst-models","--no-dnp","--output",str(out),str(BOARD)]
    q=subprocess.run(cmd,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    if q.returncode: raise RuntimeError(q.stdout)
    step_ok(out)
    v=subprocess.run([str(cli),"version"],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    return {"bytes":out.stat().st_size,"sha256":sha(out),"kicad_version":v.stdout.strip(),"source_board_sha256":sha(BOARD)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--verify-only",action="store_true")
    ap.add_argument("--ingest-metcase-step",type=Path)
    args=ap.parse_args()
    cfg=yaml.safe_load(CFG.read_text(encoding="utf-8"))
    report={"metcase":{},"neutrik":{}}

    m=cfg["metcase_enclosure"]
    pdf=CACHE/m["drawing_filename"]
    if not args.verify_only: download(m["drawing_url"],pdf,m["product_page"])
    pdf_ok(pdf,m["drawing_min_bytes"])
    if sha(pdf)!=m["drawing_sha256"]: raise RuntimeError("METCASE drawing SHA drift")
    report["metcase"]["drawing"]={"bytes":pdf.stat().st_size,"sha256":sha(pdf)}

    for k,a in cfg["neutrik_assets"].items():
        dest=CACHE/a["filename"]
        if not args.verify_only: download(a["download_url"],dest,a["product_page"])
        step_ok(dest,a["min_bytes"])
        if sha(dest)!=a["sha256"]: raise RuntimeError(f"{k} SHA drift")
        report["neutrik"][k]={"bytes":dest.stat().st_size,"sha256":sha(dest)}

    if args.ingest_metcase_step:
        src=args.ingest_metcase_step.expanduser().resolve()
        step_ok(src,100000)
        dest=CACHE/m["step_filename"]
        dest.write_bytes(src.read_bytes())

    step_dest=CACHE/m["step_filename"]
    if m["exact_step_ingested"]:
        step_ok(step_dest,100000)
        observed_step_sha=sha(step_dest)
        if observed_step_sha!=m["step_sha256"]:
            raise RuntimeError(f"METCASE STEP SHA drift: {observed_step_sha} != {m['step_sha256']}")
        report["metcase"]["manual_step"]={
            "bytes":step_dest.stat().st_size,
            "sha256":observed_step_sha,
            "path":str(step_dest.relative_to(ROOT)),
            "status":"HASH_VERIFIED",
        }
    else:
        report["metcase"]["manual_step"]={"status":m["step_status"]}

    board_sha=sha(BOARD)
    if board_sha!=cfg["pcb_step"]["source_board_sha256"]:
        raise RuntimeError(f"governed PCB source hash drift: {board_sha} != {cfg['pcb_step']['source_board_sha256']}")

    if args.verify_only:
        pcb_path=PCB_DIR/cfg["pcb_step"]["filename"]
        step_ok(pcb_path,4096)
        observed_pcb_sha=sha(pcb_path)
        if observed_pcb_sha!=cfg["pcb_step"]["observed_sha256"]:
            raise RuntimeError(f"PCB STEP SHA drift: {observed_pcb_sha} != {cfg['pcb_step']['observed_sha256']}")
        report["pcb_step"]={
            "status":"HASH_VERIFIED",
            "source_board_sha256":board_sha,
            "bytes":pcb_path.stat().st_size,
            "sha256":observed_pcb_sha,
        }
    else:
        report["pcb_step"]=export_pcb(cfg)
    print(json.dumps(report,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
