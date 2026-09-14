# AE-056 — Shellac LTspice / Analytical Correlation Implementation
**Project:** Shellac
**Status:** PRE-SPICE CORRELATION IMPLEMENTATION
**Date:** 2026-09-13

## 1. Purpose

Add controlled LTspice counterparts to the three independent AE-055 analytical
correlation cases and automatically compare solver output against independently
calculated expected values.

This is the first solver-to-analysis correlation increment under AE-053.

## 2. Implemented correlation cases

### DR039 direct RC
LTspice model:
- ideal AC source;
- 1 uF series capacitor;
- 330 kOhm return;
- AC sweep.

Extract:
- -3 dB corner;
- 20 Hz magnitude.

Compare to AE-055 closed-form high-pass calculation.

### SCH101 nominal gain arithmetic
LTspice model:
- ideal source;
- controlled ideal voltage-gain element;
- gain = 4;
- nominal 1 kHz AC point.

Extract gain in dB and compare to 20 log10(4).

This remains an arithmetic correlation case, not a model of the selected LT5400
implementation.

### Matrix equal-resistor average
LTspice model:
- equal 4.7 kOhm L/R legs to averaging node;
- high-impedance load;
- four deterministic source combinations.

Compare L-only, R-only, equal and opposite-phase results to AE-055 arithmetic.

## 3. Acceptance philosophy

Numerical tolerances in `correlation_ltspice.yaml` are correlation tolerances, not
product-performance acceptance criteria. They establish whether the solver/extraction
path reproduces simple independently calculable cases.

A material disagreement is an anomaly and blocks expansion of the integrated model.

## 4. Explicit non-scope

AE-056 does not:
- model real op-amp macro-models;
- qualify LT5400 CMRR/noise/headroom;
- implement AE-042 gain selection;
- implement AE-052 DR039/SCH107 topology in the generator;
- qualify matrix parasitics, crosstalk or switching;
- create manufacturing authority.

## 5. Next step

After the three cases pass on the target machine:
1. freeze the successful target-machine invocation/configuration evidence;
2. add unchanged vendor/reference macro-models with hashes/provenance;
3. construct the first integrated `SHELLAC_TOP` skeleton;
4. perform RUN00 DC operating-state checks using canonical AE-050 node names;
5. correlate simple integrated checkpoints before proceeding to RUN01 onward.

## 6. Review perspectives

### QUAD
The correlation circuits are intentionally ideal/minimal. No circuit complexity is
introduced beyond what is needed to validate the toolchain.

### HP / Agilent / Keysight
Expected values, solver outputs, deltas and tolerances are explicit and machine-readable.

### Airbus civil TDA
Independent analysis is preserved; solver disagreement becomes controlled anomaly
evidence rather than prompting silent analytical-model adjustment.

## Confidence

- correlation architecture conforms to AE-053: 99%
- independence from product design implementation preserved: 100%
- suitable gate before integrated macro-model expansion: 99%
