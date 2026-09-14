# AE-042 — SCH101 Pre-SPICE Interim Design Authority
**Project:** Shellac
**Status:** INTERIM / ANALYSED / SPICE REQUIRED
**Date:** 2026-09-11

## Purpose
Capture the current SCH101 design conclusions before moving to SCH103. This document is intentionally interim: no item below is BASELINED until the required SPICE, review and bench-verification gates are completed.

## Governing design intent
SCH101 is the balanced cartridge input stage. It shall support the Grado 78E and Audio-Technica AT-VM95SP as co-equal primary 78-rpm qualification families, retain LP compatibility with the Grado Gold/8MZ case, preserve independent L/R generator outputs where electrically available, and require no PCB modification when changing between qualified cartridge families.

Affordable-performance rule: premium tolerance or component technology is justified only where analysis/simulation demonstrates material system benefit. Distinguish absolute-value accuracy from matching/ratio accuracy.

## Selected architecture
- OPA1656 low-noise balanced gain stage feeding LT5400-7 precision differential conversion.
- Fixed differential cartridge resistance: 47.4 kΩ (23.7 kΩ per leg arrangement), retained.
- Fixed symmetric RF/common-mode capacitors: 47 pF from each signal leg to chassis, retained.
- Existing vague 22 pF differential DNP provision to be removed/redefined as part of explicit cartridge-load programming.
- Input series resistance: 100 Ω per leg, retained pending mismatch/CMRR simulation.
- Three service gain settings retained: nominal 14 / 18 / 22 dB.
- Configuration is internal service programming, not a user top-panel control.
- Power shall be OFF before changing service configuration.

## Revised fail-safe gain programming
The historical precision-feedback solder-link bypass topology is to be replaced. The revised topology makes DEFAULT a complete working amplifier without any programming shunt.

Per gain leg:
- Fixed RF = 999 Ω
- Fixed RG = 1.000 kΩ
- DEFAULT: no electrical programming branch; total gain ≈ 18.057 dB
- LOW: 332 Ω branch in parallel with RF; total gain ≈ 13.974 dB
- HIGH: 866 Ω branch in parallel with RG; total gain ≈ 22.015 dB

Failure behaviour:
- Missing/lost/open shunt returns the circuit to DEFAULT 18 dB.
- No open-feedback condition.
- No unintended fourth normal gain state.
- Simultaneous LOW+HIGH population is invalid but shall remain electrically benign.

The previous 0 Ω solder-link bypass implementation and ordinary DIP-switch concepts are superseded.

## Gain service hardware
Preferred concept:
- One ganged four-position gold-contact shunt for all four gain legs.
- Candidate shunt: Samtec MNT-104-BK-G.
- Candidate LOW/HIGH/PARK headers: Samtec TSW-104-07-G-D.
- PARK is mechanically useful but electrically inert.
- Only one programming shunt is intended to be supplied.

Before manufacturing release, verify the actual production MNT-104 internal pairings/orientation by drawing review and continuity test.

## Cartridge capacitance programming
Do not switch the fixed 47 pF signal-to-chassis RF capacitors.

Add explicit matched differential C0G/NP0 loading across L+/L− and R+/R−:
- BASE: +0 pF
- +47 pF
- +100 pF

Provisional service hardware:
- Samtec MNT-102-BK-G ganged L/R shunt.
- Samtec TSW-102-07-G-D headers for +47 pF, PARK/BASE and +100 pF.
- No shunt = BASE.
- PARK electrically inert.
- Simultaneous +47 pF and +100 pF is invalid but benign (+147 pF).

These capacitance values remain provisional until cartridge/cable SPICE sweeps confirm the useful loading envelope.

## Cartridge qualification cases
Primary:
1. Grado 78E — model centred approximately on 475 Ω / 45 mH.
2. Audio-Technica AT-VM95SP — model centred approximately on 485 Ω / 550 mH.

Compatibility:
3. Grado Gold / 8MZ — approximately 660 Ω / 50 mH.

