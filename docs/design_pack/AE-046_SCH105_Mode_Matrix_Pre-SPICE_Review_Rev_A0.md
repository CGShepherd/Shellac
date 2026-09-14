# AE-046 — SCH105 Mode Matrix Pre-SPICE Review
**Project:** Shellac
**Status:** INTERIM / ANALYSED / SPICE REQUIRED
**Date:** 2026-09-11

## Purpose
Capture the SCH105 review after AE-041 A1 and before full SPICE/BOM optimisation. This is an interim evidence record, not a baseline or manufacturing release.

## Governing intent
SCH105 shall provide four channel-routing modes: DUAL LEFT, STEREO, L+R MONO, and DUAL RIGHT. The selector shall be passive and BBM/non-shorting. Active circuitry after the switch shall provide unity buffering only. No additional gain or hidden summing function is permitted.

## Live implementation reconciliation
The live generator implements:
- one 3P4T mode selector;
- CCW->CW order DUAL L / STEREO / L+R / DUAL R;
- Pole A selects the left output source;
- Pole B selects the right output source;
- Pole C connects MONO_R_LEG to MONO_AVG only in L+R;
- two OPA1656 unity-gain output buffers;
- one 2.2 MOhm input return from each buffer input to 0VA;
- one 100 Ohm / 1% output-isolation resistor per buffer;
- local rail decoupling and test points.

No hidden active summing amplifier or gain stage remains.

## Truth table
| Mode | Left output source | Right output source | Pole C |
|---|---|---|---|
| DUAL L | BUFFERED_L | BUFFERED_L | OPEN |
| STEREO | BUFFERED_L | BUFFERED_R | OPEN |
| L+R | MONO_AVG | MONO_AVG | MONO_R_LEG -> MONO_AVG |
| DUAL R | BUFFERED_R | BUFFERED_R | OPEN |

This matches AE-041 A1.

## 2.2 MOhm input-return analysis
The two 2.2 MOhm returns serve two functions:
1. define each OPA1656 input during the BBM switch-open interval;
2. provide a DC reference without materially loading normal direct or mono paths.

### Direct path
With a 100 Ohm source-isolation resistor:
- gain = 2.2M / (2.2M + 100) = 0.9999545
- insertion error ≈ -0.000395 dB

### Mono path
The two 2.2 MOhm returns appear in parallel at MONO_AVG:
- effective load = 1.1 MOhm
- mono Thevenin source impedance = 4.7k || 4.7k = 2.35 kOhm
- equal-input mono gain = 0.997868
- error ≈ -0.01854 dB

### Alternative return values
Approximate equal-input mono insertion loss:
- 2.2 MOhm each: -0.0185 dB
- 1.0 MOhm each: -0.0407 dB
- 470 kOhm each: about -0.086 dB

Therefore reducing the returns materially below 2.2 MOhm buys little in normal operation while increasing mono loading. The present value is provisionally well judged.

## BBM/open-input behaviour
During the selector break interval, the 2.2 MOhm return prevents the OPA1656 non-inverting input from becoming truly floating.

The actual transient depends on:
- switch break duration;
- OPA1656 input capacitance;
- switch/PCB stray capacitance;
- charge on the previously selected source;
- source impedance of the next selected path;
- matrix-output buffer input model.

The operating rule remains:
MUTE -> MATRIX -> RUN

No additional pull-down or lower return resistor should be added merely by convention.

## Switch contact resistance
The preferred C&K A30403RNCB is a low-level gold-contact rotary switch. Contact resistance is negligible compared with 100 Ohm direct-path isolation, 4.7 kOhm mono resistors, and 2.2 MOhm input returns.

Contact resistance therefore is not expected to influence steady-state gain materially. It remains relevant for reliability, low-level integrity, channel consistency and manufacturing continuity verification.

## Switch parasitics
Off-state capacitance and inter-pole capacitance can create small AC feedthrough paths even when the 3P4T removes the intentional L-R resistive bridge.

SPICE shall sweep plausible parasitic ranges for:
- open-contact capacitance;
- adjacent-terminal capacitance;
- Pole-C coupling;
- PCB trace capacitance around MONO_AVG / MONO_R_LEG.

