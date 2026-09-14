# AE-043 — SCH103 Pre-SPICE Interim Analysis
**Project:** Shellac
**Status:** INTERIM / ANALYSED IN PROGRESS / SPICE REQUIRED
**Date:** 2026-09-11

## Purpose
Capture the current SCH103 replay-equalisation review before detailed SPICE and BOM value engineering. This is an interim evidence record, not a baseline or manufacturing release.

## Governing intent
SCH103 provides independently selectable bass and treble replay equalisation for historical 78 rpm records plus complete RIAA LP replay.

The controls are intentionally independent. The 5 x 5 matrix therefore exposes 25 electrical combinations. Only a subset corresponds to named historical starting points or the exact RIAA configuration; the remaining combinations are legitimate user-adjustment states, not unintended functionality.

## Architecture reconciliation
The live implementation and DR-037 agree:
- complete RIAA is implemented wholly within SCH103;
- RIAA bass selection = TRUE RIAA 3180/318 us;
- RIAA treble selection = 2121 Hz / 75 us;
- no downstream independent 3180 us stage;
- no independent 3180 ON/BYPASS switch.

Current signal structure per channel:
1. OPA1612 non-inverting active LF EQ stage.
2. Fixed RF = 100 kΩ and RG = 2.70 kΩ.
3. Bass selector chooses FLAT or one complete RS+C branch.
4. Fixed 750 Ω passive treble resistor.
5. Treble selector chooses FLAT or one shunt capacitor network.
6. OPA1612 non-inverting recovery stage, gain 2.1 x.
7. DR-039 1 uF PET film DC blocking capacitor.
8. 330 kΩ downstream DC reference.
9. Output to SCH107.

## Realised bass values
| Position | Function | RS | Aggregate C | Realised pole | Realised zero |
|---|---|---:|---:|---:|---:|
| 1 | FLAT | — | — | — | — |
| 2 | 200 Hz | 8.20 kΩ | 73.6 nF | 19.986 Hz | 199.689 Hz |
| 3 | 400 Hz | 2.49 kΩ | 77.66 nF | 19.996 Hz | 400.347 Hz |
| 4 | 500 Hz 78 | 1.43 kΩ | 78.47 nF | 19.996 Hz | 499.684 Hz |
| 5 | TRUE RIAA | 8.20 kΩ | 29.4 nF | 50.032 Hz | 499.901 Hz |

Physical capacitor synthesis currently used:
- 200 Hz: 68 nF + 5.6 nF
- 400 Hz: 68 nF + 9.1 nF + 560 pF
- 500 Hz: 68 nF + 10 nF + 470 pF
- RIAA: 27 nF + 2.4 nF

## Realised treble values
Fixed R = 750 Ω.

| Position | Function | Aggregate C | Realised pole |
|---|---|---:|---:|
| 1 | FLAT | — | — |
| 2 | 1600 Hz | 132 nF | 1607.63 Hz |
| 3 | 2121 Hz RIAA | 100 nF | 2122.07 Hz |
| 4 | 3400 Hz | 62.2 nF | 3411.68 Hz |
| 5 | 5800 Hz | 36.6 nF | 5797.99 Hz |

Physical capacitor synthesis currently used:
- 1600 Hz: 120 nF + 12 nF
- 2121 Hz: 100 nF
- 3400 Hz: 56 nF + 6.2 nF
- 5800 Hz: 33 nF + 3.6 nF

## Nominal curve accuracy
The existing generated replay-curve analysis reports extremely small nominal shape errors after 1 kHz normalisation:
- historical target combinations: worst cases approximately 0.004 to 0.031 dB;
- true RIAA: approximately 0.008 dB worst case.

This is substantially tighter than the inherent uncertainty in historical 78 equalisation practice. Therefore nominal synthesis accuracy alone is not sufficient justification for the present component count or tolerance grades.

## Preliminary value-engineering observation
The present implementation uses multiple parallel C0G/NP0 capacitors to synthesise several timing values very closely.

Preliminary analytical substitutions demonstrate the likely scale of the trade:
- 200 Hz branch: replacing 73.6 nF with 75 nF gives about 0.14 dB worst normalised shape error versus the nominal 20/200 target.
- 400 Hz branch: replacing 77.66 nF with 78 nF gives about 0.023 dB.
- 500 Hz branch: replacing 78.47 nF with 78 nF gives about 0.034 dB.
- RIAA branch: replacing 29.4 nF with 30 nF gives about 0.12 dB versus the 50.05/500.5 Hz target.

These are analytical sensitivity examples only, not component substitutions selected for implementation. Availability, dielectric, voltage coefficient, tolerance, temperature coefficient, channel matching and complete-chain SPICE must be considered before changing values.

