> **SUPERSEDED by AE-002 Rev A. Do not use the 14.3 kΩ bass-network values below.**

# Project Shellac — AE-001 Replay Equalisation Synthesis

**Revision:** A  
**Status:** switched frequency-setting networks approved; complete SCH103 not yet frozen  
**Date:** 14 July 2026

## 1. Purpose

This report replaces the provisional copying of ESP Project 91 capacitor
values with independently calculated Project Shellac networks.

The calculation uses:

\[
f = \frac{1}{2\pi RC}
\]

The Project 91 table remains the source for the selected replay break
frequencies. Project 06 provides the underlying active-bass/passive-treble
architecture and the updated 750 ohm / 100 nF RIAA treble network.

## 2. Design decisions

### Bass network

A fixed **14.3 kΩ, 0.1% metal-film resistor** is used for the switched bass
capacitors. It provides close realisation of 200, 400 and 500 Hz using common
main capacitor values and inexpensive C0G trim capacitors.

### Treble network

A fixed **750 Ω, 0.1% metal-film resistor** is retained from the updated
Project 06 recommendation. All treble selections are recalculated around that
resistor instead of retaining the older Project 91 capacitor table unchanged.

## 3. Approved network values

| Section | Selection | Fixed R | Capacitor implementation | Total C | Realised | Error |
|---|---:|---:|---:|---:|---:|---:|
| Bass | Flat | — | Switch short | — | — | — |
| Bass | 200 Hz | 14.3 kΩ | 56 nF | 56.00 nF | 198.745 Hz | −0.628% |
| Bass | 400 Hz | 14.3 kΩ | 27 nF + 820 pF | 27.82 nF | 400.062 Hz | +0.015% |
| Bass | 500 Hz RIAA | 14.3 kΩ | 22 nF + 270 pF | 22.27 nF | 499.763 Hz | −0.047% |
| Treble | Flat | — | Switch open | — | — | — |
| Treble | 1,600 Hz | 750 Ω | 120 nF + 12 nF | 132.00 nF | 1,607.626 Hz | +0.477% |
| Treble | 2,121 Hz RIAA | 750 Ω | 100 nF | 100.00 nF | 2,122.066 Hz | +0.050% |
| Treble | 3,400 Hz | 750 Ω | 56 nF + 6.2 nF | 62.20 nF | 3,411.682 Hz | +0.344% |
| Treble | 5,800 Hz | 750 Ω | 33 nF + 3.6 nF | 36.60 nF | 5,797.994 Hz | −0.035% |

The worst break-frequency error is **0.628%**.

This is materially tighter than simply reusing the Project 91 source
capacitors with a changed resistor baseline, while requiring no exotic
values.

## 4. Component implementation

- Fixed resistors: 0.1% metal film, 1206 preferred.
- Main capacitors: film or C0G/NP0, selected for low loss and stability.
- Trim capacitors: C0G/NP0.
- Left/right aggregate capacitance should be matched to 0.5% or better.
- Parallel components shall be placed adjacent to one another and to the
  switch/core node.
- Rotary-switch wiring shall remain extremely short, as required by P91.

The use of two parallel capacitors is deliberate. It gives better accuracy
with readily available values and allows channel matching without purchasing
special-value capacitors.

## 5. Replay coverage

The approved switch positions cover the practical groupings identified in
Project 91:

- flat/acoustic;
- bass turnover at 200, 400 and 500 Hz;
- treble flat, 1,600, 2,121, 3,400 and 5,800 Hz.

The controls remain independently selectable, allowing the operator to choose
the closest documented characteristic and then optimise by listening where
recording practice departed from nominal standards.

## 6. Items not yet approved

This report does **not** freeze:

1. SCH103 active-stage gain;
2. complete signal-chain gain allocation;
3. overload margin;
4. noise contribution;
5. the circuit topology and values for the bypassable 50.05 Hz / 3180 µs
   RIAA bass-flattening pole;
6. the final post-EQ gain setting.

Those items form AE-001B. They must be reconciled with the approximately
17–18 dB THAT1512 input-stage gain before the detailed LM4562 core is generated.

## 7. External references

- ESP Project 91, *Multi Standard 78 RPM and RIAA Phono Equaliser*:
  `https://sound-au.com/project91.htm`
- ESP Project 06, *Hi-Fi Phono Preamp (RIAA Equalisation)*:
  `https://sound-au.com/project06.htm`

Accessed 14 July 2026. The source material is used for this personal
construction project under the conditions stated by its author.
