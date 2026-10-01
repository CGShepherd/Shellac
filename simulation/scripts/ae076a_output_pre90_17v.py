#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import yaml

from simulation.scripts import ae069_run06 as r6
from simulation.scripts.sim_support import ROOT, resolve_source, validate_ltspice, write_json

CFG = ROOT / "simulation/config/ae076a_17v_requalification.yaml"
HIST = ROOT / "simulation/config/ae069_run06_output.yaml"
TMP = ROOT / ".ae076a_output_pre90_17v_tmp"
RESULT_DIR = ROOT / "simulation/results/ae076a_17v"
RESULT_JSON = RESULT_DIR / "ae076a_output_pre90_17v.json"
RESULT_MD = RESULT_DIR / "ae076a_output_pre90_17v.md"


def main() -> int:
    app = yaml.safe_load(CFG.read_text(encoding="utf-8"))
    hist = yaml.safe_load(HIST.read_text(encoding="utf-8"))
    cfg = copy.deepcopy(hist)
    validate_ltspice()

    if app["nominal_rails_v"] != {"plus": 17.0, "minus": -17.0}:
        raise RuntimeError("AE-076A configuration is not +/-17 V")

    # Reuse the qualified AE-069 device/topology machinery without rewriting
    # historical AE-069. Intercept each generated deck and translate only its
    # solver-local rail aliases/sources to the AE-076A 17 V condition.
    original_execute = r6.execute_deck

    def execute_17v(tag, deck, outdir):
        translated = deck.replace("VPLUS18", "VPLUS17").replace("VMINUS18", "VMINUS17")
        translated = translated.replace("VPLUS VPLUS17 0 18", "VPLUS VPLUS17 0 17")
        translated = translated.replace("VMINUS VMINUS17 0 -18", "VMINUS VMINUS17 0 -17")
        if "VPLUS18" in translated or "VMINUS18" in translated:
            raise RuntimeError("stale 18 V solver node alias remains in translated deck")
        return original_execute(tag, translated, outdir)

    r6.execute_deck = execute_17v
    r6.TMP = TMP
    old_vendor = ROOT / ".ae069_run06_tmp/vendor"
    r6.VENDOR = old_vendor if old_vendor.is_dir() else TMP / "vendor"

    cfg["execution"]["headroom_input_rms_v"] = [0.321, 3.21, 4.66, 5.0]
    cfg["execution"]["rails_v"] = 17.0

    that = resolve_source("THAT1646", r6.VENDOR)
    s1g = resolve_source("S1G", r6.VENDOR)

    q = app["output_requalification"]
    ref_load = float(q["reference_load_ohm"])
    normal_load = float(q["normal_load_ohm"])
    pre90_load = float(q["pre90_load_ohm"])
    high_input = float(q["high_gain_that1646_input_rms_v"])
    sensitivity = float(q["pre90_published_input_sensitivity_vrms_at_0db"])
    criteria = app["criteria"]

    ferrites = {}
    insertion_values = []

    for ferrite in cfg["ferrite_brackets"]:
        audio_ac = {}
        for cable_pf in q["cable_capacitance_per_leg_pf"]:
            reference = r6.ac_case(
                cfg, that, s1g, ferrite, ref_load, float(cable_pf)
            )
            loaded = r6.ac_case(
                cfg, that, s1g, ferrite, pre90_load, float(cable_pf)
            )
            rows = {}
            for hz in cfg["execution"]["ac_report_hz"]:
                key = str(hz)
                ratio = (
                    loaded["differential_gain_linear"][key]
                    / reference["differential_gain_linear"][key]
                )
                db = r6.db20(ratio)
                insertion_values.append(db)
                rows[key] = {
                    "ratio": ratio,
                    "insertion_db_vs_100k": db,
                }
            audio_ac[str(cable_pf)] = rows

        dc_pre90 = r6.dc_case(cfg, that, s1g, ferrite, pre90_load)
        qs_normal = r6.quasistatic_transfer_case(
            cfg, that, s1g, ferrite, normal_load
        )
        qs_pre90 = r6.quasistatic_transfer_case(
            cfg, that, s1g, ferrite, pre90_load
        )

        high_row = next(
            row for row in qs_pre90["headroom_sweep"]
            if abs(row["input_rms_v"] - high_input) < 1e-9
        )
        high_output = high_row[
            "output_rms_v_from_symmetric_peak_transfer"
        ]
        high_margin = r6.db20(sensitivity / high_output)

        ferrites[ferrite] = {
            "audio_ac_pre90_vs_100k": audio_ac,
            "dc_pre90": dc_pre90,
            "quasistatic_10k": qs_normal,
            "quasistatic_pre90_2k": qs_pre90,
            "high_gain_pre90": {
                "that1646_input_rms_v": high_input,
                "output_rms_v": high_output,
                "compression_fraction_vs_low_level":
                    high_row["compression_fraction_vs_quasistatic_low_level"],
                "margin_to_pre90_9p3vrms_db": high_margin,
            },
        }

    worst_insertion = max(abs(x) for x in insertion_values)
    dc_pass = all(
        row["dc_pre90"]["diff_absolute_pass"]
        and row["dc_pre90"]["cm_absolute_pass"]
        for row in ferrites.values()
    )
    severe_margin_min = min(
        row["quasistatic_10k"]["severe_margin_to_10vrms_design_ceiling_db"]
        for row in ferrites.values()
    )
    high_compression_max = max(
        row["high_gain_pre90"]["compression_fraction_vs_low_level"]
        for row in ferrites.values()
    )
    pre90_margin_min = min(
        row["high_gain_pre90"]["margin_to_pre90_9p3vrms_db"]
        for row in ferrites.values()
    )
    high_output_max = max(
        row["high_gain_pre90"]["output_rms_v"]
        for row in ferrites.values()
    )

    gates = {
        "pre90_insertion_loss_pass":
            worst_insertion <= float(criteria["pre90_insertion_loss_abs_db_max"]),
        "dc_absolute_pass": dc_pass,
        "severe_3p21vrms_10k_margin_pass":
            severe_margin_min
            >= float(criteria["severe_3p21vrms_margin_to_10vrms_db_min"]),
        "high_gain_2k_compression_pass":
            high_compression_max
            <= float(criteria["local_compression_fraction_max"]),
        "pre90_high_gain_level_margin_pass":
            pre90_margin_min
            >= float(criteria["pre90_high_gain_margin_db_min"]),
    }
    passed = all(gates.values())

    result = {
        "schema_version": 1,
        "authority": "AE-076A",
        "run_id": "OUTPUT_PRE90_17V",
        "status": (
            "PASS_17V_OUTPUT_PRE90_REQUALIFICATION_BENCH_GATES_RETAINED"
            if passed else
            "FAIL_17V_OUTPUT_PRE90_REQUALIFICATION_REVIEW_REQUIRED"
        ),
        "pass": passed,
        "nominal_rails_v": app["nominal_rails_v"],
        "historical_ae069_modified": False,
        "historical_ae075g_modified": False,
        "method": (
            "AE-069 qualified topology/device helper reused through execution-time "
            "solver rail translation to +/-17 V; historical source/evidence unchanged"
        ),
        "gates": gates,
        "headline": {
            "worst_abs_insertion_loss_db_vs_100k": worst_insertion,
            "severe_3p21vrms_10k_margin_to_10vrms_db_min": severe_margin_min,
            "high_gain_pre90_output_rms_v_max": high_output_max,
            "high_gain_pre90_compression_fraction_max": high_compression_max,
            "high_gain_pre90_margin_to_9p3vrms_db_min": pre90_margin_min,
        },
        "ferrites": ferrites,
        "bench_and_future_gates_retained": app["boundary"],
    }

    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(RESULT_JSON, result)

    lines = [
        "# AE-076A +/-17 V output and PRE90 requalification",
        "",
        f"Status: **{result['status']}**",
        "",
        f"- Worst absolute 2 kOhm insertion loss vs 100 kOhm: {worst_insertion:.6f} dB",
        f"- Minimum 3.21 Vrms / 10 kOhm margin to 10 Vrms design ceiling: {severe_margin_min:.4f} dB",
        f"- Maximum high-gain PRE90 output at 4.66 Vrms THAT1646 input: {high_output_max:.6f} Vrms",
        f"- Maximum high-gain compression fraction: {high_compression_max:.8f}",
        f"- Minimum margin to PRE90 9.3 Vrms @ 0 dB sensitivity: {pre90_margin_min:.4f} dB",
        "",
        "Historical AE-069 and AE-075G evidence is unchanged.",
        "RUN06 load/cable stability and dynamic-THD bench gates remain open.",
        "RUN08 overload/recovery, RUN13 rail variation and RUN14 phantom-fault work remain open.",
        "Powered PSU setpoint/dropout/ripple/startup/thermal qualification remains open.",
        "",
    ]
    RESULT_MD.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    print("=== AE-076A +/-17 V output/PRE90 requalification ===")
    for key, value in result["headline"].items():
        print(f"{key}: {value}")
    for key, value in gates.items():
        print(f"{key}: {'PASS' if value else 'FAIL'}")
    print(f"Result: {RESULT_JSON.relative_to(ROOT)}")
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
