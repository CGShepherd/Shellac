# AE-076A — +17 V / 0VA / -17 V Rail Authority Migration and Requalification — Rev A0

## Status

**CURRENT_REQUIREMENT_IMPLEMENTATION_REQUALIFICATION — PASS; routing remains held.**

Baseline: `d2f5c9f775b6080c66a9754a8355c7692cd4ba6a` (AE-075G).

## Purpose

Close CDR finding `SYS-01`: intended Shellac regulated audio rails are
**+17.0 V / 0VA / -17.0 V**, while live generator, current simulation contracts,
commissioning models and native PCB rail names had drifted to historical ±18 V.

AE-076A changes current authority and implementation atomically. Historical
±18 V design/assurance records are preserved and are not rewritten.

## Current product authority

- Positive rail: **+17.0 V**
- Analogue reference: **0VA**
- Negative rail: **-17.0 V**
- External/current rail identities: `+17VA_IN`, `-17VA_IN`, `+17V`, `-17V`.
- The existing 8.2 kOhm rail-LED resistors are retained. With the controlled
  2.4 V design forward-voltage assumption, nominal LED current is approximately
  **1.7805 mA**.
- `DATASHEET_MAX_OUTPUT_RMS_V = 18.0` in the THAT1646 engineering model is a
  device-performance datum, not the Shellac supply-rail authority, and is
  intentionally unchanged.

## Historical boundary

The following remain historical/provenance and are not edited to mimic the new
rail authority:

- AE-036 rail-margin audit;
- AE-049 numerical acceptance record;
- AE-058 RUN00 correction;
- AE-065 integrated ±18 V RUN00 evidence;
- AE-066 nominal campaign configuration/evidence;
- AE-069 SCH108 ±18 V output evidence;
- AE-073 PSU target-17 discriminator;
- AE-075G PRE90 evidence.

The AE-073 target-17 model result supports the decision but does not replace
powered PSU set-point, dropout, ripple, startup or thermal qualification.

## Fresh ±17 V evidence

Integrated RUN00:
- authority: `AE-076A`
- run id: `RUN00_INTEGRATED_17V`
- pass: **True**
- configured rails: +17.0 V /
  -17.0 V

SCH108 / PRE90 targeted rail requalification:
- worst absolute 2 kOhm insertion loss vs 100 kOhm:
  **0.209239 dB**
- minimum 3.21 Vrms / 10 kOhm margin to the 10 Vrms design ceiling:
  **3.9128 dB**
- maximum high-gain PRE90 output at 4.66 Vrms THAT1646 input:
  **9.071872 Vrms**
- maximum high-gain quasi-static compression fraction:
  **0.00000000**
- minimum margin to the published PRE90 9.3 Vrms @ 0 dB sensitivity:
  **0.2157 dB**

The targeted ±17 V electrical requalification passes. The PRE90 high-level
operating-state bench check remains mandatory.

## Gates deliberately retained

AE-076A does **not** close or waive:

- RUN06 prototype load/cable stability;
- RUN06 dynamic large-signal THD bench qualification;
- RUN08 overload/recovery;
- RUN10 tolerance/CMRR/parasitic qualification;
- RUN13 rail variation / external PSU behaviour;
- RUN14 phantom/fault-energy behaviour;
- powered PSU set-point/dropout/ripple/startup/thermal qualification;
- B03/B04/B08;
- manual placement reconciliation;
- final routing, layout freeze, BOM freeze or manufacturing release.

## CDR disposition

`SYS-01 PRE_LAYOUT_BLOCKING_TECHNICAL_DEBT` is **CLOSED by AE-076A** for
nominal rail authority/implementation consistency and targeted ±17 V
requalification.

The broader PRE-LAYOUT gate remains **HOLD** for the other independent CDR
findings.
