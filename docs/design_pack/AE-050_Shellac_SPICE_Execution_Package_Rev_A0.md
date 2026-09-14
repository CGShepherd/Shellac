# AE-050 — Shellac SPICE Execution Package
**Project:** Shellac
**Status:** INTERIM / PRE-SPICE EXECUTION AUTHORITY
**Date:** 2026-09-11

## Purpose
Convert AE-048 and AE-049 into a practical simulation execution package for the full-system Shellac SPICE campaign.

The execution package shall make the simulation repeatable, reviewable, and traceable.

---

## 1. Authoritative model hierarchy

Use one top-level model as the source of truth for all node voltages and operating conditions.

Recommended hierarchy:

SHELLAC_TOP
├── SRC_CARTRIDGE_L
├── SRC_CARTRIDGE_R
├── SCH101_L
├── SCH101_R
├── SCH103_L
├── SCH103_R
├── DR039_SCH107_L
├── DR039_SCH107_R
├── SCH104_L
├── SCH104_R
├── SCH105_MATRIX
├── SCH105_BUF_L
├── SCH105_BUF_R
├── SW905_MUTE
├── SCH108_L
├── SCH108_R
├── LOAD_BALANCED_L
├── LOAD_BALANCED_R
├── PSU_PLUS18
├── PSU_MINUS18
└── CHASSIS_GROUND_MODEL

Do not derive critical system behaviour by multiplying isolated transfer functions once the integrated model exists.

Analytical Python models remain useful for:
- expected-value cross-checks;
- tolerance sensitivity;
- regression comparisons;
- reporting.

They are not the final authority for integrated node behaviour.

---

## 2. Required model fidelity

### 2.1 Cartridge/source models
Each cartridge model shall include:
- source voltage;
- source resistance;
- source inductance;
- cable capacitance;
- left/right independence.

Primary models:
- Grado 78E;
- Audio-Technica AT-VM95SP.

Compatibility:
- Grado Gold / 8MZ.

Optional tolerated generic MM/MI model only if useful.

### 2.2 SCH101
Model:
- 100 Ohm input series resistors;
- 47.4 kOhm differential load;
- fixed CM shunts;
- selected differential capacitance state;
- selected fail-safe gain architecture;
- LT5400 converter;
- actual op-amp macro-model where practical.

Gain-state parameters:
- GAIN=LOW
- GAIN=DEFAULT
- GAIN=HIGH

### 2.3 SCH103
Model all intended:
- Bass states FLAT / 200 / 400 / 500 / TRUE_RIAA;
- Treble states FLAT / 1600 / 2121 / 3400 / 5800;
- active LF OPA1612 stage;
- fixed 750 Ohm treble element;
- recovery gain 2.1;
- all actual capacitor combinations unless a candidate simplification is being explicitly compared.

### 2.4 DR-039 + SCH107
Treat as one coupled subsystem until final topology is selected.

Candidate parameter:
LF_TOPOLOGY =
- CURRENT
- BIG_C
- POST_SWITCH_BLOCK
- SPLIT_BLOCK
- RUMBLE_SCALE_2
- RUMBLE_SCALE_5
- RUMBLE_SCALE_10

Do not populate all candidates simultaneously.

### 2.5 SCH104
Model:
- OPA1656 unity buffer;
- 100 Ohm output isolation;
- 4.7 kOhm mono branch;
- switch/PCB parasitic candidate if required.

### 2.6 SCH105
Model:
- 3P4T truth table;
- 2.2 MOhm returns;
- BBM break interval;
- OPA1656 output buffers;
- 100 Ohm output isolation.

Matrix parameter:
MODE =
- DUAL_L
- STEREO
- MONO
- DUAL_R

### 2.7 SCH108
Model:
- SW905 RUN/MUTE;
- THAT1646 macro-model;
- OUT/SNS 10 uF capacitors;
- ferrites;
- 100 pF chassis RF capacitors;
- 1N4004 rail clamps;
- realistic XLR load and cable.

### 2.8 PSU
Normal AC/noise runs may use simplified regulated rails where justified.

Transient/fault runs must include:
- regulator output impedance;
- reverse-current/reverse-energy behaviour;
- harness resistance/inductance;
- 470 uF local rail reservoirs;
- local decoupling;
- bleeders.

---

## 3. Global parameter set

Recommended global parameters:

CARTRIDGE
GAIN
BASS
TREBLE
RUMBLE
MODE
MUTE
CABLE_PF
LOAD_CAP_STATE
OUTPUT_LOAD
OUTPUT_CABLE_PF
LF_TOPOLOGY
RAIL_PLUS
RAIL_MINUS
RAIL_RIPPLE
BBM_TIME
SWITCH_PARASITIC_PF
TEMP
TOLERANCE_MODE
MC_SEED

