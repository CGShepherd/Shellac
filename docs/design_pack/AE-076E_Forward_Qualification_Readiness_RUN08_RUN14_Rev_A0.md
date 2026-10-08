# AE-076E Forward Qualification Readiness Review — RUN08–RUN14 — Rev A0

**Parent governed baseline:** `4975fba11a12f25744e35ea61e11578c66f3d50f`\
**Status:** PROVISIONAL READ-ONLY FORWARD REVIEW — NO QUALIFICATION EXECUTED\
**Purpose:** identify executable prerequisites and stale historical assumptions before implementing RUN08–RUN14.

## 1. Executive finding

The governed repository contains completed executable campaign infrastructure through RUN07, but **does not yet contain implemented RUN08–RUN14 campaign scripts/configurations**.

AE-048/049/050 remain historical methodology/criteria/execution authorities, while AE-076A and AE-076D provide the current execution delta. Therefore RUN08–RUN14 must be implemented under a new controlled campaign increment; they must not be executed by copying historical AE-050 constants verbatim.

Current conditions that must override stale historical run text:

- regulated nominal rails: `+17.0 V / 0VA / -17.0 V`;
- primary 78-rpm cartridge: Grado Prestige 78C, not historical 78E wording;
- current cartridge load states: BASE / +47 pF / +100 pF;
- after AE-076E, the physical load mechanism is per-channel personality cards but the electrical states remain the same;
- DR-039 live branch-local DIRECT/BYPASS topology under AE-074;
- THAT1646 source semantics: 25 Ω per leg / 50 Ω differential under AE-075G;
- SCH108 clamp identity: Vishay S1G in SMA under AE-063;
- H801/H802 balanced output harness carries HOT/COLD only, with no PCB-panel 0VA conductor;
- current release permissions remain false.

## 2. Infrastructure state

Present governed executable campaign:

- RUN00: implemented / sanity evidence;
- RUN01–RUN03: AE-066;
- RUN04: AE-067;
- RUN05: AE-068;
- RUN06: AE-069;
- RUN07: AE-070.

No files currently implement dedicated:

- `simulation/scripts/*run08*`;
- `simulation/scripts/*run09*`;
- `simulation/scripts/*run10*`;
- `simulation/scripts/*run11*`;
- `simulation/scripts/*run12*`;
- `simulation/scripts/*run13*`;
- `simulation/scripts/*run14*`;

and the planned AE-050 `simulation/runs/run08_*` through `run14_*` structure was never instantiated as governed execution infrastructure.

This is an OPEN implementation prerequisite, not evidence that the qualification plan is invalid.

## 3. RUN08 — overload / clipping / recovery

### Readiness: BLOCKED BY LARGE-SIGNAL COMPOSITION METHOD

AE-070 reproducibly established:

- isolated AE-069 THAT1646 output pair: PASS;
- complete dual-channel upstream chain without THAT1646: PASS;
- same chain with ideal balanced output: PASS;
- complete chain with controlled vendor THAT1646 macro: TIMEOUT.

AE-070's AC surrogate is explicitly restricted to small-signal qualification and **cannot support overload/recovery**.

Therefore RUN08 must not use the AE-070 AC surrogate to claim clipping or recovery.

### Recommended discriminator

Preferred first approach:

1. run a complete nonlinear upstream chain to the SCH108/THAT1646 input boundary using stiff current-authority ±17 V rails;
2. record first-clipping node and recovery through SCH101/SCH103/SCH107/SCH104/SCH105;
3. drive the isolated controlled AE-069/THAT1646 output model with the boundary waveform;
4. qualify output-stage clipping/recovery/load response independently;
5. correlate the boundary and nominal cascade against the existing RUN07 small-signal result;
6. document why cascade partition is valid: there is no signal feedback from the balanced output stage into the upstream signal path under stiff-rail RUN08 conditions.

If nonlinear partitioning exposes a shared-rail interaction capable of changing the result, promote that interaction to RUN13 rather than hiding it.

### RUN08 acceptance retained

- determine first material clipping for each gain and representative EQ case;
- >=6 dB nominal margin preferred, >=3 dB minimum;
- 10x nominal transient recovery to within 1% in <=100 ms unless an identified LF network physically requires longer;
- document HIGH-gain restricted operating envelope if necessary;
- no absolute maximum violation.

## 4. RUN09 — system noise

### Readiness: METHOD IMPLEMENTATION OPEN

Representative states remain sensible:

