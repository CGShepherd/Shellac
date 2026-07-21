# Project Shellac — AE-002 Transfer Function Engine

**Revision:** A  
**Status:** validated  
**Date:** 14 July 2026

## Purpose

AE-002 corrects the superseded simple-RC treatment of the P06/P91 active bass
network. The implemented topology is:

```text
ZF = RF || (RS + 1/sC)
A(s) = 1 + ZF/RG
```

The exact pole and zero are calculated from the complete non-inverting
feedback network. The former 14.3 kΩ fixed-resistor model is withdrawn.

## Reconstructed published network

| P91 selection | RF | RS | RG | C | Pole | Zero |
|---|---:|---:|---:|---:|---:|---:|
| 200 Hz | 100 kΩ | 10 kΩ | 2.7 kΩ | 56 nF | 25.837 Hz | 225.041 Hz |
| 400 Hz | 100 kΩ | 10 kΩ | 2.7 kΩ | 27 nF | 53.588 Hz | 466.753 Hz |
| 500 Hz historical 78 | 100 kΩ | 10 kΩ | 2.7 kΩ | 22 nF | 65.767 Hz | 572.833 Hz |

The P91 position names are practical historical replay categories, not exact
single-RC break frequencies.

## True-RIAA active branch

The exact solution for 50.05 Hz and 500.5 Hz with RF=100 kΩ and RG=2.7 kΩ is:

- RS = approximately 8.190 kΩ;
- C = approximately 29.392 nF.

Selected preferred implementation:

- RS = 8.20 kΩ, 0.1%;
- C = 27 nF + 2.4 nF, matched aggregate;
- passive treble branch = 750 Ω + 100 nF.

The true-RIAA branch is dedicated. The original 22 nF P91 position remains a
historical 78 setting and is not described as accurate LP/RIAA playback.

## Engine capability

`generator/model/replay_eq_transfer.py` provides:

- exact complex transfer function;
- pole, zero, DC gain, HF gain and shelf magnitude;
- magnitude and phase at arbitrary frequencies;
- exact RS/C solution for a requested pole-zero pair;
- logarithmic frequency grids for later error analysis and plotting.

## Scope boundary

AE-002 validates the network mathematics and true-RIAA branch. It does not yet
claim that the historical 78 networks are optimised replacements for the P91
source values. Full replay-curve error optimisation, gain allocation and
low-frequency overload closure remain on the SCH103 critical path.