Avoid hidden parameters in individual subcircuits.

---

## 4. Canonical node names

Use stable labels across all runs:

VIN_CART_L
VIN_CART_R

N101_L_OUT
N101_R_OUT

N103_L_LF
N103_R_LF
N103_L_OUT
N103_R_OUT

N107_L_IN
N107_R_IN
N107_L_OUT
N107_R_OUT
N107_L_BYPASS
N107_R_BYPASS

N104_L_OUT
N104_R_OUT
MONO_AVG
MONO_R_LEG

N105_L_IN
N105_R_IN
N105_L_OUT
N105_R_OUT

N108_L_IN
N108_R_IN
XLR_L_POS
XLR_L_NEG
XLR_R_POS
XLR_R_NEG

VPLUS18
VMINUS18
ZERO_VA
CHASSIS

This naming should be mirrored in plots, result exports and bench test points where practical.

---

## 5. Deterministic execution sequence

### RUN 00 — Model sanity
Purpose:
- convergence;
- operating points;
- no impossible node states;
- no floating nodes in valid switch positions.

Output:
- DC operating-point table.

Pass:
- no unexpected saturation;
- no invalid DC state.

### RUN 01 — SCH101 cartridge/loading
Sweep:
- all primary cartridges;
- 50/100/150/200/300 pF cable;
- BASE/+47/+100 pF.

Output:
- cartridge terminal response;
- SCH101 input and output response;
- HF peaking table.

### RUN 02 — SCH101 gain/CMRR
Gain:
- LOW/DEFAULT/HIGH.

Input stimuli:
- differential;
- common-mode.

Output:
- gain accuracy;
- CMRR vs frequency;
- internal headroom.

### RUN 03 — SCH103 EQ
All 25 Bass x Treble states.

Output:
- magnitude/phase;
- named-target error;
- RIAA error;
- L/R tracking.

### RUN 04 — DR039/SCH107 candidate comparison
Compare candidate LF topologies.

Output:
- 10/15/20/30/50 Hz gain;
- group delay;
- noise;
- component-value summary;
- transient settling.

Decision output:
- preferred topology;
- runner-up;
- reject reasons.

### RUN 05 — SCH104/SCH105 matrix
All matrix states.

Stimuli:
- L only;
- R only;
- equal;
- unequal;
- opposite phase.

Output:
- insertion loss;
- mono weighting;
- crosstalk;
- dormant-path coupling.

### RUN 06 — SCH108 nominal output
Loads:
- 100k
- 20k
- 10k
- 600 stress.

Cable:
- representative low/nominal/high capacitance.

Output:
- differential gain;
- CM behaviour;
- stability;
- output headroom.

### RUN 07 — End-to-end nominal chain
Representative operating states:
- 78 nominal;
- 78 alternate EQ;
- RIAA;
- rumble bypass;
- rumble in;
- stereo;
- mono.

Output:
- complete transfer;
- node-by-node signal levels;
- total gain.

### RUN 08 — Headroom / overload
For each cartridge and gain state:
- nominal;
- 2x nominal;
- 4x nominal;
- amplitude sweep to clipping;
- 10x burst recovery.

Output:
- first clipping node;
- cartridge input limit;
- output limit;
- recovery time.

### RUN 09 — Noise
Representative states:
- DEFAULT/RIAA;
- DEFAULT/78;
- HIGH/RIAA;
- LOW/78;
- rumble bypass/filter.

Output:
- output noise;
- input-referred noise;
- contribution ranking.

### RUN 10 — Sensitivity
One-at-a-time perturbation.

Priority parts:
- SCH101 gain network;
- LT5400 grade;
- input R/C;
- SCH103 timing R/C;
- SCH107 R/C;
- 4.7k mono pair;
- 2.2M returns.

Output:
- performance derivative or delta per tolerance step;
- tolerance category A/B/C.

### RUN 11 — Monte Carlo
Only high-leverage cases identified in RUN 10.

Minimum:
- 1000 runs where practical.

Output:
- yield;
- worst run;
- percentile table;
- pass/fail count.

### RUN 12 — Switching transients
Rumble:
- BYPASS<->FILTER.

Matrix:
- adjacent BBM transitions.

Mute:
- RUN<->MUTE.

Repeat:
- muted normal-use case;
- live stress case.

Output:
- differential peak;
- common-mode peak;
- settling time.

### RUN 13 — Rail variation/ripple
Sweep:
- +/-17.5 to +/-18.5 V;
- rail asymmetry;
- 100 Hz ripple.

