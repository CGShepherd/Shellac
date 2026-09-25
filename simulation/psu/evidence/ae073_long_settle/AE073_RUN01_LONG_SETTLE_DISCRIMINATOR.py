from pathlib import Path
import subprocess, sys, re, tempfile, shutil, time, csv

ROOT = Path.cwd()
SRC = ROOT / "simulation/psu/results/run00_diagnostics/run01_1000/run01_1000.cir"
OUT = ROOT / "simulation/psu/results/run00_diagnostics/ae073_long_settle"

if not (ROOT / "simulation/psu/scripts/psu_run.py").is_file():
    raise SystemExit("AE073-LONG: run from Shellac repository root")
if not SRC.is_file():
    raise SystemExit(f"AE073-LONG: prerequisite diagnostic deck missing: {SRC}")

sys.path.insert(0, str(ROOT))
from simulation.scripts.shellac_spice import find_ltspice, build_command, parse_measurements

base = SRC.read_text(encoding="utf-8", errors="replace")
required_once = [
    ".param RSET=1000",
    "RADJP VOUTP ADJP 220",
    "RADJN VOUTN ADJN 220",
    "RSETP OP ADJP {RSET}",
    "RSETN ON ADJN {RSET}",
    ".tran 0 400m 0 20u",
]
for needle in required_once:
    if base.count(needle) != 1:
        raise SystemExit(f"AE073-LONG: source invariant failed for {needle!r}")

# Separate positive and negative settings; preserve the generated/vendor payloads exactly.
base = base.replace(
    ".param RSET=1000",
    ".param RSETP_DIAG=2260\n.param RSETN_DIAG=2160",
    1,
)
base = base.replace("RSETP OP ADJP {RSET}", "RSETP OP ADJP {RSETP_DIAG}", 1)
base = base.replace("RSETN ON ADJN {RSET}", "RSETN ON ADJN {RSETN_DIAG}", 1)

# Eight seconds is intentionally much longer than the existing 400 ms evidence window.
# 100 us max step retains 100 samples/cycle at 100 Hz ripple while keeping execution tractable.
base = base.replace(".tran 0 400m 0 20u", ".tran 0 8 0 100u uic", 1)

# Remove the original six RUN01 measurements so this discriminator has one unambiguous report set.
base = re.sub(r"(?mi)^\s*\.meas\s+tran\s+(?:VP_AVG|VN_AVG|VP_MIN|VP_MAX|VN_MIN|VN_MAX)\b.*$", "", base)

# The composed deck embeds vendor .SUBCKT payloads containing many .ENDS lines.
# Match only a standalone top-level .end directive; substring counting would
# incorrectly count every .ENDS as another deck terminator.
end_matches = list(re.finditer(r"(?mi)^\s*\.end\s*$", base))
if len(end_matches) != 1:
    raise SystemExit(
        f"AE073-LONG: expected exactly one standalone .end in composed source deck; found {len(end_matches)}"
    )

windows = [
    ("W04", 0.30, 0.40),
    ("W10", 0.90, 1.00),
    ("W20", 1.90, 2.00),
    ("W40", 3.90, 4.00),
    ("W80", 7.90, 8.00),
]

meas = []
for tag, a, b in windows:
    for name, expr in [
        ("VP", "V(VOUTP)"),
        ("VN", "V(VOUTN)"),
        ("OP", "V(OP)"),
        ("ON", "V(ON)"),
        ("ADJP", "V(ADJP)"),
        ("ADJN", "V(ADJN)"),
        ("RAWP", "V(RAWP)"),
        ("RAWN", "V(RAWN)"),
        ("NMP", "V(NMP)"),
        ("NMN", "V(NMN)"),
    ]:
        meas.append(f".meas tran {tag}_{name} AVG {expr} FROM {a:g} TO {b:g}")
    meas.append(f".meas tran {tag}_IPROG_P AVG I(RADJP) FROM {a:g} TO {b:g}")
    meas.append(f".meas tran {tag}_IPROG_N AVG I(RADJN) FROM {a:g} TO {b:g}")
    meas.append(f".meas tran {tag}_IRSET_P AVG I(RSETP) FROM {a:g} TO {b:g}")
    meas.append(f".meas tran {tag}_IRSET_N AVG I(RSETN) FROM {a:g} TO {b:g}")

# Late-window ripple and convergence metrics.
meas += [
    ".meas tran W80_VP_MIN MIN V(VOUTP) FROM 7.9 TO 8",
    ".meas tran W80_VP_MAX MAX V(VOUTP) FROM 7.9 TO 8",
    ".meas tran W80_VN_MIN MIN V(VOUTN) FROM 7.9 TO 8",
    ".meas tran W80_VN_MAX MAX V(VOUTN) FROM 7.9 TO 8",
]

insert = "\n* AE-073 long-settle discriminator measurements\n" + "\n".join(meas) + "\n"
# Re-find after measurement removal and insert immediately before the one
# standalone top-level .end directive.
end_matches = list(re.finditer(r"(?mi)^\s*\.end\s*$", base))
if len(end_matches) != 1:
    raise SystemExit(
        f"AE073-LONG: standalone .end invariant changed before insertion; found {len(end_matches)}"
    )
idx = end_matches[0].start()
base = base[:idx] + insert + base[idx:]

