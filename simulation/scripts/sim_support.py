#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import urllib.request
import zipfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
ACQ_CFG = ROOT / "simulation/config/vendor_source_acquisition.yaml"
LTSPICE = Path.home() / "AppData/Local/Programs/ADI/LTspice/LTspice.exe"

FATAL_TERMS = (
    "fatal error",
    "unknown subcircuit",
    "can't find definition",
    "missing node",
    "singular matrix",
    "time step too small",
)

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def load_acquisition_config() -> dict:
    return yaml.safe_load(ACQ_CFG.read_text(encoding="utf-8"))

def validate_ltspice() -> Path:
    cfg = load_acquisition_config()["ltspice"]
    expected_path = Path.home() / cfg["executable_user_relative_path"]
    if expected_path != LTSPICE:
        raise RuntimeError(f"LTspice configured path mismatch: {expected_path} != {LTSPICE}")
    if not LTSPICE.is_file():
        raise RuntimeError(f"LTspice executable not found: {LTSPICE}")
    actual = sha256(LTSPICE)
    if actual != cfg["executable_sha256"]:
        raise RuntimeError(
            f"LTspice executable hash {actual} != controlled {cfg['executable_sha256']}"
        )
    return LTSPICE

def common_search_roots() -> list[Path]:
    roots = [
        ROOT / ".ae062_vendor_cache",
        ROOT / ".ae062_qualification_tmp",
        ROOT / ".ae063_vendor_cache",
        ROOT / ".ae063_qualification_tmp",
        Path.home() / "Downloads",
    ]
    return [p for p in roots if p.exists()]

def _find_named(basename: str, expected_hash: str) -> Path | None:
    for base in common_search_roots():
        try:
            matches = base.rglob(basename)
        except OSError:
            continue
        for p in matches:
            if p.is_file():
                try:
                    if sha256(p) == expected_hash:
                        print(f"MODEL source resolved locally: {p}")
                        return p
                except OSError:
                    pass
    return None

def _find_archive(expected_hash: str) -> Path | None:
    for base in common_search_roots():
        try:
            matches = base.rglob("*.zip")
        except OSError:
            continue
        for p in matches:
            if p.is_file():
                try:
                    if sha256(p) == expected_hash:
                        print(f"ARCHIVE source resolved locally: {p}")
                        return p
                except OSError:
                    pass
    return None

