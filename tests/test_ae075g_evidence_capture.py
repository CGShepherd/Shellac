from pathlib import Path
import json
import subprocess

JSON_EVIDENCE = Path(
    "simulation/results/ae075g_pre90_output/ae075g_pre90_output.json"
)
MD_EVIDENCE = Path(
    "simulation/results/ae075g_pre90_output/ae075g_pre90_output.md"
)


def test_ae075g_pre90_controlled_evidence_exists_and_is_coherent():
    assert JSON_EVIDENCE.is_file()
    assert MD_EVIDENCE.is_file()

    data = json.loads(JSON_EVIDENCE.read_text(encoding="utf-8"))
    assert data["authority"] == "AE-075G"
    assert (
        data["status"]
        == "LOAD_COMPATIBILITY_PASS_HIGH_LEVEL_MARGIN_REQUIRES_BENCH_CONFIRMATION"
    )
    assert data["historical_run06_modified"] is False
    assert data["headline"]["load_compatibility_pass"] is True
    assert data["headline"]["dc_absolute_pass"] is True
    assert data["headline"]["hf_small_signal_evidence_complete"] is True
    assert data["bench_gates_retained"]["output_load_cable_stability_bench_gate_retained"] is True
    assert data["bench_gates_retained"]["dynamic_thd_bench_gate_retained"] is True
    assert data["bench_gates_retained"]["output_header_xy_provisional"] is True

    md = MD_EVIDENCE.read_text(encoding="utf-8")
    assert "LOAD_COMPATIBILITY_PASS_HIGH_LEVEL_MARGIN_REQUIRES_BENCH_CONFIRMATION" in md
    assert "Worst absolute insertion loss vs 100 kOhm: 0.209239 dB" in md
    assert "worst_high_gain: 9.098397 Vrms" in md
    assert "RUN06 load/cable stability and dynamic-THD bench gates remain open." in md
    assert "H801/H802 XY remains provisional" in md


def test_ae075g_pre90_evidence_is_explicitly_unignored():
    ignore = Path(".gitignore").read_text(encoding="utf-8")
    required = (
        "!simulation/results/ae075g_pre90_output/",
        "simulation/results/ae075g_pre90_output/*",
        "!simulation/results/ae075g_pre90_output/ae075g_pre90_output.json",
        "!simulation/results/ae075g_pre90_output/ae075g_pre90_output.md",
    )
    for entry in required:
        assert entry in ignore

    for path in (JSON_EVIDENCE, MD_EVIDENCE):
        p = subprocess.run(
            ["git", "check-ignore", "-q", "--", path.as_posix()],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        assert p.returncode == 1, (
            f"{path} is still ignored by Git: stdout={p.stdout!r} stderr={p.stderr!r}"
        )

def test_ae075g_pre90_evidence_is_on_git_control_surface():
    paths = (JSON_EVIDENCE.as_posix(), MD_EVIDENCE.as_posix())

    tracked = subprocess.run(
        ["git", "ls-files", "--cached", "--", *paths],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    untracked_visible = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "--", *paths],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )

    visible = {
        line.strip().replace("\\", "/")
        for line in (tracked.stdout + untracked_visible.stdout).splitlines()
        if line.strip()
    }
    for path in paths:
        assert path in visible, (
            f"{path} is neither tracked nor visible as untracked controlled evidence"
        )
