#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import yaml

from generator.model.replay_eq import (
    BASS_NETWORKS,
    RIAA_BASS_NETWORK,
    RECOVERY_GAIN,
    TREBLE_NETWORKS,
)
from generator.model.replay_curve_analysis import (
    CURVE_TARGETS,
    ideal_curve_transfer,
    realised_curve_transfer,
)
from simulation.scripts.sim_support import (
    LTSPICE,
    ROOT,
    execute_deck,
    parse_measure,
    resolve_source,
    sha256,
    validate_ltspice,
    write_json,
)

TMP = ROOT / ".ae066_run01_03_tmp"
VENDOR = TMP / "vendor"
RESULTS = ROOT / "simulation/results"
CFG_PATH = ROOT / "simulation/config/ae066_ac_campaign.yaml"
QUAL_LIB = ROOT / "simulation/models/qualification/sch101_sch103_ae066.lib"
WRAPPERS = ROOT / "simulation/models/wrappers"

RUN01_JSON = RESULTS / "run01_input_loading/ae066_run01.json"
RUN02_JSON = RESULTS / "run02_gain_cmrr/ae066_run02.json"
RUN03_JSON = RESULTS / "run03_eq/ae066_run03.json"
SUMMARY_JSON = RESULTS / "ae066_summary.json"
SUMMARY_CSV = RESULTS / "ae066_summary.csv"
SUMMARY_MD = RESULTS / "ae066_summary.md"
DESIGN_RECORD = ROOT / "docs/design_pack/AE-066_Integrated_AC_RUN01_RUN03_and_Infrastructure_Rev_A0.md"

CARTRIDGES = {
    "GRADO_78C": (
        ROOT / "simulation/models/cartridges/grado_78c_shellac.lib",
        "SHELLAC_GRADO_78C",
    ),
    "AT_VM95SP": (
        ROOT / "simulation/models/cartridges/at_vm95sp_shellac.lib",
        "SHELLAC_AT_VM95SP",
    ),
    "GRADO_GOLD_8MZ": (
        ROOT / "simulation/models/cartridges/grado_gold_8mz_shellac.lib",
        "SHELLAC_GRADO_GOLD_8MZ",
    ),
}

def db(value: float) -> float:
    if value <= 0:
        return -300.0
    return 20.0 * math.log10(value)

def fmt_spice(value: float) -> str:
    if value >= 1e11:
        return "1T"
    return f"{value:g}"

def common_preamble(*model_paths: Path) -> str:
    include_lines = "\n".join(f'.include "{p}"' for p in model_paths)
    return f""".options meascplxfmt=cartesian measdgt=12
{include_lines}
VPLUS VPLUS18 0 18
VMINUS VMINUS18 0 -18
VZERO ZERO_VA 0 0
VBOND CHASSIS ZERO_VA 0
"""

