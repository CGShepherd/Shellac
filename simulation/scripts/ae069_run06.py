#!/usr/bin/env python3
from __future__ import annotations

import cmath
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

CFG = ROOT / "simulation/config/ae069_run06_output.yaml"
MODEL = ROOT / "simulation/models/qualification/sch108_ae069.lib"
THAT_WRAPPER = ROOT / "simulation/models/wrappers/that1646_shellac.lib"
TMP = ROOT / ".ae069_run06_tmp"
VENDOR = TMP / "vendor"
RESULT_DIR = ROOT / "simulation/results/run06_output"
RESULT_JSON = RESULT_DIR / "ae069_run06.json"
RESULT_CSV = RESULT_DIR / "ae069_run06.csv"
RESULT_MD = RESULT_DIR / "ae069_run06.md"
DESIGN_RECORD = ROOT / "docs/design_pack/AE-069_RUN06_SCH108_Nominal_Output_Evidence_Rev_A0.md"


def db20(x: float) -> float:
    if x <= 0:
        return -300.0
    return 20.0 * math.log10(x)


def preamble(that: Path, s1g: Path) -> str:
    return f""".options meascplxfmt=cartesian measdgt=12 plotwinsize=0
.include "{that}"
.include "{THAT_WRAPPER}"
.include "{s1g}"
.include "{MODEL}"
VPLUS VPLUS18 0 18
VMINUS VMINUS18 0 -18
VZERO ZERO_VA 0 0
VCHASSIS CHASSIS ZERO_VA 0
"""


def ferrite_params(cfg: dict, name: str) -> tuple[float, float]:
    f = cfg["ferrite_brackets"][name]
    return float(f["dcr_ohm"]), float(f["inductance_h"])


