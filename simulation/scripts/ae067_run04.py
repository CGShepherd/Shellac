#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
import re
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

CFG = ROOT / "simulation/config/ae067_run04_lf_trade.yaml"
MODEL = ROOT / "simulation/models/qualification/dr039_sch107_ae067.lib"
WRAPPER = ROOT / "simulation/models/wrappers/opa1656_shellac.lib"
TMP = ROOT / ".ae067_run04_tmp"
VENDOR = TMP / "vendor"
RESULT_DIR = ROOT / "simulation/results/run04_lf_trade"
RESULT_JSON = RESULT_DIR / "ae067_run04.json"
RESULT_CSV = RESULT_DIR / "ae067_run04.csv"
RESULT_MD = RESULT_DIR / "ae067_run04.md"
DESIGN_RECORD = ROOT / "docs/design_pack/AE-067_RUN04_DR039_SCH107_LF_Trade_Evidence_Rev_A0.md"

def db(x: float) -> float:
    if x <= 0:
        return -300.0
    return 20.0 * math.log10(x)

def optional_measure(text: str, name: str):
    try:
        return parse_measure(text, name)
    except RuntimeError:
        return None

def parse_when_time(text: str, name: str) -> float:
    prefix = name.strip().lower() + ":"
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.lower().startswith(prefix):
            continue
        marker = stripped.upper().rfind(" AT ")
        if marker < 0:
            continue
        token = stripped[marker + 4:].strip()
        try:
            return float(token)
        except ValueError:
            continue
    raise RuntimeError(f"missing timing measurement {name}")

def preamble(opa: Path) -> str:
    return f""".options meascplxfmt=cartesian measdgt=12
.include "{opa}"
.include "{WRAPPER}"
.include "{MODEL}"
VPLUS VPLUS18 0 18
VMINUS VMINUS18 0 -18
VZERO ZERO_VA 0 0
"""

def unwrap_delta_deg(delta: float) -> float:
    while delta > 180.0:
        delta -= 360.0
    while delta < -180.0:
        delta += 360.0
    return delta

def group_delay_ms(phi_minus: float, phi_plus: float, f_minus: float, f_plus: float) -> float:
    dphi = unwrap_delta_deg(phi_plus - phi_minus)
    return -1000.0 * dphi / (360.0 * (f_plus - f_minus))

def analytical_sk_hp(f: float, r1: float, r2: float, c: float) -> complex:
    s = 1j * 2.0 * math.pi * f
    return (c*c*r1*r2*s*s) / (c*c*r1*r2*s*s + 2.0*c*r1*s + 1.0)

def analytical_sch107(f: float, scale: float = 1.0) -> complex:
    c = 470e-9 / scale
    h1 = analytical_sk_hp(f, 20.8e3*scale, 24.3e3*scale, c)
    h2 = analytical_sk_hp(f, 8.66e3*scale, 59e3*scale, c)
    return h1 * h2

def find_f3(grid: list[tuple[float, float]]) -> float | None:
    target = -3.01029995664
    for (f0, y0), (f1, y1) in zip(grid, grid[1:]):
        if y0 <= target <= y1:
            if y1 == y0:
                return f0
            # Interpolate in log-frequency, which is appropriate for Bode data.
            x0 = math.log(f0)
            x1 = math.log(f1)
            frac = (target - y0) / (y1 - y0)
            return math.exp(x0 + frac * (x1 - x0))
    return None