def run01(cfg: dict, sources: dict) -> dict:
    print("\n=== AE-066 RUN01: cartridge/loading matrix ===")
    opa1656 = sources["OPA1656"]
    lt5400 = sources["LT5400"]
    cases = []
    for cartridge in cfg["execution"]["run01"]["cartridges"]:
        cart_file, cart_subckt = CARTRIDGES[cartridge]
        for cable_pf in cfg["execution"]["run01"]["cable_pf"]:
            for service_pf in cfg["execution"]["run01"]["service_cap_pf"]:
                case_id = f"{cartridge}_CABLE{cable_pf}_SERVICE{service_pf}"
                service_value = "1e-18" if service_pf == 0 else f"{service_pf}p"
                deck = common_preamble(
                    opa1656,
                    lt5400,
                    WRAPPERS / "opa1656_shellac.lib",
                    WRAPPERS / "lt5400_7_shellac.lib",
                    cart_file,
                    QUAL_LIB,
                ) + f"""
VDRIVE DRIVE CART_N AC 1 0
XCART CART_P CART_N DRIVE {cart_subckt}
CCABLE CART_P CART_N {cable_pf}p
X101 CART_P CART_N N101_OUT VPLUS18 VMINUS18 ZERO_VA CHASSIS SHELLAC_SCH101_AE066 PARAMS: RFPROG=1T RGPROG=1T CDIFF={service_value}
.ac dec 100 10 100k
.meas ac CART_1K FIND mag(V(CART_P,CART_N)) AT=1k
.meas ac CART_MAX20 MAX mag(V(CART_P,CART_N)) FROM 20 TO 20k
.meas ac CART_MAX50 MAX mag(V(CART_P,CART_N)) FROM 20 TO 50k
.meas ac CART_20K FIND mag(V(CART_P,CART_N)) AT=20k
.meas ac CART_50K FIND mag(V(CART_P,CART_N)) AT=50k
.meas ac N101_1K FIND mag(V(N101_OUT)) AT=1k
.meas ac N101_MAX20 MAX mag(V(N101_OUT)) FROM 20 TO 20k
.end
"""
                log = execute_deck("run01_" + case_id.lower(), deck, TMP / "run01")
                cart_1k = parse_measure(log, "CART_1K")
                peak20 = db(parse_measure(log, "CART_MAX20") / cart_1k)
                peak50 = db(parse_measure(log, "CART_MAX50") / cart_1k)
                n101_1k = parse_measure(log, "N101_1K")
                n101_peak20 = db(parse_measure(log, "N101_MAX20") / n101_1k)
                effective_pf = cable_pf + service_pf + 23.5
                ae049_full = peak20 <= 1.0 + 1e-9 and peak50 <= 2.0 + 1e-9

                role = "CHARACTERISATION"
                gating = False
                if cartridge == "AT_VM95SP" and 100.0 <= effective_pf <= 200.0:
                    role = "PRIMARY_GATING_OFFICIAL_100_200PF"
                    gating = True
                elif cartridge == "GRADO_78C" and cable_pf == 100 and service_pf == 0:
                    role = "PRIMARY_NOMINAL_AUDIO_BAND_GATING_EXTENDED_BAND_OPEN"
                    gating = True
                elif cartridge == "GRADO_GOLD_8MZ":
                    role = "COMPATIBILITY_NON_GATING"

                case = {
                    "case_id": case_id,
                    "cartridge": cartridge,
                    "cable_pf": cable_pf,
                    "service_cap_pf": service_pf,
                    "bookkeeping_effective_total_pf": effective_pf,
                    "qualification_role": role,
                    "gating": gating,
                    "terminal_1khz_v_per_v_generated": cart_1k,
                    "peak_below_20khz_db": peak20,
                    "peak_below_50khz_db": peak50,
                    "terminal_20khz_db_rel_1khz": db(parse_measure(log, "CART_20K") / cart_1k),
                    "terminal_50khz_db_rel_1khz": db(parse_measure(log, "CART_50K") / cart_1k),
                    "sch101_output_1khz_v_per_v_generated": n101_1k,
                    "sch101_peak_below_20khz_db": n101_peak20,
                    "ae049_full_peaking_pass": ae049_full,
                    "audio_20khz_pass": peak20 <= 1.0 + 1e-9,
                    "extended_50khz_pass": peak50 <= 2.0 + 1e-9,
                }
                cases.append(case)
                print(
                    f"{case_id}: peak20={peak20:+.3f} dB peak50={peak50:+.3f} dB "
                    f"{'FULL-PASS' if ae049_full else 'REVIEW'}"
                )

    at_gating = [
        c for c in cases
        if c["cartridge"] == "AT_VM95SP" and c["qualification_role"] == "PRIMARY_GATING_OFFICIAL_100_200PF"
    ]
    grado_nominal = next(
        c for c in cases
        if c["cartridge"] == "GRADO_78C" and c["cable_pf"] == 100 and c["service_cap_pf"] == 0
    )
    hard_pass = (
        bool(at_gating)
        and all(c["ae049_full_peaking_pass"] for c in at_gating)
        and grado_nominal["audio_20khz_pass"]
    )
    grado_extended_open = not grado_nominal["extended_50khz_pass"]

    status = "QUALIFICATION_MATRIX_RESOLVED"
    if grado_extended_open:
        status = "PARTIAL_GRADO_EXTENDED_BAND_MODEL_VALIDITY_OPEN"
    if not hard_pass:
        status = "FAIL_GATING_CASE"

    result = {
        "schema_version": 1,
        "authority": "AE-066",
        "run_id": "RUN01",
        "status": status,
        "hard_gate_pass": hard_pass,
        "grado_extended_band_open": grado_extended_open,
        "case_count": len(cases),
        "at_official_envelope_gating_case_count": len(at_gating),
        "at_official_envelope_all_pass": bool(at_gating) and all(c["ae049_full_peaking_pass"] for c in at_gating),
        "grado_nominal_100pf_base_audio20_pass": grado_nominal["audio_20khz_pass"],
        "grado_nominal_100pf_base_extended50_pass": grado_nominal["extended_50khz_pass"],
        "cases": cases,
        "qualification_note": (
            "AE-049 is not waived. Grado 20-50 kHz qualification remains open if the "
            "AE-064 R-L-only behavioural model fails the extended-band criterion; this "
            "requires improved manufacturer/bench high-frequency evidence under R-021/R-024."
        ),
    }
    write_json(RUN01_JSON, result)
    return result

