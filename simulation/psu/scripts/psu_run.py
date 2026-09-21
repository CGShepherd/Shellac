from __future__ import annotations
import argparse, os, re, subprocess, sys, tempfile
from pathlib import Path
import yaml
from simulation.scripts.shellac_spice import find_ltspice, sha256_file, build_command, parse_measurements, ToolchainError
ROOT=Path(__file__).resolve().parents[3]; PSU=ROOT/"simulation"/"psu"
SUB=re.compile(r"^\s*\.subckt\s+(\S+)\s+(.+?)\s*$", re.I | re.M)
def cfg(): return yaml.safe_load((PSU/"config/model_sources.yaml").read_text())
def cache():
    raw=os.environ.get("SHELLAC_PSU_VENDOR_CACHE")
    return Path(raw).expanduser().resolve() if raw else (ROOT/".vendor_models/psu").resolve()
def controlled_models():
    c=cfg(); root=cache(); out={}
    for key,s in c["sources"].items():
        p=root/s["model_file"]
        if not p.is_file(): raise ToolchainError(f"{key}: missing {p}")
        if sha256_file(p).lower()!=s["model_sha256"].lower(): raise ToolchainError(f"{key}: model SHA-256 mismatch")
        t=p.read_text(encoding="utf-8",errors="replace")
        matches=[tail.split() for n,tail in SUB.findall(t) if n.lower()==s["subckt"].lower()]
        if s["pins"] not in matches: raise ToolchainError(f"{key}: .SUBCKT interface mismatch; found {matches}")
        if key=="LM317":
            lo=t.lower(); a=lo.find(".subckt lm317_trans"); b=lo.find(".ends lm317_trans",a)
            body="\n".join(t[a:b].splitlines()[1:])
            if re.search(r"\bOUT_1\b",body,re.I): raise ToolchainError("LM317 OUT_1 vendor anomaly changed; wrapper invalid")
        out[key]=p
    return out
def readlog(p):
    b=p.read_bytes()
    if b.startswith((b"\xff\xfe",b"\xfe\xff")): return b.decode("utf-16")
    if b"\x00" in b[:256]:
        try: return b.decode("utf-16")
        except UnicodeError: pass
    for e in ("utf-8","cp1252"):
        try: return b.decode(e)
        except UnicodeError: pass
    return b.decode("utf-8",errors="replace")
def _include_target(line):
    m=re.match(r'^\s*\.(?:include|lib)\s+(?:"([^"]+)"|(\S+))\s*$', line, re.I)
    return (m.group(1) or m.group(2)) if m else None
def embed_lf353_vendor(s,p):
    vendor=p.read_text(encoding="utf-8",errors="strict").rstrip()
    vendor_norm=str(p).replace("\\","/").lower()
    lines=s.splitlines(); kept=[]; removed=0
    for line in lines:
        target=_include_target(line)
        norm=target.replace("\\","/").lower() if target else None
        basename=norm.rsplit("/",1)[-1] if norm else None
        if norm is not None and (norm==vendor_norm or basename==p.name.lower()):
            removed+=1
        else: kept.append(line)
    if removed!=1: raise ToolchainError(f"LF353: expected exact vendor include once, found {removed}")
    i=next((i for i in range(len(kept)-1,-1,-1) if kept[i].strip().lower()==".end"),None)
    if i is None: raise ToolchainError("LF353: smoke deck has no .end")
    kept[i:i]=["","* BEGIN SHA-VERIFIED TI LF353 VENDOR PAYLOAD",vendor,"* END SHA-VERIFIED TI LF353 VENDOR PAYLOAD",""]
    return "\n".join(kept)+"\n"
def embed_lf353_wrapper(s,p):
    wrapper=p.read_text(encoding="utf-8",errors="strict").rstrip()
    lines=s.splitlines(); kept=[]; removed=0
    for line in lines:
        target=_include_target(line)
        basename=target.replace("\\","/").lower().rsplit("/",1)[-1] if target else None
        if basename==p.name.lower():
            removed+=1
        else:
            kept.append(line)
    if removed!=1: raise ToolchainError(f"LF353: expected wrapper include once, found {removed}")
    i=next((i for i in range(len(kept)-1,-1,-1) if kept[i].strip().lower()==".end"),None)
    if i is None: raise ToolchainError("LF353: smoke deck has no .end")
    kept[i:i]=["","* BEGIN CONTROLLED SHELLAC LF353 WRAPPER",wrapper,
               "* END CONTROLLED SHELLAC LF353 WRAPPER",""]
    return "\n".join(kept)+"\n"
def qcfg():
    return yaml.safe_load((PSU/"config/qualification.yaml").read_text(encoding="utf-8"))
def require_measurements(name,measurements):
    required=[str(x).upper() for x in qcfg()["required_measurements"][name]]
    missing=[x for x in required if x not in measurements]
    if missing:
        raise ToolchainError(f"{name}: missing required measurements {missing}; parsed keys={sorted(measurements)}")
    return {x:measurements[x] for x in required}
