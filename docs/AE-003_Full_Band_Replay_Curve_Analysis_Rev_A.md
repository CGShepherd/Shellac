# Project Shellac — AE-003 Full-Band Replay-Curve Analysis

**Revision:** A  
**Status:** calculation baseline  
**Date:** 14 July 2026

## Purpose

AE-003 evaluates the complete active-bass and passive-treble response from
20 Hz to 20 kHz. Every response is normalised at 1 kHz, so the reported error
is equalisation-shape error rather than absolute gain error.

The analysis has two distinct purposes:

1. verify the dedicated true-RIAA branch against the 3180/318/75 us target;
2. quantify how the practical P91 switch positions approximate nominal 78 rpm
   curve families.

## Source interpretation

ESP Project 91 states that four bass ranges and five treble ranges are enough
to cover most historical records within roughly 2 dB, and explicitly warns
that the historical standards and actual cutting practice were inconsistent.
Consequently, the historical results are operating guidance, not archival
claims about every pressing.

The historical target families use the nominal P91 assumptions:

- lower bass break: 20 Hz;
- upper bass turnover: 200, 400 or 500 Hz;
- treble pole: flat, 1600, 3400 or 5800 Hz.

The LP target is exact standard RIAA:

- 50.05 Hz;
- 500.5 Hz;
- 2121 Hz.

## Output

Run:

```cmd
python scripts\report_replay_curve_analysis.py
```

The script prints the full-band error summary and writes:

```text
out\replay_curve_analysis.csv
```

The report includes worst-case error, frequency of worst error, RMS error, and
spot errors at 20 Hz, 50 Hz, 100 Hz, 1 kHz, 10 kHz and 20 kHz.

## Switch-matrix policy

- True RIAA is a dedicated active bass branch paired with the 2121 Hz treble
  selection.
- The original 22 nF / 500 Hz P91 branch remains labelled `500 Hz 78`; it is
  not presented as LP/RIAA.
- Historical controls remain independently selectable because the documented
  curves and real records are too variable to justify mechanical interlocking.
- The operator guide provides label-based starting points, followed by
  adjustment by ear where necessary.

## Design boundary

AE-003 does not yet freeze the entire SCH103 schematic. Its results feed the
final switch matrix, gain/headroom closure and detailed OPA1612 implementation.

## Optimised active bass branches

Full-band analysis of the original capacitor-only P91 branches showed that the
400 Hz and 500 Hz selections moved the lower pole upward as well as changing
the upper turnover. Shellac therefore switches the complete series resistor
and capacitor branch:

| Position | Series resistor | Capacitor aggregate | Realised pole | Realised zero |
|---|---:|---:|---:|---:|
| 200 Hz | 8.20 kΩ | 68 nF + 5.6 nF | 19.986 Hz | 199.689 Hz |
| 400 Hz | 2.49 kΩ | 68 nF + 9.1 nF + 560 pF | 19.996 Hz | 400.347 Hz |
| 500 Hz 78 | 1.43 kΩ | 68 nF + 10 nF + 470 pF | 19.996 Hz | 499.684 Hz |
| True RIAA | 8.20 kΩ | 27 nF + 2.4 nF | 50.032 Hz | 499.901 Hz |

This changes the bass control from four capacitor-only positions to five
complete branches: flat, 200 Hz, 400 Hz, 500 Hz historical 78, and true RIAA.
A stereo implementation therefore requires a mechanically linked 2-pole,
5-position selector, one pole per channel.
