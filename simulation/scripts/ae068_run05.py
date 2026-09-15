#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import yaml

from simulation.scripts.sim_support import (
    ROOT,
    execute_deck,
    parse_measure,
    resolve_source,
    sha256,
    validate_ltspice,
    write_json,
)

CFG = ROOT / "simulation/config/ae068_run05_matrix.yaml"
MODEL = ROOT / "simulation/models/qualification/sch104_sch105_ae068.lib"
WRAPPER = ROOT / "simulation/models/wrappers/opa1656_shellac.lib"
TMP = ROOT / ".ae068_run05_tmp"
VENDOR = TMP / "vendor"
RESULT_DIR = ROOT / "simulation/results/run05_matrix"
RESULT_JSON = RESULT_DIR / "ae068_run05.json"
RESULT_CSV = RESULT_DIR / "ae068_run05.csv"
RESULT_MD = RESULT_DIR / "ae068_run05.md"
DESIGN_RECORD = ROOT / "docs/design_pack/AE-068_RUN05_SCH104_SCH105_Matrix_Evidence_Rev_A0.md"

MODES = {
    "DUAL_L": "AE068_MATRIX_DUAL_L",
    "STEREO": "AE068_MATRIX_STEREO",
    "MONO": "AE068_MATRIX_MONO",
    "DUAL_R": "AE068_MATRIX_DUAL_R",
}

def db20(x: float) -> float:
    if x <= 0:
        return -300.0
    return 20.0 * math.log10(x)

def sep_db(victim: float, wanted: float) -> float:
    if victim <= 0:
        return 300.0
    if wanted <= 0:
        return -300.0
    return -db20(victim / wanted)

def preamble(opa: Path) -> str:
    return f""".options meascplxfmt=cartesian measdgt=12
.include "{opa}"
.include "{WRAPPER}"
.include "{MODEL}"
VPLUS VPLUS18 0 18
VMINUS VMINUS18 0 -18
VZERO ZERO_VA 0 0
"""

def source_line(name: str, node: str, mag: float, phase: float) -> str:
    return f"V{name} {node} ZERO_VA AC {mag:.12g} {phase:.12g}"

def static_case(
    tag: str,
    mode: str,
    stim: dict,
    opa: Path,
    cfg: dict,
    *,
    cpar_pf: float,
    rret: float,
    rmono_l: float,
    rmono_r: float,
) -> dict:
    report = cfg["execution"]["report_hz"]
    measures = []
    for f in report:
        measures += [
            f".meas ac LO_{f} FIND mag(V(LOUT)) AT={f}",
            f".meas ac RO_{f} FIND mag(V(ROUT)) AT={f}",
            f".meas ac LP_{f} FIND ph(V(LOUT)) AT={f}",
            f".meas ac RP_{f} FIND ph(V(ROUT)) AT={f}",
        ]

    cpar_f = cpar_pf * 1e-12
    deck = preamble(opa) + f"""
{source_line("L", "LIN", float(stim["left_mag"]), float(stim["left_phase_deg"]))}
{source_line("R", "RIN", float(stim["right_mag"]), float(stim["right_phase_deg"]))}
X104 LIN RIN BL BR MAVG MRLEG VPLUS18 VMINUS18 ZERO_VA AE068_SCH104_PAIR
+ RMONOL={rmono_l:.12g} RMONOR={rmono_r:.12g}
XM BL BR MAVG MRLEG LOUT ROUT VPLUS18 VMINUS18 ZERO_VA {MODES[mode]}
+ RRET={rret:.12g} CPAR={cpar_f:.12g}
RLOADL LOUT ZERO_VA {int(cfg["execution"]["measurement_load_ohm"])}
RLOADR ROUT ZERO_VA {int(cfg["execution"]["measurement_load_ohm"])}
.ac dec 120 10 100k
{chr(10).join(measures)}
.end
"""
    log = execute_deck(tag, deck, TMP / "static")
    return {
        "left_mag": {str(f): parse_measure(log, f"LO_{f}") for f in report},
        "right_mag": {str(f): parse_measure(log, f"RO_{f}") for f in report},
        "left_phase_deg": {str(f): parse_measure(log, f"LP_{f}") for f in report},
        "right_phase_deg": {str(f): parse_measure(log, f"RP_{f}") for f in report},
    }

