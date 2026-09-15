from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from simulation.scripts import sim_support


def test_execute_deck_retains_timeout_deck_and_partial_log(tmp_path, monkeypatch):
    monkeypatch.setattr(sim_support, "validate_ltspice", lambda: sim_support.LTSPICE)

    def fake_run(args, cwd, text, capture_output, timeout):
        cir = Path(args[-1])
        cir.with_suffix(".log").write_text("partial timeout log\n", encoding="utf-8")
        raise subprocess.TimeoutExpired(args, timeout)

    monkeypatch.setattr(sim_support.subprocess, "run", fake_run)

    workdir = tmp_path / "diagnostics"
    with pytest.raises(RuntimeError, match="diagnostic deck/log retained"):
        sim_support.execute_deck("timeout_probe", ".op\n.end\n", workdir)

    assert (workdir / "timeout_probe.cir").read_text(encoding="utf-8") == ".op\n.end\n"
    assert (workdir / "timeout_probe.log").read_text(encoding="utf-8") == "partial timeout log\n"
