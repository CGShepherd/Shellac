#!/usr/bin/env python3
from __future__ import annotations

import math
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TMP = ROOT / ".ae064_cartridge_smoke_tmp"
LTSPICE = Path.home() / "AppData/Local/Programs/ADI/LTspice/LTspice.exe"
CARTRIDGES = ROOT / "simulation/models/cartridges"

CASES = {
    "grado_78c": {
        "file": CARTRIDGES / "grado_78c_shellac.lib",
        "subckt": "SHELLAC_GRADO_78C",
        "r": 475.0,
        "l": 0.045,
        "vac": 5e-3,
    },
    "at_vm95sp": {
        "file": CARTRIDGES / "at_vm95sp_shellac.lib",
        "subckt": "SHELLAC_AT_VM95SP",
        "r": 485.0,
        "l": 0.550,
        "vac": 2.7e-3,
    },
    "grado_gold_8mz": {
        "file": CARTRIDGES / "grado_gold_8mz_shellac.lib",
        "subckt": "SHELLAC_GRADO_GOLD_8MZ",
        "r": 660.0,
        "l": 0.050,
        "vac": 5e-3,
    },
}

RLOAD = 47400.0
FREQS = (1000.0, 20000.0)
REL_TOL = 2e-3

def expected(vac: float, r: float, l: float, freq: float) -> float:
    z_series = complex(r, 2.0 * math.pi * freq * l)
    ratio = RLOAD / (RLOAD + z_series)
    return abs(vac * ratio)

def parse_measure(log_text: str, name: str) -> float:
    """Return an AC measurement as a linear magnitude.

    LTspice 26 may emit FIND mag(V(...)) measurements either as a plain
    scalar or as a complex-style dB/phase tuple, e.g.
        v1k: mag(V(P,N)) =(-46.1073604768dB,0°) at 1000
    Accept both forms so the qualification is robust across LTspice output
    formatting while preserving the comparison in linear volts.
    """
    line_match = re.search(
        rf"(?im)^\s*{re.escape(name)}\s*:\s*.*?=\s*(.+?)\s+at\s+",
        log_text,
    )
    if not line_match:
        raise ValueError(f"measure {name!r} not found")

    value_text = line_match.group(1).strip()

    db_match = re.fullmatch(
        r"\(\s*([+\-0-9.eE]+)\s*dB\s*,\s*([+\-0-9.eE]+)\s*°?\s*\)",
        value_text,
        flags=re.IGNORECASE,
    )
    if db_match:
        db = float(db_match.group(1))
        return 10.0 ** (db / 20.0)

    scalar_match = re.fullmatch(r"([+\-0-9.eE]+)", value_text)
    if scalar_match:
        return float(scalar_match.group(1))

    raise ValueError(f"unrecognised measure format for {name!r}: {value_text!r}")

def run_case(name: str, case: dict) -> bool:
    work = TMP / name
    work.mkdir(parents=True, exist_ok=True)
    cir = work / f"{name}.cir"
    deck = f"""* AE-064 cartridge behavioural-model qualification: {name}
.include "{case['file']}"
VREF N 0 0
VDRV DRIVE N AC {case['vac']:.12g}
XCAR P N DRIVE {case['subckt']}
RLOAD P N {RLOAD:.12g}
.ac lin 2 1k 20k
.meas AC v1k FIND mag(V(P,N)) AT=1k
.meas AC v20k FIND mag(V(P,N)) AT=20k
.end
"""
    cir.write_text(deck, encoding="utf-8", newline="\n")
    proc = subprocess.run(
        [str(LTSPICE), "-b", str(cir)],
        cwd=work,
        text=True,
        capture_output=True,
    )
    log = cir.with_suffix(".log")
    log_text = log.read_text(encoding="utf-8", errors="ignore") if log.exists() else ""
    low = log_text.lower()
    fatal = any(
        marker in low
        for marker in ("fatal error", "unknown subcircuit", "can't find definition", "missing node")
    )
    if proc.returncode != 0 or not log.exists() or fatal:
        print(f"{name}: FAIL (LTspice execution)")
        print(log_text[-3000:])
        return False

    ok = True
    for label, freq in (("v1k", 1000.0), ("v20k", 20000.0)):
        measured = parse_measure(log_text, label)
        target = expected(case["vac"], case["r"], case["l"], freq)
        rel = abs(measured - target) / max(abs(target), 1e-30)
        passed = rel <= REL_TOL
        ok &= passed
        print(
            f"{name} {label}: {'PASS' if passed else 'FAIL'} "
            f"measured={measured:.9g} expected={target:.9g} rel_err={rel:.3e}"
        )
    return ok

def main() -> int:
    if not LTSPICE.exists():
        print(f"LTspice not found: {LTSPICE}")
        return 1
    missing = [str(c["file"]) for c in CASES.values() if not c["file"].exists()]
    if missing:
        print("Missing cartridge model file(s):")
        for path in missing:
            print("  -", path)
        return 1

    TMP.mkdir(exist_ok=True)
    results = [run_case(name, case) for name, case in CASES.items()]
    passed = sum(results)
    all_passed = all(results)
    print(f"AE-064 cartridge smoke: {'PASS' if all_passed else 'FAIL'} ({passed}/{len(results)})")
    if all_passed:
        shutil.rmtree(TMP, ignore_errors=True)
    return 0 if all_passed else 2

if __name__ == "__main__":
    raise SystemExit(main())