## Tolerance hypothesis to test
Do not assume all current 0.1% resistors or compound capacitor networks are necessary.

For each timing network SPICE shall separate:
1. absolute curve accuracy;
2. left/right channel matching;
3. resistor-ratio sensitivity;
4. capacitor absolute tolerance;
5. capacitor channel matching;
6. temperature drift/tracking;
7. switch/contact resistance sensitivity.

Historical 78 positions may justify looser absolute accuracy than RIAA because the source standards and actual mastering practice are intrinsically variable. RIAA should retain a separately defined tighter objective.

The affordable-performance objective is to use the least expensive component grade and minimum component count that demonstrably satisfy the respective historical and RIAA requirements.

## 25-state control matrix
The five Bass positions and five Treble positions yield 25 selectable combinations.

This is intentional. AE-003 explicitly rejects mechanical interlocking because documented historical curves and actual records are too variable. The named label recommendations are starting points, followed by adjustment where appropriate.

Therefore:
- independent Bass/Treble selection = RETAIN;
- non-named combinations = RETAIN as intentional adjustment range;
- do not remove states merely because they lack a named curve target.

## Control-authority conflict requiring reconciliation
The live SCH103 schematic represents separate per-channel 1P5 selector blocks.

AE-040B (2026-09-04) still records an older authority:
- linked-stereo 2P5 Bass and Treble;
- Lorlin PT preferred;
- Grayhill rejected.

Subsequent design discussion selected a dual-mono control approach using four independent rotary controls and NKK NR01-family hardware. This later decision is not yet reconciled into the controlled Dropbox authority.

Disposition:
- electrical 5-position requirement: RETAIN;
- exact mechanical selector architecture/MPN: EVIDENCE / CONTROL-AUTHORITY RECONCILIATION REQUIRED;
- do not manufacture from AE-040B rotary data until reconciled.

## Recovery and DC block
Current recovery stage:
- RG = 10 kΩ
- RF = 11 kΩ
- gain = 2.1 x / 6.444 dB.

DR-039 DC block:
- 1 uF PET film series capacitor;
- 330 kΩ downstream return;
- nominal high-pass corner about 0.482 Hz.

These are retained pending full headroom/noise/DC/transient SPICE.

## Required SCH103 SPICE evidence
1. All 25 Bass x Treble states, 20 Hz–20 kHz minimum.
2. Complete RIAA state against canonical 3180/318/75 us response.
3. Historical named states against nominal target families.
4. Absolute gain and headroom at each active internal node.
5. Overload/clipping and recovery under cartridge stress vectors.
6. OPA1612 noise contribution including high LF noise gain.
7. DC offset and DR-039 transient settling.
8. Resistor tolerance sensitivity.
9. Capacitor tolerance sensitivity.
10. L/R mismatch sensitivity.
11. Timing-part TCR/temperature sensitivity.
12. Switch/contact resistance sensitivity.
13. Simplified capacitor-value alternatives to determine whether compound networks materially improve audible/measurement performance.
14. Determine separate economical tolerance requirements for historical positions and RIAA.
15. Derive production BOM grades only after the above evidence.

## Intent/minimality disposition
RETAIN:
- active LF P06/P91-derived topology
- independent 5-position Bass and 5-position Treble controls
- TRUE-RIAA bass branch
- 2121 Hz RIAA treble position
- fixed 750 Ω treble resistor
- OPA1612 active devices
- 2.1 x recovery stage
- DR-039 post-EQ DC block
- test points required for commissioning

REMOVE / REJECT:
- any independent downstream 3180 us stage
- any 3180-only bypass switch
- mechanical interlock between Bass and Treble solely to enforce named curves
- stale Grayhill procurement authority

EVIDENCE REQUIRED:
- whether all 0.1% resistors are necessary
- whether every parallel capacitor combination is necessary
- final historical-curve tolerance objective
- final RIAA tolerance objective
- final dual-mono selector MPN/footprint/control authority
- full SPICE headroom/noise/DC/transient evidence

## Gate status
SCH103 = ANALYSED IN PROGRESS.
Topology and curve synthesis are analytically coherent.
Nominal curve accuracy is substantially tighter than the historical source uncertainty.
Next gate = complete tolerance/headroom/noise SPICE plus control-authority reconciliation.
No manufacturing release and no baseline claim is authorised by this interim record.

## Confidence
- DR-037 architecture reconciliation: 99%
- nominal transfer-function reconstruction: 99%
- 25-state independence is intentional: 99%
- evidence that some component precision/count deserves value-engineering challenge: 97%
- any actual BOM simplification before SPICE: not yet authorised
