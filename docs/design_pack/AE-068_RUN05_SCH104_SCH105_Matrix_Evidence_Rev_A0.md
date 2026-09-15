# AE-068 — RUN05 SCH104/SCH105 Matrix Evidence — Rev A0

**Project:** Shellac
**Status:** REVIEWED / STEADY-STATE QUALIFIED / TRANSIENT AND BENCH QUALIFICATION OPEN
**Execution baseline:** `69ecf0118d2ff733247f9468e620a05b606c3eff`

## Purpose
Execute AE-050 RUN05 against the selected AE-041 A1 / AE-046 SCH104/SCH105 architecture without migrating the product generator.

## Phase-A scope
- all four routing modes;
- L-only, R-only, equal, unequal and opposite-phase stimuli;
- direct-path insertion;
- mono insertion and L/R weighting;
- stereo crosstalk with a conservative selector/PCB parasitic sweep;
- dormant-input coupling in DUAL L / DUAL R;
- 2.2 MOhm return-value steady-state sweep;
- 4.7 kOhm mono-pair mismatch sweep.

The parasitic model is deliberately a lumped engineering bracket, not a claimed manufacturer switch model.

## Headline evidence
- direct worst insertion: 0.000861 dB — PASS;
- mono equal insertion @1k: -0.018608 dB left / -0.018608 dB right;
- mono nominal weighting mismatch @1k: 0.000000%;
- stereo separation with 5.0 pF lumped bracket: 98.02 dB @1k / 72.00 dB @20k.

## Reviewed disposition

**QUALIFY:** the AE-041 A1 3P4T SCH104/SCH105 architecture for RUN05 steady-state electrical behaviour.

- retain 2.2 MOhm selector-output returns as the nominal value; the sweep shows 1 MOhm enters the preferred mono-insertion region, while 2.2 MOhm provides materially greater margin without an identified cost or implementation penalty;
- retain the existing AE-041 A1 4.7 kOhm / 0.1% mono-resistor implementation for now; the RUN05 sweep shows pair mismatch, rather than absolute value, controls mono weighting. Carry <=0.10% pair mismatch preferred and <=0.25% maximum forward as a derived RUN10 tolerance/value-engineering criterion; AE-068 does not authorise a BOM tolerance relaxation;
- retain the passive 3P4T matrix and unity OPA1656 output buffers; no active summing stage or extra gain is justified;
- treat 5 pF as the conservative RUN05 qualification bracket only, not as a frozen manufacturer parasitic value; even the 10 pF bracket retains >60 dB separation at 20 kHz.

AE-041 A1 remains `CURRENT_ARCHITECTURE_QUALIFICATION_OPEN` because BBM switching transients, exact production-switch mapping/parasitics and prototype correlation remain open. No product-generator architecture change is authorised by AE-068.

## Deferred qualification
- RUN09 full-system noise;
- RUN10 tolerance/sensitivity;
- RUN12 adjacent BBM switching transients, muted and live;
- production-switch continuity mapping and bench correlation.

## Evidence
- `simulation/results/run05_matrix/ae068_run05.json`
- `simulation/results/run05_matrix/ae068_run05.csv`
- `simulation/results/run05_matrix/ae068_run05.md`