def ac_case(name: str, subckt: str, cfg: dict, opa: Path) -> dict:
    ac = cfg["execution"]["ac"]
    direct_freqs = ac["direct_report_hz"]
    filter_freqs = ac["filter_report_hz"]
    gd_freqs = ac["group_delay_hz"]

    f3_start = float(ac["f3_grid_start_hz"])
    f3_stop = float(ac["f3_grid_stop_hz"])
    f3_step = float(ac["f3_grid_step_hz"])
    count = int(round((f3_stop - f3_start) / f3_step)) + 1
    f3_freqs = [f3_start + i*f3_step for i in range(count)]

    measures = [
        ".meas ac DREF FIND mag(V(DOUT)) AT=1k",
        ".meas ac FREF FIND mag(V(FOUT)) AT=1k",
        ".meas ac FMAX MAX mag(V(FOUT)) FROM 20 TO 20k",
    ]
    for f in direct_freqs:
        measures.append(f".meas ac D_{f} FIND mag(V(DOUT)) AT={f}")
    for f in filter_freqs:
        measures.append(f".meas ac F_{f} FIND mag(V(FOUT)) AT={f}")
    for i, f in enumerate(f3_freqs):
        measures.append(f".meas ac FG_{i} FIND mag(V(FOUT)) AT={f:.9g}")
    for f in gd_freqs:
        fm = f * 0.99
        fp = f * 1.01
        measures += [
            f".meas ac DP_{f}_M FIND ph(V(DOUT)) AT={fm:.9g}",
            f".meas ac DP_{f}_P FIND ph(V(DOUT)) AT={fp:.9g}",
            f".meas ac FP_{f}_M FIND ph(V(FOUT)) AT={fm:.9g}",
            f".meas ac FP_{f}_P FIND ph(V(FOUT)) AT={fp:.9g}",
        ]

    deck = preamble(opa) + f"""
VIN IN 0 AC 1
XCAND IN DIRECT FILTER VPLUS18 VMINUS18 ZERO_VA {subckt}
XDIRECT DIRECT DOUT VPLUS18 VMINUS18 ZERO_VA AE067_SCH104
XFILTER FILTER FOUT VPLUS18 VMINUS18 ZERO_VA AE067_SCH104
RLD DOUT ZERO_VA 100k
RLF FOUT ZERO_VA 100k
.ac dec 150 1 100k
{chr(10).join(measures)}
.end
"""
    log = execute_deck("run04_ac_" + name.lower(), deck, TMP / "ac")
    dref = parse_measure(log, "DREF")
    fref = parse_measure(log, "FREF")

    direct_db = {str(f): db(parse_measure(log, f"D_{f}") / dref) for f in direct_freqs}
    filter_db = {str(f): db(parse_measure(log, f"F_{f}") / fref) for f in filter_freqs}
    fgrid = [(f, db(parse_measure(log, f"FG_{i}") / fref)) for i, f in enumerate(f3_freqs)]
    f3 = find_f3(fgrid)
    peak = db(parse_measure(log, "FMAX") / fref)

    gd = {"direct_ms": {}, "filter_ms": {}}
    for f in gd_freqs:
        fm, fp = f*0.99, f*1.01
        gd["direct_ms"][str(f)] = group_delay_ms(
            parse_measure(log, f"DP_{f}_M"), parse_measure(log, f"DP_{f}_P"), fm, fp
        )
        gd["filter_ms"][str(f)] = group_delay_ms(
            parse_measure(log, f"FP_{f}_M"), parse_measure(log, f"FP_{f}_P"), fm, fp
        )

    crit = cfg["criteria"]
    d20 = direct_db["20"]
    d50 = direct_db["50"]
    direct_checks = {
        "20hz_absolute": d20 >= -float(crit["direct"]["loss_20_db_absolute_max"]) - 1e-9,
        "20hz_preferred": d20 >= -float(crit["direct"]["loss_20_db_preferred_max"]) - 1e-9,
        "50hz_preferred": d50 >= -float(crit["direct"]["loss_50_db_preferred_max"]) - 1e-9,
    }
    fc = crit["filter"]
    f3_lo = float(fc["f3_hz_nominal"]) * (1.0 - float(fc["f3_percent_max"])/100.0)
    f3_hi = float(fc["f3_hz_nominal"]) * (1.0 + float(fc["f3_percent_max"])/100.0)
    filter_checks = {
        "f3": f3 is not None and f3_lo <= f3 <= f3_hi,
        "20hz": filter_db["20"] >= float(fc["gain_20_db_min"]) - 1e-9,
        "30hz": filter_db["30"] >= float(fc["gain_30_db_min"]) - 1e-9,
        "10hz": filter_db["10"] <= float(fc["gain_10_db_max"]) + 1e-9,
        "5hz": filter_db["5"] <= float(fc["gain_5_db_max"]) + 1e-9,
        "passband_peak": peak <= float(fc["passband_peak_db_max"]) + 1e-9,
    }

    return {
        "direct_db_rel_1khz": direct_db,
        "filter_db_rel_1khz": filter_db,
        "filter_f3_hz": f3,
        "filter_peak_20hz_20khz_db_rel_1khz": peak,
        "group_delay": gd,
        "direct_checks": direct_checks,
        "filter_checks": filter_checks,
        "lf_hard_pass": direct_checks["20hz_absolute"] and all(filter_checks.values()),
        "lf_preferred_pass": all(direct_checks.values()) and all(filter_checks.values()),
    }

