# AE-071A — SCH101 Product Migration — Rev A0

**Project:** Shellac
**Baseline:** `87769300eaa51aff20f560d2850b0d0433b9217b` (AE-071)
**Status:** PRODUCT MIGRATION IMPLEMENTED / QUALIFICATION AND ROUTING GATES OPEN

## Purpose

Migrate the AE-042 SCH101 selected-next electrical architecture into the live product generator after AE-066 RUN01/RUN02 nominal qualification, without changing DR-039 or releasing routing.

## Implemented electrical migration

- Fixed per-leg RF = 999 ohm and RG = 1.000 kohm.
- LOW: 332 ohm branch in parallel with RF.
- DEFAULT: no LOW/HIGH branch bridged; complete working amplifier at approximately 18 dB.
- HIGH: 866 ohm branch in parallel with RG.
- The eight historical 0-ohm service-link components are removed.
- Fixed 47 pF signal-leg-to-CHASSIS RF capacitors remain.
- The obsolete 22 pF differential DNP representation is replaced by explicit ganged L/R BASE/+47/+100 pF differential service loading.
- AE-064 cartridge identity remains current: Grado Prestige 78C, AT-VM95SP and Grado Gold/8MZ compatibility.
- AE-071 OPA1655 converter identity, LT5400 B-grade candidate, local 100 nF package bypassing and EP-open status are preserved.

## Service hardware representation

Candidate gain hardware remains Samtec MNT-104-BK-G with three TSW-104-07-G-D header banks for LOW, HIGH and PARK. Candidate load hardware remains MNT-102-BK-G with three TSW-102-07-G-D banks for +47 pF, BASE/PARK and +100 pF.

The product generator represents logical A/B pairs and real PCB footprints. It does not claim production MNT internal pairing/orientation is verified. Continuity/orientation plus cartridge-load service-header parasitic/layout correlation remain explicit final-routing blockers.

## Qualification boundary

AE-066 RUN02 is nominal gain/CMRR evidence. RUN10 retains tolerance/mismatch/value-engineering authority, including the complete LT5400 B-grade stack and gain-program component tolerances. Prototype/bench verification remains required.

DR-039 remains untouched and pending its separate controlled migration.

## Configuration disposition

- DR-038 becomes `CURRENT_ARCHITECTURE_QUALIFICATION_OPEN`.
- AE071-B01 / AE071-F01 product migration closes.
- New service-hardware pairing/orientation/parasitic-layout blocker remains open.
- Final routing, layout freeze, BOM freeze and manufacturing release remain prohibited.