- DEFAULT/RIAA;
- DEFAULT/78;
- HIGH/RIAA;
- LOW/78;
- rumble BYPASS/FILTER.

Before implementation:

- confirm controlled vendor/wrapper models expose useful LTspice noise semantics;
- where a macromodel lacks credible internal noise, do not silently treat it as noiseless;
- preserve both absolute output/input-referred noise and comparative/value-engineering metrics;
- identify contribution ranking only where model fidelity supports it.

The AE-049 absolute DEFAULT/RIAA output-noise target remains provisional until bench correlation. Comparative <=0.25/0.75/>0.75 dB value-engineering bands remain useful.

RUN09 can drive component decisions and therefore remains pre-layout.

## 5. RUN10 — sensitivity / tolerance / value engineering

### Readiness: HIGH PRIORITY / LAYOUT-DRIVING

RUN10 is expected to be one of the strongest remaining pre-layout drivers and should run immediately after deterministic RUN08/09 methods are established.

Mandatory current priority set:

### SCH101

- LT5400 B-grade complete-stage CMRR/tolerance;
- gain-programming resistor/shunt parasitic and matching;
- fixed 23.7 kΩ/leg load;
- fixed 47 pF/leg CHASSIS RF shunts;
- 100 Ω RF series pair;
- **AE-076E personality socket/card parasitic capacitance and L/R mismatch**;
- +47/+100 pF card capacitor absolute tolerance and pair matching.

Recommended personality-interface parasitic method:

- use geometry/model/measurement-informed nominal when available;
- also sweep a deliberately conservative bracket so layout sensitivity is visible;
- treat common added differential capacitance separately from L/R mismatch;
- do not claim the interface closed until exact footprint/card geometry is represented.

### SCH103

- timing networks including the current 1600 Hz decomposition issue;
- test the practical 132 nF versus candidate 133 nF implementations against the current acceptance envelope;
- retain TRUE-RIAA 29.4 nF decomposition/procurement closure;
- derive the loosest technically sufficient tolerance/dielectric requirement.

### SCH107

- branch-local 1 µF / 330 kΩ tolerance;
- rumble R/C ratios;
- system-noise impact.

### SCH104/SCH105

- 4.7 kΩ mono-pair mismatch;
- AE-068 preferred <=0.10%, maximum <=0.25% remains the starting evidence;
- 2.2 MΩ returns and parasitic significance.

### SCH108

- ferrite bracket/value trade;
- sense/RF/clamp passive tolerance where material;
- output load/cable sensitivity.

RUN10 output should explicitly classify components:
A — absolute value matters;
B — ratio/matching matters;
C — low sensitivity.

This is also where one-off hand matching should be preferred over unnecessary premium tolerance where technically justified.

## 6. RUN11 — Monte Carlo

### Readiness: DEPENDENT ON RUN10

Do not implement a full combinatorial Monte Carlo campaign first.

RUN11 should consume only high-leverage variables identified by RUN10.

Minimum methodology retained:

- >=1000 runs where practical;
- zero Cat-A safety/function failures;
- >=99% performance yield;
- tail failures understood and translated into component/assembly rules.

For the one-off unit, statistical yield is informative but **measured selection/matching can be a legitimate controlled assembly strategy** where RUN10 shows that matching matters more than absolute tolerance.

## 7. RUN12 — switching transients

### Readiness: COMPONENT-TIMING/PARASITIC INPUTS OPEN

Required mechanisms:

- rumble FILTER↔BYPASS;
- matrix adjacent BBM transitions;
- mute RUN↔MUTE.

Normal operator procedure remains:

`MUTE -> select -> RUN`

Live switching is a stress case, not the default operating requirement.

Before runner implementation:

- obtain or bound actual break-before-make interval for the selected NKK/C&K parts where manufacturer evidence permits;
- bound switch parasitic capacitance;
- model contact transition without inventing automatic sequencing;
- preserve DR-039 branch charge state correctly.

RUN12 can still drive local discharge/bias/recovery provisions and therefore remains pre-layout.

## 8. RUN13 — rail variation, ripple, startup

### Readiness: HISTORICAL SWEEP MUST NOT BE REUSED AS CURRENT NOMINAL BAND

Historical AE-049/050 wording uses ±18 V-era values including ±17.5 to ±18.5 V.

AE-076A supersedes current nominal rail authority to ±17.0 V while deliberately preserving historical records.

Therefore:

