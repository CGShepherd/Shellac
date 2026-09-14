#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TMP = ROOT / ".ae065_integrated_run00_tmp"
VENDOR = TMP / "vendor"
RESULT = ROOT / "simulation/results/run00_sanity/ae065_integrated_run00.json"
LTSPICE = Path.home() / "AppData/Local/Programs/ADI/LTspice/LTspice.exe"
LT5400 = Path.home() / "AppData/Local/LTspice/lib/sub/LT5400.lib"

LT5400_HASH = "f2c8ec58c2573983a8211393f7bcd27792769155b9ecf494ad027155b3e1d553"

SOURCES = {
    "OPA1656": {
        "member": "OPA1656.LIB",
        "model_sha256": "9847ed60c62e792ee6f1c84899278a3c11ce71a6d21804bdd88f51199f1ba055",
        "archive_sha256": "8f696ee73bfb9a5d7d15b70ed27629dfe5b92ba54e8da894aa25fe51d3cb312f",
        "archive_url": "https://www.ti.com/lit/zip/SBOMAW6",
    },
    "OPA1612": {
        "member": "OPA161x.LIB",
        "model_sha256": "c86df5d4b2d26ec196c0a6158a61004a6747aec5440fcc2031674ad62a448ef7",
        "archive_sha256": "8b567b729dd8bdc459650d41a5af84a5f7082a7ea06ea77406ba8a9db1348440",
        "archive_url": "https://www.ti.com/lit/zip/SBOM396",
    },
    "THAT1646": {
        "member": "1646_Macro_02.lib",
        "model_sha256": "9abb4f6762935415db6f485de62687fe98b2ef7ea015ed4a320bd158ff264159",
        "archive_sha256": "a5699cf253cbe2b063a03b2dd8cc2927fe1ab03903ed2f1bb9ae23a0e867733b",
        "archive_url": "https://thatcorp.com/wp-content/uploads/2020/11/THATMacroModels-Rev05.zip",
    },
}

S1G = {
    "model_sha256": "ffd79ea06d6ab712987b44e577c8787dbe54d25a90de58e3f6901a1b89642ed4",
    "url": "https://www.vishay.com/docs/89655/s1g.txt",
}

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def common_search_roots() -> list[Path]:
    roots = [
        ROOT / ".ae062_vendor_cache",
        ROOT / ".ae062_qualification_tmp",
        ROOT / ".ae063_vendor_cache",
        ROOT / ".ae063_qualification_tmp",
        Path.home() / "Downloads",
    ]
    return [p for p in roots if p.exists()]

def find_exact_file(basename: str, expected_hash: str) -> Path | None:
    for base in common_search_roots():
        try:
            hits = list(base.rglob(basename))
        except OSError:
            continue
        for p in hits:
            if p.is_file():
                try:
                    if sha256(p) == expected_hash:
                        print(f"MODEL source resolved locally: {p}")
                        return p
                except OSError:
                    pass
    return None

def find_exact_archive(expected_hash: str) -> Path | None:
    for base in common_search_roots():
        try:
            hits = list(base.rglob("*.zip"))
        except OSError:
            continue
        for p in hits:
            if p.is_file():
                try:
                    if sha256(p) == expected_hash:
                        print(f"ARCHIVE source resolved locally: {p}")
                        return p
                except OSError:
                    pass
    return None

def download(url: str, destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 Shellac-AE065/1.0",
            "Accept": "*/*",
        },
    )
    print(f"DOWNLOAD {url}")
    with urllib.request.urlopen(req, timeout=90) as response:
        destination.write_bytes(response.read())
    return destination

def extract_member(archive: Path, member_basename: str, expected_hash: str, destination: Path) -> Path:
    with zipfile.ZipFile(archive, "r") as zf:
        matches = [name for name in zf.namelist() if Path(name).name.lower() == member_basename.lower()]
        if len(matches) != 1:
            raise RuntimeError(
                f"{archive.name}: expected exactly one {member_basename}, found {matches}"
            )
        data = zf.read(matches[0])
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    actual = sha256(destination)
    if actual != expected_hash:
        raise RuntimeError(
            f"{member_basename}: extracted hash mismatch {actual}, expected {expected_hash}"
        )
    return destination