Output:
- gain;
- RIAA shift;
- DC offset;
- headroom;
- output ripple.

### RUN 14 — Phantom fault
Cases:
- powered/unpowered;
- one leg/both legs;
- application/removal;
- asymmetric;
- conservative external coupling capacitor.

Output:
- output node peaks;
- clamp current;
- diode pulse energy;
- rail excursion;
- regulator reverse current;
- connected-device supply maxima.

---

## 6. Standard result record

Every simulation run shall produce one structured result row containing:

RUN_ID
MODEL_REV
SIMULATOR
SIM_VERSION
DATE
CARTRIDGE
GAIN
BASS
TREBLE
RUMBLE
MODE
MUTE
LF_TOPOLOGY
LOAD
RAIL_STATE
PARAM_SWEEP
MEASURED_METRIC
MEASURED_VALUE
UNIT
ACCEPTANCE_LIMIT
PASS_FAIL
NOTES

Do not rely on plot inspection alone.

---

## 7. Plot set

Minimum standard plots:

P01 complete magnitude response
P02 complete phase response
P03 SCH101 CMRR
P04 RIAA error
P05 historical EQ target error
P06 DR039/SCH107 LF comparison
P07 node-by-node headroom
P08 output-load response
P09 noise spectrum / integrated noise
P10 sensitivity ranking
P11 Monte Carlo histogram / worst-case overlay
P12 matrix switching transient
P13 mute transient
P14 rail ripple response
P15 phantom rail excursion and clamp current

Use consistent axis ranges across candidate comparisons.

---

## 8. Decision tables

### 8.1 DR-039/SCH107 trade table
Columns:
- topology;
- 20 Hz loss;
- 30 Hz loss;
- 10 Hz rejection;
- integrated noise delta;
- settling;
- capacitor count;
- estimated component cost;
- PCB area;
- decision.

### 8.2 Precision-component table
Columns:
- ref/function;
- nominal value;
- sensitivity;
- absolute tolerance required;
- matching required;
- TCR required;
- candidate series;
- hand-match viable Y/N;
- estimated cost;
- decision.

### 8.3 Cartridge/gain envelope
Rows:
- cartridge x gain state.

Columns:
- nominal output;
- clipping input threshold;
- margin dB;
- recommended usage;
- restricted usage;
- pass/fail.

---

## 9. Folder structure for results

Recommended controlled structure:

/simulation/
  /models/
  /runs/
    /run00_sanity/
    /run01_input_loading/
    /run02_gain_cmrr/
    /run03_eq/
    /run04_lf_trade/
    /run05_matrix/
    /run06_output/
    /run07_end_to_end/
    /run08_headroom/
    /run09_noise/
    /run10_sensitivity/
    /run11_monte_carlo/
    /run12_switching/
    /run13_rails/
    /run14_phantom/
  /results/
    results_master.csv
    result_summary.md
  /plots/
  /scripts/

Do not create this controlled structure until the simulation toolchain is confirmed.

---

## 10. Toolchain requirements
Record:
- SPICE engine and version;
- op-amp macro-model source/version;
- THAT1646 model source/version;
- diode model source;
- temperature;
- numerical tolerances;
- convergence options.

Where a vendor macro-model is unavailable or unsuitable, explicitly document the behavioural substitute and what claims it cannot support.

---

## 11. Sunday operator workflow
1. Confirm repository clean state.
2. Record current commit.
3. Confirm simulator/version.
4. Reconcile model against AE-047 to AE-050.
5. Run RUN 00.
6. Stop if DC/convergence fails.
7. Run deterministic RUN 01 to RUN 07.
8. Resolve topology defects before overload/noise.
9. Run RUN 08 to RUN 10.
10. Select only necessary Monte Carlo cases.
11. Run RUN 11 to RUN 14.
12. Export master result table.
13. Review against AE-049 acceptance criteria.
14. Record anomalies before making design changes.

No ad-hoc schematic changes during the run set without creating an explicit candidate variant.

---

## 12. Exit package
The simulation campaign should leave:
- authoritative top-level model;
- all subcircuits;
- model-source manifest;
- run scripts;
- raw result data;
- master result CSV;
- standard plots;
- candidate trade tables;
- pass/fail summary;
- anomaly log;
- recommended controlled design changes.

---

## Confidence
- hierarchy appropriate for full-chain Shellac validation: 99%
- parameter set sufficient for current architecture: 98%
- deterministic run order appropriate: 100%
- node naming and results schema improve traceability materially: 99%
- execution sequence minimises wasted Monte Carlo/fault work: 99%
