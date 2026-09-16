#!/usr/bin/env python3
from __future__ import annotations

import cmath
import csv
import json
import math
from pathlib import Path

import yaml

from generator.model.replay_curve_analysis import CURVE_TARGETS, ideal_curve_transfer
from generator.model.replay_eq import BASS_NETWORKS, RIAA_BASS_NETWORK, TREBLE_NETWORKS
from simulation.scripts.sim_support import ROOT, execute_deck, parse_measure, resolve_source, validate_ltspice, write_json

CFG = ROOT / "simulation/config/ae070_run07_end_to_end.yaml"
TMP = ROOT / ".ae070_run07_tmp"
VENDOR = TMP / "vendor"
RESULT_DIR = ROOT / "simulation/results/run07_end_to_end"
RESULT_JSON = RESULT_DIR / "ae070_run07.json"
RESULT_CSV = RESULT_DIR / "ae070_run07.csv"
RESULT_MD = RESULT_DIR / "ae070_run07.md"
DESIGN_RECORD = ROOT / "docs/design_pack/AE-070_RUN07_End_to_End_Nominal_Chain_Evidence_Rev_A0.md"

WRAP = ROOT / "simulation/models/wrappers"
LIB66 = ROOT / "simulation/models/qualification/sch101_sch103_ae066.lib"
LIB67 = ROOT / "simulation/models/qualification/dr039_sch107_ae067.lib"
LIB68 = ROOT / "simulation/models/qualification/sch104_sch105_ae068.lib"
LIB69 = ROOT / "simulation/models/qualification/sch108_ae069.lib"
SURROGATE = ROOT / "simulation/models/qualification/sch108_ae070_ac_surrogate.lib"
AE069_RESULT = ROOT / "simulation/results/run06_output/ae069_run06.json"
COMPOSITION_RESULT = ROOT / "simulation/results/run07_end_to_end/ae070_model_composition_discriminator.json"

CARTRIDGES = {
    "GRADO_78C": (ROOT / "simulation/models/cartridges/grado_78c_shellac.lib", "SHELLAC_GRADO_78C"),
    "AT_VM95SP": (ROOT / "simulation/models/cartridges/at_vm95sp_shellac.lib", "SHELLAC_AT_VM95SP"),
    "GRADO_GOLD_8MZ": (ROOT / "simulation/models/cartridges/grado_gold_8mz_shellac.lib", "SHELLAC_GRADO_GOLD_8MZ"),
}
GAIN_PARAMS = {
    "LOW": (332.0, 1.0e12),
    "DEFAULT": (1.0e12, 1.0e12),
    "HIGH": (1.0e12, 866.0),
}
TARGETS = {x.identifier: x for x in CURVE_TARGETS}


def db20(x: float) -> float:
    return -300.0 if x <= 0 else 20.0 * math.log10(x)


def fmt(v: float) -> str:
    return "1T" if v >= 1e11 else f"{v:.12g}"


def log_grid(lo: float, hi: float, count: int) -> list[float]:
    a, b = math.log10(lo), math.log10(hi)
    return [10 ** (a + (b - a) * i / (count - 1)) for i in range(count)]


def frequencies() -> list[float]:
    vals = set(log_grid(20.0, 20000.0, 61))
    vals.update(log_grid(5.0, 50.0, 41))
    vals.update([5.0, 10.0, 20.0, 30.0, 50.0, 100.0, 1000.0, 10000.0, 15000.0, 20000.0])
    return sorted(vals)


FREQS = frequencies()


def nearest_index(freq: float) -> int:
    return min(range(len(FREQS)), key=lambda i: abs(FREQS[i] - freq))


def network(name: str):
    if name == RIAA_BASS_NETWORK.name:
        return RIAA_BASS_NETWORK
    return next(x for x in BASS_NETWORKS if x.name == name)


def treble(name: str):
    return next(x for x in TREBLE_NETWORKS if x.name == name)


