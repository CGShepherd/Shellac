#!/usr/bin/env python3
from __future__ import annotations
import hashlib
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TMP = ROOT / ".ae062_wrapper_smoke_tmp"
LTSPICE = Path.home() / "AppData/Local/Programs/ADI/LTspice/LTspice.exe"
LT5400 = Path.home() / "AppData/Local/LTspice/lib/sub/LT5400.lib"

EXPECTED = {
    "OPA1656.LIB": "9847ed60c62e792ee6f1c84899278a3c11ce71a6d21804bdd88f51199f1ba055",
    "OPA161x.LIB": "c86df5d4b2d26ec196c0a6158a61004a6747aec5440fcc2031674ad62a448ef7",
    "1646_Macro_02.lib": "9abb4f6762935415db6f485de62687fe98b2ef7ea015ed4a320bd158ff264159",
}
LT5400_HASH = "f2c8ec58c2573983a8211393f7bcd27792769155b9ecf494ad027155b3e1d553"

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def find_file(name):
    for base in (ROOT / ".ae062_qualification_tmp", ROOT / ".ae062_vendor_cache"):
        if base.exists():
            hits = list(base.rglob(name))
            if hits:
                return hits[0]
    return None

def run_case(name, deck):
    case = TMP / name
    case.mkdir(parents=True, exist_ok=True)
    cir = case / f"{name}.cir"
    cir.write_text(deck, encoding="utf-8", newline="\n")
    p = subprocess.run([str(LTSPICE), "-b", str(cir)], cwd=case, text=True, capture_output=True)
    log = cir.with_suffix(".log")
    log_text = log.read_text(encoding="utf-8", errors="ignore") if log.exists() else ""
    low = log_text.lower()
    fatal = any(s in low for s in ("fatal error", "unknown subcircuit", "can't find definition", "missing node"))
    ok = p.returncode == 0 and log.exists() and not fatal
    print(f"{name}: {'PASS' if ok else 'FAIL'} (returncode={p.returncode})")
    if not ok:
        print(log_text[-3000:])
    return ok

def main():
    if not LTSPICE.exists():
        print(f"LTspice not found: {LTSPICE}")
        return 1
    if not LT5400.exists() or sha256(LT5400) != LT5400_HASH:
        print("Controlled LT5400 installed library missing or hash mismatch.")
        return 1

    TMP.mkdir(exist_ok=True)
    vendor = {}
    for name, expected in EXPECTED.items():
        src = find_file(name)
        if src is None:
            print(f"Missing qualified local vendor model: {name}")
            return 1
        actual = sha256(src)
        if actual != expected:
            print(f"Hash mismatch for {name}: {actual}")
            return 1
        dst = TMP / name
        shutil.copyfile(src, dst)
        vendor[name] = dst

    wrappers = ROOT / "simulation/models/wrappers"
    cases = [
        ("opa1656_wrapper", f"""* AE062 OPA1656 wrapper smoke
.include "{vendor['OPA1656.LIB']}"
.include "{wrappers/'opa1656_shellac.lib'}"
VPLUS VPLUS 0 18
VMINUS VMINUS 0 -18
VIN IN 0 0.1
XU IN OUT VPLUS VMINUS OUT SHELLAC_OPA1656
RLOAD OUT 0 100k
.op
.end
"""),
        ("opa1612_wrapper", f"""* AE062 OPA1612 wrapper smoke
.include "{vendor['OPA161x.LIB']}"
.include "{wrappers/'opa1612_shellac.lib'}"
VPLUS VPLUS 0 18
VMINUS VMINUS 0 -18
VIN IN 0 0.1
XU IN OUT VPLUS VMINUS OUT SHELLAC_OPA1612
RLOAD OUT 0 100k
.op
.end
"""),
        ("lt5400_wrapper", f"""* AE062 LT5400-7 wrapper smoke
.include "{LT5400}"
.include "{wrappers/'lt5400_7_shellac.lib'}"
V1 P1 0 1
V3 P3 0 1
V5 P5 0 1
V7 P7 0 1
XU P1 0 P3 0 P5 0 P7 0 0 SHELLAC_LT5400_7
.op
.end
"""),
        ("that1646_wrapper", f"""* AE062 THAT1646 wrapper smoke
.include "{vendor['1646_Macro_02.lib']}"
.include "{wrappers/'that1646_shellac.lib'}"
VPLUS VPLUS 0 18
VMINUS VMINUS 0 -18
VIN IN 0 0.1
XU OUTM OUTM 0 IN VMINUS VPLUS OUTP OUTP SHELLAC_THAT1646
RLP OUTP 0 100k
RLM OUTM 0 100k
.op
.end
"""),
    ]
    results = [run_case(name, deck) for name, deck in cases]
    print(f"AE-062 wrapper smoke: {'PASS' if all(results) else 'FAIL'} ({sum(results)}/4)")
    return 0 if all(results) else 2

if __name__ == "__main__":
    raise SystemExit(main())