exe = find_ltspice()
if exe is None:
    raise SystemExit("AE073-LONG: LTspice not found")

# Cases are diagnostic only; no controlled project file is modified.
cases = [
    # First case answers the central question using the untouched as-found trimmer settings.
    dict(name="as_found_nominal_rprog", rsetp=2260, rsetn=2160, rprogp=220, rprogn=220),
    # Same settings with today's in-circuit measured OUT-ADJ resistances.
    dict(name="as_found_measured_rprog", rsetp=2260, rsetn=2160, rprogp=219, rprogn=216),
    # Analytical first estimate of settings for about +/-17 V using measured Rprog and typical Iadj.
    # This is a diagnostic stimulus, not a calibration authority.
    dict(name="target17_estimate", rsetp=2735, rsetn=2691, rprogp=219, rprogn=216),
]

OUT.mkdir(parents=True, exist_ok=True)
summary_rows = []

for case in cases:
    s = base
    s = s.replace(".param RSETP_DIAG=2260", f".param RSETP_DIAG={case['rsetp']}", 1)
    s = s.replace(".param RSETN_DIAG=2160", f".param RSETN_DIAG={case['rsetn']}", 1)
    s = s.replace("RADJP VOUTP ADJP 220", f"RADJP VOUTP ADJP {case['rprogp']}", 1)
    s = s.replace("RADJN VOUTN ADJN 220", f"RADJN VOUTN ADJN {case['rprogn']}", 1)

    ev = OUT / case["name"]
    ev.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="ae073_long_") as td0:
        td = Path(td0)
        deck = td / "case.cir"
        deck.write_text(s, encoding="utf-8", newline="\n")
        t0 = time.perf_counter()
        try:
            q = subprocess.run(
                build_command(exe, deck),
                cwd=td,
                capture_output=True,
                text=True,
                timeout=240,
                check=False,
            )
            elapsed = time.perf_counter() - t0
            status = f"rc={q.returncode}"
            std = (q.stdout or "") + "\n" + (q.stderr or "")
        except subprocess.TimeoutExpired as e:
            elapsed = time.perf_counter() - t0
            status = "TIMEOUT"
            stdout = e.stdout.decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
            stderr = e.stderr.decode(errors="replace") if isinstance(e.stderr, bytes) else (e.stderr or "")
            std = stdout + "\n" + stderr

        log = deck.with_suffix(".log")
        txt = std + ("\n" + log.read_text(encoding="utf-8", errors="replace") if log.is_file() else "")
        for f in td.iterdir():
            if f.is_file():
                shutil.copy2(f, ev / f.name)
        (ev / "combined.txt").write_text(txt, encoding="utf-8", newline="\n")

    m = parse_measurements(txt)
    print(f"\nAE073-LONG CASE {case['name']}  {status}  elapsed={elapsed:.2f}s")
    print(f"  RSET+={case['rsetp']} RSET-={case['rsetn']} RPROG+={case['rprogp']} RPROG-={case['rprogn']}")

    for tag, _, _ in windows:
        keys = [f"{tag}_{x}" for x in ("VP", "VN", "OP", "ON", "ADJP", "ADJN", "RAWP", "RAWN")]
        if all(k in m for k in keys):
            print(
                f"  {tag}: VP={m[tag+'_VP']: .6f} VN={m[tag+'_VN']: .6f} "
                f"OP={m[tag+'_OP']: .6f} ON={m[tag+'_ON']: .6f} "
                f"ADJP={m[tag+'_ADJP']: .6f} ADJN={m[tag+'_ADJN']: .6f} "
                f"RAWP={m[tag+'_RAWP']: .6f} RAWN={m[tag+'_RAWN']: .6f}"
            )
        else:
            print(f"  {tag}: measurements missing")

    # Evidence discriminator, deliberately descriptive rather than a product PASS/FAIL gate.
    if "W80_OP" in m and "W80_ON" in m and "W80_VP" in m and "W80_VN" in m:
        op = float(m["W80_OP"]); on = float(m["W80_ON"])
        vp = float(m["W80_VP"]); vn = float(m["W80_VN"])
        satp = abs(op - (vn + 1.5)) < 0.25
        satn = abs(on - (vp - 1.5)) < 0.25
        print(f"  W80 saturation signature: U1B_NEG_RAIL={satp} U1A_POS_RAIL={satn}")
        print(f"  W80 servo outputs toward zero: |OP|={abs(op):.6f} V |ON|={abs(on):.6f} V")

    row = {
        "case": case["name"], "status": status, "elapsed_s": elapsed,
        "rsetp": case["rsetp"], "rsetn": case["rsetn"],
        "rprogp": case["rprogp"], "rprogn": case["rprogn"],
    }
    for k, v in m.items():
        if k.startswith(("W04_", "W10_", "W20_", "W40_", "W80_")):
            row[k] = v
    summary_rows.append(row)

fields = sorted({k for row in summary_rows for k in row.keys()}, key=lambda x: (x not in ["case","status","elapsed_s","rsetp","rsetn","rprogp","rprogn"], x))
with (OUT / "summary.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader(); w.writerows(summary_rows)

print(f"\nAE073-LONG: evidence written to {OUT}")
print("AE073-LONG: controlled project files were not modified.")
print("AE073-LONG: interpret W04 as reproduction of the old 300-400 ms window; W80 is the late 7.9-8.0 s discriminator.")
