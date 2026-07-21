# Project Shellac — AE-005 SCH107 Rumble Filter

**Revision:** A  
**Status:** electrically closed  
**Date:** 14 July 2026

## 1. Decision

SCH107 shall use a **fourth-order Butterworth high-pass filter** with a nominal
15 Hz -3 dB frequency.

A second-order filter was rejected because obtaining useful attenuation at
5–10 Hz would require materially greater loss in the wanted 20–30 Hz region.

The chosen fourth-order response provides approximately:

| Frequency | Response |
|---:|---:|
| 0.55 Hz | -115 dB |
| 1 Hz | -94 dB |
| 5 Hz | -38.2 dB |
| 10 Hz | -14.3 dB |
| 15 Hz | -3.06 dB |
| 20 Hz | -0.46 dB |
| 30 Hz | -0.04 dB |
| 50 Hz | -0.01 dB |

This gives strong rejection of warp, bearing and structural energy while
preserving wanted bass.

## 2. Topology

Each channel uses two cascaded unity-gain Sallen-Key high-pass sections.

For C1 = C2 = C:

\[
f_0=\frac{1}{2\pi C\sqrt{R_1R_2}}
\]

\[
Q=\frac{1}{2}\sqrt{\frac{R_2}{R_1}}
\]

The Butterworth section Q values are 0.541196 and 1.306563.

## 3. Frozen values

All capacitors are 470 nF film.

| Section | R1 | R2 | Realised f0 | Realised Q |
|---|---:|---:|---:|---:|
| A | 20.8 kΩ | 24.3 kΩ | approximately 15.1 Hz | approximately 0.540 |
| B | 8.66 kΩ | 59.0 kΩ | approximately 15.0 Hz | approximately 1.305 |

Use 0.1% metal-film resistors where practical. Match left/right capacitor sets
to 1% or better.

## 4. Amplifier

OPA1656 is selected because it:

- is specified for ±18 V operation;
- is unity-gain stable;
- has FET inputs and negligible bias-current loading;
- provides low noise and distortion;
- is available as a dual SOIC-8 device.

One dual OPA1656 is used per channel, allowing compact local feedback loops and
straightforward supply decoupling.

## 5. Bypass

A linked stereo **2P2T break-before-make** switch selects either:

- the direct SCH103 output; or
- the SCH107 filtered output.

The filter input remains connected and driven in both positions. This avoids
floating filter nodes and reduces switching transients.

The switch is an operating control, not a gain or equalisation control.

## 6. Signal-chain order

The electrically approved order is:

```text
SCH101 -> SCH103 -> SCH107 -> SCH104 -> SCH105 -> SCH108
```

This removes infrasonic energy before the final 6 dB gain and before mode
routing.

## 7. Decoupling and layout

Per dual OPA1656:

- 100 nF from +18 V to 0VA;
- 100 nF from -18 V to 0VA;
- 10 µF local bulk capacitor on each rail.

The 100 nF parts shall be placed at the IC supply pins. Keep each Sallen-Key
feedback loop compact and route left/right channels symmetrically.

## 8. Verification

Bench acceptance:

- bypass response flat within measurement uncertainty;
- filtered response approximately -3 dB at 15 Hz;
- attenuation at 10 Hz at least 13.5 dB;
- attenuation at 5 Hz at least 36 dB;
- passband loss at 30 Hz below 0.1 dB;
- no oscillation or material channel mismatch;
- DC output near zero in both bypass and filtered modes.