def run02(cfg: dict, sources: dict) -> dict:
    print("\n=== AE-066 RUN02: SCH101 gain / CMRR ===")
    opa1656 = sources["OPA1656"]
    lt5400 = sources["LT5400"]
    cases = []
    freqs = [20, 1000, 20000]
    criteria = cfg["execution"]["run02"]["criteria"]

    for gain_name, gain_cfg in cfg["execution"]["run02"]["gains"].items():
        rfprog = fmt_spice(float(gain_cfg["rf_program_ohm"]))
        rgprog = fmt_spice(float(gain_cfg["rg_program_ohm"]))
        base = common_preamble(
            opa1656,
            lt5400,
            WRAPPERS / "opa1656_shellac.lib",
            WRAPPERS / "lt5400_7_shellac.lib",
            QUAL_LIB,
        )
        measure_lines = "\n".join(
            f".meas ac OUT_{f} FIND mag(V(OUT)) AT={f}" for f in freqs
        )
        diff_deck = base + f"""
VINP INP 0 AC 0.5 0
VINM INM 0 AC 0.5 180
X101 INP INM OUT VPLUS18 VMINUS18 ZERO_VA CHASSIS SHELLAC_SCH101_AE066 PARAMS: RFPROG={rfprog} RGPROG={rgprog} CDIFF=1e-18
.ac dec 100 20 20k
{measure_lines}
.end
"""
        common_deck = base + f"""
VINP INP 0 AC 1 0
VINM INM 0 AC 1 0
X101 INP INM OUT VPLUS18 VMINUS18 ZERO_VA CHASSIS SHELLAC_SCH101_AE066 PARAMS: RFPROG={rfprog} RGPROG={rgprog} CDIFF=1e-18
.ac dec 100 20 20k
{measure_lines}
.end
"""
        dlog = execute_deck(f"run02_{gain_name.lower()}_diff", diff_deck, TMP / "run02")
        clog = execute_deck(f"run02_{gain_name.lower()}_common", common_deck, TMP / "run02")
        differential = {f: parse_measure(dlog, f"OUT_{f}") for f in freqs}
        common = {f: parse_measure(clog, f"OUT_{f}") for f in freqs}
        gain_db = {f: db(differential[f]) for f in freqs}
        cmrr_db = {
            f: (300.0 if common[f] <= 1e-15 else db(differential[f] / common[f]))
            for f in freqs
        }
        nominal = float(gain_cfg["nominal_db"])
        gain_checks = {f: abs(gain_db[f] - nominal) <= criteria["gain_error_db_max"] + 1e-9 for f in freqs}
        cmrr_checks = {
            20: cmrr_db[20] >= criteria["cmrr_db_min_20hz"] - 1e-9,
            1000: cmrr_db[1000] >= criteria["cmrr_db_min_1khz"] - 1e-9,
            20000: cmrr_db[20000] >= criteria["cmrr_db_min_20khz"] - 1e-9,
        }
        passed = all(gain_checks.values()) and all(cmrr_checks.values())
        case = {
            "gain": gain_name,
            "nominal_gain_db": nominal,
            "rf_program_ohm": float(gain_cfg["rf_program_ohm"]),
            "rg_program_ohm": float(gain_cfg["rg_program_ohm"]),
            "gain_db": {str(k): v for k, v in gain_db.items()},
            "cmrr_db": {str(k): v for k, v in cmrr_db.items()},
            "gain_checks": {str(k): v for k, v in gain_checks.items()},
            "cmrr_checks": {str(k): v for k, v in cmrr_checks.items()},
            "pass": passed,
        }
        cases.append(case)
        print(
            f"{gain_name}: gain1k={gain_db[1000]:.4f} dB, "
            f"CMRR 20/1k/20k={cmrr_db[20]:.1f}/{cmrr_db[1000]:.1f}/{cmrr_db[20000]:.1f} dB "
            f"{'PASS' if passed else 'FAIL'}"
        )

    result = {
        "schema_version": 1,
        "authority": "AE-066",
        "run_id": "RUN02",
        "status": "QUALIFIED_NOMINAL" if all(c["pass"] for c in cases) else "FAIL",
        "pass": all(c["pass"] for c in cases),
        "case_count": len(cases),
        "cases": cases,
        "qualification_limit": "Nominal models only; tolerance/mismatch sensitivity remains RUN10.",
    }
    write_json(RUN02_JSON, result)
    return result

def _all_bass():
    return tuple(BASS_NETWORKS) + (RIAA_BASS_NETWORK,)

def _named_target_map():
    return {(t.bass_name, t.treble_name): t for t in CURVE_TARGETS}

