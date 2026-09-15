# AE-069 — RUN06 SCH108 Nominal Output Evidence — Rev A0

**Project:** Shellac
**Status:** SIMULATION_EVIDENCE_COMPLETE / BENCH_STABILITY_AND_DYNAMIC_THD_OPEN
**Execution baseline:** `79d3520eb0ff132ce7ebb0618cef3cfc0dd80d3c`

## Purpose
Execute AE-050 RUN06 against the current SCH108 THAT1646 output architecture without changing product-generator authority.

## Scope
- balanced 100 kOhm / 20 kOhm / 10 kOhm normal loads;
- 600 Ohm stress load;
- 100 pF / 500 pF / 2 nF per-leg cable-capacitance engineering brackets;
- controlled THAT1646 manufacturer macro-model and S1G rail-clamp model;
- existing 10 uF OUT/SNS capacitors and 100 pF connector-side chassis shunts;
- 60 Ohm and 220 Ohm @100 MHz ferrite candidate R-L brackets;
- AC gain/common-mode/peaking and DC offset; exact-topology official-Murata high-frequency small-signal AC evidence; converged fast load/capacitance transient runs are supportive diagnostic evidence only;
- quasi-static nonlinear transfer for local SCH108 headroom and stress-distortion estimation.

## Confirmed THAT1646 macro-model limitation
The controlled THAT1646 manufacturer macro executes low-level periodic transient analysis but stalls at large-signal zero crossings. The limitation reproduces in the minimal device circuit with ferrites, cable capacitance and clamps removed, and also reproduces using Gear integration. The quasi-static transfer is treated as qualification evidence only through +/-5 V input; wider exploratory sweeps are not used to infer the physical clipping limit.

Therefore AE-069 does not interpret periodic large-signal timeout as hardware overload. Periodic large-signal THD is explicitly not qualified by this macro. AC and operating-point analysis remain reproducible evidence domains; quasi-static nonlinear transfer is used only inside the validated input envelope. Fast transient results are supportive diagnostic evidence where they converge, not a reproducible qualification gate.

## Ferrite model boundary
Audio-band and quasi-static calculations retain R-L engineering brackets because the detailed Murata models are declared only for 1 MHz-3 GHz small-signal, zero-DC-bias operation. Exact-topology high-frequency small-signal AC evidence uses the controlled official Murata models in that declared domain; converged transient cases remain supportive only. Neither method freezes final ferrite selection.

## Headline evidence
- worst normal-load gain variation versus 100 kOhm: 0.038809 dB;
- worst normal-load passband peaking: 0.000419 dB;
- 600 Ohm AC gain droop range versus 100 kOhm: -0.6880 to -0.6873 dB;
- 600 Ohm quasi-static harmonic-distortion estimate: 0.000001% to 0.000001%;
- worst 10 kOhm 3.21 Vrms margin to 10 Vrms design ceiling: 3.9128 dB;
- normal-load gain/peaking gate: PASS;
- DC absolute-offset gate: PASS;
- exact-topology official-Murata HF AC evidence: COMPLETE;
- transient load-stability is not reproducibly qualified in LTspice; prototype load/cable stability bench verification remains mandatory;
- local 10 kOhm severe-input headroom minimum: PASS.

## Distortion evidence boundary
AE-049 requires 600 Ohm stress distortion to be recorded. AE-069 records a quasi-static nonlinear-transfer harmonic estimate to quantify modelled nonlinearity without pretending the vendor macro completed a periodic 1 kHz large-signal run. This estimate is not a substitute for bench THD; transient/audio-frequency distortion remains an explicit prototype-correlation obligation.
The quasi-static transfer is treated as physically usable only through 5 Vrms input. Earlier 7.5/9 Vrms exploratory points exceeded the +/-18 V rails in the macro-model and are excluded from qualification evidence; true clipping/recovery remains RUN08.

## Decision boundary
This record completes the reproducible RUN06 simulation evidence but does not fully qualify RUN06. It does not select a final ferrite, change the sense-capacitor footprint, change SCH108 topology, or auto-promote RUN06. Prototype load/cable stability and dynamic THD remain mandatory RUN06 bench gates. Full-chain first-clipping/recovery remains RUN08; noise RUN09; tolerance/value engineering RUN10; rail variation RUN13; phantom fault RUN14.

## Evidence
- `simulation/results/run06_output/ae069_run06.json`
- `simulation/results/run06_output/ae069_run06.csv`
- `simulation/results/run06_output/ae069_run06.md`