Acceptance should be based on resulting stereo crosstalk and high-frequency response, not on an arbitrary capacitance limit.

## Mono resistor matching
The 4.7 kOhm mono resistors belong electrically to the SCH104/SCH105 interface. Their ratio determines L/R weighting in mono far more strongly than their absolute value.

For a one-off hand-built unit:
- buy a modest quantity of low-TCR thin-film 4.7 kOhm resistors;
- select the closest pair using the new multimeter if its repeatability/resolution are adequate;
- record measured values;
- install symmetrically.

Premium absolute 0.1% parts are not automatically justified if an inexpensive selected pair meets the derived mismatch requirement.

## Output buffers
The two OPA1656 buffers:
- are unity gain;
- isolate the passive switch network from SCH108;
- drive the downstream mute/output-driver input network through 100 Ohm isolation;
- have no additional intended functionality.

Retain pending full stability/headroom/noise SPICE.

## Headroom
The live mode-matrix model uses a severe input of 6.42 Vrms and a 10 Vrms design ceiling, giving >3.8 dB margin.

This is a later and more conservative stress point than the older SCH104 3.21 Vrms case. Full-chain SPICE shall use one authoritative node-by-node stress vector and reconcile all older local models.

## Quantity-one supply-chain implications
For one hand-built Shellac:
- exact switch quantity-one availability matters more than bulk pricing;
- a stocked fallback is valuable even if the preferred C&K part has lead-time exposure;
- hand-selected resistors are economically credible;
- extra distributor baskets should be avoided unless they improve landed cost or supply risk;
- production-switch continuity testing should be performed before committing PCB/panel geometry.

Current preferred/fallback architecture remains:
- Preferred: C&K A30403RNCB
- Fallback: TE/Alcoswitch MRJE3404

The final procurement decision shall be revisited in the whole-product supply-chain pass after SPICE.

## Required SPICE evidence
1. All four routing modes.
2. Equal and unequal L/R signals.
3. Opposite-phase L/R signals.
4. Mono weighting versus resistor mismatch.
5. Mono insertion loss.
6. Direct-path insertion loss.
7. BBM open interval.
8. Switch transition with MUTE asserted.
9. Live switching as a stress case even if not an operating requirement.
10. OPA1656 input bias/capacitance effects with 2.2 MOhm returns.
11. Sweep return resistor value to confirm 2.2 MOhm optimum region.
12. Open-contact and inter-terminal capacitance sweeps.
13. Crosstalk outside mono.
14. Pole-C parasitic coupling.
15. Output-buffer stability and capacitive loading.
16. Noise contribution.
17. Power-up/down and DC transient interaction.

## Intent/minimality disposition
RETAIN:
- 3P4T passive matrix;
- DUAL L / STEREO / L+R / DUAL R order;
- Pole C mono-leg switching;
- 2.2 MOhm input returns provisionally;
- OPA1656 unity output buffers;
- 100 Ohm output isolation;
- MUTE -> MATRIX -> RUN operating rule;
- test points needed for commissioning.

REMOVE / REJECT:
- permanent L-R bridge outside mono;
- active summing amplifier;
- extra gain;
- additional switch poles without evidence;
- lower-value input returns without transient evidence;
- arbitrary pull-down components.

EVIDENCE REQUIRED:
- final 2.2 MOhm value confirmation;
- BBM transient magnitude;
- switch-parasitic crosstalk;
- final 4.7 kOhm matching requirement;
- production-switch continuity mapping;
- preferred versus fallback procurement choice.

## Gate status
SCH105 = ANALYSED.
Architecture is intent-conformant and functionally minimal.
No obvious extraneous functionality remains.
Next logical block: SCH108 balanced output and mute integration, including phantom-power fault protection and final output-interface stress analysis.

## Confidence
- truth-table reconciliation: 100%
- 2.2 MOhm returns are functionally justified: 98%
- 2.2 MOhm is near the correct value region: 95% pending transient SPICE
- contact resistance is negligible for steady-state gain: 99%
- switch parasitics remain a real but unquantified crosstalk item: 95%
- SCH105 ready to stop at ANALYSED pending SPICE: 99%
