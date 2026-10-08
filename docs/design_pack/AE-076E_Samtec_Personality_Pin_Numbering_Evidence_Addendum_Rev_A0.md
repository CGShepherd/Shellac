# AE-076E — Samtec Personality Interface Pin-Numbering Evidence Addendum — Rev A0

**Parent governed baseline:** `4975fba11a12f25744e35ea61e11578c66f3d50f`\
**Status:** PROVISIONAL COMPONENT-EVIDENCE ADDENDUM — NO PRODUCT MIGRATION

## 1. Purpose

Close the remaining ambiguity in the AE-076E pre-implementation review over whether the selected diagonal duplicate-node map is compatible with the manufacturer numbering pattern of the chosen 2x2 Samtec SLW/TSW interface.

## 2. Manufacturer evidence reviewed

Official Samtec material:

- SLW series manufacturing print `SLW-1XX-01-X-X-MKT`;
- SLW recommended through-hole PCB footprint;
- TSW series manufacturing print `TSW-XXX-XX-XXX-X-XX-XXX-MKT`;
- TSW recommended through-hole PCB footprint;
- exact selected products:
  - `SLW-102-01-G-D`;
  - `TSW-102-07-G-D`.

Relevant dimensional evidence:

### SLW

- 2.54 mm position pitch;
- 2.54 mm double-row spacing;
- recommended PTH diameter 0.86 mm;
- double-row body width 4.95 mm;
- body height 4.57 mm;
- tail length 2.92 mm.

The SLW manufacturing print explicitly labels pins 01 and 02 at the same end of the double-row strip. Pin numbering then progresses by position along the strip.

### TSW

- 2.54 mm position pitch;
- 2.54 mm double-row spacing;
- recommended THT PCB hole diameter 1.02 mm;
- 0.635 mm square posts;
- selected -07 lead style has 5.84 mm mating post and 10.92 mm overall length.

The TSW manufacturing print shows the double-row numbering sequence and explicit pin-1 identification.

**Important:** SLW and TSW have different manufacturer-recommended PCB hole diameters. The service-card TSW footprint must not copy the SLW 0.86 mm hole.

## 3. 2x2 rotational mapping

For the four-corner 2x2 geometry produced by the Samtec numbering sequence, a 180° rotation exchanges opposite corners:

- 1 ↔ 4;
- 2 ↔ 3.

Therefore the selected AE-076C duplicate-node map:

- pins 1 and 4 = POS;
- pins 2 and 3 = NEG;

is invariant under a 180° rotated insertion.

This confirms the **topological anti-reversal principle**.

## 4. Remaining mating-face check

The above does not by itself authorise a footprint/card release.

Before fabricating the service card, the exact KiCad footprint orientations must still prove the physical **mating-face correspondence** between:

- main-board `SLW-102-01-G-D`; and
- card-side `TSW-102-07-G-D`.

That check shall demonstrate that the intended card copper connects the actual mated contact pairings correctly in the normal insertion orientation.

This is a footprint/orientation verification, not a reopening of the selected electrical architecture.

## 5. Footprint rule

Main board:

- exact SLW 2x2;
- 2.54 x 2.54 mm grid;
- 0.86 mm manufacturer recommended PTH;
- pin-1 indication and explicit orientation datum.

Service card:

- exact TSW 2x2;
- 2.54 x 2.54 mm grid;
- 1.02 mm manufacturer recommended hole;
- pin-1 indication and explicit orientation datum.

Do not use one generic 2x2 footprint for both components merely because the pitch matches.

## 6. Disposition

**Diagonal duplicate-node anti-reversal topology: SUPPORTED BY MANUFACTURER NUMBERING EVIDENCE.**

Still `CLOSE_BEFORE_FAB`:

- exact SLW footprint orientation;
- exact TSW footprint orientation;
- socket-to-header mating-face contact correspondence;
- native H120/H220 net/pad verification;
- service-card copper/net verification;
- RUN10 parasitic-capacitance and L/R matching acceptance.

No release permission changes.
