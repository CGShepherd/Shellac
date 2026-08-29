# AE-013 — SCH101 Noise and CMRR Design-Assurance Review

**Revision:** A0  
**Status:** REVIEW COMPLETE — design optimisation required before formal SCH101 precision closure  
**Date:** 29 August 2026  
**Base commit:** `b7f3385bf85335c30c839989b72a72c03f20957e`

## 1. Why this review was performed

AE-012 closed the end-to-end gain/headroom envelope. The next assurance step was integrated noise and common-mode rejection.

Because SCH101 dominates both quantities, this review first tests whether the existing front-end resistor policy is sufficiently robust before propagating noise through the rest of the signal chain. Closing a complete noise budget around an implementation that is likely to change would create false precision.

## 2. Controlled current implementation

SCH101 currently uses:

- OPA1656-class matched non-inverting gain legs;
- 10 kΩ gain-to-ground resistor per leg;
- selectable total feedback resistance of 4.42 kΩ / 12.7 kΩ / 26.1 kΩ;
- four-resistor differential converter using 10 kΩ / 34.8 kΩ;
- 0.1% discrete resistor tolerance in the schematic;
- 100 Ω RF series resistor on each cartridge leg.

The differential-converter schematic note permits “0.1% or matched network”; the gain ladders are explicitly 0.1%.

Working cartridge source for the noise calculation is the Grado Prestige 78C: 475 Ω DC resistance, 45 mH inductance, nominal 5 mV output and 47 kΩ recommended load.

## 3. CMRR result

An exact ideal-op-amp corner enumeration was performed with all four gain-setting resistors and all four differential-converter resistors independently allowed to reach either end of their stated ±0.1% tolerance.

Worst-case CMRR:

| SCH101 gain | Worst-case CMRR, current 0.1% policy |
|---|---:|
| LOW | ~53.5 dB |
| DEFAULT | ~50.1 dB |
| HIGH | ~48.4 dB |

This is not sufficient evidence for a precision balanced cartridge receiver. It is particularly weak in HIGH gain because gain-ladder mismatch is amplified before differential conversion.

The problem is not OPA1656 intrinsic CMRR; it is resistor-ratio uncertainty.

### Candidate ratio policy

Repeating the same corner analysis at **0.01% ratio tracking** gives approximately:

| SCH101 gain | Worst-case CMRR, 0.01% ratio tracking |
|---|---:|
| LOW | >73 dB |
| DEFAULT | ~70.1 dB |
| HIGH | >68 dB |

These are deterministic resistor-mismatch figures and do not yet include PCB parasitics or RF-component asymmetry.

**Disposition: AMBER/RED until a matched-ratio implementation is selected.**

No previous explicit system CMRR requirement was found in the controlled baseline. A release acceptance value should therefore be created rather than retroactively claimed.

## 4. Front-end white-noise result

A first-order 300 K white-noise model includes:

- 475 Ω cartridge resistance;
- both 100 Ω RF series resistors;
- both OPA1656 gain-leg voltage-noise sources;
- gain-ladder Johnson noise;
- differential-converter OPA1656 voltage noise;
- Johnson noise of all four differential-converter resistors.

The model uses 4.3 nV/√Hz as a conservative OPA1656 1 kHz working value.

Current estimated input-referred density:

| SCH101 gain | Current input-referred white noise | Flat 20 Hz–20 kHz equivalent SNR at 5 mV |
|---|---:|---:|
| LOW | ~19.2 nV/√Hz | ~65.3 dB |
| DEFAULT | ~18.0 nV/√Hz | ~65.9 dB |
| HIGH | ~18.0 nV/√Hz | ~65.9 dB |

This is an electronics-only estimate and is not an assertion of practical 78-rpm replay SNR, which will normally be dominated by record/surface noise.

The important engineering result is the source breakdown: **the resistor networks contribute materially more noise than is necessary for an OPA1656 front end.**

## 5. Candidate impedance scaling

Scaling the SCH101 gain and differential-converter resistor networks to approximately one tenth of their current impedance while retaining the same ratios gives:

- gain Rg: 10 kΩ -> approximately 1 kΩ;
- feedback values scaled by the same factor;
- differential converter: 10 kΩ / 34.8 kΩ -> approximately 1 kΩ / 3.48 kΩ.

First-order DEFAULT input-referred white noise falls from approximately **18.0 nV/√Hz to 9.0 nV/√Hz**, an improvement of about **6 dB** in the flat 20 Hz–20 kHz equivalent SNR.

OPA1656 output-current capability is ample for these feedback-network currents; nevertheless component loading, switch contact resistance and exact preferred values must be checked before selection.

## 6. Combined design direction

The noise and CMRR results point to the same preferred action:

1. retain the SCH101 topology;
2. retain the 14/18/22 dB gain choices;
3. lower the resistor-network impedance substantially;
4. implement the gain and differential ratios with controlled **ratio matching/tracking**, not merely 0.1% independent absolute tolerance;
5. preserve matched geometry across L+, L-, R+ and R-;
6. then rerun the complete end-to-end noise and CMRR model.

A matched thin-film resistor network or networks are likely preferable to eight independent precision resistors, but component down-selection is deliberately not made in AE-013.

## 7. What is not being changed yet

AE-013 does **not** alter SCH101 component values or footprints.

This is intentional. The next action is component/topology implementation selection, including whether one or more resistor arrays can supply the required ratios and channel tracking without creating awkward DIP-switch or layout constraints.

## 8. Release disposition

- AE-012 gain/headroom: remains GREEN.
- SCH101 topology: GREEN.
- SCH101 gain values: GREEN.
- Current 0.1% independent resistor implementation for precision balance: **NOT CLOSED**.
- Current resistor impedance from a noise-optimisation perspective: **AMBER**.
- Candidate 10:1 impedance reduction + 0.01% ratio tracking: **PROMISING; requires component selection and verification**.

## 9. Next step

Perform SCH101 resistor-network down-selection and physical implementation review.

Once that implementation is selected, complete:

- exact CMRR including resistor network ratio specification and RF mismatch;
- frequency-dependent Grado source impedance;
- full end-to-end noise integration through SCH103/SCH107/SCH104/SCH105/SCH108;
- commissioning CMRR and noise acceptance tests.