def noise_case(name: str, subckt: str, path: str, cfg: dict, opa: Path) -> float:
    node = "DIRECT" if path == "direct" else "FILTER"
    ncfg = cfg["execution"]["noise"]
    deck = preamble(opa) + f"""
VIN IN 0 AC 1
XCAND IN DIRECT FILTER VPLUS18 VMINUS18 ZERO_VA {subckt}
XOUT {node} OUT VPLUS18 VMINUS18 ZERO_VA AE067_SCH104
RLOAD OUT ZERO_VA {int(ncfg["output_load_ohm"])}
.noise V(OUT) VIN dec 100 {ncfg["low_hz"]} {ncfg["high_hz"]}
.meas NOISE ONOISE INTEG V(onoise) FROM {ncfg["low_hz"]} TO {ncfg["high_hz"]}
.end
"""
    log = execute_deck(f"run04_noise_{name.lower()}_{path}", deck, TMP / "noise")
    return parse_measure(log, "ONOISE")

def offset_step_case(name: str, subckt: str, cfg: dict, opa: Path) -> dict:
    stress = cfg["execution"]["dc_offset_stress"]
    v = float(stress["input_offset_v"])
    t = float(stress["step_time_s"])
    threshold = float(stress["direct_one_percent_v"])
    deck = preamble(opa) + f"""
VIN IN 0 PULSE(0 {v} {t} 1u 1u 5 10)
XCAND IN DIRECT FILTER VPLUS18 VMINUS18 ZERO_VA {subckt}
XDIRECT DIRECT DOUT VPLUS18 VMINUS18 ZERO_VA AE067_SCH104
XFILTER FILTER FOUT VPLUS18 VMINUS18 ZERO_VA AE067_SCH104
RLD DOUT ZERO_VA 100k
RLF FOUT ZERO_VA 100k
.tran 0 3 0 1m
.meas tran DMAX MAX V(DOUT) FROM {t} TO 3
.meas tran DMIN MIN V(DOUT) FROM {t} TO 3
.meas tran FMAXT MAX V(FOUT) FROM {t} TO 3
.meas tran FMINT MIN V(FOUT) FROM {t} TO 3
.meas tran D100 FIND V(DOUT) AT={t+0.1}
.meas tran D500 FIND V(DOUT) AT={t+0.5}
.meas tran D1000 FIND V(DOUT) AT={t+1.0}
.meas tran D2000 FIND V(DOUT) AT={t+2.0}
.meas tran F100 FIND V(FOUT) AT={t+0.1}
.meas tran F500 FIND V(FOUT) AT={t+0.5}
.meas tran F1000 FIND V(FOUT) AT={t+1.0}
.meas tran F2000 FIND V(FOUT) AT={t+2.0}
.meas tran DSET WHEN V(DOUT)={threshold} FALL=1 TD={t+0.002}
.end
"""
    log = execute_deck("run04_offset_" + name.lower(), deck, TMP / "offset")
    dset_abs = parse_when_time(log, "DSET")
    return {
        "direct_peak_v": max(abs(parse_measure(log, "DMAX")), abs(parse_measure(log, "DMIN"))),
        "filter_peak_v": max(abs(parse_measure(log, "FMAXT")), abs(parse_measure(log, "FMINT"))),
        "direct_residual_v": {
            "100ms": parse_measure(log, "D100"),
            "500ms": parse_measure(log, "D500"),
            "1000ms": parse_measure(log, "D1000"),
            "2000ms": parse_measure(log, "D2000"),
        },
        "filter_residual_v": {
            "100ms": parse_measure(log, "F100"),
            "500ms": parse_measure(log, "F500"),
            "1000ms": parse_measure(log, "F1000"),
            "2000ms": parse_measure(log, "F2000"),
        },
        "direct_settle_to_1pct_s_after_step": (
            None if dset_abs is None else max(0.0, dset_abs - t)
        ),
        "physical_lf_coupling_settling_note": (
            "This is a DC-step charge-settling discriminator, not the RUN08 "
            "10x audio-burst recovery criterion."
        ),
    }