def _freq_grid() -> list[float]:
    start = math.log10(20.0)
    stop = math.log10(20000.0)
    values = [10 ** (start + (stop - start) * i / 120.0) for i in range(121)]
    values += [30.0, 50.0, 100.0, 1000.0, 10000.0, 15000.0, 20000.0]
    return sorted({round(v, 6) for v in values})

def run03(cfg: dict, sources: dict) -> dict:
    print("\n=== AE-066 RUN03: SCH103 all 25 states ===")
    opa1612 = sources["OPA1612"]
    criteria = cfg["execution"]["run03"]["criteria"]
    freqs = _freq_grid()
    phase_freqs = [20, 50, 100, 1000, 10000, 20000]
    targets = _named_target_map()
    states = []

    for bass in _all_bass():
        for treble in TREBLE_NETWORKS:
            bass_key = bass.name.replace(" ", "_").replace("/", "_")
            treble_key = treble.name.replace(" ", "_").replace("/", "_")
            case_id = f"{bass_key}__{treble_key}"
            case_index = str(len(states)).zfill(2)

            ct = "1e-18" if treble.capacitance_nf is None else f"{treble.capacitance_nf:g}n"
            if bass.switch_condition == "SHORT":
                subckt = "SHELLAC_SCH103_FLAT_AE066"
                params = f"CT={ct}"
            else:
                subckt = "SHELLAC_SCH103_EQ_AE066"
                params = f"RS={bass.rs_ohm:g} CB={bass.capacitance_nf:g}n CT={ct}"

            preamble = common_preamble(
                opa1612,
                WRAPPERS / "opa1612_shellac.lib",
                QUAL_LIB,
            )
            instances = f"""
VINL INL 0 AC 1 0
VINR INR 0 AC 1 0
XL INL LFOUTL OUTL VPLUS18 VMINUS18 ZERO_VA {subckt} PARAMS: {params}
XR INR LFOUTR OUTR VPLUS18 VMINUS18 ZERO_VA {subckt} PARAMS: {params}
"""

            # LTspice 26.0.2 batch mode rejects a single deck containing both
            # .ac and .tran ("More than one analysis specified"). Preserve the
            # AE-066 acceptance contract by running the same nominal circuit
            # twice: one AC deck and one zero-input transient/DC-sanity deck.
            mag_measures = []
            for i, f in enumerate(freqs):
                mag_measures.append(f".meas ac ML{i} FIND mag(V(OUTL)) AT={f:.9g}")
                mag_measures.append(f".meas ac MR{i} FIND mag(V(OUTR)) AT={f:.9g}")
            phase_measures = []
            for i, f in enumerate(phase_freqs):
                phase_measures.append(f".meas ac PL{i} FIND ph(V(OUTL)) AT={f:g}")
                phase_measures.append(f".meas ac PR{i} FIND ph(V(OUTR)) AT={f:g}")

            ac_deck = preamble + instances + f"""
.ac dec 100 20 20k
{chr(10).join(mag_measures)}
{chr(10).join(phase_measures)}
.end
"""
            ac_log = execute_deck(
                f"run03_{case_index}_ac",
                ac_deck,
                TMP / "run03",
            )

            # AC source specifications have zero DC value, so the transient
            # deck retains the exact zero-signal DC condition used originally.
            dc_deck = preamble + instances + """
.tran 0 1u 0 1u
.meas tran DCLF_L FIND V(LFOUTL) AT=1u
.meas tran DCOUT_L FIND V(OUTL) AT=1u
.meas tran DCLF_R FIND V(LFOUTR) AT=1u
.meas tran DCOUT_R FIND V(OUTR) AT=1u
.end
"""
            dc_log = execute_deck(
                f"run03_{case_index}_dc",
                dc_deck,
                TMP / "run03",
            )

            ml = [parse_measure(ac_log, f"ML{i}") for i in range(len(freqs))]
            mr = [parse_measure(ac_log, f"MR{i}") for i in range(len(freqs))]
            phase_l = {
                str(f): parse_measure(ac_log, f"PL{i}")
                for i, f in enumerate(phase_freqs)
            }
            phase_r = {
                str(f): parse_measure(ac_log, f"PR{i}")
                for i, f in enumerate(phase_freqs)
            }

            ref_index = min(range(len(freqs)), key=lambda i: abs(freqs[i] - 1000.0))
            l_norm_db = [db(v / ml[ref_index]) for v in ml]
            r_norm_db = [db(v / mr[ref_index]) for v in mr]

            expected_complex = [
                realised_curve_transfer(1j * 2 * math.pi * f, bass, treble)
                for f in freqs
            ]
            expected_ref = expected_complex[ref_index]
            expected_db = [db(abs(v / expected_ref)) for v in expected_complex]
            corr_errors = [l_norm_db[i] - expected_db[i] for i in range(len(freqs))]
            max_corr = max(abs(v) for v in corr_errors)
            lr_mismatch = max(abs(l_norm_db[i] - r_norm_db[i]) for i in range(len(freqs)))

            target = targets.get((bass.name, treble.name))
            target_kind = "UNNAMED_ADJUSTMENT"
            target_error = None
            target_pass = True
            if target is not None:
                target_kind = "RIAA" if target.exact_standard else "NAMED_HISTORICAL"
                ideal_complex = [
                    ideal_curve_transfer(1j * 2 * math.pi * f, target)
                    for f in freqs
                ]
                ideal_ref = ideal_complex[ref_index]
                ideal_db = [db(abs(v / ideal_ref)) for v in ideal_complex]
                if target.exact_standard:
                    indices = range(len(freqs))
                    limit = criteria["riaa_error_db_max_20hz_20khz"]
                else:
                    indices = [i for i, f in enumerate(freqs) if 30.0 <= f <= 15000.0]
                    limit = criteria["historical_error_db_max_30hz_15khz"]
                target_error = max(abs(l_norm_db[i] - ideal_db[i]) for i in indices)
                target_pass = target_error <= limit + 1e-9

            if target_kind == "RIAA":
                lr_limit = criteria["riaa_lr_mismatch_db_max"]
            elif target_kind == "NAMED_HISTORICAL":
                lr_limit = criteria["historical_lr_mismatch_db_max"]
            else:
                lr_limit = criteria["unnamed_lr_mismatch_db_max"]

            dc = {
                "lf_l_v": parse_measure(dc_log, "DCLF_L"),
                "out_l_v": parse_measure(dc_log, "DCOUT_L"),
                "lf_r_v": parse_measure(dc_log, "DCLF_R"),
                "out_r_v": parse_measure(dc_log, "DCOUT_R"),
            }
            dc_pass = (
                max(abs(v) for v in dc.values())
                <= criteria["representative_internal_dc_v_abs_max"] + 1e-12
            )
            correlation_pass = (
                max_corr <= criteria["model_vs_analytical_correlation_db_max"] + 1e-9
            )
            lr_pass = lr_mismatch <= lr_limit + 1e-9
            passed = correlation_pass and target_pass and lr_pass and dc_pass

            state = {
                "case_id": case_id,
                "bass": bass.name,
                "treble": treble.name,
                "target_kind": target_kind,
                "target_identifier": target.identifier if target else None,
                "max_model_vs_analytical_error_db": max_corr,
                "target_max_error_db": target_error,
                "max_lr_mismatch_db": lr_mismatch,
                "phase_l_deg": phase_l,
                "phase_r_deg": phase_r,
                "dc": dc,
                "analysis_execution": {
                    "ac_deck": f"run03_{case_index}_ac",
                    "dc_deck": f"run03_{case_index}_dc",
                    "reason": "LTspice 26.0.2 batch mode permits one analysis per deck",
                },
                "correlation_pass": correlation_pass,
                "target_pass": target_pass,
                "lr_pass": lr_pass,
                "dc_pass": dc_pass,
                "pass": passed,
            }
            states.append(state)
            target_text = "" if target_error is None else f" target={target_error:.4f}dB"
            print(
                f"{case_id}: corr={max_corr:.4f}dB{target_text} "
                f"L/R={lr_mismatch:.5f}dB "
                f"maxDC={max(abs(v) for v in dc.values()):.4f}V "
                f"{'PASS' if passed else 'FAIL'}"
            )

    result = {
        "schema_version": 1,
        "authority": "AE-066",
        "run_id": "RUN03",
        "status": (
            "QUALIFIED_NOMINAL_ALL_25_STATES"
            if all(s["pass"] for s in states)
            else "FAIL"
        ),
        "pass": all(s["pass"] for s in states),
        "state_count": len(states),
        "execution_note": (
            "Each state uses separate AC and zero-input transient decks because "
            "LTspice 26.0.2 batch execution rejects multiple analyses in one deck."
        ),
        "states": states,
        "qualification_limit": (
            "Nominal component values only; tolerance/Monte Carlo/headroom/noise remain later runs."
        ),
    }
    write_json(RUN03_JSON, result)
    return result


