# AE-075D — B03 Control Z-Stack and EQ Control-PCB Architecture Discriminator — Rev A0

**Project:** Shellac
**Status:** CLOSED — PRE-ROUTING DESIGN IMPLEMENTATION VALIDATED
**Baseline:** `22f651f78c9448671b9305db70c7fbd0ddf74993`

## Purpose

Continue AE071-B03 without inventing final footprints or control coordinates. AE-075D reconciles the installed NKK control-plane dimension, tests the frozen carrier against the METCASE guide system, and downselects the physical ownership architecture for the four channel-local Bass/Treble controls.

## Manufacturer/mechanical evidence

### NKK NR01

The selected `NR01105ANG13-2A/-2C` controls remain five-position, SP5T, non-shorting/BBM, gold-contact, straight-PC devices.

Two different dimensions must not be conflated:

- switch/catalogue depth behind panel: **10.5 mm**;
- AT3009 flanged-knob installation, panel to PCB: **12.3 mm**.

AE-075C stored only the 10.5 mm catalogue depth. AE-075D adds the 12.3 mm installed PCB-plane datum explicitly.

### METCASE M5502119

The UNICASE family provides four PCB guide positions, but the current METCASE catalogue specifies **1.6 mm PCB thickness** for this guide system. Shellac SR-040 freezes a **2.0 mm aluminium carrier plate**. The carrier is therefore not qualified for use as a slide-in guide-rail PCB and no carrier Z-height may be inferred from those guide positions.

### Existing Shellac Z envelope

The controlled SCH108 Panasonic `ECEA1VN100U` sense capacitor is 11.0 mm high. If the complete main PCB were moved to the NKK 12.3 mm panel-to-PCB plane, that known component alone would leave only **1.3 mm nominal cover clearance**, before component tolerance, PCB/carrier tolerance, cover flex, assembly tolerance, insulation/service margin, or any taller uncontrolled part.

This does not prove every possible direct-main-PCB redesign impossible, but it is not a robust released control plane and would require avoidable component-side/Z redesign.

## Electrical locality discriminator

The SCH103 Bass and Treble switches are analogue signal-path elements, not low-risk logic controls:

- Bass selects complete op-amp feedback R-C branches;
- Treble selects passive shunt capacitors at the recovery-stage input;
- the live schematic explicitly requires switch wiring to remain extremely short;
- AE-041 requires Bass/Treble to remain local to their channel circuitry.

A single remote top-cover control strip with long analogue runs is therefore rejected.

## Selected B03 architecture for Bass/Treble

The four NKK EQ controls shall use **two channel-local EQ mezzanine PCBs**, one per channel. REG-08 remains the AE-041 top-cover mechanical-registration authority; it is not the physical identity of either PCB:

- each mezzanine owns that channel's Bass and Treble NKK switches;
- it sits directly above/adjacent to the corresponding SCH103 channel region;
- interconnect topology is not frozen: short rigid board-to-board and short low-parasitic flex/harness implementations remain candidates; long remote analogue runs are prohibited;
- final partition of the switch-adjacent passive branches between main PCB and mezzanine remains open and must minimise analogue loop length;
- if switched passives remain on the main PCB, the interconnect parasitic must be explicitly bounded;
- if switched passives migrate to the mezzanine, electrical topology/values remain unchanged but physical ownership and RUN10 parasitic/stability evidence must be reconciled.

The exact mezzanine outline, interconnect family/stack height, mechanical support, footprints, pin maps, courtyards, XY coordinates and passive ownership are **not** frozen by AE-075D.

## Shared C&K controls

`A30403RNCB` Channel, `7201SYCBE` Rumble and `7201SYCBE` Mute remain selected parts. Their final direct-main-PCB versus local control-PCB ownership remains open until the exact C&K PCB-plane/bushing stack is overlaid against the chosen main-board Z.

A single central remote analogue-control strip remains prohibited.

## B03 disposition after AE-075D

Resolved/narrowed:

- exact control MPNs;
- NKK 10.5 mm depth versus 12.3 mm installed panel-to-PCB distinction;
- METCASE 1.6 mm guide system is not a 2.0 mm carrier Z solution;
- central long-run remote-control-strip architecture rejected;
- Bass/Treble ownership selected as two channel-local EQ mezzanines.

Still open before final routing:

1. exact main-PCB/carrier Z;
2. exact C&K installed stack and shared-control PCB ownership;
3. EQ mezzanine interconnect family, stack height and mechanical support;
4. exact switch footprints, pin maps, courtyards and body envelopes;
5. switch-local passive ownership and RUN10 parasitic/stability qualification;
6. final control XY coordinates, top-cover apertures and keep-outs;
7. physical CAD migration.

No native PCB geometry, final routing, layout freeze, BOM freeze or manufacturing release is authorised by AE-075D.

## Evidence sources

- NKK NR01 rotary-switch datasheet and AT3009 mounting/installation drawing.
- METCASE UNICASE catalogue and M5502119 manufacturer product/drawing data.
- C&K A Series and 7000 Series manufacturer data.
- SR-040 mechanical freeze.
- AE-041 Rev A1 control authority.
- AE-075A sense-cap reconciliation.
- AE-075C exact control-hardware reconciliation.

## Validation result

Final AE-075D qualification completed after control-architecture semantic reconciliation and historical/current test-ownership hardening:

- full regression suite: **693 passed**;
- generated KiCad provenance: PASS, build ID `f3b53e012062f2a9`, 14 immutable files verified;
- native hierarchical ERC: **0 violations**;
- native PCB integrity: PASS;
- routing authority: **false**;
- integrated preflight: PASS;
- decision/configuration authority audit: PASS;
- working-tree `git diff --check`: PASS.

AE071-B03 remains intentionally open for the exact main-PCB/carrier Z datum, C&K installed stack/shared-control ownership, EQ mezzanine interconnect/support, switch-local passive partition and RUN10 parasitic qualification, exact control footprints/pin maps/courtyards/body envelopes, XY keep-outs and final physical CAD migration.

Routing, layout freeze, BOM freeze and manufacturing release remain explicitly unauthorised.