- nominal RUN13 centre must be ±17.0 V;
- ±18 V must never be described as current nominal;
- retain rail-asymmetry stress as a separate dimension;
- retain 100 Hz ripple injection;
- include startup behaviour where the model supports it.

### Rail sweep bound remains to be frozen

Do **not** silently convert the historical ±17.5–18.5 band into a guessed new acceptance band.

Recommended engineering distinction:

1. **audio-circuit robustness sweep** around ±17 V — a deliberately bounded stress range to be approved before execution;
2. **physical PSU qualification** — set-point, raw-rail ripple trough, dropout, startup/overshoot and thermal behaviour from the actual one-off supply.

AE-073 supports plausibility of a target-17 set point but explicitly does not establish physical dropout/set-point/ripple/thermal limits.

A candidate robustness bracket such as ±16.5/17.0/17.5 V may be evaluated during runner design, but it is **not current authority until explicitly adopted**.

## 9. RUN14 — phantom / external fault energy

### Readiness: CURRENT OUTPUT/PSU FAULT MODEL MUST BE RECONCILED FIRST

Historical AE-048/050 fault wording predates several current facts.

RUN14 must use:

- nominal ±17 V rail authority;
- S1G rail clamps, not generic axial 1N4004;
- THAT1646 current source semantics;
- current SCH108 sense/RF/ferrite/clamp topology;
- H801/H802 HOT/COLD-only output loom;
- realistic cable/harness impedance;
- 470 µF rail reservoirs where present;
- powered and unpowered states;
- one-leg, both-leg, application/removal and asymmetric fault cases.

The external phantom source should use a controlled representative +48 V feed model and realistic feed resistance, not an ideal zero-impedance 48 V source.

### Regulator reverse-energy limitation

AE-073 qualifies forward/startup discriminator behaviour of the reconstructed PSU model but does **not** establish trustworthy regulator reverse-current/reverse-energy behaviour.

RUN14 therefore needs one of:

- a controlled regulator model whose reverse behaviour is demonstrably valid for the fault case; or
- a conservative explicit reverse-energy surrogate plus bench/absolute-maximum closure.

Do not infer regulator survival merely because a vendor forward-regulation macromodel numerically converges.

### Required RUN14 outputs

- XLR leg voltages;
- S1G clamp current waveform and pulse energy;
- positive/negative rail peak and duration;
- local reservoir-cap charge/energy;
- THAT1646 pin absolute maxima;
- regulator reverse current/voltage or conservative surrogate;
- opposite-channel coupling;
- electrolytic polarity/voltage stress.

Fault acceptance is an absolute-maximum/survival gate, not an audio-performance gate.

## 10. Recommended controlled implementation order after AE-076E

1. Reconcile current RUN08–RUN14 execution delta in structured config.
2. Implement large-signal composition discriminator.
3. RUN08 overload/recovery.
4. RUN09 noise.
5. RUN10 sensitivity/value engineering.
6. Reconcile any component/footprint changes produced by RUN10.
7. RUN11 selected Monte Carlo only.
8. Acquire/bound switch timing/parasitics and execute RUN12.
9. Freeze current ±17 V robustness sweep and execute RUN13.
10. Reconcile non-ideal/reverse PSU fault model and execute RUN14.
11. Regenerate current qualification summary.
12. Perform formal block-by-block independent review.
13. Consider routing only with zero HOLD dispositions.

## 11. Pre-layout change-risk classification

Highest probability of changing PCB/component decisions:

1. RUN10 — HIGH;
2. RUN14 — MEDIUM/HIGH because fault-energy mitigation may change protection;
3. RUN12 — MEDIUM;
4. RUN13 — MEDIUM if rail/dropout/startup evidence changes decoupling/power interface;
5. RUN08 — MEDIUM if hidden clipping/recovery is found;
6. RUN09 — LOW/MEDIUM, mostly value/tolerance/layout decisions;
7. RUN11 — derivative of RUN10 rather than independent architecture driver.

This ranking supports keeping routing held until the campaign closes.

## 12. Disposition

**Forward qualification readiness: HOLD FOR EXECUTION INFRASTRUCTURE / CURRENT-DELTA IMPLEMENTATION.**

No evidence currently justifies changing the architecture or abandoning the existing qualification framework.

The next immediate critical-path action remains AE-076E personality/native-CAD migration. This review exists so that, once AE-076E closes, the project proceeds into RUN08–RUN14 using current conditions rather than stale historical execution constants.