def write_csv(run01_result: dict, run02_result: dict, run03_result: dict) -> None:
    SUMMARY_CSV.parent.mkdir(parents=True, exist_ok=True)
    with SUMMARY_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["RUN_ID", "CASE_ID", "METRIC", "VALUE", "UNIT", "PASS_FAIL", "NOTES"])
        for c in run01_result["cases"]:
            w.writerow([
                "RUN01", c["case_id"], "peak_below_20khz",
                f"{c['peak_below_20khz_db']:.9g}", "dB",
                "PASS" if c["audio_20khz_pass"] else "FAIL",
                c["qualification_role"],
            ])
            w.writerow([
                "RUN01", c["case_id"], "peak_below_50khz",
                f"{c['peak_below_50khz_db']:.9g}", "dB",
                "PASS" if c["extended_50khz_pass"] else "FAIL",
                c["qualification_role"],
            ])
        for c in run02_result["cases"]:
            w.writerow([
                "RUN02", c["gain"], "gain_1khz",
                f"{c['gain_db']['1000']:.9g}", "dB",
                "PASS" if c["gain_checks"]["1000"] else "FAIL", "",
            ])
            w.writerow([
                "RUN02", c["gain"], "cmrr_20khz",
                f"{c['cmrr_db']['20000']:.9g}", "dB",
                "PASS" if c["cmrr_checks"]["20000"] else "FAIL", "",
            ])
        for s in run03_result["states"]:
            w.writerow([
                "RUN03", s["case_id"], "model_correlation_max_error",
                f"{s['max_model_vs_analytical_error_db']:.9g}", "dB",
                "PASS" if s["correlation_pass"] else "FAIL", s["target_kind"],
            ])
            if s["target_max_error_db"] is not None:
                w.writerow([
                    "RUN03", s["case_id"], "target_max_error",
                    f"{s['target_max_error_db']:.9g}", "dB",
                    "PASS" if s["target_pass"] else "FAIL", s["target_identifier"],
                ])

