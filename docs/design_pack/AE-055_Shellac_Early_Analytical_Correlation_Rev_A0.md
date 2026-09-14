# AE-055 — Shellac Early Analytical Correlation
**Project:** Shellac
**Status:** PRE-SPICE CORRELATION EVIDENCE
**Date:** 2026-09-13

## 1. Purpose

Implement the first independent analytical correlation cases required by AE-053,
before broader integrated LTspice modelling.

The objective is not to replace LTspice. It is to create simple, independently
checkable expected values against which later LTspice extraction can be compared.

## 2. Controlled correlation cases

### 2.1 DR-039 direct branch candidate
Candidate:
- C = 1 uF
- R = 330 kOhm

Analytical first-order high-pass:
- fc = 1 / (2*pi*R*C)
- nominal fc approximately 0.4823 Hz
- 20 Hz attenuation approximately -0.0025 dB

This confirms only the isolated first-order direct branch. It does not qualify the
integrated DR039/SCH107 subsystem.

### 2.2 SCH101 nominal converter gain arithmetic
Nominal voltage gain = 4.0.

Analytical conversion:
- 20*log10(4) approximately 12.0412 dB.

This is a numerical cross-check only. It does not qualify LT5400/op-amp CMRR, noise,
headroom, tolerance or the selected 14/18/22 dB overall gain architecture.

### 2.3 Matrix equal-resistor arithmetic
With equal 4.7 kOhm summing legs:
- L-only -> 0.5
- R-only -> 0.5
- equal L/R -> 1.0
- equal/opposite phase -> 0.0

This proves ideal passive averaging arithmetic only. It does not close crosstalk,
switch parasitics, source impedance interaction, BBM transient behaviour or layout.

## 3. Independence rule

The analytical implementation uses closed-form Python calculations and controlled YAML
inputs. It is intentionally independent of the LTspice result parser and should not be
modified merely to force agreement with future LTspice results.

Any material disagreement becomes an anomaly.

## 4. Next controlled step

After target-machine RUN00 is proven, add LTspice correlation cases matching these
three analytical cases and compare extracted values automatically.

Only after agreement should the integrated `SHELLAC_TOP` hierarchy begin expanding.

## 5. Review

### QUAD
No additional analogue functionality is introduced. Calculations are minimal and
directly tied to already selected architecture/candidates.

### HP / Agilent / Keysight
Expected values are explicit, machine-readable and independently reproducible.

### Airbus civil TDA
The analytical source is separated from solver authority and preserves anomaly
independence.

## Confidence

- DR039 isolated RC arithmetic: 100%
- nominal gain conversion arithmetic: 100%
- ideal equal-resistor matrix arithmetic: 100%
- suitability as independent early correlation evidence: 99%
