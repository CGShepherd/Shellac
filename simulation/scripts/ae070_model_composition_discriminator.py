#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

import yaml

from simulation.scripts.sim_support import (
    FATAL_TERMS,
    LTSPICE,
    ROOT,
    _decode_ltspice_log,
    resolve_source,
    validate_ltspice,
    write_json,
)
from simulation.scripts.ae070_run07 import eq_instance, matrix_instance

CFG = ROOT / "simulation/config/ae070_run07_end_to_end.yaml"
OUT = ROOT / ".ae070_run07_tmp" / "composition_discriminator"
VENDOR = ROOT / ".ae070_run07_tmp" / "vendor"
RESULT = ROOT / "simulation/results/run07_end_to_end/ae070_model_composition_discriminator.json"

WRAP = ROOT / "simulation/models/wrappers"
LIB66 = ROOT / "simulation/models/qualification/sch101_sch103_ae066.lib"
LIB67 = ROOT / "simulation/models/qualification/dr039_sch107_ae067.lib"
LIB68 = ROOT / "simulation/models/qualification/sch104_sch105_ae068.lib"
LIB69 = ROOT / "simulation/models/qualification/sch108_ae069.lib"
CART = ROOT / "simulation/models/cartridges/grado_78c_shellac.lib"

TIMEOUT_S = 20
EXPECTED = {
    "output_pair_only": "PASS",
    "dual_upstream_no_that": "PASS",
    "dual_full_ideal_output": "PASS",
    "dual_full_vendor_that": "TIMEOUT",
}


def resolve_sources():
    return {
        "OPA1656": resolve_source("OPA1656", VENDOR),
        "OPA1612": resolve_source("OPA1612", VENDOR),
        "LT5400": resolve_source("LT5400", VENDOR),
        "THAT1646": resolve_source("THAT1646", VENDOR),
        "S1G": resolve_source("S1G", VENDOR),
    }


def preamble(src, vendor_output: bool):
    paths = [
        src["OPA1656"], src["OPA1612"], src["LT5400"], src["S1G"],
        WRAP / "opa1656_shellac.lib",
        WRAP / "opa1612_shellac.lib",
        WRAP / "lt5400_7_shellac.lib",
        CART, LIB66, LIB67, LIB68,
    ]
    if vendor_output:
        paths += [src["THAT1646"], WRAP / "that1646_shellac.lib", LIB69]
    inc = "\n".join(f'.include "{x}"' for x in paths)
    return (
        ".options meascplxfmt=cartesian measdgt=12 plotwinsize=0\n"
        + inc
        + "\nVPLUS VPLUS18 0 18\n"
          "VMINUS VMINUS18 0 -18\n"
          "VZERO ZERO_VA 0 0\n"
          "VBOND CHASSIS ZERO_VA 0\n"
    )


def representative_case():
    cfg = yaml.safe_load(CFG.read_text(encoding="utf-8"))
    case = next(
        x for x in cfg["cases"]
        if x["id"] == "GRADO78_500_3400_BYPASS_STEREO"
    )
    return cfg, case


def upstream(cfg, case):
    cpar = float(cfg["execution"]["switch_parasitic_pf"]) * 1e-12
    cable = float(case["cable_pf"]) * 1e-12
    eq_l = eq_instance("L", case)
    eq_r = eq_instance("R", case)
    matrix = matrix_instance(case, cpar)
    return f"""
VDRIVEL DRIVE_L CART_LN AC 0.005
VDRIVER DRIVE_R CART_RN AC 0.005
XCARTL CART_LP CART_LN DRIVE_L SHELLAC_GRADO_78C
XCARTR CART_RP CART_RN DRIVE_R SHELLAC_GRADO_78C
CCABLEL CART_LP CART_LN {cable:.12g}
CCABLER CART_RP CART_RN {cable:.12g}

X101L CART_LP CART_LN N101_L_OUT VPLUS18 VMINUS18 ZERO_VA CHASSIS SHELLAC_SCH101_AE066 PARAMS: RFPROG=1T RGPROG=1T CDIFF=1e-18
X101R CART_RP CART_RN N101_R_OUT VPLUS18 VMINUS18 ZERO_VA CHASSIS SHELLAC_SCH101_AE066 PARAMS: RFPROG=1T RGPROG=1T CDIFF=1e-18

{eq_l}
{eq_r}

X107L N103_L_OUT N107_L_DIRECT N107_L_FILTER VPLUS18 VMINUS18 ZERO_VA AE067_BRANCH_LOCAL
X107R N103_R_OUT N107_R_DIRECT N107_R_FILTER VPLUS18 VMINUS18 ZERO_VA AE067_BRANCH_LOCAL
VSEL_L N107_L_SELECTED N107_L_DIRECT 0
VSEL_R N107_R_SELECTED N107_R_DIRECT 0

X104 N107_L_SELECTED N107_R_SELECTED N104_L N104_R MONO_AVG MONO_R_LEG VPLUS18 VMINUS18 ZERO_VA AE068_SCH104_PAIR
{matrix}
"""