def resolve_zip_source(key: str) -> Path:
    spec = SOURCES[key]

    direct = find_exact_file(spec["member"], spec["model_sha256"])
    if direct is not None:
        return direct

    archive = find_exact_archive(spec["archive_sha256"])
    if archive is None:
        archive = VENDOR / f"{key}.zip"
        download(spec["archive_url"], archive)
        actual_archive = sha256(archive)
        if actual_archive != spec["archive_sha256"]:
            raise RuntimeError(
                f"{key}: downloaded archive hash mismatch {actual_archive}, "
                f"expected {spec['archive_sha256']}"
            )

    destination = VENDOR / spec["member"]
    return extract_member(archive, spec["member"], spec["model_sha256"], destination)

def resolve_s1g() -> Path:
    direct = find_exact_file("s1g.txt", S1G["model_sha256"])
    if direct is not None:
        return direct

    # The earlier qualification cache may use a different filename; hash-check likely small text files.
    for base in common_search_roots():
        try:
            candidates = list(base.rglob("*"))
        except OSError:
            continue
        for p in candidates:
            if not p.is_file() or p.stat().st_size > 1024 * 1024:
                continue
            try:
                if sha256(p) == S1G["model_sha256"]:
                    print(f"MODEL source resolved locally by hash: {p}")
                    return p
            except OSError:
                pass

    destination = VENDOR / "s1g.txt"
    download(S1G["url"], destination)
    actual = sha256(destination)
    if actual != S1G["model_sha256"]:
        raise RuntimeError(
            f"S1G downloaded model hash mismatch {actual}, expected {S1G['model_sha256']}"
        )
    return destination

def measure(text: str, name: str) -> float:
    """Parse LTspice .meas output across scalar and expression-prefixed formats."""
    number = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?"
    prefix = re.compile(rf"^\s*{re.escape(name)}\s*(?::|=)", re.I)
    for line in text.splitlines():
        if not prefix.search(line):
            continue
        equals_values = re.findall(rf"=\s*({number})", line)
        if equals_values:
            return float(equals_values[-1])
        direct = re.search(rf"^\s*{re.escape(name)}\s*:\s*({number})", line, re.I)
        if direct:
            return float(direct.group(1))
    raise RuntimeError(f"missing measurement {name}")

