# AE-045 — SCH104 Isolation / Mono-Preparation Pre-SPICE Review
**Project:** Shellac
**Status:** INTERIM / ANALYSED / SPICE REQUIRED
**Date:** 2026-09-11

## Purpose
Capture the SCH104 review after AE-041 A1 and before full SPICE/BOM optimisation. This is an interim evidence record, not a baseline or manufacturing release.

## Governing intent
SCH104 shall:
1. isolate the SCH107 output from the passive channel-mode matrix;
2. provide unity voltage gain only;
3. provide a low-impedance source for the direct matrix paths;
4. provide two passive 4.7 kOhm mono-averaging branches ahead of the 100 Ohm direct-path isolation resistors;
5. introduce no additional gain, EQ, mode logic or other functionality.

Final +6 dB differential conversion remains the responsibility of the THAT1646 in SCH108.

## Live implementation reconciliation
Per channel the current generator implements:
- OPA1656 unity-gain follower;
- 100 Ohm / 1% direct-path output isolation resistor;
- 4.7 kOhm mono-averaging resistor taken directly from the OPA1656 output, before the 100 Ohm resistor;
- left mono leg -> MONO_AVG permanently;
- right mono leg -> MONO_R_LEG;
- local +18 V / -18 V decoupling;
- input and output test points.

There is no residual +6 dB SCH104 gain stage.

## Matrix interaction
AE-041 A1 defines a 3P4T matrix.

Outside L+R:
- right 4.7 kOhm leg is disconnected from MONO_AVG by SW903 Pole C;
- left 4.7 kOhm leg terminates at the otherwise unselected MONO_AVG node;
- therefore there is no intentional conductive L-R path in DUAL L, STEREO or DUAL R.

In L+R:
- both 4.7 kOhm legs are connected to MONO_AVG;
- both SCH105 matrix-buffer inputs select MONO_AVG;
- each SCH105 input has a 2.2 MOhm return to 0VA.

## Mono loading / gain
The two SCH105 2.2 MOhm input returns appear in parallel at MONO_AVG:
- effective load = 1.1 MOhm.

For equal L and R sources:
- Thevenin source resistance from two equal 4.7 kOhm legs = 2.35 kOhm;
- mono gain due to loading = 1.1M / (1.1M + 2.35k) = 0.997868;
- error = approximately -0.01854 dB.

This is negligible for the intended function and is already represented in the live mode-matrix model.

## Direct-path loading
The 100 Ohm direct-path isolation resistor drives a 2.2 MOhm matrix-buffer return.

Approximate direct-path gain:
- 2.2M / (2.2M + 100) = 0.9999545;
- error ≈ -0.000395 dB.

No correction is justified.

## 4.7 kOhm tolerance interpretation
The absolute value of 4.7 kOhm is not the principal determinant of mono accuracy.

For two summing resistors RL and RR, the relative L/R weighting is governed mainly by their ratio. Approximate worst-case weighting bias for symmetrical tolerance extremes:

| Individual tolerance extremes | Approx. L/R weighting imbalance |
|---|---:|
| ±1% | 1.0% |
| ±0.5% | 0.5% |
| ±0.1% | 0.1% |
| ±0.05% | 0.05% |
| ±0.01% | 0.01% |

The equal-input mono insertion loss remains approximately -0.01854 dB across these cases because it is dominated by the nominal 4.7 kOhm versus 1.1 MOhm loading.

Therefore the current 0.1% specification should be treated as a **matching requirement candidate**, not yet as an absolute-value requirement.

For a single hand-built Shellac, a credible lower-cost strategy is:
- buy a modest quantity of low-TCR 1% or 0.1% 4.7 kOhm thin-film resistors;
- measure and select a closely matched pair;
- record installed values;
- place the pair symmetrically for thermal tracking.

Final allowed mismatch shall be derived from SPICE / mono acceptance, not assumed.

## Thermal noise
Two 4.7 kOhm summing resistors in parallel present approximately 2.35 kOhm source resistance at MONO_AVG.

Johnson noise at 300 K:
- approximately 6.24 nV/sqrt(Hz).

This is not obviously material relative to the complete Shellac noise budget, but full SPICE shall confirm its output-referred contribution.

