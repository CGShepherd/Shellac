#!/usr/bin/env python3
from __future__ import annotations

import yaml

from simulation.scripts.sim_support import (
    ROOT,
    execute_deck,
    parse_measure,
    resolve_source,
    validate_ltspice,
    write_json,
)

CFG = ROOT / "simulation/config/ae070_run07_end_to_end.yaml"
TMP = ROOT / ".ae070_run07_tmp" / "phase_correlation"
VENDOR = TMP / "vendor"
RESULT = ROOT / "simulation/results/run07_end_to_end/ae070_output_phase_correlation.json"
WRAP = ROOT / "simulation/models/wrappers/that1646_shellac.lib"
LIB69 = ROOT / "simulation/models/qualification/sch108_ae069.lib"
SURROGATE = ROOT / "simulation/models/qualification/sch108_ae070_ac_surrogate.lib"
FREQS = (20, 1000, 20000)


def wrap_deg(value: float) -> float:
    while value > 180.0:
        value -= 360.0
    while value <= -180.0:
        value += 360.0
    return value


def main() -> int:
    cfg = yaml.safe_load(CFG.read_text(encoding="utf-8"))
    if cfg.get("authority") != "AE-070" or cfg.get("run_id") != "RUN07":
        raise RuntimeError("AE-070 configuration identity mismatch")
    phase_cfg = cfg["run07_output_model"]["phase_correlation"]
    limit = float(phase_cfg["max_abs_delta_deg"])
    load = float(cfg["execution"]["output_load_ohm"])
    cout = float(cfg["execution"]["output_cable_pf_per_leg"]) * 1e-12

    validate_ltspice()
    that = resolve_source("THAT1646", VENDOR)
    s1g = resolve_source("S1G", VENDOR)

    rows = []
    worst = 0.0
    for ferrite_name in ("LOW_60OHM_100MHZ", "HIGH_220OHM_100MHZ"):
        ferrite = cfg["ferrite_brackets"][ferrite_name]
        rfb = float(ferrite["r_ohm"])
        lfb = float(ferrite["l_h"])
        measures = []
        for f in FREQS:
            measures.extend([
                f".meas ac VPH{f} FIND ph(V(VP,VM)/V(IN)) AT={f}",
                f".meas ac SPH{f} FIND ph(V(SP,SM)/V(IN)) AT={f}",
            ])
        deck = f""".options meascplxfmt=cartesian measdgt=12 plotwinsize=0
.include "{that}"
.include "{s1g}"
.include "{WRAP}"
.include "{LIB69}"
.include "{SURROGATE}"
VPLUS VPLUS18 0 18
VMINUS VMINUS18 0 -18
VZERO ZERO_VA 0 0
VBOND CHASSIS ZERO_VA 0
VIN IN ZERO_VA AC 1
XV IN VP VM VPLUS18 VMINUS18 ZERO_VA CHASSIS AE069_SCH108 PARAMS: RFB={rfb:.12g} LFB={lfb:.12g}
RV VP VM {load:.12g}
CVP VP CHASSIS {cout:.12g}
CVM VM CHASSIS {cout:.12g}
XS IN SP SM VPLUS18 VMINUS18 ZERO_VA CHASSIS AE070_SCH108_AC_SURROGATE PARAMS: RFB={rfb:.12g} LFB={lfb:.12g}
RS SP SM {load:.12g}
CSP SP CHASSIS {cout:.12g}
CSM SM CHASSIS {cout:.12g}
.ac dec 100 5 100000
{chr(10).join(measures)}
.end
"""
        log = execute_deck(f"ae070_phase_{ferrite_name.lower()}", deck, TMP / "cases")
        for f in FREQS:
            vendor_phase = parse_measure(log, f"VPH{f}")
            surrogate_phase = parse_measure(log, f"SPH{f}")
            delta = wrap_deg(vendor_phase - surrogate_phase)
            worst = max(worst, abs(delta))
            rows.append({
                "ferrite_bracket": ferrite_name,
                "frequency_hz": f,
                "vendor_phase_deg": vendor_phase,
                "surrogate_phase_deg": surrogate_phase,
                "vendor_minus_surrogate_deg": delta,
            })

    passed = worst <= limit + 1e-12
    result = {
        "schema_version": 1,
        "authority": "AE-070",
        "run_id": "RUN07_PHASE_CORRELATION",
        "purpose": "Output-only THAT1646 vendor-macro phase correlation for the RUN07 AC surrogate.",
        "model_semantics": "SUPPORTING_CORRELATION_EVIDENCE_NOT_PRODUCT_MODEL",
        "configuration": {
            "output_load_ohm": load,
            "output_cable_pf_per_leg": cfg["execution"]["output_cable_pf_per_leg"],
            "frequencies_hz": list(FREQS),
            "ferrite_brackets": ["LOW_60OHM_100MHZ", "HIGH_220OHM_100MHZ"],
        },
        "acceptance": {
            "max_abs_delta_deg": limit,
            "worst_abs_delta_deg": worst,
            "pass": passed,
        },
        "rows": rows,
        "interpretation": (
            "The phase delta is the isolated output-stage correction omitted by the "
            "qualification-only RUN07 surrogate. RUN07 phase is informative rather "
            "than a separate AE-049 product gate; this record prevents a zero-phase "
            "surrogate from being mistaken for vendor-macro phase authority."
        ),
    }
    write_json(RESULT, result)
    print("=== AE-070 output-stage phase correlation ===")
    for row in rows:
        print(
            f"{row['ferrite_bracket']} {row['frequency_hz']:>5} Hz: "
            f"vendor={row['vendor_phase_deg']:+.6f} deg, "
            f"surrogate={row['surrogate_phase_deg']:+.6f} deg, "
            f"delta={row['vendor_minus_surrogate_deg']:+.6f} deg"
        )
    print(f"Worst |vendor-surrogate| phase delta: {worst:.6f} deg")
    print("Phase correlation gate:", "PASS" if passed else "FAIL")
    print("Wrote", RESULT.relative_to(ROOT))
    if not passed:
        raise RuntimeError(
            f"AE-070 output phase correlation {worst:.6f} deg exceeds {limit:.6f} deg"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