def write_summary_and_record(run01_result: dict, run02_result: dict, run03_result: dict, sources: dict) -> dict:
    hard_pass = run01_result["hard_gate_pass"] and run02_result["pass"] and run03_result["pass"]
    open_findings = []
    if run01_result["grado_extended_band_open"]:
        open_findings.append("GRADO_78C_EXTENDED_20_TO_50KHZ_MODEL_VALIDITY")
    if any(not c["ae049_full_peaking_pass"] for c in run01_result["cases"]):
        open_findings.append("RUN01_LOADING_MATRIX_CONTAINS_REJECTED_OR_REVIEW_COMBINATIONS")

    if hard_pass and run01_result["grado_extended_band_open"]:
        campaign_status = "PASS_WITH_GRADO_EXTENDED_BAND_OPEN"
    elif hard_pass:
        campaign_status = "PASS"
    else:
        campaign_status = "FAIL"

    summary = {
        "schema_version": 1,
        "authority": "AE-066",
        "title": "Integrated AC RUN01-RUN03 campaign",
        "repository_commit_before_ae066": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "simulator": "LTspice",
        "simulator_executable_sha256": sha256(LTSPICE),
        "model_semantics": "SELECTED_NEXT_CANDIDATE_ANALYSIS",
        "generator_migration_implied": False,
        "run01": {
            "status": run01_result["status"],
            "hard_gate_pass": run01_result["hard_gate_pass"],
            "result_record": str(RUN01_JSON.relative_to(ROOT)).replace("\\", "/"),
        },
        "run02": {
            "status": run02_result["status"],
            "pass": run02_result["pass"],
            "result_record": str(RUN02_JSON.relative_to(ROOT)).replace("\\", "/"),
        },
        "run03": {
            "status": run03_result["status"],
            "pass": run03_result["pass"],
            "result_record": str(RUN03_JSON.relative_to(ROOT)).replace("\\", "/"),
        },
        "campaign_status": campaign_status,
        "hard_gate_pass": hard_pass,
        "open_findings": open_findings,
        "source_resolution": {
            name: {"filename": path.name, "sha256": sha256(path)}
            for name, path in sources.items()
        },
        "remaining_runs": ["RUN04", "RUN05", "RUN06", "RUN07", "RUN08", "RUN09", "RUN10", "RUN11", "RUN12", "RUN13", "RUN14"],
    }
    write_json(SUMMARY_JSON, summary)

    rejected = [c for c in run01_result["cases"] if not c["ae049_full_peaking_pass"]]
    worst_corr = max(s["max_model_vs_analytical_error_db"] for s in run03_result["states"])
    named = [s for s in run03_result["states"] if s["target_max_error_db"] is not None]
    worst_target = max(named, key=lambda s: s["target_max_error_db"])
    riaa = next(s for s in run03_result["states"] if s["target_kind"] == "RIAA")
    max_dc_state = max(
        run03_result["states"],
        key=lambda s: max(abs(v) for v in s["dc"].values())
    )
    max_dc = max(abs(v) for v in max_dc_state["dc"].values())

    summary_md = f"""# AE-066 simulation summary

Campaign status: **{campaign_status}**

- RUN01: {run01_result['status']} ({run01_result['case_count']} cases)
- RUN02: {run02_result['status']} ({run02_result['case_count']} gain states)
- RUN03: {run03_result['status']} ({run03_result['state_count']} Bass x Treble states)
- RUN01 loading combinations not meeting both AE-049 peaking limits: {len(rejected)}
- RUN03 worst model/analytical correlation error: {worst_corr:.6f} dB
- RUN03 worst named target error: {worst_target['target_max_error_db']:.6f} dB ({worst_target['case_id']})
- RIAA target error: {riaa['target_max_error_db']:.6f} dB
- Largest RUN03 representative DC magnitude: {max_dc:.6f} V ({max_dc_state['case_id']})
- Open findings: {', '.join(open_findings) if open_findings else 'none'}

This summary is evidence for selected-next candidate analysis only. It does not migrate the product generator.
"""
    SUMMARY_MD.write_text(summary_md, encoding="utf-8", newline="\n")

    record = f"""# AE-066 — Integrated AC RUN01–RUN03 and Infrastructure Consolidation — Rev A0

**Project:** Shellac
**Status:** {campaign_status}
**Execution baseline:** `{summary['repository_commit_before_ae066']}`

## 1. Purpose

AE-066 executes the first substantial integrated AC tranche after AE-065 RUN00: RUN01 cartridge/loading, RUN02 SCH101 gain/CMRR and RUN03 all 25 SCH103 Bass x Treble states. It also establishes reusable exact-hash model acquisition/parsing infrastructure and prepares controlled component/model candidates for RUN04-RUN06.

The work remains `SELECTED_NEXT_CANDIDATE_ANALYSIS`. No product-generator or CAD migration is authorised by this record.

## 2. RUN01 — cartridge/loading

Executed {run01_result['case_count']} combinations across Grado Prestige 78C, Audio-Technica AT-VM95SP and non-gating Grado Gold/8MZ compatibility; cable capacitance 50/100/150/200/300 pF; service capacitance BASE/+47/+100 pF.

Disposition: **{run01_result['status']}**.

The AT-VM95SP cases inside its official 100-200 pF bookkeeping envelope {'all meet' if run01_result['at_official_envelope_all_pass'] else 'DO NOT all meet'} the AE-049 +1 dB below 20 kHz / +2 dB below 50 kHz peaking limits.

The nominal Grado 78C 100 pF cable / BASE state {'meets' if run01_result['grado_nominal_100pf_base_audio20_pass'] else 'DOES NOT meet'} the below-20-kHz AE-049 criterion. Its extended 20-50-kHz R-L-only model result {'meets' if run01_result['grado_nominal_100pf_base_extended50_pass'] else 'does not meet'} the +2 dB criterion. Where it does not meet, AE-066 does not waive AE-049: extended-band qualification remains open because the AE-064 model does not contain manufacturer-authoritative cartridge self-capacitance/mechanical high-frequency behaviour. R-021/R-024 remain open.

The qualification matrix is therefore allowed to reject particular cable/service combinations; AE-042 explicitly made BASE/+47/+100 pF provisional pending this sweep.

## 3. RUN02 — SCH101 gain/CMRR

Disposition: **{run02_result['status']}**.

| State | Gain @1 kHz | CMRR 20 Hz | CMRR 1 kHz | CMRR 20 kHz | Pass |
|---|---:|---:|---:|---:|---|
""" + "\n".join(
        f"| {c['gain']} | {c['gain_db']['1000']:.4f} dB | {c['cmrr_db']['20']:.2f} dB | "
        f"{c['cmrr_db']['1000']:.2f} dB | {c['cmrr_db']['20000']:.2f} dB | {'PASS' if c['pass'] else 'FAIL'} |"
        for c in run02_result["cases"]
    ) + f"""

AE-049 nominal limits are +/-0.10 dB gain error, >=70 dB CMRR 20 Hz-1 kHz and >=60 dB at 20 kHz. Tolerance/mismatch qualification remains RUN10; nominal model success does not freeze resistor grades or LT5400 value-for-money decisions.

## 4. RUN03 — all 25 SCH103 states

Disposition: **{run03_result['status']}**.

All {run03_result['state_count']} intended Bass x Treble states were executed with nominal left/right instances. The worst LTspice-versus-independent analytical normalised response error is **{worst_corr:.6f} dB**. The worst named target error is **{worst_target['target_max_error_db']:.6f} dB** in `{worst_target['case_id']}`. True RIAA error is **{riaa['target_max_error_db']:.6f} dB**.

The largest representative SCH103 DC magnitude observed in the state matrix is **{max_dc:.6f} V** in `{max_dc_state['case_id']}`. This is a nominal sanity observation only; headroom, overload, recovery and tolerance remain later-run work.

Unnamed combinations are retained as intentional adjustment states and are judged for model correlation/L-R consistency/DC sanity rather than invented historical target accuracy.

## 5. Infrastructure debt closed

AE-066 introduces:
- reusable exact-hash external-model acquisition metadata;
- reusable model resolution, LTspice execution and scalar/polar `.meas` parsing support;
- a qualification-only parameterised SCH101/SCH103 model rather than modifying AE-065 RUN00 evidence;
- controlled RUN01/RUN02/RUN03 JSON plus CSV/Markdown summaries;
- concise `.gitignore` policy with explicit controlled-result exceptions;
- `.gitattributes` line-ending policy to reduce Windows LF/CRLF churn without mass renormalisation.

Historical AE-065 evidence and runner are not rewritten.

## 6. RUN04-RUN06 source preparation

The controlled source-candidate file identifies:
- Murata BLM21PG600SN1D and BLM21PG221SN1D as 0805 low/high impedance brackets for frequency-dependent RUN06 ferrite modelling;
- Panasonic ECEA1VN100U as a credible 10 uF / 35 V bipolar THAT1646 sense-capacitor candidate with 5 mm diameter, 11 mm body and 2 mm pitch;
- the current generator's H5.0 capacitor footprint as a mechanical inconsistency to reconcile before PCB freeze;
- WIMA MKS 2 family candidates for the AE-052 1 uF direct block and 470 nF SCH107 timing capacitors, with hand-matching retained as a value-engineering option;
- SCH103 timing-capacitor source feasibility, including a non-authoritative 100 nF + 33 nF C0G candidate for the 1600 Hz treble state where the current 120 nF + 12 nF decomposition has a 120 nF / 50 V / 1% sourcing weakness;
- exact NKK NR01 and Samtec service-hardware candidates for later mechanical/procurement closure.

No vendor simulation/CAD payload is committed merely because a download exists; redistribution remains controlled.

## 7. Configuration and risk disposition

- DR-038 remains selected pending product implementation.
- DR-039 remains implementation/requalification open.
- R-020 remains open.
- R-021 remains bench/model-validation open.
- R-024 remains open because RUN04-RUN14 and any RUN01 Grado extended-band finding remain.
- Shellac remains +/-18 V.
- Mechanical SW905 mute and no-automatic-sequencing authority are unchanged.
- No `main` promotion is authorised.

## 8. Evidence

- `{RUN01_JSON.relative_to(ROOT).as_posix()}`
- `{RUN02_JSON.relative_to(ROOT).as_posix()}`
- `{RUN03_JSON.relative_to(ROOT).as_posix()}`
- `{SUMMARY_JSON.relative_to(ROOT).as_posix()}`
- `{SUMMARY_CSV.relative_to(ROOT).as_posix()}`
- `{SUMMARY_MD.relative_to(ROOT).as_posix()}`
- `simulation/config/run04_run06_model_candidates.yaml`

Full structured results, rather than plot inspection, determine the dispositions above.
"""
    DESIGN_RECORD.parent.mkdir(parents=True, exist_ok=True)
    DESIGN_RECORD.write_text(record, encoding="utf-8", newline="\n")
    return summary

