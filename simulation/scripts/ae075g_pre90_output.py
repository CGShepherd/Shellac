#!/usr/bin/env python3
from __future__ import annotations

import math
import yaml

from simulation.scripts import ae069_run06 as r6
from simulation.scripts.sim_support import (
    ROOT, resolve_source, validate_ltspice, write_json
)

CFG = ROOT / "simulation/config/ae075g_pre90_output.yaml"
RUN06_CFG = ROOT / "simulation/config/ae069_run06_output.yaml"
RESULT_DIR = ROOT / "simulation/results/ae075g_pre90_output"
RESULT_JSON = RESULT_DIR / "ae075g_pre90_output.json"
RESULT_MD = RESULT_DIR / "ae075g_pre90_output.md"
TMP = ROOT / ".ae075g_pre90_tmp"

def main():
    app = yaml.safe_load(CFG.read_text(encoding="utf-8"))
    hist = yaml.safe_load(RUN06_CFG.read_text(encoding="utf-8"))
    validate_ltspice()

    r6.TMP = TMP
    old_vendor = ROOT / ".ae069_run06_tmp/vendor"
    r6.VENDOR = old_vendor if old_vendor.is_dir() else TMP / "vendor"

    that = resolve_source("THAT1646", r6.VENDOR)
    s1g = resolve_source("S1G", r6.VENDOR)
    _, murata = r6.resolve_murata_models(hist)

    load = float(app["application"]["balanced_input_load_ohm"])
    ref_load = float(app["application"]["reference_load_ohm"])
    insertions, peaks, ratios = [], [], []
    ferrites = {}

    for ferrite in hist["ferrite_brackets"]:
        ac_rows = {}
        for cable_pf in app["execution"]["cable_capacitance_per_leg_pf"]:
            ref = r6.ac_case(hist, that, s1g, ferrite, ref_load, float(cable_pf))
            dut = r6.ac_case(hist, that, s1g, ferrite, load, float(cable_pf))
            freq = {}
            for hz in hist["execution"]["ac_report_hz"]:
                k = str(hz)
                ratio = (
                    dut["differential_gain_linear"][k]
                    / ref["differential_gain_linear"][k]
                )
                db = r6.db20(ratio)
                freq[k] = {"ratio": ratio, "insertion_db_vs_100k": db}
                insertions.append(db)
                ratios.append(ratio)
            peak = dut["passband_peak_db_rel_1khz"]
            peaks.append(peak)
            ac_rows[str(cable_pf)] = {
                "frequency": freq,
                "passband_peak_db_rel_1khz": peak,
            }

        dc = r6.dc_case(hist, that, s1g, ferrite, load)
        hf = r6.hf_stability_ac_case(hist, that, s1g, ferrite, load, murata)
        qs = r6.quasistatic_transfer_case(hist, that, s1g, ferrite, load)
        ferrites[ferrite] = {
            "audio_ac": ac_rows,
            "dc": dc,
            "hf_small_signal": hf,
            "quasistatic": qs,
        }

    worst_loss = max(abs(x) for x in insertions)
    worst_peak = max(peaks)
    max_ratio = max(ratios)

    insertion_pass = worst_loss <= float(app["criteria"]["insertion_loss_abs_db_max"])
    peak_pass = worst_peak <= float(app["criteria"]["passband_peak_db_max"])
    dc_pass = all(
        v["dc"]["diff_absolute_pass"] and v["dc"]["cm_absolute_pass"]
        for v in ferrites.values()
    )
    hf_complete = all(v["hf_small_signal"]["completed"] for v in ferrites.values())
    headroom_pass = all(
        v["quasistatic"]["severe_minimum_margin_pass"]
        for v in ferrites.values()
    )
    distortion_recorded = all(
        math.isfinite(
            v["quasistatic"]["distortion_estimate"]["thd_percent_h2_to_hmax"]
        )
        for v in ferrites.values()
    )
    load_pass = all((
        insertion_pass, peak_pass, dc_pass,
        hf_complete, headroom_pass, distortion_recorded
    ))

    sensitivity = float(
        app["application"]["published_input_sensitivity_vrms_at_0db"]
    )
    loaded = {
        k: float(v) * max_ratio
        for k, v in app["representative_shellac_outputs_vrms_unloaded"].items()
    }
    margins = {k: r6.db20(sensitivity / v) for k, v in loaded.items()}
    high_margin = margins["worst_high_gain"]

    result = {
        "schema_version": 1,
        "authority": "AE-075G",
        "status": (
            "LOAD_COMPATIBILITY_PASS_HIGH_LEVEL_MARGIN_REQUIRES_BENCH_CONFIRMATION"
            if load_pass else
            "APPLICATION_LOAD_DISCRIMINATOR_FAIL_REVIEW_REQUIRED"
        ),
        "historical_run06_modified": False,
        "application": app["application"],
        "headline": {
            "worst_abs_insertion_loss_db_vs_100k": worst_loss,
            "worst_passband_peak_db": worst_peak,
            "insertion_loss_pass": insertion_pass,
            "passband_peak_pass": peak_pass,
            "dc_absolute_pass": dc_pass,
            "hf_small_signal_evidence_complete": hf_complete,
            "severe_3p21vrms_headroom_pass": headroom_pass,
            "quasistatic_distortion_estimate_recorded": distortion_recorded,
            "load_compatibility_pass": load_pass,
        },
        "ferrites": ferrites,
        "loaded_representative_shellac_outputs_vrms": loaded,
        "pre90_0db_sensitivity_margin_db": margins,
        "high_gain_level_disposition": (
            "MARGINAL_BENCH_CONFIRMATION_REQUIRED"
            if high_margin < 1.0 else
            "AT_LEAST_1DB_MARGIN"
        ),
        "bench_gates_retained": app["boundary"],
        "placement_disposition":
            "H801_H802_XY_PROVISIONAL_PENDING_MANUAL_PLACEMENT_RECONCILIATION",
    }

    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(RESULT_JSON, result)

    lines = [
        "# AE-075G PRE90 2 kOhm discriminator",
        "",
        f"Status: **{result['status']}**",
        "",
        f"- Worst absolute insertion loss vs 100 kOhm: {worst_loss:.6f} dB",
        f"- Worst passband peak: {worst_peak:.6f} dB",
        f"- Load discriminator: {'PASS' if load_pass else 'FAIL'}",
        "",
        "## Loaded representative Shellac outputs",
    ]
    for key, value in loaded.items():
        lines.append(
            f"- {key}: {value:.6f} Vrms; "
            f"margin to 9.3 Vrms @0 dB = {margins[key]:.4f} dB"
        )
    lines += [
        "",
        "Historical AE-069 RUN06 evidence is unchanged.",
        "RUN06 load/cable stability and dynamic-THD bench gates remain open.",
        "H801/H802 XY remains provisional pending manual placement reconciliation.",
        "",
    ]
    RESULT_MD.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    print("=== AE-075G PRE90 discriminator ===")
    print(f"Worst abs insertion loss vs 100k: {worst_loss:.6f} dB")
    print(f"Worst passband peak: {worst_peak:.6f} dB")
    print(f"Load compatibility: {'PASS' if load_pass else 'FAIL'}")
    print(
        "Worst-high-gain loaded estimate: "
        f"{loaded['worst_high_gain']:.6f} Vrms; "
        f"margin to 9.3 Vrms = {margins['worst_high_gain']:.4f} dB"
    )
    print(f"Result: {RESULT_JSON.relative_to(ROOT)}")
    return 0 if load_pass else 2

if __name__ == "__main__":
    raise SystemExit(main())
