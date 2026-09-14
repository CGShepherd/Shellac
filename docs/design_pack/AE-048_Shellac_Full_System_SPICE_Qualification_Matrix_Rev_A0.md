# AE-048 — Shellac Full-System SPICE Qualification Matrix
**Project:** Shellac
**Status:** INTERIM / QUALIFICATION PLAN / PRE-SPICE
**Date:** 2026-09-11

## Objective
Define the minimum simulation evidence required to progress Shellac from ANALYSED to SIMULATED without feature churn.

Principle:
Every simulation shall answer a controlled design or release question.

## A. Model configuration freeze before simulation
Before accepting results, the SPICE model shall reflect:
- selected fail-safe 14 / 18 / 22 dB SCH101 gain architecture;
- Grado 78E and AT-VM95SP primary 78-rpm cartridge models;
- Grado Gold / 8MZ LP compatibility model;
- 47.4 kOhm fixed differential input loading;
- candidate BASE / +47 pF / +100 pF differential capacitance;
- DR-037 complete-RIAA SCH103 architecture;
- all 25 intentional Bass x Treble states;
- candidate DR-039/SCH107 integrated topology;
- SCH104 unity isolation buffers and 4.7 kOhm mono branches;
- AE-041 A1 3P4T SCH105 matrix;
- 2.2 MOhm matrix input returns;
- SW905 input-side mute;
- THAT1646 x2 differential output;
- output sense/RFI/protection network;
- regulated +/-18 V rails.

No superseded independent 3180-us stage, 4P4T matrix, relay mute, automatic sequencing or stale gain topology may appear.

## B. Deterministic AC transfer
### B1 Input/loading
For each cartridge family:
- cable capacitance: 50 / 100 / 150 / 200 / 300 pF;
- Shellac capacitance: BASE / +47 pF / +100 pF;
- sweep 5 Hz to at least 100 kHz.

Record:
- cartridge terminal loading;
- 20 Hz-20 kHz response;
- HF resonance/peaking;
- selected capacitance suitability.

### B2 Replay EQ
For all 25 Bass x Treble combinations:
- nominal transfer;
- 20 Hz-20 kHz magnitude and phase;
- named historical curve error;
- RIAA error separately.

Do not reject unnamed combinations: they are intentional adjustment states.

### B3 Rumble
Compare:
- BYPASS;
- FILTER;
- candidate SCH107 impedance scales / DR-039 arrangements.

Record:
- passband error;
- 15 Hz characteristic;
- interaction with DR-039;
- phase/group-delay behaviour where useful.

### B4 Matrix
Verify all four states:
- DUAL L;
- STEREO;
- L+R;
- DUAL R.

Stimuli:
- L only;
- R only;
- equal in phase;
- unequal;
- opposite phase;
- unrelated phase.

Record gain, crosstalk and mono weighting.

### B5 Output loads
At minimum:
- 100 kOhm;
- 20 kOhm;
- 10 kOhm;
- 600 Ohm stress case;
- representative balanced cable capacitance.

Record differential gain, common-mode behaviour and stability.

## C. Headroom and overload
Replace historical local severe constants with one end-to-end methodology.

For each qualified cartridge family and gain setting:
1. nominal cartridge output;
2. defined hot-record / high-velocity level;
3. overload sweep until first material non-linearity/clipping;
4. recovery after overload.

Track node maxima at:
- SCH101 internal/output;
- SCH103 LF active output;
- SCH103 recovery output;
- DR-039/SCH107 interface;
- SCH104 output;
- SCH105 buffer output;
- THAT1646 input;
- XLR differential output.

Acceptance:
- no hidden earlier-stage clipping;
- operator gain settings have documented usable envelopes;
- HIGH gain need not support every 5 mV source if its intended low-output use case is documented.

## D. Noise
Calculate input-referred and output noise for:
- LOW / DEFAULT / HIGH;
- representative 78 EQ;
- RIAA;
- rumble BYPASS/FILTER.

Break down contributions where practical:
- cartridge/source;
- SCH101 resistors/op-amps/LT5400;
- SCH103;
- SCH107;
- SCH104;
- SCH105;
- SCH108.

Use results to determine whether impedance-scaling SCH107 materially worsens system noise.

## E. Tolerance and value engineering
For each electrically significant component classify:
1. absolute value matters;
2. matching/ratio matters;
3. neither materially matters.

Run sensitivity first, Monte Carlo second.