def source_paths() -> dict[str, Path]:
    return {
        "OPA1656": resolve_source("OPA1656", VENDOR),
        "OPA1612": resolve_source("OPA1612", VENDOR),
        "LT5400": resolve_source("LT5400", VENDOR),
        "S1G": resolve_source("S1G", VENDOR),
    }


def preamble(src: dict[str, Path], cart_file: Path) -> str:
    paths = [
        src["OPA1656"], src["OPA1612"], src["LT5400"], src["S1G"],
        WRAP / "opa1656_shellac.lib", WRAP / "opa1612_shellac.lib",
        WRAP / "lt5400_7_shellac.lib",
        cart_file, LIB66, LIB67, LIB68, SURROGATE,
    ]
    inc = "\n".join(f'.include "{p}"' for p in paths)
    return f""".options meascplxfmt=cartesian measdgt=12 plotwinsize=0
{inc}
VPLUS VPLUS18 0 18
VMINUS VMINUS18 0 -18
VZERO ZERO_VA 0 0
VBOND CHASSIS ZERO_VA 0
"""


def eq_instance(prefix: str, case: dict) -> str:
    b = network(case["bass"])
    t = treble(case["treble"])
    ct = 1e-18 if t.capacitance_nf is None else t.capacitance_nf * 1e-9
    if b.switch_condition == "SHORT":
        return (
            f"X103{prefix} N101_{prefix}_OUT N103_{prefix}_LF N103_{prefix}_OUT "
            f"VPLUS18 VMINUS18 ZERO_VA SHELLAC_SCH103_FLAT_AE066 PARAMS: CT={ct:.12g}"
        )
    return (
        f"X103{prefix} N101_{prefix}_OUT N103_{prefix}_LF N103_{prefix}_OUT "
        f"VPLUS18 VMINUS18 ZERO_VA SHELLAC_SCH103_EQ_AE066 "
        f"PARAMS: RS={b.rs_ohm:.12g} CB={b.capacitance_nf*1e-9:.12g} CT={ct:.12g}"
    )


def matrix_instance(case: dict, cpar_f: float) -> str:
    sub = "AE068_MATRIX_STEREO" if case["mode"] == "STEREO" else "AE068_MATRIX_MONO"
    return (
        f"X105 N104_L N104_R MONO_AVG MONO_R_LEG N105_L_OUT N105_R_OUT "
        f"VPLUS18 VMINUS18 ZERO_VA {sub} PARAMS: RRET=2.2Meg CPAR={cpar_f:.12g}"
    )