def vendor_output(cfg):
    f = cfg["ferrite_brackets"]["LOW_60OHM_100MHZ"]
    rfb = float(f["r_ohm"])
    lfb = float(f["l_h"])
    load = float(cfg["execution"]["output_load_ohm"])
    cout = float(cfg["execution"]["output_cable_pf_per_leg"]) * 1e-12
    return f"""
X108L N105_L_OUT XLR_L_POS XLR_L_NEG VPLUS18 VMINUS18 ZERO_VA CHASSIS AE069_SCH108 PARAMS: RFB={rfb:.12g} LFB={lfb:.12g}
X108R N105_R_OUT XLR_R_POS XLR_R_NEG VPLUS18 VMINUS18 ZERO_VA CHASSIS AE069_SCH108 PARAMS: RFB={rfb:.12g} LFB={lfb:.12g}
RLOADL XLR_L_POS XLR_L_NEG {load:.12g}
RLOADR XLR_R_POS XLR_R_NEG {load:.12g}
COUTLP XLR_L_POS CHASSIS {cout:.12g}
COUTLM XLR_L_NEG CHASSIS {cout:.12g}
COUTRP XLR_R_POS CHASSIS {cout:.12g}
COUTRM XLR_R_NEG CHASSIS {cout:.12g}
"""


def ideal_output(cfg):
    load = float(cfg["execution"]["output_load_ohm"])
    cout = float(cfg["execution"]["output_cable_pf_per_leg"]) * 1e-12
    return f"""
EIP_L XLR_L_POS ZERO_VA N105_L_OUT ZERO_VA 1
EIM_L XLR_L_NEG ZERO_VA N105_L_OUT ZERO_VA -1
EIP_R XLR_R_POS ZERO_VA N105_R_OUT ZERO_VA 1
EIM_R XLR_R_NEG ZERO_VA N105_R_OUT ZERO_VA -1
RLOADL XLR_L_POS XLR_L_NEG {load:.12g}
RLOADR XLR_R_POS XLR_R_NEG {load:.12g}
COUTLP XLR_L_POS CHASSIS {cout:.12g}
COUTLM XLR_L_NEG CHASSIS {cout:.12g}
COUTRP XLR_R_POS CHASSIS {cout:.12g}
COUTRM XLR_R_NEG CHASSIS {cout:.12g}
"""


def finish(expr):
    return f"""
.ac lin 1 1000 1000
.meas ac PROBE FIND mag({expr}) AT=1000
.end
"""


def decks(src):
    cfg, case = representative_case()

    output_pair = (
        preamble(src, True)
        + "\nVINL IN_L ZERO_VA AC 0.1\nVINR IN_R ZERO_VA AC 0.1\n"
        + """
X108L IN_L XLR_L_POS XLR_L_NEG VPLUS18 VMINUS18 ZERO_VA CHASSIS AE069_SCH108 PARAMS: RFB=0.02 LFB=95.49296055n
X108R IN_R XLR_R_POS XLR_R_NEG VPLUS18 VMINUS18 ZERO_VA CHASSIS AE069_SCH108 PARAMS: RFB=0.02 LFB=95.49296055n
RLOADL XLR_L_POS XLR_L_NEG 20k
RLOADR XLR_R_POS XLR_R_NEG 20k
COUTLP XLR_L_POS CHASSIS 500p
COUTLM XLR_L_NEG CHASSIS 500p
COUTRP XLR_R_POS CHASSIS 500p
COUTRM XLR_R_NEG CHASSIS 500p
"""
        + finish("V(XLR_L_POS,XLR_L_NEG)")
    )

    upstream_only = (
        preamble(src, False)
        + upstream(cfg, case)
        + "\nRTERML N105_L_OUT ZERO_VA 100k\nRTERMR N105_R_OUT ZERO_VA 100k\n"
        + finish("V(N105_L_OUT)")
    )

    full_ideal = (
        preamble(src, False)
        + upstream(cfg, case)
        + ideal_output(cfg)
        + finish("V(XLR_L_POS,XLR_L_NEG)")
    )

    full_vendor = (
        preamble(src, True)
        + upstream(cfg, case)
        + vendor_output(cfg)
        + finish("V(XLR_L_POS,XLR_L_NEG)")
    )

    return [
        ("output_pair_only", output_pair),
        ("dual_upstream_no_that", upstream_only),
        ("dual_full_ideal_output", full_ideal),
        ("dual_full_vendor_that", full_vendor),
    ]