def direct_insertion(cfg: dict, opa: Path) -> dict:
    ideal_pf = 0.001
    rret = float(cfg["execution"]["nominal_return_ohm"])
    rmono = float(cfg["execution"]["nominal_sum_resistor_ohm"])
    frequencies = cfg["execution"]["report_hz"]
    cases = {}
    for mode, stim_name in (
        ("DUAL_L", "L_ONLY"),
        ("STEREO", "L_ONLY"),
        ("STEREO", "R_ONLY"),
        ("DUAL_R", "R_ONLY"),
    ):
        key = f"{mode}_{stim_name}"
        x = static_case(
            "run05_direct_" + key.lower(),
            mode,
            cfg["stimuli"][stim_name],
            opa,
            cfg,
            cpar_pf=ideal_pf,
            rret=rret,
            rmono_l=rmono,
            rmono_r=rmono,
        )
        wanted_nodes = ["left_mag", "right_mag"] if mode in ("DUAL_L", "DUAL_R") else (
            ["left_mag"] if stim_name == "L_ONLY" else ["right_mag"]
        )
        errors = {}
        for node in wanted_nodes:
            errors[node] = {str(f): db20(x[node][str(f)]) for f in frequencies}
        cases[key] = {"raw": x, "insertion_db": errors}

    worst = max(
        abs(v)
        for case in cases.values()
        for node in case["insertion_db"].values()
        for v in node.values()
    )
    return {
        "cases": cases,
        "worst_abs_insertion_db": worst,
        "pass": worst <= float(cfg["criteria"]["direct_insertion_db_max"]) + 1e-12,
    }

def mono_nominal(cfg: dict, opa: Path) -> dict:
    rret = float(cfg["execution"]["nominal_return_ohm"])
    rmono = float(cfg["execution"]["nominal_sum_resistor_ohm"])
    qpf = float(cfg["execution"]["qualification_parasitic_pf"])
    equal = static_case(
        "run05_mono_equal", "MONO", cfg["stimuli"]["EQUAL"], opa, cfg,
        cpar_pf=qpf, rret=rret, rmono_l=rmono, rmono_r=rmono,
    )
    left = static_case(
        "run05_mono_lonly", "MONO", cfg["stimuli"]["L_ONLY"], opa, cfg,
        cpar_pf=qpf, rret=rret, rmono_l=rmono, rmono_r=rmono,
    )
    right = static_case(
        "run05_mono_ronly", "MONO", cfg["stimuli"]["R_ONLY"], opa, cfg,
        cpar_pf=qpf, rret=rret, rmono_l=rmono, rmono_r=rmono,
    )
    unequal = static_case(
        "run05_mono_unequal", "MONO", cfg["stimuli"]["UNEQUAL"], opa, cfg,
        cpar_pf=qpf, rret=rret, rmono_l=rmono, rmono_r=rmono,
    )
    opposite = static_case(
        "run05_mono_opposite", "MONO", cfg["stimuli"]["OPPOSITE"], opa, cfg,
        cpar_pf=qpf, rret=rret, rmono_l=rmono, rmono_r=rmono,
    )

    fkey = "1000"
    equal_err_l = db20(equal["left_mag"][fkey])
    equal_err_r = db20(equal["right_mag"][fkey])
    w_l = left["left_mag"][fkey]
    w_r = right["left_mag"][fkey]
    mismatch = 100.0 * abs(w_l - w_r) / ((w_l + w_r) / 2.0)
    residual = max(opposite["left_mag"][fkey], opposite["right_mag"][fkey])
    cancel = -db20(residual) if residual > 0 else 300.0

    expected_unequal = w_l * 1.0 + w_r * 0.5
    unequal_actual = unequal["left_mag"][fkey]
    unequal_delta = db20(unequal_actual / expected_unequal) if expected_unequal > 0 else 0.0

    crit = cfg["criteria"]
    hard = (
        abs(equal_err_l) <= float(crit["mono_equal_insertion_db_max"]) + 1e-12
        and abs(equal_err_r) <= float(crit["mono_equal_insertion_db_max"]) + 1e-12
        and mismatch <= float(crit["mono_weight_mismatch_percent_max"]) + 1e-12
    )
    preferred = (
        abs(equal_err_l) <= float(crit["mono_equal_insertion_db_preferred"]) + 1e-12
        and abs(equal_err_r) <= float(crit["mono_equal_insertion_db_preferred"]) + 1e-12
        and mismatch <= float(crit["mono_weight_mismatch_percent_preferred"]) + 1e-12
    )
    return {
        "equal": equal,
        "left_only": left,
        "right_only": right,
        "unequal": unequal,
        "opposite_phase": opposite,
        "equal_insertion_db_1khz": {"left": equal_err_l, "right": equal_err_r},
        "left_weight_1khz": w_l,
        "right_weight_1khz": w_r,
        "weight_mismatch_percent_1khz": mismatch,
        "opposite_phase_residual_1khz": residual,
        "opposite_phase_cancellation_db_1khz": cancel,
        "unequal_linearity_delta_db_1khz": unequal_delta,
        "hard_pass": hard,
        "preferred_pass": preferred,
    }