Increasing the summing resistors merely to reduce source-to-source current would increase noise and source impedance and is not presently justified.

## Dormant left mono branch
Outside L+R, the left 4.7 kOhm resistor terminates at an unselected MONO_AVG node.

Ideal-circuit effect:
- no DC or intentional audio-frequency load;
- no L-R resistive path.

Real implementation:
- switch off-capacitance, PCB capacitance and trace capacitance provide a small AC load;
- this must be included in detailed SPICE only if estimated/measured parasitics make it material.

No fourth switch pole is justified merely to remove this dormant branch unless SPICE or bench evidence demonstrates a measurable problem.

## OPA1656 / headroom
SCH104 is unity gain.

Current model assumptions:
- nominal input ≈ 0.321 Vrms;
- severe input ≈ 3.21 Vrms;
- design output ceiling = 10 Vrms;
- severe-case model margin > 9.8 dB.

The wider end-to-end review has also used a severe matrix-domain level of 6.42 Vrms. Full-chain SPICE must reconcile these different stress-reference points and verify actual SCH104 peak swing on ±18 V rails.

This is an evidence-consistency issue, not evidence of a circuit fault.

## Component/value-engineering disposition
OPA1656:
- RETAIN pending full noise/stability SPICE.
- No reason currently to substitute.

100 Ohm isolation resistors:
- 1% appears fully adequate for absolute value;
- no precision matching case identified;
- RETAIN provisionally as commodity-quality parts.

4.7 kOhm mono resistors:
- nominal 4.7 kOhm RETAIN;
- 0.1% absolute tolerance NOT YET JUSTIFIED;
- pair matching matters more than absolute tolerance;
- one-off hand selection is a strong candidate.

Local decoupling:
- functional requirement RETAIN;
- exact capacitor series/grade to be handled in whole-product supply-chain rationalisation.

Test points:
- RETAIN where needed for commissioning and verification.

No additional SCH104 functionality is required.

## Required SPICE evidence
1. Unity transfer / stability with actual OPA1656 model.
2. Full-chain headroom using reconciled severe input vectors.
3. Direct-path load and capacitive-load stability.
4. Mono equal-input gain.
5. Mono unequal-input weighting.
6. 4.7 kOhm absolute tolerance sensitivity.
7. 4.7 kOhm L/R mismatch sensitivity.
8. 4.7 kOhm thermal-noise contribution.
9. MONO_AVG dormant-node parasitic capacitance outside L+R.
10. Matrix BBM transition interaction.
11. Output isolation resistor tolerance and capacitive-load interaction.
12. Power-up/down and DC-offset interaction with adjacent stages.

## Intent/minimality disposition
RETAIN:
- OPA1656 unity buffers;
- 100 Ohm output isolation;
- two 4.7 kOhm mono branches before the 100 Ohm resistors;
- permanent left MONO_AVG leg;
- switched right MONO_R_LEG;
- local decoupling;
- commissioning test points.

REMOVE / REJECT:
- any SCH104 +6 dB gain;
- permanent L-R averaging bridge outside mono;
- fourth matrix pole solely to disconnect the dormant left branch without evidence;
- premium absolute tolerance on 4.7 kOhm solely by convention.

EVIDENCE REQUIRED:
- final 4.7 kOhm matching requirement;
- exact hand-selection strategy;
- dormant-node parasitic effect;
- reconciled severe-level headroom;
- full SPICE stability/noise/transient evidence.

## Gate status
SCH104 = ANALYSED.
Architecture is minimal and intent-conformant.
No obvious extraneous functionality remains.
The principal value-engineering question is 4.7 kOhm matching versus absolute tolerance.

Next logical review block: SCH105 mode matrix, using AE-041 A1 as authority and extending the analysis into switch parasitics, BBM transient behaviour, 2.2 MOhm return necessity and supply-chain implications.

## Confidence
- unity-buffer intent/implementation reconciliation: 99%
- absence of intentional L-R path outside mono: 99%
- mono loading calculation: 99%
- 4.7 kOhm matching more important than absolute tolerance: 98%
- 0.1% absolute tolerance can potentially be relaxed via hand matching: 95% pending SPICE/acceptance definition
- SCH104 ready to stop at ANALYSED pending SPICE: 99%