def _download(url: str, destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 Shellac-Simulation/1.0", "Accept": "*/*"},
    )
    print(f"DOWNLOAD {url}")
    with urllib.request.urlopen(request, timeout=90) as response:
        destination.write_bytes(response.read())
    return destination

def resolve_source(key: str, vendor_dir: Path) -> Path:
    cfg = load_acquisition_config()["sources"][key]
    source_type = cfg["source_type"]

    if source_type == "INSTALLED_LTSPICE_LIBRARY":
        p = Path.home() / cfg["user_relative_path"]
        if not p.is_file():
            raise RuntimeError(f"{key}: installed LTspice library missing: {p}")
        actual = sha256(p)
        if actual != cfg["library_sha256"]:
            raise RuntimeError(f"{key}: installed library hash {actual} != {cfg['library_sha256']}")
        return p

    if source_type == "ZIP_MEMBER":
        direct = _find_named(cfg["member"], cfg["model_sha256"])
        if direct is not None:
            return direct
        archive = _find_archive(cfg["archive_sha256"])
        if archive is None:
            archive = vendor_dir / f"{key}.zip"
            _download(cfg["archive_url"], archive)
            actual_archive = sha256(archive)
            if actual_archive != cfg["archive_sha256"]:
                raise RuntimeError(
                    f"{key}: archive hash {actual_archive} != {cfg['archive_sha256']}"
                )
        with zipfile.ZipFile(archive, "r") as zf:
            matches = [
                name for name in zf.namelist()
                if Path(name).name.lower() == cfg["member"].lower()
            ]
            if len(matches) != 1:
                raise RuntimeError(f"{key}: expected one {cfg['member']}, found {matches}")
            data = zf.read(matches[0])
        out = vendor_dir / cfg["member"]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
        actual_model = sha256(out)
        if actual_model != cfg["model_sha256"]:
            raise RuntimeError(
                f"{key}: model hash {actual_model} != {cfg['model_sha256']}"
            )
        return out

    if source_type == "DIRECT_FILE":
        direct = _find_named(cfg["filename"], cfg["model_sha256"])
        if direct is not None:
            return direct
        out = vendor_dir / cfg["filename"]
        _download(cfg["file_url"], out)
        actual = sha256(out)
        if actual != cfg["model_sha256"]:
            raise RuntimeError(f"{key}: model hash {actual} != {cfg['model_sha256']}")
        return out

    raise RuntimeError(f"{key}: unsupported source_type {source_type!r}")

def parse_measure(text: str, name: str) -> float:
    """Parse LTspice .meas values, including AC dB/phase tuple output."""
    number = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?"
    prefix = re.compile(rf"^\s*{re.escape(name)}\s*(?::|=)", re.I)
    for line in text.splitlines():
        if not prefix.search(line):
            continue

        lower = line.lower()

        # Current LTspice can emit mag(...) AC measurements as dB tuples:
        # name: mag(V(...))=(-0.085274dB,0°) at 1000
        if "mag(" in lower:
            m = re.search(rf"=\s*\(\s*({number})\s*dB", line, re.I)
            if m:
                return 10.0 ** (float(m.group(1)) / 20.0)

        # Preserve signed phase in degrees.
        if "ph(" in lower:
            m = re.search(rf"=\s*\(\s*({number})", line, re.I)
            if m:
                return float(m.group(1))

        # Generic tuple fallback.
        m = re.search(rf"=\s*\(\s*({number})", line)
        if m:
            return float(m.group(1))

        # Scalar expression.
        values = re.findall(rf"=\s*({number})", line)
        if values:
            return float(values[-1])

        # Direct scalar.
        m = re.search(rf"^\s*{re.escape(name)}\s*:\s*({number})", line, re.I)
        if m:
            return float(m.group(1))
    raise RuntimeError(f"missing measurement {name}")

def _decode_ltspice_log(path: Path) -> str:
    data = path.read_bytes()
    if data.startswith(b"\xff\xfe"):
        return data.decode("utf-16-le", errors="replace")
    if data.startswith(b"\xfe\xff"):
        return data.decode("utf-16-be", errors="replace")
    if data and data.count(b"\x00") > len(data) // 4:
        return data.decode("utf-16-le", errors="replace")
    for encoding in ("utf-8", "cp1252"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            pass
    return data.decode("utf-8", errors="replace")


def execute_deck(name: str, deck: str, workdir: Path) -> str:
    """Run LTspice from local TEMP using current -b -run batch syntax."""
    validate_ltspice()
    workdir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="Shellac_LTspice_") as tmp:
        local = Path(tmp)
        cir = local / f"{name}.cir"
        cir.write_text(deck, encoding="utf-8", newline="\n")

        try:
            proc = subprocess.run(
                [str(LTSPICE), "-b", "-run", str(cir)],
                cwd=local,
                text=True,
                capture_output=True,
                timeout=60,
            )
        except subprocess.TimeoutExpired as exc:
            # Preserve the exact timeout stimulus and any partial LTspice log
            # before TemporaryDirectory cleanup. This is diagnostic evidence,
            # not a successful simulation result.
            log = cir.with_suffix(".log")
            shutil.copy2(cir, workdir / cir.name)
            if log.exists():
                shutil.copy2(log, workdir / log.name)
            raise RuntimeError(
                f"{name}: LTspice batch execution timed out after 60 s; "
                f"diagnostic deck/log retained under {workdir}; "
                "treat any persistent interactive LTspice window as a launch failure"
            ) from exc
        log = cir.with_suffix(".log")
        log_text = _decode_ltspice_log(log) if log.exists() else ""

        shutil.copy2(cir, workdir / cir.name)
        if log.exists():
            shutil.copy2(log, workdir / log.name)

        low = log_text.lower()
        fatal = [term for term in FATAL_TERMS if term in low]
        launch_failures = [
            term for term in (
                "could not open input deck",
                "can't open input deck",
                "cannot open input deck",
                "no such file or directory",
            )
            if term in low
        ]
        if proc.returncode != 0 or not log.exists() or fatal or launch_failures:
            raise RuntimeError(
                f"{name}: LTspice execution failed returncode={proc.returncode}, "
                f"fatal={fatal}, launch_failures={launch_failures}, "
                f"stdout={proc.stdout[-1000:]!r}, stderr={proc.stderr[-1000:]!r}, "
                f"log_tail={log_text[-1500:]!r}"
            )
        return log_text

def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
    tmp.replace(path)