def run_case(cfg: dict, src: dict[str, Path], case: dict, ferrite_name: str) -> dict:
    cart_file, cart_sub = CARTRIDGES[case["cartridge"]]
    rf, rg = GAIN_PARAMS[case["gain"]]
    ferrite = cfg["ferrite_brackets"][ferrite_name]
    rfb = float(ferrite["r_ohm"])
    lfb = float(ferrite["l_h"])
    src_v = float(case["source_rms_v"])
    cable_f = float(case["cable_pf"]) * 1e-12
    service_pf = float(cfg["execution"]["cartridge_service_cap_pf"])
    service_f = 1e-18 if service_pf == 0 else service_pf * 1e-12
    out_c_f = float(cfg["execution"]["output_cable_pf_per_leg"]) * 1e-12
    load = float(cfg["execution"]["output_load_ohm"])
    cpar_f = float(cfg["execution"]["switch_parasitic_pf"]) * 1e-12

    rumble_node_l = "N107_L_FILTER" if case["rumble"] == "FILTER" else "N107_L_DIRECT"
    rumble_node_r = "N107_R_FILTER" if case["rumble"] == "FILTER" else "N107_R_DIRECT"

    measures = []
    for i, f in enumerate(FREQS):
        measures += [
            f".meas ac TERM_{i} FIND mag(V(CART_LP,CART_LN)) AT={f:.12g}",
            f".meas ac OUTL_{i} FIND mag(V(XLR_L_POS,XLR_L_NEG)) AT={f:.12g}",
            f".meas ac OUTR_{i} FIND mag(V(XLR_R_POS,XLR_R_NEG)) AT={f:.12g}",
        ]
    for name, expr in {
        "TERM1K": "mag(V(CART_LP,CART_LN))",
        "N101": "mag(V(N101_L_OUT))",
        "N103LF": "mag(V(N103_L_LF))",
        "N103": "mag(V(N103_L_OUT))",
        "N107": "mag(V(N107_L_SELECTED))",
        "N104": "mag(V(N104_L))",
        "N105": "mag(V(N105_L_OUT))",
        "N108": "mag(V(N108_L_IN))",
        "OUT1K": "mag(V(XLR_L_POS,XLR_L_NEG))",
    }.items():
        measures.append(f".meas ac {name} FIND {expr} AT=1000")
    measures += [
        ".meas ac PH20 FIND ph(V(XLR_L_POS,XLR_L_NEG)/V(CART_LP,CART_LN)) AT=20",
        ".meas ac PH1K FIND ph(V(XLR_L_POS,XLR_L_NEG)/V(CART_LP,CART_LN)) AT=1000",
        ".meas ac PH20K FIND ph(V(XLR_L_POS,XLR_L_NEG)/V(CART_LP,CART_LN)) AT=20000",
    ]

    deck = preamble(src, cart_file) + f"""
VDRIVEL DRIVE_L CART_LN AC {src_v:.12g}
VDRIVER DRIVE_R CART_RN AC {src_v:.12g}
XCARTL CART_LP CART_LN DRIVE_L {cart_sub}
XCARTR CART_RP CART_RN DRIVE_R {cart_sub}
CCABLEL CART_LP CART_LN {cable_f:.12g}
CCABLER CART_RP CART_RN {cable_f:.12g}

X101L CART_LP CART_LN N101_L_OUT VPLUS18 VMINUS18 ZERO_VA CHASSIS SHELLAC_SCH101_AE066 PARAMS: RFPROG={fmt(rf)} RGPROG={fmt(rg)} CDIFF={service_f:.12g}
X101R CART_RP CART_RN N101_R_OUT VPLUS18 VMINUS18 ZERO_VA CHASSIS SHELLAC_SCH101_AE066 PARAMS: RFPROG={fmt(rf)} RGPROG={fmt(rg)} CDIFF={service_f:.12g}

{eq_instance("L", case)}
{eq_instance("R", case)}

X107L N103_L_OUT N107_L_DIRECT N107_L_FILTER VPLUS18 VMINUS18 ZERO_VA AE067_BRANCH_LOCAL
X107R N103_R_OUT N107_R_DIRECT N107_R_FILTER VPLUS18 VMINUS18 ZERO_VA AE067_BRANCH_LOCAL
VSEL_L N107_L_SELECTED {rumble_node_l} 0
VSEL_R N107_R_SELECTED {rumble_node_r} 0

X104 N107_L_SELECTED N107_R_SELECTED N104_L N104_R MONO_AVG MONO_R_LEG VPLUS18 VMINUS18 ZERO_VA AE068_SCH104_PAIR
{matrix_instance(case, cpar_f)}

VMUTE_L N108_L_IN N105_L_OUT 0
VMUTE_R N108_R_IN N105_R_OUT 0

X108L N108_L_IN XLR_L_POS XLR_L_NEG VPLUS18 VMINUS18 ZERO_VA CHASSIS AE070_SCH108_AC_SURROGATE PARAMS: RFB={rfb:.12g} LFB={lfb:.12g}
X108R N108_R_IN XLR_R_POS XLR_R_NEG VPLUS18 VMINUS18 ZERO_VA CHASSIS AE070_SCH108_AC_SURROGATE PARAMS: RFB={rfb:.12g} LFB={lfb:.12g}
RLOADL XLR_L_POS XLR_L_NEG {load:.12g}
RLOADR XLR_R_POS XLR_R_NEG {load:.12g}
COUTLP XLR_L_POS CHASSIS {out_c_f:.12g}
COUTLM XLR_L_NEG CHASSIS {out_c_f:.12g}
COUTRP XLR_R_POS CHASSIS {out_c_f:.12g}
COUTRM XLR_R_NEG CHASSIS {out_c_f:.12g}

.ac dec {int(cfg["execution"]["ac_points_per_decade"])} {cfg["execution"]["ac_start_hz"]} {cfg["execution"]["ac_stop_hz"]}
{chr(10).join(measures)}
.end
"""
    tag = f"run07_{case['id'].lower()}_{ferrite_name.lower()}"
    log = execute_deck(tag, deck, TMP / "cases")

    term = [parse_measure(log, f"TERM_{i}") for i in range(len(FREQS))]
    outl = [parse_measure(log, f"OUTL_{i}") for i in range(len(FREQS))]
    outr = [parse_measure(log, f"OUTR_{i}") for i in range(len(FREQS))]
    i1k = nearest_index(1000.0)
    replay = [outl[i] / max(term[i], 1e-30) for i in range(len(FREQS))]
    ref = replay[i1k]
    replay_norm = [x / ref for x in replay]
    lr_db = [abs(db20(outl[i] / max(outr[i], 1e-30))) for i in range(len(FREQS))]

    target = TARGETS[case["target_id"]]
    sref = 1j * 2 * math.pi * 1000.0
    ideal_ref = ideal_curve_transfer(sref, target)
    errors = []
    for f, measured in zip(FREQS, replay_norm):
        s = 1j * 2 * math.pi * f
        ideal = abs(ideal_curve_transfer(s, target) / ideal_ref)
        errors.append(db20(measured / ideal))

    if case["replay_gate"] == "RIAA":
        idx = [i for i, f in enumerate(FREQS) if 20.0 <= f <= 20000.0]
        limit = float(cfg["criteria"]["riaa_error_db_max_20hz_20khz"])
        track_limit = float(cfg["criteria"]["riaa_lr_tracking_db_max"])
    elif case["replay_gate"] == "HISTORICAL":
        idx = [i for i, f in enumerate(FREQS) if 30.0 <= f <= 15000.0]
        limit = float(cfg["criteria"]["historical_error_db_max_30hz_15khz"])
        track_limit = float(cfg["criteria"]["historical_lr_tracking_db_max"])
    else:
        idx = []
        limit = None
        track_limit = float(cfg["criteria"]["historical_lr_tracking_db_max"])

    worst_error = max((abs(errors[i]) for i in idx), default=None)
    replay_pass = None if not idx else worst_error <= limit + 1e-9
    worst_track = max(lr_db)
    tracking_pass = worst_track <= track_limit + 1e-9

    nodes = {k: parse_measure(log, k) for k in ("TERM1K", "N101", "N103LF", "N103", "N107", "N104", "N105", "N108", "OUT1K")}
    return {
        "case_id": case["id"],
        "role": case["role"],
        "cartridge": case["cartridge"],
        "source_rms_v": src_v,
        "source_level_semantics": case["source_level_semantics"],
        "gain": case["gain"],
        "bass": case["bass"],
        "treble": case["treble"],
        "rumble": case["rumble"],
        "mode": case["mode"],
        "ferrite_bracket": ferrite_name,
        "target_id": case["target_id"],
        "replay_gate": case["replay_gate"],
        "total_gain_db_generated_emf_to_output_1khz": db20(nodes["OUT1K"] / src_v),
        "replay_gain_db_terminal_to_output_1khz": db20(nodes["OUT1K"] / max(nodes["TERM1K"], 1e-30)),
        "phase_deg_terminal_to_output": {
            "20": parse_measure(log, "PH20"),
            "1000": parse_measure(log, "PH1K"),
            "20000": parse_measure(log, "PH20K"),
        },
        "node_rms_v_1khz": nodes,
        "frequencies_hz": FREQS,
        "terminal_rms_v": term,
        "output_left_rms_v": outl,
        "output_right_rms_v": outr,
        "replay_error_db": errors,
        "worst_replay_error_db": worst_error,
        "replay_limit_db": limit,
        "replay_pass": replay_pass,
        "worst_lr_tracking_db": worst_track,
        "tracking_limit_db": track_limit,
        "tracking_pass": tracking_pass,
    }