def run_case(name, deck):
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="Shellac_AE070_composition_") as td:
        local = Path(td)
        cir = local / f"{name}.cir"
        log = cir.with_suffix(".log")
        raw = cir.with_suffix(".raw")
        cir.write_text(deck, encoding="utf-8", newline="\n")

        timed_out = False
        try:
            proc = subprocess.run(
                [str(LTSPICE), "-b", "-run", str(cir)],
                cwd=local,
                text=True,
                capture_output=True,
                timeout=TIMEOUT_S,
            )
            rc = proc.returncode
            stdout = proc.stdout or ""
            stderr = proc.stderr or ""
        except subprocess.TimeoutExpired as exc:
            timed_out = True
            rc = None
            stdout = (exc.stdout or "") if isinstance(exc.stdout, str) else ""
            stderr = (exc.stderr or "") if isinstance(exc.stderr, str) else ""

        shutil.copy2(cir, OUT / cir.name)
        if log.exists():
            shutil.copy2(log, OUT / log.name)
        if raw.exists():
            shutil.copy2(raw, OUT / raw.name)

        text = _decode_ltspice_log(log) if log.exists() else ""
        low = text.lower()
        fatal = [x for x in FATAL_TERMS if x in low]
        launch = [
            x for x in (
                "could not open input deck",
                "can't open input deck",
                "cannot open input deck",
                "no such file or directory",
            )
            if x in low
        ]
        measurement = "probe:" in low

        if timed_out:
            status = "TIMEOUT"
        elif rc != 0 or not log.exists() or fatal or launch:
            status = "FAIL"
        elif not measurement:
            status = "NO_MEASUREMENT"
        else:
            status = "PASS"

        return {
            "case": name,
            "status": status,
            "timeout_s": TIMEOUT_S,
            "returncode": rc,
            "measurement_present": measurement,
            "direct_newton_failed": "direct newton iteration failed" in low,
            "gmin_failed": "gmin stepping failed" in low,
            "source_stepping_started": "starting source stepping" in low,
            "fatal_terms": fatal,
            "launch_failures": launch,
            "stdout_tail": stdout[-1000:],
            "stderr_tail": stderr[-1000:],
        }


def main():
    validate_ltspice()
    src = resolve_sources()
    rows = [run_case(name, deck) for name, deck in decks(src)]
    actual = {x["case"]: x["status"] for x in rows}
    matched = actual == EXPECTED

    result = {
        "schema_version": 1,
        "authority": "AE-070",
        "run_id": "RUN07_MODEL_COMPOSITION_DISCRIMINATOR",
        "purpose": "Reproducible isolation of the THAT1646 vendor-macro integrated operating-point composition limitation.",
        "expected": EXPECTED,
        "actual": actual,
        "pattern_match": matched,
        "status": "MODEL_COMPOSITION_LIMIT_CONFIRMED" if matched else "REVIEW_REQUIRED",
        "interpretation": (
            "The AE-069 THAT1646 output pair and the complete upstream dual-channel chain "
            "solve independently. The same upstream chain also solves with an ideal balanced "
            "output. The complete upstream chain with the controlled AE-069/THAT1646 output "
            "stage does not reproducibly reach the AC operating point inside the controlled "
            "timeout. This supports the explicit qualification-only RUN07 AC surrogate; it "
            "is not evidence of physical hardware instability."
        ),
        "cases": rows,
    }
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    write_json(RESULT, result)

    print("=== AE-070 controlled model-composition discriminator ===")
    for row in rows:
        print(
            f"{row['case']}: {row['status']} "
            f"(measurement={row['measurement_present']}, "
            f"NewtonFail={row['direct_newton_failed']}, "
            f"GminFail={row['gmin_failed']}, "
            f"SourceStep={row['source_stepping_started']})"
        )
    print("Expected:", EXPECTED)
    print("Actual:  ", actual)
    print("pattern_match:", matched)
    print("Result:", RESULT.relative_to(ROOT))
    if not matched:
        raise RuntimeError(
            "AE-070 controlled composition discriminator did not match the controlled pattern."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
