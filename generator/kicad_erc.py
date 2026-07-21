"""Native KiCad ERC execution and report summarisation."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import os
import re
import shutil
import subprocess
import time


_VIOLATION = re.compile(r"^\[([^\]]+)\]:", re.MULTILINE)


def find_kicad_cli() -> Path:
    discovered = shutil.which("kicad-cli")
    if discovered:
        return Path(discovered)
    program_files = Path(os.environ.get("ProgramFiles", r"C:\Program Files"))
    candidate = program_files / "KiCad" / "9.0" / "bin" / "kicad-cli.exe"
    if candidate.exists():
        return candidate
    raise FileNotFoundError(
        "KiCad 9 command-line tools were not found. Add kicad-cli to PATH or install KiCad 9."
    )


def summarise_erc_report(report_text: str) -> dict[str, int]:
    return dict(sorted(Counter(_VIOLATION.findall(report_text)).items()))


def run_hierarchical_erc(
    schematic: Path, report: Path, executable: Path | None = None,
) -> dict[str, int]:
    executable = executable or find_kicad_cli()
    report.parent.mkdir(parents=True, exist_ok=True)
    completed = None
    for attempt in range(2):
        completed = subprocess.run(
            [str(executable), "sch", "erc", "--output", str(report), str(schematic)],
            capture_output=True, text=True, check=False,
        )
        if completed.returncode == 0:
            break
        if attempt == 0:
            time.sleep(0.25)
    assert completed is not None
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(
            f"KiCad hierarchical ERC failed with exit code {completed.returncode}: {detail}"
        )
    return summarise_erc_report(report.read_text(encoding="utf-8"))