def interpolate_crossing(freqs: list[float], vals_db: list[float], target_db: float) -> float | None:
    for a, b, ya, yb in zip(freqs, freqs[1:], vals_db, vals_db[1:]):
        if (ya - target_db) * (yb - target_db) <= 0 and yb != ya:
            t = (target_db - ya) / (yb - ya)
            return 10 ** (math.log10(a) + t * (math.log10(b) - math.log10(a)))
    return None


def analyse_pairs(cfg: dict, cases: list[dict]) -> tuple[dict, dict]:
    by_key = {(c["case_id"], c["ferrite_bracket"]): c for c in cases}
    rumble = {}
    mono = {}
    c = cfg["criteria"]
    for ferrite in cfg["ferrite_brackets"]:
        if ferrite == "interpretation":
            continue
        bp = by_key[("GRADO78_500_3400_BYPASS_STEREO", ferrite)]
        fl = by_key[("GRADO78_500_3400_FILTER_STEREO", ferrite)]
        delta = [db20(f / max(b, 1e-30)) for f, b in zip(fl["output_left_rms_v"], bp["output_left_rms_v"])]
        f3 = interpolate_crossing(FREQS, delta, -3.0)

        def at(freq: float) -> float:
            return delta[nearest_index(freq)]

        passband_peak = max(v for f, v in zip(FREQS, delta) if 20.0 <= f <= 20000.0)
        gates = {
            "f3_pass": f3 is not None and float(c["rumble_f3_hz_min"]) <= f3 <= float(c["rumble_f3_hz_max"]),
            "20hz_pass": at(20.0) >= float(c["rumble_20hz_attenuation_db_min"]) - 1e-9,
            "30hz_pass": at(30.0) >= float(c["rumble_30hz_attenuation_db_min"]) - 1e-9,
            "10hz_pass": at(10.0) <= float(c["rumble_10hz_attenuation_db_max"]) + 1e-9,
            "5hz_pass": at(5.0) <= float(c["rumble_5hz_attenuation_db_max"]) + 1e-9,
            "passband_peaking_pass": passband_peak <= float(c["rumble_passband_peaking_db_max"]) + 1e-9,
        }
        rumble[ferrite] = {
            "f3_hz": f3,
            "attenuation_db": {"5": at(5), "10": at(10), "20": at(20), "30": at(30), "50": at(50)},
            "passband_peak_db": passband_peak,
            "gates": gates,
            "pass": all(gates.values()),
        }

        mo = by_key[("GRADO78_500_3400_BYPASS_MONO", ferrite)]
        insertion = db20(mo["node_rms_v_1khz"]["OUT1K"] / bp["node_rms_v_1khz"]["OUT1K"])
        mono[ferrite] = {
            "insertion_db_1khz": insertion,
            "preferred_pass": abs(insertion) <= float(c["mono_insertion_abs_db_preferred"]) + 1e-9,
            "hard_pass": abs(insertion) <= float(c["mono_insertion_abs_db_max"]) + 1e-9,
        }
    return rumble, mono