def truth_table(cfg: dict, opa: Path) -> dict:
    qpf = float(cfg["execution"]["qualification_parasitic_pf"])
    rret = float(cfg["execution"]["nominal_return_ohm"])
    rmono = float(cfg["execution"]["nominal_sum_resistor_ohm"])
    out = {}
    for mode in MODES:
        out[mode] = {}
        for stim_name, stim in cfg["stimuli"].items():
            out[mode][stim_name] = static_case(
                f"run05_truth_{mode.lower()}_{stim_name.lower()}",
                mode, stim, opa, cfg,
                cpar_pf=qpf, rret=rret, rmono_l=rmono, rmono_r=rmono,
            )
    return out

def stereo_crosstalk(cfg: dict, opa: Path) -> dict:
    rret = float(cfg["execution"]["nominal_return_ohm"])
    rmono = float(cfg["execution"]["nominal_sum_resistor_ohm"])
    freqs = cfg["execution"]["crosstalk_hz"]
    sweep = {}
    for pf in cfg["execution"]["parasitic_sweep_pf"]:
        pf = float(pf)
        l = static_case(
            f"run05_xtalk_l_{pf:g}pf", "STEREO", cfg["stimuli"]["L_ONLY"], opa, cfg,
            cpar_pf=pf, rret=rret, rmono_l=rmono, rmono_r=rmono,
        )
        r = static_case(
            f"run05_xtalk_r_{pf:g}pf", "STEREO", cfg["stimuli"]["R_ONLY"], opa, cfg,
            cpar_pf=pf, rret=rret, rmono_l=rmono, rmono_r=rmono,
        )
        sep_l_to_r = {}
        sep_r_to_l = {}
        for f in freqs:
            k = str(f)
            sep_l_to_r[k] = sep_db(l["right_mag"][k], l["left_mag"][k])
            sep_r_to_l[k] = sep_db(r["left_mag"][k], r["right_mag"][k])
        sweep[str(pf)] = {
            "l_to_r_separation_db": sep_l_to_r,
            "r_to_l_separation_db": sep_r_to_l,
        }

    q = sweep[str(float(cfg["execution"]["qualification_parasitic_pf"]))]
    worst_1k = min(q["l_to_r_separation_db"]["1000"], q["r_to_l_separation_db"]["1000"])
    worst_20k = min(q["l_to_r_separation_db"]["20000"], q["r_to_l_separation_db"]["20000"])
    crit = cfg["criteria"]
    return {
        "parasitic_sweep_pf": sweep,
        "qualification_parasitic_pf": float(cfg["execution"]["qualification_parasitic_pf"]),
        "qualification_worst_separation_db_1khz": worst_1k,
        "qualification_worst_separation_db_20khz": worst_20k,
        "hard_pass": (
            worst_1k >= float(crit["stereo_separation_db_1khz_min"]) - 1e-9
            and worst_20k >= float(crit["stereo_separation_db_20khz_min"]) - 1e-9
        ),
        "preferred_1khz_pass": worst_1k >= float(crit["stereo_separation_db_1khz_preferred"]) - 1e-9,
    }

