# Project Shellac — AE-004 SCH103 Electrical Closure

**Revision:** A  
**Status:** electrically closed; pin-level KiCad rendering remains a renderer task  
**Date:** 14 July 2026

## 1. Frozen circuit architecture

Each channel contains:

1. OPA1612 active low-frequency pole-zero stage;
2. linked five-position complete bass branch selector;
3. passive 750-ohm switched treble network;
4. OPA1612 non-inverting recovery stage;
5. local dual-rail decoupling and four signal test points.

The active stage retains 100 kΩ RF and 2.70 kΩ RG. Each bass position
selects its own RS and aggregate capacitance, as approved by AE-003.

## 2. Recovery stage

The fixed recovery stage uses:

| Item | Value |
|---|---:|
| RG | 10.0 kΩ, 0.1% |
| RF | 11.0 kΩ, 0.1% |
| Gain | 2.100× |
| Gain in dB | 6.444 dB |

The small gain error against an abstract 6 dB target is immaterial and avoids
special resistor values.

## 3. Conservative headroom rule

A **10 V RMS** internal output ceiling is used as a conservative design limit.
This is deliberately below rail-limited theoretical swing and is not an
absolute-maximum claim.

With the default SCH101 gain of 7.94×, the first active EQ stage is the
low-frequency overload constraint. The worst calculated flat-amplitude test
limit is greater than **30 mV RMS at the cartridge input**, versus the 5 mV
nominal reference. This provides more than 15 dB nominal-input margin.

The calculation is intentionally severe because real recorded spectra do not
normally present equal high amplitude at 20 Hz and 1 kHz. Warp and structural
energy remain the practical low-frequency concern, supporting placement of the
rumble filter before the final 6 dB system gain.

## 4. Noise and impedance

The 100 kΩ feedback resistor has the largest individual Johnson-noise density,
approximately 40.7 nV/√Hz at 300 K. It is retained because it is intrinsic to
the validated P06/P91 topology and because SCH101 provides approximately 18 dB
of low-noise gain ahead of SCH103.

The recovery resistors are held at 10–11 kΩ rather than higher values to limit
thermal noise and bias-current error. The passive treble resistor remains
750 Ω.

Bench noise measurement remains mandatory because complete integrated noise
depends on frequency-dependent noise gain, op-amp current noise, source
impedance, switch wiring and PCB parasitics.

## 5. Stability and decoupling

For each dual OPA1612 package:

- 100 nF local capacitor from +18 V to 0VA;
- 100 nF local capacitor from −18 V to 0VA;
- 10 µF local bulk capacitor from +18 V to 0VA;
- 10 µF local bulk capacitor from −18 V to 0VA.

The 100 nF parts shall be placed immediately adjacent to the supply pins with
short return paths. The 10 µF capacitors shall be nearby but need not displace
the HF parts.

Switch wiring and high-impedance feedback nodes shall be kept extremely short.

## 6. Test points

Per channel:

- EQ input;
- active LF-stage output;
- passive HF-network output;
- final SCH103 output.

Rail and ground test points are already provided by SCH106.

## 7. CAD limitation

The present KiCad writer places functional blocks but does not expose symbol
pin coordinates. AE-004 therefore renders every approved component and value,
but retains the OPA1612 stages as functional symbols rather than inventing
pin-level wiring.

This is a renderer limitation, not an unresolved analogue-design issue.
