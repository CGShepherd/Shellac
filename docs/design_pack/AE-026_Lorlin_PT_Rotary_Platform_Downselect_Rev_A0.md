# AE-026 — Lorlin PT Rotary Platform Down-Selection

**Revision:** A0  
**Status:** PREFERRED PLATFORM — exact gold-contact MPNs / sample validation open

## Decision summary

Use **Lorlin PT** as the preferred mechanical platform for all three Shellac rotary controls:

- Bass: 2P5T, one wafer, BBM;
- Treble: 2P5T, one wafer, BBM;
- Channel: 4P4T realised as two synchronised 2-pole PT wafers, BBM, stopped at four positions.

The existing C&K 7201SYCBE toggles remain the preferred Rumble and Mute devices.

## Why one PT family wins

The roughly £30 saving of a CK/PT hybrid is not compelling once assembly,
alignment and serviceability are included.

A common PT platform gives one 6 mm shaft standard, one M10 x 0.75 panel bush,
one 10 mm panel hole, one PCB terminal pitch, one shaft/knob interface, one
mechanical datum, and common indexing feel.

The multi-wafer Channel switch grows rearward but preserves the same front-panel geometry.

## Manufacturer-supported geometry

Published PT metric dimensions:

- spindle diameter: 6.0 mm;
- standard spindle length: 50 mm;
- bush thread: M10 x 0.75;
- mounting hole: 10 mm;
- PCB terminal pitch: 2.54 mm;
- standard indexing: 30 degrees;
- multi-wafer spacers: 6.35 / 7.63 / 10.16 mm;
- up to five additional wafers supported.

The standard single-wafer metric non-shorting 2P5T part is PT6004.
The stocked PT6422/BMH is a useful geometry/procurement proxy, but its exact
contact plating must not be assumed to satisfy the production gold-contact requirement.

## Contact system

Production requirement:

- BBM/non-shorting;
- gold-plated contacts preferred;
- gold flash acceptable only by explicit review;
- ordinary silver-contact stock parts are not preferred for Shellac's low-level analogue switching.

Lorlin publishes initial contact resistance below 20 mΩ, insulation resistance
above 999 MΩ at 500 VDC, and >10,000-cycle life for PT.

## Channel architecture

A single 30-degree PT wafer cannot provide 4P4T. The correct PT solution is two
synchronised 2-pole wafers, using minimum practical wafer spacing.

## Remaining Foundry gates before FROZEN

1. Exact gold-contact order code for metric BBM 2P5T.
2. Exact two-wafer 4P4T Channel order code.
3. Manufacturer drawings for both assemblies.
4. Confirm common 6 mm shaft / M10 x 0.75 bush datum.
5. Confirm shaft length against actual PCB-to-panel stack.
6. Confirm Channel rear depth and PCB keep-out.
7. Confirm knob bore and nut/washer stack.
8. Obtain prototype pricing/lead time.
9. Buy at least one single-wafer and one two-wafer sample.
10. Measure actual panel-to-PCB datum before production freeze.

## Current disposition

- Grayhill 71BDF30: **REJECTED — right-angle geometry**.
- Lorlin CK/PT hybrid: **VALID ALTERNATIVE — not preferred**.
- Lorlin PT all-rotary platform: **PREFERRED PENDING EXACT MPN/SAMPLE GATE**.