def dormant_coupling(cfg: dict, opa: Path) -> dict:
    qpf = float(cfg["execution"]["qualification_parasitic_pf"])
    rret = float(cfg["execution"]["nominal_return_ohm"])
    rmono = float(cfg["execution"]["nominal_sum_resistor_ohm"])
    dl = static_case(
        "run05_dormant_dual_l", "DUAL_L", cfg["stimuli"]["R_ONLY"], opa, cfg,
        cpar_pf=qpf, rret=rret, rmono_l=rmono, rmono_r=rmono,
    )
    dr = static_case(
        "run05_dormant_dual_r", "DUAL_R", cfg["stimuli"]["L_ONLY"], opa, cfg,
        cpar_pf=qpf, rret=rret, rmono_l=rmono, rmono_r=rmono,
    )
    return {
        "qualification_parasitic_pf": qpf,
        "DUAL_L_R_ONLY": dl,
        "DUAL_R_L_ONLY": dr,
        "note": "Informative dormant-input coupling; DUAL L/R deliberate duplication is excluded from stereo separation criteria.",
    }

def return_sweep(cfg: dict, opa: Path) -> dict:
    rmono = float(cfg["execution"]["nominal_sum_resistor_ohm"])
    ideal_pf = 0.001
    out = {}
    for rret in cfg["execution"]["return_sweep_ohm"]:
        rret = float(rret)
        direct = static_case(
            f"run05_rret_direct_{int(rret)}", "STEREO", cfg["stimuli"]["L_ONLY"], opa, cfg,
            cpar_pf=ideal_pf, rret=rret, rmono_l=rmono, rmono_r=rmono,
        )
        mono = static_case(
            f"run05_rret_mono_{int(rret)}", "MONO", cfg["stimuli"]["EQUAL"], opa, cfg,
            cpar_pf=ideal_pf, rret=rret, rmono_l=rmono, rmono_r=rmono,
        )
        out[str(int(rret))] = {
            "direct_insertion_db_1khz": db20(direct["left_mag"]["1000"]),
            "mono_equal_insertion_db_1khz": db20(mono["left_mag"]["1000"]),
        }
    return out

def mismatch_sweep(cfg: dict, opa: Path) -> dict:
    rret = float(cfg["execution"]["nominal_return_ohm"])
    rnom = float(cfg["execution"]["nominal_sum_resistor_ohm"])
    qpf = float(cfg["execution"]["qualification_parasitic_pf"])
    out = {}
    for pair_mismatch in cfg["execution"]["mono_pair_mismatch_percent"]:
        pair_mismatch = float(pair_mismatch)
        frac = pair_mismatch / 100.0
        rl = rnom * (1.0 + frac / 2.0)
        rr = rnom * (1.0 - frac / 2.0)
        left = static_case(
            f"run05_mm_l_{pair_mismatch:g}", "MONO", cfg["stimuli"]["L_ONLY"], opa, cfg,
            cpar_pf=qpf, rret=rret, rmono_l=rl, rmono_r=rr,
        )
        right = static_case(
            f"run05_mm_r_{pair_mismatch:g}", "MONO", cfg["stimuli"]["R_ONLY"], opa, cfg,
            cpar_pf=qpf, rret=rret, rmono_l=rl, rmono_r=rr,
        )
        wl = left["left_mag"]["1000"]
        wr = right["left_mag"]["1000"]
        wm = 100.0 * abs(wl - wr) / ((wl + wr) / 2.0)
        out[str(pair_mismatch)] = {
            "rmono_l_ohm": rl,
            "rmono_r_ohm": rr,
            "left_weight_1khz": wl,
            "right_weight_1khz": wr,
            "weight_mismatch_percent_1khz": wm,
            "pass_max_0p25_percent": wm <= float(cfg["criteria"]["mono_weight_mismatch_percent_max"]) + 1e-12,
        }
    return out

