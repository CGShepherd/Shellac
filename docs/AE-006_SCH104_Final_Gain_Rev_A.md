# SUPERSEDED BY AE-008

AE-008 selected THAT1646, whose fixed +6 dB differential gain requires SCH104 to operate at unity. The original AE-006 2× design is retained below for traceability only.

# Project Shellac — AE-006 SCH104 Final Gain and Buffer

**Revision:** A  
**Status:** electrically closed  
**Date:** 14 July 2026

## Decision

SCH104 is a stereo fixed-gain non-inverting OPA1656 stage placed after SCH107.
One dual OPA1656 serves both channels.

| Item | Value |
|---|---:|
| RG | 10.0 kΩ, 0.1% |
| RF | 10.0 kΩ, 0.1% |
| Gain | 2.000× |
| Gain | 6.021 dB |
| Output isolation | 100 Ω |
| Rails | ±18 V |

The equal resistor pair is preferred over a nominally exact but more awkward
6.00 dB combination. The 0.021 dB difference is immaterial.

## Level budget

The nominal SCH104 input is approximately 0.321 V RMS and produces 0.642 V RMS.
A deliberately severe 3.21 V RMS input produces 6.42 V RMS (9.08 V peak).
Against the conservative 10 V RMS internal design ceiling this retains more
than 3.8 dB margin.

## Noise and loading

The OPA1656 FET input places negligible load on SCH107. Ten-kilohm feedback
resistors balance thermal noise, current demand and PCB practicality. The
100-ohm output resistor isolates the op amp from wiring and downstream
capacitance without materially changing gain into the high-impedance mode
matrix.

## Decoupling

At the dual OPA1656 package provide 100 nF and 10 µF from each rail to 0VA.
The 100 nF components shall be placed at the supply pins.

## Verification

- gain 2.000× ± resistor tolerance;
- channel gain mismatch below 0.05 dB;
- nominal output approximately 0.642 V RMS for 0.321 V RMS input;
- clean output at 6.42 V RMS;
- no oscillation into the following mode matrix;
- DC offset recorded at both outputs.