The live model's GRADO_78C naming should ultimately be updated to GRADO_78E and the AT-VM95SP model added. Exact terminal/body isolation of the physical Grado 78E and AT-VM95SP remains a bench-verification item.

## PCB/environmental decisions
- PCB finish: ENIG.
- Standard solder mask.
- No conformal coating.
- No selective hard gold required on PCB pads because the mechanical mating interface is gold header to gold shunt.
- Controlled indoor operating environment.

## Cost/value-engineering conclusions
Do not freeze premium discrete-resistor tolerances before SPICE.
The SPICE sensitivity work shall distinguish:
1. absolute-value requirement,
2. ratio/matching requirement,
3. TCR/tracking requirement,
4. components for which ordinary tolerance is adequate.

Potential production strategy for critical discrete resistors: buy economical low-TCR thin-film parts in quantity and hand-select matched quartets if simulation demonstrates matching is the governing requirement. Avoid dependence on widespread hand selection; use it only at high-leverage locations.

LT5400-7A remains selected pending simulation evidence. Its grade/cost shall be challenged after CMRR sensitivity results exist rather than changed speculatively.

Cost optimisation is deferred until complete SPICE sensitivity evidence. Final procurement shall optimise the whole-product supplier basket including shipping, minimum-order quantities, PCB manufacture, enclosure machining, wiring/harness work, assembly, test/commissioning and other manufacturing costs.

Maintain two future cost views:
- replication cost: complete cost to manufacture another Shellac from nothing;
- owner-build cash cost: incremental cost after crediting suitable parts already owned.

## Required SCH101 SPICE evidence
1. AC transfer for all gain and cartridge-load states.
2. Grado 78E, AT-VM95SP and Grado Gold/8MZ source models.
3. Cable/input capacitance sweep over the qualified envelope.
4. Gain accuracy.
5. Noise.
6. Headroom, clipping and overload recovery on ±18 V rails.
7. DC operating points and offsets.
8. Frequency-dependent CMRR.
9. 100 Ω input-resistor mismatch.
10. Gain-network absolute tolerance versus inter-leg ratio mismatch.
11. Gain-program resistor tolerance/TCR and shunt-contact mismatch.
12. Capacitor mismatch and PCB/parasitic asymmetry.
13. Thermal-gradient stress.
14. Determine the maximum economical component tolerances that still meet the block requirements.

Provisional CMRR acceptance target carried into simulation:
- ≥70 dB, 20 Hz–1 kHz
- ≥60 dB at 20 kHz
These remain subject to formal confirmation before baseline.

## Intent/minimality disposition
RETAIN:
- balanced cartridge interface
- OPA1656 gain architecture
- LT5400-7 differential conversion
- fixed 47.4 kΩ loading
- fixed 47 pF leg-to-chassis RF capacitors
- 100 Ω input series resistors, pending verification
- 14/18/22 dB gain intent

MODIFY:
- solder-link gain programming -> fail-safe gold ganged service programming
- vague differential capacitance provision -> explicit BASE/+47/+100 pF service loading
- cartridge model set -> Grado 78E + AT-VM95SP primary, Gold/8MZ compatibility

REMOVE / REJECT:
- ordinary DIP gain switching
- precision zero-ohm bypass contact in the gain ratio
- switchable resistive cartridge loading
- hot-change requirement
- conformal coating
- any extra SCH101 function without controlled requirement

EVIDENCE REQUIRED:
- complete SPICE package above
- exact shunt pairing/orientation
- physical cartridge terminal/body isolation
- production resistor tolerance/grade
- final cartridge capacitance values
- LT5400 grade/value-for-money decision

## Gate status
SCH101 = ANALYSED.
Architecture is locked for pre-SPICE purposes.
Next gate = SIMULATED.
No manufacturing release and no baseline claim is authorised by this interim record.

## Confidence
- Gain architecture / fail-safe default: 99%
- Ganged gold service-programming concept: 98%
- Fixed 47.4 kΩ load: 99%
- BASE/+47/+100 pF loading set: 96% pending SPICE
- Overall SCH101 architecture ready for simulation: 98%