def write_csv(path: Path, result: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = [
        ["metric", "value", "unit", "pass"],
        ["direct_worst_abs_insertion", result["direct_insertion"]["worst_abs_insertion_db"], "dB", result["direct_insertion"]["pass"]],
        ["mono_equal_left", result["mono_nominal"]["equal_insertion_db_1khz"]["left"], "dB", result["mono_nominal"]["hard_pass"]],
        ["mono_weight_mismatch", result["mono_nominal"]["weight_mismatch_percent_1khz"], "%", result["mono_nominal"]["hard_pass"]],
        ["stereo_sep_1khz", result["stereo_crosstalk"]["qualification_worst_separation_db_1khz"], "dB", result["stereo_crosstalk"]["hard_pass"]],
        ["stereo_sep_20khz", result["stereo_crosstalk"]["qualification_worst_separation_db_20khz"], "dB", result["stereo_crosstalk"]["hard_pass"]],
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)

def write_markdown(path: Path, result: dict) -> None:
    d = result["direct_insertion"]
    m = result["mono_nominal"]
    x = result["stereo_crosstalk"]
    lines = [
        "# AE-068 RUN05 summary",
        "",
        f"- Direct-path worst insertion: {d['worst_abs_insertion_db']:.6f} dB — {'PASS' if d['pass'] else 'FAIL'}",
        f"- Mono equal insertion L/R @1k: {m['equal_insertion_db_1khz']['left']:+.6f} / {m['equal_insertion_db_1khz']['right']:+.6f} dB — {'PASS' if m['hard_pass'] else 'FAIL'}",
        f"- Mono nominal weight mismatch @1k: {m['weight_mismatch_percent_1khz']:.6f}% ",
        f"- Stereo separation @ {x['qualification_parasitic_pf']:.1f} pF bracket: {x['qualification_worst_separation_db_1khz']:.2f} dB @1k, {x['qualification_worst_separation_db_20khz']:.2f} dB @20k — {'PASS' if x['hard_pass'] else 'FAIL'}",
        "",
        "Full switching transient remains RUN12; full-system noise remains RUN09; tolerance/sensitivity remains RUN10.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

def write_design_record(result: dict) -> None:
    d = result["direct_insertion"]
    m = result["mono_nominal"]
    x = result["stereo_crosstalk"]
    lines = [
        "# AE-068 — RUN05 SCH104/SCH105 Matrix Evidence — Rev A0",
        "",
        "**Project:** Shellac",
        "**Status:** EVIDENCE_COMPLETE_REVIEW_REQUIRED",
        f"**Execution baseline:** `{result['repository_commit_before_ae068']}`",
        "",
        "## Purpose",
        "Execute AE-050 RUN05 against the selected AE-041 A1 / AE-046 SCH104/SCH105 architecture without migrating the product generator.",
        "",
        "## Phase-A scope",
        "- all four routing modes;",
        "- L-only, R-only, equal, unequal and opposite-phase stimuli;",
        "- direct-path insertion;",
        "- mono insertion and L/R weighting;",
        "- stereo crosstalk with a conservative selector/PCB parasitic sweep;",
        "- dormant-input coupling in DUAL L / DUAL R;",
        "- 2.2 MOhm return-value steady-state sweep;",
        "- 4.7 kOhm mono-pair mismatch sweep.",
        "",
        "The parasitic model is deliberately a lumped engineering bracket, not a claimed manufacturer switch model.",
        "",
        "## Headline evidence",
        f"- direct worst insertion: {d['worst_abs_insertion_db']:.6f} dB — {'PASS' if d['pass'] else 'FAIL'};",
        f"- mono equal insertion @1k: {m['equal_insertion_db_1khz']['left']:+.6f} dB left / {m['equal_insertion_db_1khz']['right']:+.6f} dB right;",
        f"- mono nominal weighting mismatch @1k: {m['weight_mismatch_percent_1khz']:.6f}%;",
        f"- stereo separation with {x['qualification_parasitic_pf']:.1f} pF lumped bracket: {x['qualification_worst_separation_db_1khz']:.2f} dB @1k / {x['qualification_worst_separation_db_20khz']:.2f} dB @20k.",
        "",
        "## Decision boundary",
        "This Phase-A evidence does not auto-promote SCH105 to implemented/qualified authority and does not freeze an exact switch parasitic capacitance.",
        "",
        "## Deferred qualification",
        "- RUN09 full-system noise;",
        "- RUN10 tolerance/sensitivity;",
        "- RUN12 adjacent BBM switching transients, muted and live;",
        "- production-switch continuity mapping and bench correlation.",
        "",
        "## Evidence",
        "- `simulation/results/run05_matrix/ae068_run05.json`",
        "- `simulation/results/run05_matrix/ae068_run05.csv`",
        "- `simulation/results/run05_matrix/ae068_run05.md`",
    ]
    DESIGN_RECORD.parent.mkdir(parents=True, exist_ok=True)
    DESIGN_RECORD.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

def main() -> int:
    cfg = yaml.safe_load(CFG.read_text(encoding="utf-8"))
    validate_ltspice()
    opa = resolve_source("OPA1656", VENDOR)

    print("\n=== AE-068 RUN05: SCH104/SCH105 matrix qualification ===")

    direct = direct_insertion(cfg, opa)
    print(f"Direct insertion worst: {direct['worst_abs_insertion_db']:.6f} dB ({'PASS' if direct['pass'] else 'FAIL'})")

    mono = mono_nominal(cfg, opa)
    print(
        "Mono @1k: "
        f"L={mono['equal_insertion_db_1khz']['left']:+.6f} dB, "
        f"R={mono['equal_insertion_db_1khz']['right']:+.6f} dB, "
        f"weight mismatch={mono['weight_mismatch_percent_1khz']:.6f}% "
        f"({'PASS' if mono['hard_pass'] else 'FAIL'})"
    )

    xtalk = stereo_crosstalk(cfg, opa)
    print(
        f"Stereo separation @ {xtalk['qualification_parasitic_pf']:.1f} pF bracket: "
        f"{xtalk['qualification_worst_separation_db_1khz']:.2f} dB @1k, "
        f"{xtalk['qualification_worst_separation_db_20khz']:.2f} dB @20k "
        f"({'PASS' if xtalk['hard_pass'] else 'FAIL'})"
    )

    truth = truth_table(cfg, opa)
    dormant = dormant_coupling(cfg, opa)
    returns = return_sweep(cfg, opa)
    mismatch = mismatch_sweep(cfg, opa)

    result = {
        "schema_version": 1,
        "authority": "AE-068",
        "run_id": "RUN05",
        "title": "SCH104/SCH105 matrix qualification",
        "repository_commit_before_ae068": cfg["baseline_commit"],
        "model_semantics": cfg["model_semantics"],
        "generator_migration_implied": False,
        "status": "EVIDENCE_COMPLETE_REVIEW_REQUIRED",
        "direct_insertion": direct,
        "mono_nominal": mono,
        "stereo_crosstalk": xtalk,
        "truth_table": truth,
        "dormant_path_coupling": dormant,
        "return_resistor_sweep": returns,
        "mono_pair_mismatch_sweep": mismatch,
        "criteria": cfg["criteria"],
        "decision": {
            "automatic_architecture_promotion": False,
            "review_required": True,
        },
        "open_qualification": {
            "RUN09": "full-system noise",
            "RUN10": "tolerance/sensitivity and value engineering",
            "RUN12": "adjacent BBM matrix switching, muted/live",
            "BENCH": "switch mapping, parasitic correlation and prototype verification",
        },
        "model_sources": {
            "OPA1656": {"path": opa.name, "sha256": sha256(opa)},
            "qualification_model_sha256": sha256(MODEL),
        },
    }

    write_json(RESULT_JSON, result)
    write_csv(RESULT_CSV, result)
    write_markdown(RESULT_MD, result)
    write_design_record(result)

    hard_pass = direct["pass"] and mono["hard_pass"] and xtalk["hard_pass"]
    print("\n=== RUN05 PHASE-A SUMMARY ===")
    print(f"Direct insertion: {'PASS' if direct['pass'] else 'FAIL'}")
    print(f"Mono steady-state: {'PASS' if mono['hard_pass'] else 'FAIL'}")
    print(f"Stereo crosstalk bracket: {'PASS' if xtalk['hard_pass'] else 'FAIL'}")
    print(f"AE-068 RUN05 Phase A: {'EVIDENCE_COMPLETE_REVIEW_REQUIRED' if hard_pass else 'EVIDENCE_COMPLETE_WITH_FAILURE_REVIEW_REQUIRED'}")
    print(f"Result: {RESULT_JSON.relative_to(ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