def switch_case(name: str, subckt: str, cfg: dict, opa: Path) -> dict:
    scfg = cfg["execution"]["switch_discrimination"]
    v = float(scfg["source_dc_offset_v"])
    f_open = float(scfg["filter_open_s"])
    d_close = float(scfg["direct_close_s"])

    if name == "POST_SWITCH_COMMON":
        topology = f"""
VIN IN 0 {v}
XRAW IN DRAW FRAW VPLUS18 VMINUS18 ZERO_VA AE067_POST_RAW
VCF CF 0 PULSE(1 0 {f_open} 1u 1u 1 2)
VCD CD 0 PULSE(0 1 {d_close} 1u 1u 1 2)
SF FRAW PRE CF 0 AE067_SW
SD IN PRE CD 0 AE067_SW
RNUMPRE PRE ZERO_VA 1G
CPOST PRE SEL 1u
RPOST SEL ZERO_VA 330k
"""
        dnode, fnode = "IN", "FRAW"
    else:
        topology = f"""
VIN IN 0 {v}
XCAND IN DIRECT FILTER VPLUS18 VMINUS18 ZERO_VA {subckt}
VCF CF 0 PULSE(1 0 {f_open} 1u 1u 1 2)
VCD CD 0 PULSE(0 1 {d_close} 1u 1u 1 2)
SF FILTER SEL CF 0 AE067_SW
SD DIRECT SEL CD 0 AE067_SW
RNUM SEL ZERO_VA 1G
"""
        dnode, fnode = "DIRECT", "FILTER"

    deck = preamble(opa) + topology + f"""
XOUT SEL OUT VPLUS18 VMINUS18 ZERO_VA AE067_SCH104
RLOAD OUT ZERO_VA 100k
.tran 0 0.5 0 50u
.meas tran DPRE FIND V({dnode}) AT=0.09
.meas tran FPRE FIND V({fnode}) AT=0.09
.meas tran SELPRE FIND V(SEL) AT=0.09
.meas tran SMAX MAX V(SEL) FROM 0.095 TO 0.5
.meas tran SMIN MIN V(SEL) FROM 0.095 TO 0.5
.meas tran OMAX MAX V(OUT) FROM 0.095 TO 0.5
.meas tran OMIN MIN V(OUT) FROM 0.095 TO 0.5
.meas tran S110 FIND V(SEL) AT=0.110
.meas tran S200 FIND V(SEL) AT=0.200
.meas tran S400 FIND V(SEL) AT=0.400
.end
"""
    log = execute_deck("run04_switch_" + name.lower(), deck, TMP / "switch")
    sel_peak = max(abs(parse_measure(log, "SMAX")), abs(parse_measure(log, "SMIN")))
    out_peak = max(abs(parse_measure(log, "OMAX")), abs(parse_measure(log, "OMIN")))
    objective = float(scfg["internal_selector_peak_objective_v"])
    return {
        "direct_input_pre_switch_v": parse_measure(log, "DPRE"),
        "filter_input_pre_switch_v": parse_measure(log, "FPRE"),
        "selector_pre_switch_v": parse_measure(log, "SELPRE"),
        "selector_peak_abs_v": sel_peak,
        "sch104_output_peak_abs_v": out_peak,
        "selector_residual_v": {
            "9ms_after_direct_close": parse_measure(log, "S110"),
            "99ms_after_direct_close": parse_measure(log, "S200"),
            "299ms_after_direct_close": parse_measure(log, "S400"),
        },
        "internal_selector_peak_objective_v": objective,
        "internal_selector_objective_pass": sel_peak <= objective + 1e-12,
        "scope_note": (
            "Candidate-discrimination only. Full muted/live switching at balanced "
            "output remains RUN12."
        ),
    }

