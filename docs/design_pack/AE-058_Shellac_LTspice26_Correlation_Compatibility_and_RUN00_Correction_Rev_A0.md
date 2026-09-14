# AE-058 — LTspice 26 Correlation Compatibility and RUN00 Correction — Rev A0

## Status
Pre-SPICE design-assurance evidence. This record does not constitute manufacturing baseline authority.

## Purpose
Close compatibility defects observed while correlating AE-055 analytical checks against LTspice 26.0.2 and correct RUN00 midpoint topology before toolchain acceptance.

## Changes
1. Measurement parsing distinguishes true `WHEN ... AT ...` results from complex `(dB, phase)` AC outputs.
2. Scalar `name: expression = number` measurements are accepted.
3. SCH101 correlation measures scalar magnitude and converts to dB in Python.
4. Matrix correlation remains four deterministic independent operating-point cases; `.alter` is not used.
5. RUN00 divider spans `VPLUS18` to `VMINUS18`; midpoint acceptance is 0 V and both rails are exercised.
6. Regression tests cover parser discrimination, magnitude-to-dB conversion, SCH101 x4 arithmetic and RUN00 bipolar topology.

## Authority relationship
AE-048/049/050 remain qualification/numerical/execution authorities; AE-053 remains toolchain architecture; AE-055 remains independent analytical evidence; AE-056 remains first LTspice correlation implementation. This corrective record does not qualify the real SCH101 analogue implementation, LT5400, DR039, or integrated `SHELLAC_TOP`.