def validate_model_composition_discriminator(cfg: dict) -> dict:
    row = cfg["run07_output_model"]["discriminator"]
    result = json.loads(COMPOSITION_RESULT.read_text(encoding="utf-8"))
    expected = row["expected"]
    if result.get("authority") != "AE-070":
        raise RuntimeError("AE-070 composition discriminator authority mismatch")
    if result.get("run_id") != "RUN07_MODEL_COMPOSITION_DISCRIMINATOR":
        raise RuntimeError("AE-070 composition discriminator run_id mismatch")
    if result.get("actual") != expected:
        raise RuntimeError(
            f"AE-070 composition discriminator pattern mismatch: "
            f"{result.get('actual')} != {expected}"
        )
    if result.get("pattern_match") is not True:
        raise RuntimeError("AE-070 composition discriminator is not PASS")
    if result.get("status") != "MODEL_COMPOSITION_LIMIT_CONFIRMED":
        raise RuntimeError("AE-070 composition discriminator disposition mismatch")
    print("AE-070 model-composition discriminator: PASS")
    return result


def validate_output_surrogate(cfg: dict) -> dict:
    # Correlate deterministic RUN07 AC surrogate to controlled AE-069 vendor-macro AC.
    evidence = json.loads(AE069_RESULT.read_text(encoding="utf-8"))
    if evidence.get("authority") != "AE-069" or evidence.get("run_id") != "RUN06":
        raise RuntimeError("AE-069 correlation evidence identity mismatch")

    model_cfg = cfg["run07_output_model"]["surrogate"]
    g_open = float(model_cfg["open_circuit_differential_gain_linear_fit"])
    r_driver_leg = float(model_cfg["fitted_internal_resistance_per_leg_ohm"])
    tol_db = float(model_cfg["correlation_tolerance_db_max"])

    rows = []
    worst = 0.0
    for ferrite_name in ("LOW_60OHM_100MHZ", "HIGH_220OHM_100MHZ"):
        ferrite_r = float(cfg["ferrite_brackets"][ferrite_name]["r_ohm"])
        ae = evidence["analysis"]["ac"][ferrite_name]["nominal"]
        for load in (100000, 20000, 10000, 600):
            total_series = 2.0 * (r_driver_leg + ferrite_r)
            surrogate_1k = g_open * load / (load + total_series)
            vendor_1k = float(ae[str(load)]["differential_gain_linear"]["1000"])
            delta_1k_db = db20(surrogate_1k / vendor_1k)
            worst = max(worst, abs(delta_1k_db))

            vendor_db = ae[str(load)]["differential_gain_db"]
            intrinsic_audio_shape_db = max(
                abs(float(vendor_db["20"]) - float(vendor_db["1000"])),
                abs(float(vendor_db["20000"]) - float(vendor_db["1000"])),
            )
            worst = max(worst, intrinsic_audio_shape_db)
            rows.append({
                "ferrite": ferrite_name,
                "load_ohm": load,
                "surrogate_gain_1khz_linear": surrogate_1k,
                "vendor_gain_1khz_linear": vendor_1k,
                "delta_1khz_db": delta_1k_db,
                "vendor_intrinsic_audio_shape_db_max": intrinsic_audio_shape_db,
            })

    passed = worst <= tol_db + 1e-12
    if not passed:
        raise RuntimeError(
            f"AE-070 output surrogate correlation failed: worst {worst:.6f} dB > {tol_db:.6f} dB"
        )
    print(f"AE-070 output surrogate correlation: PASS; worst delta/shape={worst:.6f} dB")
    return {
        "source_authority": "AE-069",
        "source_result": str(AE069_RESULT.relative_to(ROOT)),
        "tolerance_db_max": tol_db,
        "worst_delta_or_vendor_shape_db": worst,
        "pass": True,
        "rows": rows,
    }


