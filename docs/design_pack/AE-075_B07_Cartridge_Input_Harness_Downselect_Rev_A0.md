# AE-075 B07 — Cartridge Input Harness Contact-System Downselect — Rev A0

**Project:** Shellac  
**Status:** CLOSED — PRE-ROUTING DESIGN IMPLEMENTATION VALIDATED  
**Baseline:** `025f33f1442dc1d57e17b7d69c71d0da060c6cb4`

## Purpose

Close the architecture/contact-system portion of AE071-B07 without falsely releasing routing before the production footprint and native PCB are reconciled.

## Selected interface

Per channel:

- panel XLR pin 1 -> shield/chassis conductor -> connector pin 1 -> CHASSIS;
- panel XLR pin 2 -> matched signal conductor -> connector pin 2 -> HOT/+;
- panel XLR pin 3 -> matched signal conductor -> connector pin 3 -> COLD/-;
- signal conductors are a short shielded twisted pair;
- 24-26 AWG is preferred for the Shellac low-level harness.

Selected connector set:

- PCB header: Molex Micro-Lock Plus `5055780321`, 3-circuit right-angle SMT, 0.38 um gold mating finish;
- cable housing: Molex `5055700301`;
- female crimp terminal: Molex `5055721200`, 22-26 AWG, 0.38 um gold mating finish.

The previous JST VH representation is rejected as the production choice for this low-level interface. It remains electrically credible, but its 3.96 mm power-oriented form factor does not earn its space in the cartridge front end.

## Affordable-performance rationale

The gold contact system, positive lock, small 2.00 mm pitch and support for 24-26 AWG wiring materially improve fit and repeatable low-level harness construction. No benefit has been demonstrated for the 0.76 um gold option in this low-cycle indoor application.

## Cross-project procurement

Molex Micro-Lock Plus is a preferred common-family candidate for Phoenix low-level balanced harnesses. This is a procurement/commonality opportunity, not Phoenix design authority. Phoenix must independently verify mechanical fit inside its narrow receiver-module envelope before adopting the family.

Engineering BOMs remain project-specific. Purchase quantities may later be consolidated in a Shellac/Phoenix procurement basket.

## Exact-part footprint verification

The exact `5055780321` KiCad EDA package supplied for review was inspected and cross-checked against the Molex drawing. The controlled footprint preserves:

- signal pads 1/2/3 at 2.00 mm pitch;
- signal pad size 1.0414 x 2.5908 mm in the supplied EDA model;
- two SMT retention pads 4/5;
- body/copper keep-out regions from the exact-part EDA package;
- pin numbering 1/2/3 required by the Shellac harness contract.

The footprint is stored under `generator/footprints/ProjectShellac.pretty` and is copied into generated KiCad output by the project writer. Native H101/H201 migration remains open until KiCad Update PCB and post-update audits pass.

## Native implementation validation

KiCad F8 reconciliation migrated H101/H201 to the controlled exact-part footprint while retaining the established board locations and channel symmetry.

Validated native mapping:

- H101 pin 1 -> `CHASSIS`, pin 2 -> `/INPUT_L_POS`, pin 3 -> `/INPUT_L_NEG`;
- H201 pin 1 -> `CHASSIS`, pin 2 -> `/INPUT_R_POS`, pin 3 -> `/INPUT_R_NEG`;
- retention pads 4/5 are present and electrically unconnected on both connectors;
- all three embedded footprint keep-outs are retained on both connectors;
- H101/H201 remain separated by 104.0 mm with identical orientation.

The temporary H101/H201 footprint-contract mechanical ECO is therefore removed.

## Residual manufacturing / commissioning checks

B07 closure is a pre-routing design closure; it does not claim a physical harness has already been manufactured. At build/commissioning:

1. inspect crimp quality and positive-lock engagement;
2. continuity-check pins 1/2/3 end-to-end before connection to the cartridge;
3. verify shield/chassis conductor continuity and absence of accidental signal-return bonding;
4. retain AE071-B06 as the separate authority for the XLR pin-1/local-chassis implementation.

These checks do not require B07 to remain a routing blocker because the PCB/harness interface, connector geometry and electrical pin contract are now controlled.

## Routing disposition

AE071-B07 is closed. Routing remains held by the five remaining AE071 routing blockers; this record does not alter them.