def main() -> int:
    cfg = yaml.safe_load(CFG_PATH.read_text(encoding="utf-8"))
    try:
        validate_ltspice()
    except Exception as exc:
        print(f"AE-066 simulator validation ERROR: {exc}")
        return 2
    TMP.mkdir(exist_ok=True)
    VENDOR.mkdir(parents=True, exist_ok=True)

    try:
        sources = {
            "OPA1656": resolve_source("OPA1656", VENDOR),
            "OPA1612": resolve_source("OPA1612", VENDOR),
            "LT5400": resolve_source("LT5400", VENDOR),
        }
        r1 = run01(cfg, sources)
        r2 = run02(cfg, sources)
        r3 = run03(cfg, sources)
        write_csv(r1, r2, r3)
        summary = write_summary_and_record(r1, r2, r3, sources)
    except Exception as exc:
        print(f"\nAE-066 execution ERROR: {exc}")
        print(f"Diagnostics retained in {TMP.relative_to(ROOT)}")
        return 2

    print(f"\nAE-066 campaign status: {summary['campaign_status']}")
    print(f"Summary: {SUMMARY_JSON.relative_to(ROOT)}")
    if summary["hard_gate_pass"]:
        shutil.rmtree(TMP, ignore_errors=True)
        return 0

    print("Hard acceptance failure: governance state will not be advanced.")
    print(f"Diagnostics retained in {TMP.relative_to(ROOT)}")
    return 2

if __name__ == "__main__":
    raise SystemExit(main())