def main() -> int:
    if not LTSPICE.exists():
        print(f"ERROR: LTspice not found: {LTSPICE}")
        return 2
    if not LT5400.exists() or sha256(LT5400) != LT5400_HASH:
        print("ERROR: controlled LT5400 installed library missing/hash mismatch.")
        return 2

    TMP.mkdir(exist_ok=True)
    VENDOR.mkdir(parents=True, exist_ok=True)

    try:
        opa1656 = resolve_zip_source("OPA1656")
        opa1612 = resolve_zip_source("OPA1612")
        that1646 = resolve_zip_source("THAT1646")
        s1g = resolve_s1g()
    except Exception as exc:
        print(f"ERROR: controlled vendor-source resolution failed: {exc}")
        print(f"Diagnostic/source cache retained in {TMP.relative_to(ROOT)}")
        return 2

    wrappers = ROOT / "simulation/models/wrappers"
    cart = ROOT / "simulation/models/cartridges/grado_78c_shellac.lib"
    top = ROOT / "simulation/models/integrated/shellac_top_ae065.lib"

    deck = f"""* AE-065 genuine integrated RUN00
.include "{opa1656}"
.include "{opa1612}"
.include "{that1646}"
.include "{LT5400}"
.include "{s1g}"
.include "{wrappers/'opa1656_shellac.lib'}"
.include "{wrappers/'opa1612_shellac.lib'}"
.include "{wrappers/'lt5400_7_shellac.lib'}"
.include "{wrappers/'that1646_shellac.lib'}"
.include "{cart}"
.include "{top}"

VPLUS VPLUS18 0 18
VMINUS VMINUS18 0 -18
VZERO ZERO_VA 0 0
VBOND CHASSIS ZERO_VA 0

* Zero generated EMF while preserving floating cartridge semantics:
* DRIVE is the cartridge N terminal, hence V(DRIVE,N)=0.
XCARTL CART_L_P CART_L_N CART_L_N SHELLAC_GRADO_78C
XCARTR CART_R_P CART_R_N CART_R_N SHELLAC_GRADO_78C
CCABLEL CART_L_P CART_L_N 100p
CCABLER CART_R_P CART_R_N 100p

X101L CART_L_P CART_L_N N101_L_OUT VPLUS18 VMINUS18 ZERO_VA CHASSIS SHELLAC_SCH101
X101R CART_R_P CART_R_N N101_R_OUT VPLUS18 VMINUS18 ZERO_VA CHASSIS SHELLAC_SCH101
V101L PRE103_L N101_L_OUT 0
V101R PRE103_R N101_R_OUT 0

X103L PRE103_L N103_L_LF N103_L_OUT VPLUS18 VMINUS18 ZERO_VA SHELLAC_SCH103_RIAA
X103R PRE103_R N103_R_LF N103_R_OUT VPLUS18 VMINUS18 ZERO_VA SHELLAC_SCH103_RIAA
V103L N107_L_IN N103_L_OUT 0
V103R N107_R_IN N103_R_OUT 0

X107L N107_L_IN N107_L_OUT N107_L_BYPASS RUMBLE_L_SELECTED VPLUS18 VMINUS18 ZERO_VA SHELLAC_DR039_SCH107
X107R N107_R_IN N107_R_OUT N107_R_BYPASS RUMBLE_R_SELECTED VPLUS18 VMINUS18 ZERO_VA SHELLAC_DR039_SCH107

X104L RUMBLE_L_SELECTED N104_L_OUT MONO_AVG VPLUS18 VMINUS18 ZERO_VA SHELLAC_SCH104
X104R RUMBLE_R_SELECTED N104_R_OUT MONO_R_LEG VPLUS18 VMINUS18 ZERO_VA SHELLAC_SCH104

XMAT N104_L_OUT N104_R_OUT MONO_AVG MONO_R_LEG N105_L_IN N105_R_IN ZERO_VA SHELLAC_SCH105_MATRIX_STEREO
X105L N105_L_IN N105_L_OUT VPLUS18 VMINUS18 ZERO_VA SHELLAC_SCH105_BUFFER
X105R N105_R_IN N105_R_OUT VPLUS18 VMINUS18 ZERO_VA SHELLAC_SCH105_BUFFER

XMUTEL N105_L_OUT N108_L_IN ZERO_VA SHELLAC_SW905_RUN
XMUTER N105_R_OUT N108_R_IN ZERO_VA SHELLAC_SW905_RUN
X108L N108_L_IN XLR_L_POS XLR_L_NEG VPLUS18 VMINUS18 ZERO_VA CHASSIS SHELLAC_SCH108
X108R N108_R_IN XLR_R_POS XLR_R_NEG VPLUS18 VMINUS18 ZERO_VA CHASSIS SHELLAC_SCH108
RLOADL XLR_L_POS XLR_L_NEG 100k
RLOADR XLR_R_POS XLR_R_NEG 100k

.op
.tran 0 1u 0 1u
.meas tran V_N101_L FIND V(N101_L_OUT) AT=1u
.meas tran V_N103_L FIND V(N103_L_OUT) AT=1u
.meas tran V_N104_L FIND V(N104_L_OUT) AT=1u
.meas tran V_N105_L FIND V(N105_L_OUT) AT=1u
.meas tran V_N108_L FIND V(N108_L_IN) AT=1u
.meas tran V_XLR_L_DIFF FIND V(XLR_L_POS,XLR_L_NEG) AT=1u
.meas tran V_XLR_L_CM PARAM (V(XLR_L_POS)+V(XLR_L_NEG))/2
.meas tran V_XLR_R_DIFF FIND V(XLR_R_POS,XLR_R_NEG) AT=1u
.meas tran V_XLR_R_CM PARAM (V(XLR_R_POS)+V(XLR_R_NEG))/2
.end
"""
    cir = TMP / "ae065_integrated_run00.cir"
    cir.write_text(deck, encoding="utf-8", newline="\n")

    proc = subprocess.run(
        [str(LTSPICE), "-b", str(cir)],
        cwd=TMP,
        text=True,
        capture_output=True,
    )
    log = cir.with_suffix(".log")
    log_text = log.read_text(encoding="utf-8", errors="ignore") if log.exists() else ""
    fatal = [
        text for text in (
            "fatal error", "unknown subcircuit", "can't find definition",
            "missing node", "singular matrix", "time step too small",
        )
        if text in log_text.lower()
    ]

    names = [
        "V_N101_L", "V_N103_L", "V_N104_L", "V_N105_L", "V_N108_L",
        "V_XLR_L_DIFF", "V_XLR_L_CM", "V_XLR_R_DIFF", "V_XLR_R_CM",
    ]
    values = {}
    parse_error = None
    if proc.returncode == 0 and log.exists() and not fatal:
        try:
            values = {name: measure(log_text, name) for name in names}
        except Exception as exc:
            parse_error = str(exc)

    checks = {}
    for name in names[:5]:
        if name in values:
            checks[name] = abs(values[name]) <= 1.0
    for name in ("V_XLR_L_DIFF", "V_XLR_R_DIFF"):
        if name in values:
            checks[name] = abs(values[name]) <= 0.025
    for name in ("V_XLR_L_CM", "V_XLR_R_CM"):
        if name in values:
            checks[name] = abs(values[name]) <= 0.250

    passed = (
        proc.returncode == 0
        and log.exists()
        and not fatal
        and parse_error is None
        and len(checks) == len(names)
        and all(checks.values())
    )

    result = {
        "schema_version": 1,
        "authority": "AE-065",
        "run_id": "RUN00_INTEGRATED",
        "model": "SHELLAC_TOP",
        "model_semantics": "SELECTED_NEXT_CANDIDATE_ANALYSIS",
        "repository_commit_before_ae065": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "simulator": "LTspice",
        "simulator_executable_sha256": sha256(LTSPICE),
        "source_resolution": {
            "OPA1656": {"path": str(opa1656), "sha256": sha256(opa1656)},
            "OPA1612": {"path": str(opa1612), "sha256": sha256(opa1612)},
            "THAT1646": {"path": str(that1646), "sha256": sha256(that1646)},
            "S1G": {"path": str(s1g), "sha256": sha256(s1g)},
            "LT5400": {"path": str(LT5400), "sha256": sha256(LT5400)},
        },
        "configuration": {
            "cartridge": "GRADO_78C",
            "gain": "DEFAULT_18DB",
            "bass": "TRUE_RIAA",
            "treble": "2121HZ_RIAA",
            "rumble": "BYPASS",
            "mode": "STEREO",
            "mute": "RUN",
            "cable_pf": 100,
            "load_cap_state": "BASE",
            "output_load_ohm": 100000,
            "rail_plus_v": 18.0,
            "rail_minus_v": -18.0,
            "lf_topology": "BRANCH_LOCAL_DIRECT_BYPASS_BLOCK",
        },
        "returncode": proc.returncode,
        "fatal_terms": fatal,
        "parse_error": parse_error,
        "measurements_v": values,
        "checks": checks,
        "pass": passed,
        "limitations": [
            "RUN00 is structural/DC sanity only, not AC qualification.",
            "SCH108 ferrites use 0.05-ohm DC equivalents; HF behaviour is deferred to RUN06.",
            "1 GOhm sense-cap leakage resistors are numerical aids only, not BOM items.",
            "Only DEFAULT/RIAA/BYPASS/STEREO/RUN is exercised.",
            "AE-042/AE-052 remain selected-next candidate analysis; no generator migration.",
        ],
    }
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print(f"LTspice return code: {proc.returncode}")
    if fatal:
        print("Fatal terms:", ", ".join(fatal))
    if parse_error:
        print("Measurement parse error:", parse_error)
    for name in names:
        if name in values:
            print(f"{name}: {values[name]:.9g} V  {'PASS' if checks.get(name) else 'FAIL'}")
    print(f"AE-065 integrated RUN00: {'PASS' if passed else 'FAIL'}")
    print(f"Result: {RESULT.relative_to(ROOT)}")

    if passed:
        shutil.rmtree(TMP, ignore_errors=True)
        return 0

    print(f"Diagnostic files retained in {TMP.relative_to(ROOT)}")
    return 2

if __name__ == "__main__":
    raise SystemExit(main())