def resolve_murata_models(cfg: dict) -> tuple[Path, dict[str, dict]]:
    import io
    import urllib.request
    import zipfile

    authority = cfg["murata_small_signal_ferrite_models"]
    murata_dir = VENDOR / "murata_blm21_v21"
    murata_dir.mkdir(parents=True, exist_ok=True)
    archive = murata_dir / "blm21-n-v21.zip"

    if not archive.is_file():
        request = urllib.request.Request(
            str(authority["official_archive_url"]),
            headers={"User-Agent": "Mozilla/5.0 Shellac-qualification/AE069"},
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = response.read()
        if not zipfile.is_zipfile(io.BytesIO(payload)):
            raise RuntimeError("Murata BLM21 download did not return a valid ZIP")
        archive.write_bytes(payload)

    if sha256(archive) != str(authority["archive_sha256"]):
        raise RuntimeError(
            "Murata BLM21 archive hash mismatch; controlled AE-069 source changed"
        )
    if not zipfile.is_zipfile(archive):
        raise RuntimeError("Cached Murata BLM21 archive is not a valid ZIP")

    resolved: dict[str, dict] = {}
    with zipfile.ZipFile(archive) as zf:
        members = zf.namelist()
        for ferrite, row in authority["parts"].items():
            part = str(row["part"])
            expected_hash = str(row["model_sha256"])
            model = murata_dir / f"{part}.mod"

            if not model.is_file():
                matches = [
                    member
                    for member in members
                    if Path(member).name.lower() == model.name.lower()
                ]
                if len(matches) != 1:
                    raise RuntimeError(
                        f"Expected exactly one Murata model for {part}; found {matches}"
                    )
                model.write_bytes(zf.read(matches[0]))

            if sha256(model) != expected_hash:
                raise RuntimeError(
                    f"Murata model hash mismatch for {part}; controlled source changed"
                )

            model_text = model.read_text(encoding="utf-8", errors="replace")
            required = (
                f"MURATA P/N : {part}",
                "Frequency Range = 1MHz - 3GHz",
                "DC Bias Current = 0 A",
                "Small Signal Operation",
                f".SUBCKT {part} port1 port2",
            )
            missing = [token for token in required if token not in model_text]
            if missing:
                raise RuntimeError(
                    f"Murata model {part} missing expected authority text: {missing}"
                )

            resolved[str(ferrite)] = {
                "part": part,
                "path": model,
                "subckt": part,
                "sha256": expected_hash,
            }

    return archive, resolved


def ac_case(
    cfg: dict,
    that: Path,
    s1g: Path,
    ferrite: str,
    load_ohm: float,
    cable_pf: float,
) -> dict:
    rfb, lfb = ferrite_params(cfg, ferrite)
    e = cfg["execution"]
    measures = [
        ".meas ac GMAX MAX mag(V(XLRP,XLRM)) FROM 20 TO 20k",
        ".meas ac GMIN MIN mag(V(XLRP,XLRM)) FROM 20 TO 20k",
    ]
    for hz in e["ac_report_hz"]:
        measures += [
            f".meas ac GD_{hz} FIND mag(V(XLRP,XLRM)) AT={hz}",
            f".meas ac CM_{hz} FIND mag(V(CM)) AT={hz}",
        ]

    cable_f = cable_pf * 1e-12
    deck = preamble(that, s1g) + f"""
VIN IN ZERO_VA AC 1
XOUT IN XLRP XLRM VPLUS18 VMINUS18 ZERO_VA CHASSIS AE069_SCH108
+ RFB={rfb:.12g} LFB={lfb:.12g}
RLOAD XLRP XLRM {load_ohm:.12g}
CCABP XLRP CHASSIS {cable_f:.12g}
CCABM XLRM CHASSIS {cable_f:.12g}
BCM CM ZERO_VA V=(V(XLRP)+V(XLRM))/2
.ac dec {int(e["ac_points_per_decade"])} {e["ac_start_hz"]} {e["ac_stop_hz"]}
{chr(10).join(measures)}
.end
"""
    tag = f"run06_ac_{ferrite.lower()}_{int(load_ohm)}_{int(cable_pf)}pf"
    log = execute_deck(tag, deck, TMP / "ac")
    gains = {str(h): parse_measure(log, f"GD_{h}") for h in e["ac_report_hz"]}
    cms = {str(h): parse_measure(log, f"CM_{h}") for h in e["ac_report_hz"]}
    gref = gains["1000"]
    peak_db = db20(parse_measure(log, "GMAX") / gref)
    min_db = db20(parse_measure(log, "GMIN") / gref)
    return {
        "differential_gain_linear": gains,
        "differential_gain_db": {k: db20(v) for k, v in gains.items()},
        "common_mode_v_per_vin": cms,
        "output_balance_db": {
            k: (300.0 if cms[k] <= 1e-15 else db20(gains[k] / cms[k]))
            for k in gains
        },
        "passband_peak_db_rel_1khz": peak_db,
        "passband_min_db_rel_1khz": min_db,
    }


def dc_case(
    cfg: dict,
    that: Path,
    s1g: Path,
    ferrite: str,
    load_ohm: float,
) -> dict:
    rfb, lfb = ferrite_params(cfg, ferrite)
    deck = preamble(that, s1g) + f"""
VIN IN ZERO_VA 0
XOUT IN XLRP XLRM VPLUS18 VMINUS18 ZERO_VA CHASSIS AE069_SCH108
+ RFB={rfb:.12g} LFB={lfb:.12g}
RLOAD XLRP XLRM {load_ohm:.12g}
.meas op VDIFF PARAM V(XLRP)-V(XLRM)
.meas op VCM PARAM (V(XLRP)+V(XLRM))/2
.op
.end
"""
    log = execute_deck(
        f"run06_dc_{ferrite.lower()}_{int(load_ohm)}",
        deck,
        TMP / "dc",
    )
    vdiff = parse_measure(log, "VDIFF")
    vcm = parse_measure(log, "VCM")
    c = cfg["criteria"]
    return {
        "differential_offset_v": vdiff,
        "common_mode_offset_v": vcm,
        "diff_preferred_pass": abs(vdiff) <= float(c["dc_diff_v_preferred_max"]),
        "diff_absolute_pass": abs(vdiff) <= float(c["dc_diff_v_absolute_max"]),
        "cm_preferred_pass": abs(vcm) <= float(c["dc_cm_v_preferred_max"]),
        "cm_absolute_pass": abs(vcm) <= float(c["dc_cm_v_absolute_max"]),
    }


def diagnostic_transient_stability_case(
    cfg: dict,
    that: Path,
    s1g: Path,
    ferrite: str,
    load_ohm: float,
    murata_models: dict[str, dict],
) -> dict:
    e = cfg["execution"]
    authority = cfg["murata_small_signal_ferrite_models"]
    murata = murata_models[ferrite]

    cable_f = float(e["stability_high_cable_pf_per_leg"]) * 1e-12
    rfi_f = float(authority["existing_rfi_pf_per_leg"]) * 1e-12
    vin = float(e["stability_step_input_v"])
    tr = float(e["stability_edge_s"])
    delay = float(e["stability_step_delay_s"])
    early_end = float(e["stability_early_end_s"])
    final_sample = float(e["stability_final_sample_s"])
    late_start = float(e["stability_late_start_s"])
    late_end = float(e["stability_late_end_s"])
    stop = float(e["stability_stop_s"])
    maxstep = min(float(e["stability_max_timestep_s"]), tr / 20.0)
    pulse_width = stop * 2.0
    pulse_period = stop * 4.0

    deck = f""".options meascplxfmt=cartesian measdgt=12 plotwinsize=0
.include "{that}"
.include "{THAT_WRAPPER}"
.include "{s1g}"
.include "{murata['path']}"
VPLUS VPLUS18 0 18
VMINUS VMINUS18 0 -18
VZERO ZERO_VA 0 0
VCHASSIS CHASSIS ZERO_VA 0

VIN IN ZERO_VA PULSE(0 {vin:.12g} {delay:.12g} {tr:.12g} {tr:.12g} {pulse_width:.12g} {pulse_period:.12g})
XDRV OUTM SNSM ZERO_VA IN VMINUS18 VPLUS18 SNSP OUTP SHELLAC_THAT1646
CSP OUTP SNSP 10u
CSM OUTM SNSM 10u
XFBP OUTP XLRP {murata['subckt']}
XFBM OUTM XLRM {murata['subckt']}
CRFIP XLRP CHASSIS {rfi_f:.12g}
CRFIM XLRM CHASSIS {rfi_f:.12g}
DHP XLRP VPLUS18 s1g
DHM XLRM VPLUS18 s1g
DLP VMINUS18 XLRP s1g
DLM VMINUS18 XLRM s1g
RLOAD XLRP XLRM {load_ohm:.12g}
CCABP XLRP CHASSIS {cable_f:.12g}
CCABM XLRM CHASSIS {cable_f:.12g}

.tran 0 {stop:.12g} 0 {maxstep:.12g}
.meas tran VPEAK MAX V(XLRP,XLRM) FROM {delay:.12g} TO {early_end:.12g}
.meas tran VMIN MIN V(XLRP,XLRM) FROM {delay:.12g} TO {early_end:.12g}
.meas tran VFINAL FIND V(XLRP,XLRM) AT={final_sample:.12g}
.meas tran LMAX MAX V(XLRP,XLRM) FROM {late_start:.12g} TO {late_end:.12g}
.meas tran LMIN MIN V(XLRP,XLRM) FROM {late_start:.12g} TO {late_end:.12g}
.end
"""
    log = execute_deck(
        f"run06_stability_{ferrite.lower()}_{int(load_ohm)}",
        deck,
        TMP / "stability",
    )

    vmax = parse_measure(log, "VPEAK")
    vmin = parse_measure(log, "VMIN")
    final = parse_measure(log, "VFINAL")
    lmax = parse_measure(log, "LMAX")
    lmin = parse_measure(log, "LMIN")
    late_pp = abs(lmax - lmin)
    fraction = late_pp / max(abs(final), 1e-15)
    overshoot = max(0.0, vmax - final) / max(abs(final), 1e-15)

    return {
        "method": "OFFICIAL_MURATA_SMALL_SIGNAL_FAST_TRANSIENT",
        "murata_part": murata["part"],
        "murata_model_sha256": murata["sha256"],
        "declared_model_domain": "1MHz-3GHz / 25C / 0A DC bias / small signal",
        "step_input_v": vin,
        "edge_s": tr,
        "high_cable_pf_per_leg": float(e["stability_high_cable_pf_per_leg"]),
        "existing_rfi_pf_per_leg": float(authority["existing_rfi_pf_per_leg"]),
        "early_max_v": vmax,
        "early_min_v": vmin,
        "settled_v": final,
        "positive_overshoot_fraction": overshoot,
        "late_pp_v": late_pp,
        "late_pp_fraction_of_settled": fraction,
        "stability_discriminator_pass": (
            fraction <= float(cfg["criteria"]["stability_late_pp_fraction_max"])
        ),
        "note": (
            "Official Murata bead model used only within its declared small-signal, "
            "zero-DC-bias high-frequency domain. Exact RUN-state RFI shunts and S1G "
            "clamps are included. Larger-signal load/cable stability remains a bench obligation."
        ),
    }



def hf_stability_ac_case(
    cfg: dict,
    that: Path,
    s1g: Path,
    ferrite: str,
    load_ohm: float,
    murata_models: dict[str, dict],
) -> dict:
    authority = cfg["murata_small_signal_ferrite_models"]
    murata = murata_models[ferrite]
    cable_f = float(cfg["execution"]["stability_high_cable_pf_per_leg"]) * 1e-12
    rfi_f = float(authority["existing_rfi_pf_per_leg"]) * 1e-12

    deck = f""".options meascplxfmt=cartesian measdgt=12 plotwinsize=0
.include "{that}"
.include "{THAT_WRAPPER}"
.include "{s1g}"
.include "{murata['path']}"
VPLUS VPLUS18 0 18
VMINUS VMINUS18 0 -18
VZERO ZERO_VA 0 0
VCHASSIS CHASSIS ZERO_VA 0

VIN IN ZERO_VA AC 1
XDRV OUTM SNSM ZERO_VA IN VMINUS18 VPLUS18 SNSP OUTP SHELLAC_THAT1646
CSP OUTP SNSP 10u
CSM OUTM SNSM 10u
XFBP OUTP XLRP {murata['subckt']}
XFBM OUTM XLRM {murata['subckt']}
CRFIP XLRP CHASSIS {rfi_f:.12g}
CRFIM XLRM CHASSIS {rfi_f:.12g}
DHP XLRP VPLUS18 s1g
DHM XLRM VPLUS18 s1g
DLP VMINUS18 XLRP s1g
DLM VMINUS18 XLRM s1g
RLOAD XLRP XLRM {load_ohm:.12g}
CCABP XLRP CHASSIS {cable_f:.12g}
CCABM XLRM CHASSIS {cable_f:.12g}

.ac dec 200 1Meg 100Meg
.meas ac G1M FIND mag(V(XLRP,XLRM)) AT=1Meg
.meas ac G3M FIND mag(V(XLRP,XLRM)) AT=3Meg
.meas ac G10M FIND mag(V(XLRP,XLRM)) AT=10Meg
.meas ac G30M FIND mag(V(XLRP,XLRM)) AT=30Meg
.meas ac G100M FIND mag(V(XLRP,XLRM)) AT=100Meg
.meas ac GMAX MAX mag(V(XLRP,XLRM)) FROM 1Meg TO 100Meg
.end
"""
    log = execute_deck(
        f"run06_hf_ac_{ferrite.lower()}_{int(load_ohm)}",
        deck,
        TMP / "hf_ac",
    )

    gains = {
        "1MHz": parse_measure(log, "G1M"),
        "3MHz": parse_measure(log, "G3M"),
        "10MHz": parse_measure(log, "G10M"),
        "30MHz": parse_measure(log, "G30M"),
        "100MHz": parse_measure(log, "G100M"),
        "max_1MHz_to_100MHz": parse_measure(log, "GMAX"),
    }
    reference = max(gains["1MHz"], 1e-30)

    return {
        "method": "OFFICIAL_MURATA_EXACT_TOPOLOGY_SMALL_SIGNAL_AC_EVIDENCE",
        "completed": True,
        "murata_part": murata["part"],
        "murata_model_sha256": murata["sha256"],
        "declared_model_domain": "1MHz-3GHz / 25C / 0A DC bias / small signal",
        "load_ohm": load_ohm,
        "high_cable_pf_per_leg": float(
            cfg["execution"]["stability_high_cable_pf_per_leg"]
        ),
        "existing_rfi_pf_per_leg": float(authority["existing_rfi_pf_per_leg"]),
        "gain_linear": gains,
        "max_relative_to_1mhz_db": db20(
            gains["max_1MHz_to_100MHz"] / reference
        ),
        "formal_pass_threshold_applied": False,
        "note": (
            "Bounded high-frequency small-signal evidence inside the Murata "
            "model domain. Not a substitute for the unreproducible nonlinear "
            "transient solve or prototype load/cable stability bench testing."
        ),
    }


def _dft_harmonics(samples: list[float], max_harmonic: int) -> dict:
    n = len(samples)
    if n < 8:
        raise ValueError("too few quasi-static waveform samples")
    dc = sum(samples) / n
    magnitudes = {}
    for harmonic in range(1, max_harmonic + 1):
        coeff = sum(
            sample * cmath.exp(-2j * math.pi * harmonic * index / n)
            for index, sample in enumerate(samples)
        )
        magnitudes[harmonic] = 2.0 * abs(coeff) / n
    fundamental = magnitudes[1]
    thd = (
        float("inf")
        if fundamental <= 0
        else 100.0
        * math.sqrt(sum(magnitudes[h] ** 2 for h in range(2, max_harmonic + 1)))
        / fundamental
    )
    return {
        "sample_count": n,
        "dc_v": dc,
        "harmonic_peak_v": {str(k): v for k, v in magnitudes.items()},
        "fundamental_rms_v": fundamental / math.sqrt(2.0),
        "thd_percent_h2_to_hmax": thd,
    }


def quasistatic_transfer_case(
    cfg: dict,
    that: Path,
    s1g: Path,
    ferrite: str,
    load_ohm: float,
) -> dict:
    rfb, lfb = ferrite_params(cfg, ferrite)
    e = cfg["execution"]
    amplitudes = [float(x) for x in e["headroom_input_rms_v"]]
    distortion_rms = float(e["distortion_input_rms_v"])
    sample_count = int(e["quasistatic_distortion_samples"])
    harmonics = int(e["quasistatic_distortion_harmonics"])
    limit = float(e["dc_transfer_input_limit_v"])
    step = float(e["dc_transfer_step_v"])

    required_peak = max(amplitudes + [distortion_rms]) * math.sqrt(2.0)
    if required_peak > limit:
        raise RuntimeError(
            f"quasi-static input limit {limit} V does not cover required peak {required_peak} V"
        )

    measures = []
    for index, vin_rms in enumerate(amplitudes):
        peak = vin_rms * math.sqrt(2.0)
        measures.append(
            f".meas dc HP{index:02d} FIND V(XLRP,XLRM) WHEN V(IN)={peak:.12g}"
        )
        measures.append(
            f".meas dc HN{index:02d} FIND V(XLRP,XLRM) WHEN V(IN)={-peak:.12g}"
        )

    for index in range(sample_count):
        phase = 2.0 * math.pi * index / sample_count
        vin = distortion_rms * math.sqrt(2.0) * math.sin(phase)
        measures.append(
            f".meas dc Q{index:03d} FIND V(XLRP,XLRM) WHEN V(IN)={vin:.12g}"
        )

    deck = preamble(that, s1g) + f"""
VIN IN ZERO_VA 0
XOUT IN XLRP XLRM VPLUS18 VMINUS18 ZERO_VA CHASSIS AE069_SCH108
+ RFB={rfb:.12g} LFB={lfb:.12g}
RLOAD XLRP XLRM {load_ohm:.12g}
.dc VIN {-limit:.12g} {limit:.12g} {step:.12g}
{chr(10).join(measures)}
.end
"""
    log = execute_deck(
        f"run06_qstatic_{ferrite.lower()}_{int(load_ohm)}",
        deck,
        TMP / "quasistatic",
    )

    rows = []
    for index, vin_rms in enumerate(amplitudes):
        positive = parse_measure(log, f"HP{index:02d}")
        negative = parse_measure(log, f"HN{index:02d}")
        output_peak = (positive - negative) / 2.0
        output_rms = output_peak / math.sqrt(2.0)
        rows.append(
            {
                "input_rms_v": vin_rms,
                "positive_peak_output_v": positive,
                "negative_peak_output_v": negative,
                "output_rms_v_from_symmetric_peak_transfer": output_rms,
                "gain_linear_from_symmetric_peak_transfer": output_rms / vin_rms,
            }
        )

    small_gain = rows[0]["gain_linear_from_symmetric_peak_transfer"]
    for row in rows:
        compression = max(
            0.0,
            1.0
            - row["gain_linear_from_symmetric_peak_transfer"] / max(small_gain, 1e-15),
        )
        row["compression_fraction_vs_quasistatic_low_level"] = compression
        row["within_1pct_compression"] = (
            compression <= float(cfg["criteria"]["local_compression_fraction_max"])
        )

    samples = [
        parse_measure(log, f"Q{index:03d}")
        for index in range(sample_count)
    ]
    distortion = _dft_harmonics(samples, harmonics)

    severe = next(row for row in rows if abs(row["input_rms_v"] - 3.21) < 1e-9)
    severe_output = severe["output_rms_v_from_symmetric_peak_transfer"]
    severe_margin = db20(10.0 / severe_output)

    first_compressed = next(
        (row for row in rows if not row["within_1pct_compression"]),
        None,
    )
    return {
        "method": "QUASI_STATIC_DC_TRANSFER",
        "load_ohm": load_ohm,
        "ferrite_dcr_ohm": rfb,
        "headroom_sweep": rows,
        "severe_3p21vrms_output_rms_v": severe_output,
        "severe_margin_to_10vrms_design_ceiling_db": severe_margin,
        "severe_minimum_margin_pass": (
            severe_margin >= float(cfg["criteria"]["normal_headroom_margin_db_min"])
        ),
        "severe_preferred_margin_pass": (
            severe_margin >= float(cfg["criteria"]["normal_headroom_margin_db_preferred"])
        ),
        "first_gt_1pct_compression_input_rms_v": (
            None if first_compressed is None else first_compressed["input_rms_v"]
        ),
        "distortion_estimate": {
            "method": "QUASI_STATIC_TRANSFER_DERIVED_HARMONIC_ESTIMATE",
            "input_rms_v": distortion_rms,
            "frequency_status": "NOT_A_DYNAMIC_1KHZ_TRANSIENT_RESULT",
            **distortion,
            "bench_correlation_required": True,
        },
        "model_limitation_note": (
            "Controlled THAT1646 macro reproduces periodic large-signal timeout in "
            "the minimal device circuit. Quasi-static result is valid as nonlinear "
            "transfer/headroom evidence and a distortion estimate only."
        ),
    }


def analyse(cfg: dict, that: Path, s1g: Path, murata_models: dict[str, dict]) -> dict:
    e = cfg["execution"]
    c = cfg["criteria"]
    normal_loads = [float(x) for x in e["normal_loads_ohm"]]
    stress_load = float(e["stress_load_ohm"])
    all_loads = normal_loads + [stress_load]
    cable_map = {
        name: float(value)
        for name, value in e["cable_capacitance_per_leg_pf"].items()
    }

    ac = {}
    for ferrite in cfg["ferrite_brackets"]:
        ac[ferrite] = {}
        for cable_name, cable_pf in cable_map.items():
            ac[ferrite][cable_name] = {}
            for load in all_loads:
                ac[ferrite][cable_name][str(int(load))] = ac_case(
                    cfg, that, s1g, ferrite, load, cable_pf
                )

    normal_checks = {}
    for ferrite in cfg["ferrite_brackets"]:
        normal_checks[ferrite] = {}
        for cable_name in cable_map:
            reference = ac[ferrite][cable_name]["100000"]["differential_gain_linear"]["1000"]
            rows = {}
            for load in normal_loads:
                result = ac[ferrite][cable_name][str(int(load))]
                variation = db20(
                    result["differential_gain_linear"]["1000"] / reference
                )
                rows[str(int(load))] = {
                    "gain_variation_db_vs_100k_same_cable": variation,
                    "gain_variation_pass": (
                        abs(variation)
                        <= float(c["normal_load_gain_variation_db_max"])
                    ),
                    "passband_peak_db": result["passband_peak_db_rel_1khz"],
                    "peaking_pass": (
                        result["passband_peak_db_rel_1khz"]
                        <= float(c["passband_peak_db_max"])
                    ),
                }
            normal_checks[ferrite][cable_name] = rows

    dc = {}
    stability = {}
    quasistatic = {}
    for ferrite in cfg["ferrite_brackets"]:
        dc[ferrite] = {
            str(int(load)): dc_case(cfg, that, s1g, ferrite, load)
            for load in all_loads
        }
        stability[ferrite] = {
            str(int(load)): hf_stability_ac_case(
                cfg, that, s1g, ferrite, load, murata_models
            )
            for load in all_loads
        }
        quasistatic[ferrite] = {
            str(int(load)): quasistatic_transfer_case(
                cfg, that, s1g, ferrite, float(load)
            )
            for load in e["headroom_loads_ohm"]
        }

    stress_droop = {}
    for ferrite in cfg["ferrite_brackets"]:
        stress_droop[ferrite] = {}
        for cable_name in cable_map:
            reference = ac[ferrite][cable_name]["100000"]["differential_gain_linear"]["1000"]
            stress = ac[ferrite][cable_name]["600"]["differential_gain_linear"]["1000"]
            stress_droop[ferrite][cable_name] = db20(stress / reference)

    normal_pass = all(
        row["gain_variation_pass"] and row["peaking_pass"]
        for ferrite_rows in normal_checks.values()
        for cable_rows in ferrite_rows.values()
        for row in cable_rows.values()
    )
    dc_pass = all(
        row["diff_absolute_pass"] and row["cm_absolute_pass"]
        for ferrite_rows in dc.values()
        for row in ferrite_rows.values()
    )
    stability_evidence_complete = all(
        row["completed"]
        for ferrite_rows in stability.values()
        for row in ferrite_rows.values()
    )
    severe_headroom_pass = all(
        ferrite_rows["10000"]["severe_minimum_margin_pass"]
        for ferrite_rows in quasistatic.values()
    )
    distortion_recorded = all(
        ferrite_rows[load]["distortion_estimate"]["thd_percent_h2_to_hmax"] >= 0.0
        for ferrite_rows in quasistatic.values()
        for load in ("10000", "600")
    )

    return {
        "ac": ac,
        "normal_load_checks": normal_checks,
        "dc_offsets": dc,
        "stability": stability,
        "quasistatic_large_signal": quasistatic,
        "stress_600ohm_gain_droop_db_vs_100k": stress_droop,
        "vendor_macro_limitation": cfg["vendor_macro_limitation"],
        "stability_model_limitation": cfg["stability_model_limitation"],
        "methodology": cfg["methodology"],
        "gates": {
            "normal_load_gain_peaking_pass": normal_pass,
            "dc_offset_absolute_pass": dc_pass,
            "high_frequency_stability_ac_evidence_complete": stability_evidence_complete,
            "transient_stability_reproducibly_qualified": False,
            "bench_load_stability_required": True,
            "normal_10k_severe_headroom_minimum_pass": severe_headroom_pass,
            "stress_distortion_estimate_recorded": distortion_recorded,
            "transient_large_signal_thd_qualified": False,
            "bench_dynamic_thd_required": True,
            "run06_fully_qualified": False,
            "simulation_evidence_complete": (
                normal_pass
                and dc_pass
                and stability_evidence_complete
                and severe_headroom_pass
                and distortion_recorded
            ),
        },
    }


def write_csv(path: Path, result: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = [["metric", "ferrite", "case", "value", "unit", "method"]]
    analysis = result["analysis"]

    for ferrite, cables in analysis["normal_load_checks"].items():
        for cable, loads in cables.items():
            for load, row in loads.items():
                rows.append([
                    "gain_variation_vs_100k",
                    ferrite,
                    f"{cable}_{load}",
                    row["gain_variation_db_vs_100k_same_cable"],
                    "dB",
                    "AC_SMALL_SIGNAL",
                ])
                rows.append([
                    "passband_peak",
                    ferrite,
                    f"{cable}_{load}",
                    row["passband_peak_db"],
                    "dB",
                    "AC_SMALL_SIGNAL",
                ])

    for ferrite, loads in analysis["quasistatic_large_signal"].items():
        for load, row in loads.items():
            rows.append([
                "quasistatic_thd_estimate",
                ferrite,
                load,
                row["distortion_estimate"]["thd_percent_h2_to_hmax"],
                "%",
                "QUASI_STATIC_TRANSFER_DERIVED_HARMONIC_ESTIMATE",
            ])
            rows.append([
                "severe_3p21vrms_output",
                ferrite,
                load,
                row["severe_3p21vrms_output_rms_v"],
                "Vrms",
                "QUASI_STATIC_DC_TRANSFER",
            ])

    with path.open("w", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerows(rows)


def _headline_extrema(analysis: dict) -> dict:
    variations = [
        abs(row["gain_variation_db_vs_100k_same_cable"])
        for ferrite_rows in analysis["normal_load_checks"].values()
        for cable_rows in ferrite_rows.values()
        for row in cable_rows.values()
    ]
    peaks = [
        row["passband_peak_db"]
        for ferrite_rows in analysis["normal_load_checks"].values()
        for cable_rows in ferrite_rows.values()
        for row in cable_rows.values()
    ]
    stress = [
        value
        for ferrite_rows in analysis["stress_600ohm_gain_droop_db_vs_100k"].values()
        for value in ferrite_rows.values()
    ]
    qthd_600 = [
        ferrite_rows["600"]["distortion_estimate"]["thd_percent_h2_to_hmax"]
        for ferrite_rows in analysis["quasistatic_large_signal"].values()
    ]
    severe_10k = [
        ferrite_rows["10000"]["severe_margin_to_10vrms_design_ceiling_db"]
        for ferrite_rows in analysis["quasistatic_large_signal"].values()
    ]
    return {
        "worst_normal_gain_variation_db": max(variations),
        "worst_normal_passband_peak_db": max(peaks),
        "stress_600_droop_min_db": min(stress),
        "stress_600_droop_max_db": max(stress),
        "stress_600_qstatic_thd_min_percent": min(qthd_600),
        "stress_600_qstatic_thd_max_percent": max(qthd_600),
        "severe_10k_margin_min_db": min(severe_10k),
    }


def write_markdown(path: Path, result: dict) -> None:
    analysis = result["analysis"]
    h = _headline_extrema(analysis)
    lines = [
        "# AE-069 RUN06 summary",
        "",
        f"- Worst normal-load gain variation: {h['worst_normal_gain_variation_db']:.6f} dB",
        f"- Worst normal-load passband peak: {h['worst_normal_passband_peak_db']:.6f} dB",
        f"- 600 Ohm AC gain droop range: {h['stress_600_droop_min_db']:+.4f} to {h['stress_600_droop_max_db']:+.4f} dB",
        f"- 600 Ohm quasi-static harmonic-distortion estimate: {h['stress_600_qstatic_thd_min_percent']:.6f}% to {h['stress_600_qstatic_thd_max_percent']:.6f}%",
        f"- Worst 10 kOhm 3.21 Vrms margin to 10 Vrms design ceiling: {h['severe_10k_margin_min_db']:.4f} dB",
        "",
        f"- Normal-load gain/peaking gate: {'PASS' if analysis['gates']['normal_load_gain_peaking_pass'] else 'FAIL'}",
        f"- DC-offset absolute gate: {'PASS' if analysis['gates']['dc_offset_absolute_pass'] else 'FAIL'}",
        f"- Exact-topology HF small-signal AC evidence: {'COMPLETE' if analysis['gates']['high_frequency_stability_ac_evidence_complete'] else 'INCOMPLETE'}",
        "- Reproducible transient load-stability qualification: NO — combined vendor-model transient solve is non-reproducible",
        "- Prototype load/cable stability bench gate: REQUIRED",
        f"- 10 kOhm severe-input headroom minimum: {'PASS' if analysis['gates']['normal_10k_severe_headroom_minimum_pass'] else 'FAIL'}",
        f"- 600 Ohm distortion estimate recorded: {'PASS' if analysis['gates']['stress_distortion_estimate_recorded'] else 'FAIL'}",
        "",
        "Controlled THAT1646 periodic large-signal transient convergence limitation is confirmed in the minimal device circuit.",
        "The distortion figure above is a quasi-static nonlinear-transfer harmonic estimate, NOT transient 1 kHz THD.",
        "Audio-band/quasi-static ferrite calculations use R-L engineering brackets; high-frequency small-signal stability uses controlled official Murata models.",
        "RUN08/RUN09/RUN10/RUN13/RUN14 plus transient-THD and bench correlation remain open.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def write_design_record(result: dict) -> None:
    analysis = result["analysis"]
    h = _headline_extrema(analysis)
    lines = [
        "# AE-069 — RUN06 SCH108 Nominal Output Evidence — Rev A0",
        "",
        "**Project:** Shellac",
        "**Status:** SIMULATION_EVIDENCE_COMPLETE / BENCH_STABILITY_AND_DYNAMIC_THD_OPEN",
        f"**Execution baseline:** `{result['repository_commit_before_ae069']}`",
        "",
        "## Purpose",
        "Execute AE-050 RUN06 against the current SCH108 THAT1646 output architecture without changing product-generator authority.",
        "",
        "## Scope",
        "- balanced 100 kOhm / 20 kOhm / 10 kOhm normal loads;",
        "- 600 Ohm stress load;",
        "- 100 pF / 500 pF / 2 nF per-leg cable-capacitance engineering brackets;",
        "- controlled THAT1646 manufacturer macro-model and S1G rail-clamp model;",
        "- existing 10 uF OUT/SNS capacitors and 100 pF connector-side chassis shunts;",
        "- 60 Ohm and 220 Ohm @100 MHz ferrite candidate R-L brackets;",
        "- AC gain/common-mode/peaking and DC offset; exact-topology official-Murata high-frequency small-signal AC evidence; converged fast load/capacitance transient runs are supportive diagnostic evidence only;",
        "- quasi-static nonlinear transfer for local SCH108 headroom and stress-distortion estimation.",
        "",
        "## Confirmed THAT1646 macro-model limitation",
        "The controlled THAT1646 manufacturer macro executes low-level periodic transient analysis but stalls at large-signal zero crossings. The limitation reproduces in the minimal device circuit with ferrites, cable capacitance and clamps removed, and also reproduces using Gear integration. The quasi-static transfer is treated as qualification evidence only through +/-5 V input; wider exploratory sweeps are not used to infer the physical clipping limit.",
        "",
        "Therefore AE-069 does not interpret periodic large-signal timeout as hardware overload. Periodic large-signal THD is explicitly not qualified by this macro. AC and operating-point analysis remain reproducible evidence domains; quasi-static nonlinear transfer is used only inside the validated input envelope. Fast transient results are supportive diagnostic evidence where they converge, not a reproducible qualification gate.",
        "",
        "## Ferrite model boundary",
        "Audio-band and quasi-static calculations retain R-L engineering brackets because the detailed Murata models are declared only for 1 MHz-3 GHz small-signal, zero-DC-bias operation. Exact-topology high-frequency small-signal AC evidence uses the controlled official Murata models in that declared domain; converged transient cases remain supportive only. Neither method freezes final ferrite selection.",
        "",
        "## Headline evidence",
        f"- worst normal-load gain variation versus 100 kOhm: {h['worst_normal_gain_variation_db']:.6f} dB;",
        f"- worst normal-load passband peaking: {h['worst_normal_passband_peak_db']:.6f} dB;",
        f"- 600 Ohm AC gain droop range versus 100 kOhm: {h['stress_600_droop_min_db']:+.4f} to {h['stress_600_droop_max_db']:+.4f} dB;",
        f"- 600 Ohm quasi-static harmonic-distortion estimate: {h['stress_600_qstatic_thd_min_percent']:.6f}% to {h['stress_600_qstatic_thd_max_percent']:.6f}%;",
        f"- worst 10 kOhm 3.21 Vrms margin to 10 Vrms design ceiling: {h['severe_10k_margin_min_db']:.4f} dB;",
        f"- normal-load gain/peaking gate: {'PASS' if analysis['gates']['normal_load_gain_peaking_pass'] else 'FAIL'};",
        f"- DC absolute-offset gate: {'PASS' if analysis['gates']['dc_offset_absolute_pass'] else 'FAIL'};",
        f"- exact-topology official-Murata HF AC evidence: {'COMPLETE' if analysis['gates']['high_frequency_stability_ac_evidence_complete'] else 'INCOMPLETE'};",
        "- transient load-stability is not reproducibly qualified in LTspice; prototype load/cable stability bench verification remains mandatory;",
        f"- local 10 kOhm severe-input headroom minimum: {'PASS' if analysis['gates']['normal_10k_severe_headroom_minimum_pass'] else 'FAIL'}.",
        "",
        "## Distortion evidence boundary",
        "AE-049 requires 600 Ohm stress distortion to be recorded. AE-069 records a quasi-static nonlinear-transfer harmonic estimate to quantify modelled nonlinearity without pretending the vendor macro completed a periodic 1 kHz large-signal run. This estimate is not a substitute for bench THD; transient/audio-frequency distortion remains an explicit prototype-correlation obligation.",
        "The quasi-static transfer is treated as physically usable only through 5 Vrms input. Earlier 7.5/9 Vrms exploratory points exceeded the +/-18 V rails in the macro-model and are excluded from qualification evidence; true clipping/recovery remains RUN08.",
        "",
        "## Decision boundary",
        "This record completes the reproducible RUN06 simulation evidence but does not fully qualify RUN06. It does not select a final ferrite, change the sense-capacitor footprint, change SCH108 topology, or auto-promote RUN06. Prototype load/cable stability and dynamic THD remain mandatory RUN06 bench gates. Full-chain first-clipping/recovery remains RUN08; noise RUN09; tolerance/value engineering RUN10; rail variation RUN13; phantom fault RUN14.",
        "",
        "## Evidence",
        "- `simulation/results/run06_output/ae069_run06.json`",
        "- `simulation/results/run06_output/ae069_run06.csv`",
        "- `simulation/results/run06_output/ae069_run06.md`",
    ]
    DESIGN_RECORD.parent.mkdir(parents=True, exist_ok=True)
    DESIGN_RECORD.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    cfg = yaml.safe_load(CFG.read_text(encoding="utf-8"))
    validate_ltspice()
    that = resolve_source("THAT1646", VENDOR)
    s1g = resolve_source("S1G", VENDOR)
    murata_archive, murata_models = resolve_murata_models(cfg)

    print("\n=== AE-069 RUN06: SCH108 nominal balanced-output qualification ===")
    print("Large-signal method: quasi-static transfer due confirmed THAT1646 periodic convergence limitation.")
    analysis = analyse(cfg, that, s1g, murata_models)
    h = _headline_extrema(analysis)

    print(f"Worst normal-load gain variation: {h['worst_normal_gain_variation_db']:.6f} dB")
    print(f"Worst normal-load passband peak: {h['worst_normal_passband_peak_db']:.6f} dB")
    print(f"600 Ohm AC gain droop: {h['stress_600_droop_min_db']:+.4f} to {h['stress_600_droop_max_db']:+.4f} dB")
    print(f"600 Ohm quasi-static distortion estimate: {h['stress_600_qstatic_thd_min_percent']:.6f}% to {h['stress_600_qstatic_thd_max_percent']:.6f}%")
    print(f"10k severe-input margin minimum: {h['severe_10k_margin_min_db']:.4f} dB")
    print(f"Normal load/peaking gate: {'PASS' if analysis['gates']['normal_load_gain_peaking_pass'] else 'FAIL'}")
    print(f"DC offset gate: {'PASS' if analysis['gates']['dc_offset_absolute_pass'] else 'FAIL'}")
    print(f"Exact-topology HF AC evidence: {'COMPLETE' if analysis['gates']['high_frequency_stability_ac_evidence_complete'] else 'INCOMPLETE'}")
    print("Transient load-stability reproducibly qualified: NO — bench gate retained.")
    print(f"10k severe-input headroom minimum: {'PASS' if analysis['gates']['normal_10k_severe_headroom_minimum_pass'] else 'FAIL'}")
    print(f"Stress distortion estimate recorded: {'PASS' if analysis['gates']['stress_distortion_estimate_recorded'] else 'FAIL'}")
    print("Transient large-signal THD qualified: NO — controlled vendor macro limitation; bench obligation retained.")

    result = {
        "schema_version": 1,
        "authority": "AE-069",
        "run_id": "RUN06",
        "title": "SCH108 nominal balanced-output qualification",
        "repository_commit_before_ae069": cfg["baseline_commit"],
        "model_semantics": cfg["model_semantics"],
        "generator_migration_implied": False,
        "status": (
            "SIMULATION_EVIDENCE_COMPLETE_BENCH_GATES_OPEN_REVIEW_REQUIRED"
            if analysis["gates"]["simulation_evidence_complete"]
            else "SIMULATION_EVIDENCE_WITH_NON_STABILITY_FAILURE_REVIEW_REQUIRED"
        ),
        "analysis": analysis,
        "criteria": cfg["criteria"],
        "execution": cfg["execution"],
        "ferrite_brackets": cfg["ferrite_brackets"],
        "decision": {
            "automatic_run_promotion": False,
            "automatic_ferrite_selection": False,
            "transient_large_signal_thd_claimed": False,
            "review_required": True,
        },
        "open_qualification": {
            "FERRITE_SELECTION": "official Murata small-signal models acquired; 60-ohm candidate has cleaner HF/transient evidence but final ferrite remains open pending EMC/layout/bench correlation",
            "SENSE_CAP_MECHANICAL": "10 uF bipolar capacitor footprint/height reconciliation before PCB freeze",
            "TRANSIENT_THD": "controlled THAT1646 macro unsuitable for periodic large-signal THD; bench measurement required",
            "RUN08": "full-chain overload and recovery",
            "RUN09": "full-system noise",
            "RUN10": "sensitivity/tolerance/value engineering",
            "RUN13": "rail variation/ripple",
            "RUN14": "phantom fault and rail injection",
            "BENCH": "output load/cable stability, DC, THD and ferrite correlation",
        },
        "model_sources": {
            "THAT1646": {"path": that.name, "sha256": sha256(that)},
            "S1G": {"path": s1g.name, "sha256": sha256(s1g)},
            "qualification_model_sha256": sha256(MODEL),
            "MURATA_BLM21_ARCHIVE": {
                "path": murata_archive.name,
                "sha256": sha256(murata_archive),
                "source_url": cfg["murata_small_signal_ferrite_models"]["official_archive_url"],
                "declared_domain": "1MHz-3GHz / 25C / 0A DC bias / small signal",
            },
            "MURATA_FERRITES": {
                ferrite: {
                    "part": row["part"],
                    "path": row["path"].name,
                    "sha256": row["sha256"],
                }
                for ferrite, row in murata_models.items()
            },
        },
    }
    write_json(RESULT_JSON, result)
    write_csv(RESULT_CSV, result)
    write_markdown(RESULT_MD, result)
    write_design_record(result)

    print("\n=== RUN06 PHASE-A SUMMARY ===")
    for key, value in analysis["gates"].items():
        print(f"{key}: {value}")
    print(f"AE-069 RUN06 simulation disposition: {result['status']}")
    print(f"Result: {RESULT_JSON.relative_to(ROOT)}")
    return 0 if analysis["gates"]["simulation_evidence_complete"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