Priority parameters:
- SCH101 gain resistors and LT5400 grade;
- input load R and capacitance;
- SCH103 RF/RG/RS and timing capacitors;
- SCH107 R/C ratios and impedance scale;
- SCH104/SCH105 4.7 kOhm mono pair;
- matrix 2.2 MOhm returns;
- output-interface passives where relevant.

Derive:
- allowable absolute tolerance;
- allowable L/R mismatch;
- TCR requirement;
- whether hand matching is economically preferable.

No premium component without demonstrated material benefit.

## F. DC operating points
For every major switch configuration:
- op-amp input/output DC;
- post-EQ raw DC;
- after DC-block candidate;
- rumble BYPASS/FILTER;
- all matrix states;
- RUN/MUTE;
- XLR differential/common-mode DC.

Include component offset/bias models where available and conservative bounded cases where not.

## G. Switching transients
### G1 Rumble SW904
Test FILTER <-> BYPASS:
- with MUTE asserted;
- live as stress case.

### G2 Matrix SW903
Test all adjacent transitions with BBM:
- with MUTE asserted;
- live as stress case;
- sweep break interval and parasitic capacitance.

### G3 Mute SW905
Test RUN <-> MUTE:
- zero input;
- representative sine;
- large signal;
- DC-offset worst case.

Record differential and common-mode output peaks and settling.

Operating sequence remains MUTE -> select -> RUN unless evidence supports otherwise.

## H. Rail variation and ripple
Normal operation:
- +/-18 V nominal;
- plausible regulator tolerance;
- rail asymmetry;
- 100 Hz residual ripple injection.

Record:
- gain/EQ sensitivity;
- noise;
- output common-mode;
- headroom.

## I. Phantom-power fault
Use non-ideal rails.

Model:
- representative +48 V phantom source/feed resistors;
- external coupling capacitors including a conservative large value;
- XLR cable;
- THAT1646 output network;
- 1N4004 rail clamps;
- local decoupling;
- 470 uF rail reservoirs;
- harness impedance;
- external regulator reverse-current/output behaviour.

Cases:
- powered Shellac;
- unpowered Shellac;
- one leg;
- both legs;
- application;
- removal/discharge;
- asymmetric fault.

Record:
- THAT1646 output voltage;
- clamp current and pulse energy;
- +/-18 V rail peak;
- regulator reverse current;
- duration outside normal rail envelope;
- effect on opposite channel.

Do not add protection until this model demonstrates a failure.

## J. Ground/bond configuration
Selected build currently uses R909 = 0 Ohm direct 0VA-CHASSIS bond.

Compare only if required:
- direct bond;
- alternative controlled ground-lift candidate.

C909 is a DNP candidate when R909 is fitted because it is electrically bypassed.

Grounding simulation is supportive only; final hum/EMC validation remains bench dependent.

## K. Simulation order
1. Model/configuration reconciliation.
2. DC operating-point sanity.
3. Nominal AC block checks.
4. End-to-end AC.
5. Headroom/overload.
6. Noise.
7. Sensitivity.
8. Selected Monte Carlo.
9. Switching transient.
10. Rail/ripple.
11. Phantom fault.
12. Consolidated review against intent and BOM.

Do not begin Monte Carlo across the full combinatorial space before deterministic nominal cases pass.

## L. Pass/fail evidence package
For each run family retain:
- model revision/hash;
- simulator/version;
- test configuration;
- plots/data;
- measured extrema;
- pass/fail criterion;
- result;
- unresolved anomaly.

Final review shall reconcile:
INTENT <-> SCHEMATIC <-> SPICE <-> BOM.

## M. Exit criteria for SIMULATED gate
The design may progress from ANALYSED to SIMULATED only when:
- every intended function has a passing deterministic model;
- no superseded functionality remains in the model;
- all material clipping/headroom issues are understood;
- DR-039/SCH107 topology is selected;
- component tolerance requirements are evidence-derived;
- switching transients are acceptable under the operating procedure;
- phantom fault either passes or generates a controlled corrective action;
- no unexplained Cat-A/B anomaly remains.

## Confidence
- qualification structure covers current open design risks: 99%
- deterministic-first approach is appropriate: 100%
- cartridge x gain operating-envelope method is preferable to one severe constant: 99%
- tolerance sensitivity before Monte Carlo is appropriate for value engineering: 99%
- phantom fault requires non-ideal rails: 99%