def write_outputs(cfg: dict, result: dict) -> None:
    write_json(RESULT_JSON, result)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    with RESULT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["case_id", "ferrite", "total_gain_db_1khz", "worst_replay_error_db", "worst_lr_tracking_db", "replay_pass", "tracking_pass"])
        for row in result["cases"]:
            w.writerow([
                row["case_id"], row["ferrite_bracket"],
                row["total_gain_db_generated_emf_to_output_1khz"],
                row["worst_replay_error_db"], row["worst_lr_tracking_db"],
                row["replay_pass"], row["tracking_pass"],
            ])
    md = [
        "# AE-070 RUN07 summary", "",
        f"Status: **{result['status']}**", "",
        f"Representative cases: {len(cfg['cases'])}; ferrite-bracket executions: {len(result['cases'])}.",
        f"Replay/track gates: {'PASS' if result['gates']['replay_and_tracking_pass'] else 'FAIL'}.",
        f"Rumble integrated gate: {'PASS' if result['gates']['rumble_pass'] else 'FAIL'}.",
        f"Mono integrated insertion gate: {'PASS' if result['gates']['mono_pass'] else 'FAIL'}.",
        "",
        "RUN08 headroom/overload, RUN09 noise, RUN10 sensitivity, RUN12 switching, RUN13 rails and RUN14 phantom remain open.",
    ]
    RESULT_MD.write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")

    design = [
        "# AE-070 — RUN07 End-to-End Nominal Chain Evidence — Rev A0", "",
        "**Project:** Shellac",
        f"**Status:** {'RUN07 NOMINAL AC QUALIFIED / BENCH CORRELATION AND LATER RUNS OPEN' if result['gates']['run07_nominal_ac_pass'] else 'REVIEW REQUIRED / RUN07 NOT QUALIFIED'}",
        f"**Execution baseline:** `{cfg['baseline_commit']}`", "",
        "## Purpose",
        "Execute AE-050 RUN07 as an integrated nominal-chain AC check using the previously qualified AE-066/067/068/069 block libraries. No product-generator migration is implied.", "",
        "## Representative-state policy",
        "- representative 78 state: 500 Hz / 3400 Hz, explicitly a RUN07 representative named target rather than a new global control default;",
        "- alternate 78 state: 200 Hz / 5800 Hz using the AT-VM95SP;",
        "- RIAA compatibility state: Grado Gold/8MZ with a 5 mV project reference level used for node-level bookkeeping, not asserted as a manufacturer output specification;",
        "- rumble FILTER is judged by paired FILTER/BYPASS transfer so intentional LF filtering is not misclassified as replay-EQ error;",
        "- mono uses equal in-phase channels and is compared with the matched stereo case;",
        "- both AE-069 ferrite engineering brackets are swept; AE-070 does not select a ferrite;",
        "- integrated vendor THAT1646 Rev02 operating-point composition is non-convergent, so RUN07 uses a qualification-only small-signal AC surrogate correlated to AE-069; this surrogate cannot support DC, CM, stability, distortion, overload, switching or fault claims;",
        "- the surrogate output-stage phase contribution is separately correlated against the isolated vendor macro at 20 Hz, 1 kHz and 20 kHz under the RUN07 load/cable condition and both ferrite brackets; the sidecar prevents the surrogate phase from being mistaken for vendor-macro phase authority.", "",
        "## Qualification boundary",
        "Replay accuracy is evaluated from loaded cartridge terminals to balanced output. Generated cartridge EMF to output is separately recorded as the complete system transfer. Nominal node levels are recorded at 1 kHz. L/R comparison in RUN07 is nominal model symmetry only; tolerance tracking remains RUN10/RUN11 work. RUN07 does not perform clipping, overload recovery, noise, switching, rail or phantom-fault qualification.", "",
        "## Headline gates",
        f"- replay and L/R nominal model symmetry: {'PASS' if result['gates']['replay_and_tracking_pass'] else 'FAIL'}; tolerance tracking remains RUN10/RUN11 work.",
        f"- integrated rumble response: {'PASS' if result['gates']['rumble_pass'] else 'FAIL'};",
        f"- integrated mono insertion: {'PASS' if result['gates']['mono_pass'] else 'FAIL'};",
        f"- overall RUN07 nominal AC: {'PASS' if result['gates']['run07_nominal_ac_pass'] else 'FAIL'}.", "",
        "## Simulation infrastructure correction",
        "AE-070 exposed a shared LTspice `ph(...)` tuple-parser defect: LTspice 26 reports phase expressions as `(magnitude dB, phase degrees)`, while the former parser returned the first tuple member. The parser is corrected and regression-tested using the exact observed LTspice format.", "",
        "Blast-radius review found phase/group-delay fields in AE-066 RUN03, AE-067 RUN04 and AE-068 RUN05. Their qualification gates do not depend on those fields; the affected structured evidence is regenerated under the corrected parser without changing their historical architecture decisions or baseline metadata.", "",
        "## Deferred",
        "- RUN08 first-clipping/headroom/recovery;",
        "- RUN09 system noise;",
        "- RUN10 sensitivity/value engineering;",
        "- RUN12 switching;",
        "- RUN13 rail variation/ripple;",
        "- RUN14 phantom fault;",
        "- prototype bench correlation, including the still-open RUN06 load-stability and dynamic-THD gates.", "",
        "## Evidence",
        "- `simulation/results/run07_end_to_end/ae070_run07.json`",
        "- `simulation/results/run07_end_to_end/ae070_run07.csv`",
        "- `simulation/results/run07_end_to_end/ae070_run07.md`",
        "- `simulation/results/run07_end_to_end/ae070_output_phase_correlation.json`",
    ]
    DESIGN_RECORD.write_text("\n".join(design) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    validate_ltspice()
    cfg = yaml.safe_load(CFG.read_text(encoding="utf-8"))
    src = source_paths()
    ferrites = [k for k in cfg["ferrite_brackets"] if k != "interpretation"]

    print("=== AE-070 RUN07: end-to-end nominal chain ===")
    model_composition_discriminator = validate_model_composition_discriminator(cfg)
    output_model_correlation = validate_output_surrogate(cfg)
    cases = []
    for spec in cfg["cases"]:
        for ferrite in ferrites:
            row = run_case(cfg, src, spec, ferrite)
            cases.append(row)
            print(
                f"{spec['id']} / {ferrite}: total1k={row['total_gain_db_generated_emf_to_output_1khz']:.3f} dB "
                f"replay_err={row['worst_replay_error_db']} track={row['worst_lr_tracking_db']:.6f} dB"
            )

    rumble, mono = analyse_pairs(cfg, cases)
    replay_track_pass = all(
        (row["replay_pass"] in (None, True)) and row["tracking_pass"]
        for row in cases
    )
    rumble_pass = all(x["pass"] for x in rumble.values())
    mono_pass = all(x["hard_pass"] for x in mono.values())
    overall = replay_track_pass and rumble_pass and mono_pass

    result = {
        "schema_version": 1,
        "authority": "AE-070",
        "run_id": "RUN07",
        "repository_commit_before_ae070": cfg["baseline_commit"],
        "model_semantics": cfg["model_semantics"],
        "generator_migration_implied": False,
        "status": "QUALIFIED_NOMINAL_REPRESENTATIVE_STATES" if overall else "REVIEW_REQUIRED",
        "case_count": len(cases),
        "cases": cases,
        "model_composition_discriminator": {
            "status": model_composition_discriminator["status"],
            "pattern_match": model_composition_discriminator["pattern_match"],
            "result": str(COMPOSITION_RESULT.relative_to(ROOT)),
        },
        "output_model_correlation": output_model_correlation,
        "derived": {"rumble": rumble, "mono": mono},
        "gates": {
            "replay_and_tracking_pass": replay_track_pass,
            "rumble_pass": rumble_pass,
            "mono_pass": mono_pass,
            "run07_nominal_ac_pass": overall,
            "ferrite_selected": False,
            "overload_qualified": False,
            "noise_qualified": False,
            "bench_correlation_required": True,
        },
        "deferred": cfg["decision_policy"],
    }
    write_outputs(cfg, result)

    print("\n=== RUN07 SUMMARY ===")
    for k, v in result["gates"].items():
        print(f"{k}: {v}")
    print("Result:", RESULT_JSON)
    return 0 if overall else 2


if __name__ == "__main__":
    raise SystemExit(main())