def preserve_diagnostics(name,deck_path,log_path,raw_path,combined_text):
    d=PSU/"results"/"run00_diagnostics"/name.lower()
    d.mkdir(parents=True,exist_ok=True)
    (d/f"{name}.cir").write_bytes(deck_path.read_bytes())
    if log_path.is_file(): (d/f"{name}.log").write_bytes(log_path.read_bytes())
    if raw_path.is_file(): (d/f"{name}.raw").write_bytes(raw_path.read_bytes())
    (d/f"{name}_combined.txt").write_text(combined_text,encoding="utf-8",newline="\n")
    return d

def deck(exe,name,template,repl,embed_vendor=None,embed_wrapper=None):
    s=template.read_text()
    for k,v in repl.items(): s=s.replace("{{"+k+"}}",str(v).replace("\\","/"))
    if "{{" in s: raise ToolchainError(f"{name}: unresolved template")
    first=s.splitlines()[0].strip() if s.splitlines() else ""
    if not first or not first.startswith("*"):
        raise ToolchainError(f"{name}: generated SPICE deck must begin with an explicit '*' title/comment line; got {first!r}")
    if embed_vendor is not None: s=embed_lf353_vendor(s,embed_vendor)
    if embed_wrapper is not None: s=embed_lf353_wrapper(s,embed_wrapper)
    with tempfile.TemporaryDirectory(prefix="shellac_psu_") as td:
        p=Path(td)/(name+".cir"); p.write_text(s,encoding="utf-8",newline="\n")
        q=subprocess.run(build_command(exe,p),cwd=p.parent,capture_output=True,text=True,timeout=60,check=False)
        log=p.with_suffix(".log"); txt=(q.stdout or "")+"\n"+(q.stderr or "")+("\n"+readlog(log) if log.is_file() else "")
        if q.returncode:
            d=preserve_diagnostics(name,p,log,p.with_suffix(".raw"),txt)
            raise ToolchainError(f"{name}: LTspice rc={q.returncode}; diagnostics preserved at {d}\n{txt[-2000:]}")
        for bad in ("unknown subcircuit","sub-circuit name is not defined","can't open","fatal error"):
            if bad in txt.lower():
                d=preserve_diagnostics(name,p,log,p.with_suffix(".raw"),txt)
                raise ToolchainError(f"{name}: {bad}; diagnostics preserved at {d}\n{txt[-2000:]}")
        m=parse_measurements(txt)
        if not m:
            d=preserve_diagnostics(name,p,log,p.with_suffix(".raw"),txt)
            raise ToolchainError(f"{name}: no measurements; diagnostics preserved at {d}\n{txt[-2000:]}")
        try:
            return require_measurements(name.upper(),m)
        except ToolchainError as e:
            d=preserve_diagnostics(name,p,log,p.with_suffix(".raw"),txt)
            raise ToolchainError(f"{e}; diagnostics preserved at {d}") from e
def qualify():
    exe=find_ltspice()
    if exe is None: raise ToolchainError("LTspice not found")
    m=controlled_models(); W=PSU/"models/wrappers"; R=PSU/"runs/run00_model_qualification"
    r={"LM317_MODEL":m["LM317"],"LM337_MODEL":m["LM337"],"LF353_MODEL":m["LF353"],
       "LM317_WRAPPER":W/"lm317_shellac_psu.lib","LM337_WRAPPER":W/"lm337_shellac_psu.lib","LF353_WRAPPER":W/"lf353_shellac_psu.lib"}
    p=deck(exe,"lm317",R/"lm317_smoke.cir.in",r); print("PSU-RUN00 LM317: REQUIRED-MEASUREMENTS PASS",p)
    n=deck(exe,"lm337",R/"lm337_smoke.cir.in",r); print("PSU-RUN00 LM337: REQUIRED-MEASUREMENTS PASS",n)
    o=deck(exe,"lf353",R/"lf353_smoke.cir.in",r,embed_vendor=m["LF353"],embed_wrapper=W/"lf353_shellac_psu.lib"); print("PSU-RUN00 LF353: REQUIRED-MEASUREMENTS PASS",o)
    f=[]
    if not 4.5<=p["VOUT_AVG"]<=5.5:f.append(f"LM317 average {p['VOUT_AVG']}")
    if p["VOUT_MAX"]-p["VOUT_MIN"]>.1:f.append("LM317 steady span")
    if not -5.5<=n["VOUT_AVG"]<=-4.5:f.append(f"LM337 average {n['VOUT_AVG']}")
    if n["VOUT_MAX"]-n["VOUT_MIN"]>.1:f.append("LM337 steady span")
    for x in ("OA_HI","OB_HI"):
        if not .15<=o[x]<=.25:f.append(f"LF353 {x}={o[x]}")
    for x in ("OA_LO","OB_LO"):
        if abs(o[x])>.02:f.append(f"LF353 {x}={o[x]}")
    if abs(o["OA_HI"]-o["OB_HI"])>.01:f.append("LF353 A/B mismatch")
    if f:
        print("PSU-RUN00: FAIL"); [print(" -",x) for x in f]; return 1
    print("PSU-RUN00: PASS"); return 0
def main(argv=None):
    a=argparse.ArgumentParser();a.add_argument("command",choices=["qualify"]);a.parse_args(argv)
    try:return qualify()
    except (ToolchainError,subprocess.TimeoutExpired) as e:print("ERROR:",e,file=sys.stderr);return 2
if __name__=="__main__":raise SystemExit(main())