def write_csv(path: Path, result: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "candidate", "prior_disposition", "lf_hard_pass", "lf_preferred_pass",
        "direct_20_db", "direct_50_db", "filter_f3_hz", "filter_5_db",
        "filter_10_db", "filter_20_db", "filter_30_db", "filter_peak_db",
        "direct_noise_uv_rms", "filter_noise_uv_rms",
        "direct_noise_delta_db_vs_branch_local",
        "filter_noise_delta_db_vs_branch_local",
        "switch_selector_peak_v", "switch_objective_pass",
        "direct_dc_step_settle_1pct_s",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for name, c in result["candidates"].items():
            w.writerow({
                "candidate": name,
                "prior_disposition": c["prior_disposition"],
                "lf_hard_pass": c["ac"]["lf_hard_pass"],
                "lf_preferred_pass": c["ac"]["lf_preferred_pass"],
                "direct_20_db": c["ac"]["direct_db_rel_1khz"]["20"],
                "direct_50_db": c["ac"]["direct_db_rel_1khz"]["50"],
                "filter_f3_hz": c["ac"]["filter_f3_hz"],
                "filter_5_db": c["ac"]["filter_db_rel_1khz"]["5"],
                "filter_10_db": c["ac"]["filter_db_rel_1khz"]["10"],
                "filter_20_db": c["ac"]["filter_db_rel_1khz"]["20"],
                "filter_30_db": c["ac"]["filter_db_rel_1khz"]["30"],
                "filter_peak_db": c["ac"]["filter_peak_20hz_20khz_db_rel_1khz"],
                "direct_noise_uv_rms": c["noise"]["direct_v_rms"] * 1e6,
                "filter_noise_uv_rms": c["noise"]["filter_v_rms"] * 1e6,
                "direct_noise_delta_db_vs_branch_local": c["noise"]["direct_delta_db_vs_branch_local"],
                "filter_noise_delta_db_vs_branch_local": c["noise"]["filter_delta_db_vs_branch_local"],
                "switch_selector_peak_v": c["switch"]["selector_peak_abs_v"],
                "switch_objective_pass": c["switch"]["internal_selector_objective_pass"],
                "direct_dc_step_settle_1pct_s": c["offset_step"]["direct_settle_to_1pct_s_after_step"],
            })

def write_markdown(path: Path, result: dict) -> None:
    lines = [
        "# AE-067 RUN04 DR039/SCH107 LF trade — Phase A evidence",
        "",
        f"Status: **{result['status']}**",
        "",
        "| Candidate | LF hard | 20 Hz direct | 15 Hz f3 | 20 Hz filter | Filter noise Δ | Switch peak |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for name, c in result["candidates"].items():
        lines.append(
            f"| {name} | {'PASS' if c['ac']['lf_hard_pass'] else 'FAIL'} | "
            f"{c['ac']['direct_db_rel_1khz']['20']:+.4f} dB | "
            f"{c['ac']['filter_f3_hz']:.3f} Hz | "
            f"{c['ac']['filter_db_rel_1khz']['20']:+.4f} dB | "
            f"{c['noise']['filter_delta_db_vs_branch_local']:+.3f} dB | "
            f"{c['switch']['selector_peak_abs_v']*1000:.2f} mV |"
        )
    lines += [
        "",
        "No topology is auto-promoted by Phase A. Review frequency, noise, DC-step settling, "
        "selector charge transient and value-engineering together before governance changes.",
        "",
        "Full system noise remains RUN09, component sensitivity/tolerance remains RUN10, "
        "and SW904-to-XLR switching remains RUN12.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

def write_design_record(result: dict) -> None:
    c = result["candidates"]
    lines = [
        "# AE-067 — RUN04 DR039/SCH107 LF Trade Evidence — Rev A0",
        "",
        "**Project:** Shellac",
        f"**Status:** {result['status']}",
        f"**Execution baseline:** `{result['repository_commit_before_ae067']}`",
        "",
        "## Purpose",
        "Execute the AE-050 RUN04 candidate comparison without migrating any candidate into the product generator.",
        "",
        "## Scope",
        "Four candidates are compared: current common pre-split block, post-switch common block, "
        "AE-052 branch-local direct block, and the x10 SCH107 / 1.2 uF common-block reference.",
        "",
        "Each candidate receives separate AC, noise, DC-offset-step and selector-transition analyses. "
        "RUN04 switching is an internal candidate discriminator only; balanced-output switching remains RUN12.",
        "",
        "## Evidence summary",
        "",
        "| Candidate | LF hard | LF preferred | Filter noise delta | Selector peak |",
        "|---|---|---|---:|---:|",
    ]
    for name, x in c.items():
        lines.append(
            f"| {name} | {'PASS' if x['ac']['lf_hard_pass'] else 'FAIL'} | "
            f"{'PASS' if x['ac']['lf_preferred_pass'] else 'REVIEW'} | "
            f"{x['noise']['filter_delta_db_vs_branch_local']:+.3f} dB | "
            f"{x['switch']['selector_peak_abs_v']*1000:.2f} mV |"
        )
    lines += [
        "",
        "## Decision boundary",
        "",
        "This evidence record deliberately does not auto-promote a topology. The RUN04 decision must be made "
        "after reviewing the quantitative LF, noise and transient evidence. DR-039 remains implementation/"
        "requalification-open until that review and later required campaign work are complete.",
        "",
        "## Open qualification",
        "",
        "- RUN09 full-system noise;",
        "- RUN10 sensitivity/tolerance and timing-capacitor value engineering;",
        "- RUN12 muted/live selector switching to the balanced output;",
        "- prototype/bench correlation.",
        "",
        "## Evidence",
        "",
        "- `simulation/results/run04_lf_trade/ae067_run04.json`",
        "- `simulation/results/run04_lf_trade/ae067_run04.csv`",
        "- `simulation/results/run04_lf_trade/ae067_run04.md`",
    ]
    DESIGN_RECORD.parent.mkdir(parents=True, exist_ok=True)
    DESIGN_RECORD.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

def main() -> int:
    cfg = yaml.safe_load(CFG.read_text(encoding="utf-8"))
    validate_ltspice()
    opa = resolve_source("OPA1656", VENDOR)

    print("\n=== AE-067 RUN04: DR039/SCH107 LF topology trade ===")
    cases = {}
    for name, ccfg in cfg["candidates"].items():
        print(f"\n-- {name} --")
        subckt = ccfg["subckt"]
        ac = ac_case(name, subckt, cfg, opa)
        nd = noise_case(name, subckt, "direct", cfg, opa)
        nf = noise_case(name, subckt, "filter", cfg, opa)
        offset = offset_step_case(name, subckt, cfg, opa)
        switch = switch_case(name, subckt, cfg, opa)
        cases[name] = {
            "prior_disposition": ccfg["prior_disposition"],
            "component_summary": ccfg,
            "ac": ac,
            "noise": {"direct_v_rms": nd, "filter_v_rms": nf},
            "offset_step": offset,
            "switch": switch,
        }
        print(
            f"LF {'PASS' if ac['lf_hard_pass'] else 'FAIL'}: "
            f"direct20={ac['direct_db_rel_1khz']['20']:+.4f} dB, "
            f"f3={ac['filter_f3_hz']:.3f} Hz, "
            f"filter20={ac['filter_db_rel_1khz']['20']:+.4f} dB, "
            f"noise(filter)={nf*1e6:.3f} uV RMS, "
            f"switch_peak={switch['selector_peak_abs_v']*1000:.2f} mV"
        )

    ref = cases["BRANCH_LOCAL_DIRECT_BYPASS_BLOCK"]["noise"]
    for c in cases.values():
        for path in ("direct", "filter"):
            key = f"{path}_v_rms"
            value = c["noise"][key]
            base = ref[key]
            delta = db(value/base) if value > 0 and base > 0 else 0.0
            c["noise"][f"{path}_delta_db_vs_branch_local"] = delta
            nc = cfg["criteria"]["noise_delta"]
            if delta <= float(nc["generally_acceptable_db_max"]) + 1e-9:
                band = "GENERALLY_ACCEPTABLE"
            elif delta <= float(nc["trade_study_db_max"]) + 1e-9:
                band = "TRADE_STUDY"
            else:
                band = "PRESUMPTIVE_REJECT_WITHOUT_COMPELLING_BENEFIT"
            c["noise"][f"{path}_decision_band"] = band

    # Independent analytical correlation for the selected nominal filter only.
    branch = cases["BRANCH_LOCAL_DIRECT_BYPASS_BLOCK"]
    corr_freqs = [5, 10, 15, 20, 30, 50]
    ref_analytic = abs(analytical_sch107(1000.0))
    errors = {}
    for f in corr_freqs:
        expected = db(abs(analytical_sch107(float(f))) / ref_analytic)
        actual = branch["ac"]["filter_db_rel_1khz"][str(f)]
        errors[str(f)] = actual - expected
    correlation_max = max(abs(v) for v in errors.values())

    result = {
        "schema_version": 1,
        "authority": "AE-067",
        "run_id": "RUN04",
        "title": "DR039/SCH107 LF topology trade",
        "repository_commit_before_ae067": cfg["baseline_commit"],
        "model_semantics": cfg["model_semantics"],
        "generator_migration_implied": False,
        "status": "EVIDENCE_COMPLETE_REVIEW_REQUIRED",
        "candidate_count": len(cases),
        "candidates": cases,
        "branch_local_filter_analytical_correlation": {
            "errors_db": errors,
            "max_abs_error_db": correlation_max,
        },
        "decision": {
            "automatic_topology_promotion": False,
            "preferred_topology": None,
            "runner_up": None,
            "review_required": True,
        },
        "open_qualification": cfg["decision_policy"]["later_open_runs"],
        "model_sources": {
            "OPA1656": {"path": opa.name, "sha256": sha256(opa)},
            "qualification_model_sha256": sha256(MODEL),
        },
    }
    write_json(RESULT_JSON, result)
    write_csv(RESULT_CSV, result)
    write_markdown(RESULT_MD, result)
    write_design_record(result)

    print("\n=== RUN04 PHASE-A SUMMARY ===")
    for name, c in cases.items():
        print(
            f"{name}: LF={'PASS' if c['ac']['lf_hard_pass'] else 'FAIL'}, "
            f"noiseΔ(filter)={c['noise']['filter_delta_db_vs_branch_local']:+.3f} dB, "
            f"switch={c['switch']['selector_peak_abs_v']*1000:.2f} mV "
            f"({'PASS' if c['switch']['internal_selector_objective_pass'] else 'REVIEW'})"
        )
    print(f"Branch-local ideal-filter correlation max error: {correlation_max:.6f} dB")
    print("AE-067 RUN04 Phase A: EVIDENCE_COMPLETE_REVIEW_REQUIRED")
    print(f"Result: {RESULT_JSON.relative_to(ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
