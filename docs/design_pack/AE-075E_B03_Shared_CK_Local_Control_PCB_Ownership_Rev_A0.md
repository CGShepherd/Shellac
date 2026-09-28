# AE-075E — B03 Shared C&K Local Control-PCB Ownership — Rev A0

**Project:** Shellac
**Status:** CLOSED — PRE-ROUTING DESIGN IMPLEMENTATION VALIDATED
**Baseline:** `5ace476f9730fd4607656f44f697ca6137064666`

## Purpose

Continue AE071-B03 from the clean AE-075D baseline without inventing the still-open absolute Z stack or manufacturing coordinates. AE-075E determines whether the selected C&K Channel, Rumble and Mute controls belong directly to the main audio PCB or to distributed local control PCB(s).

## Higher-authority constraints retained

- G3-019 requires operator switches to be PCB mounted and prohibits flying switch/potentiometer wiring.
- G3-020 requires PCB/standoff geometry to establish position before any threaded control bushing is tightened.
- AE-041 A1 retains the front-to-rear control sequence and REG-08 as top-cover mechanical-registration authority, not a central control strip.
- AE-075D rejects a long-run central analogue strip and selects two channel-local EQ mezzanines for Bass/Treble.
- The current main PCB remains a 220 x 140 mm four-layer board on the removable carrier architecture with 8 mm main-PCB standoffs; absolute carrier Z relative to the upper-cover inner face remains open.

## Manufacturer evidence

### C&K A30403RNCB Channel switch

The current Littelfuse/C&K A-series datasheet identifies:

- `A304` as 3-pole, four-position, 30-degree indexing;
- `R` mounting as 3/8-32 threaded;
- `C` termination as PC through-hole;
- `N` as non-shorting;
- `B` as gold contact material.

The manufacturer mechanical drawing defines the switch body and PC-terminal geometry, but it does **not** define a unique installed panel-to-PCB plane equivalent to the NKK AT3009 12.3 mm installation datum. PCB location therefore remains a controlled assembly-stack decision.

Manufacturer source:
`https://www.ckswitches.com/media/1349/arotary.pdf`

### C&K 7201SYCBE Rumble/Mute switches

The current Littelfuse/C&K 7000-series datasheet identifies:

- `Y` as the 0.350 inch / 8.89 mm high 1/4-40 threaded bushing;
- `C` as PC through-hole termination;
- the C termination as 0.250 inch / 6.35 mm long PC pins;
- the panel-mount and PCB-hole geometry separately.

Again, the drawing does **not** define a single installed panel-to-PCB plane; the PCB may not be positioned by assuming that catalogue body depth equals a released stack dimension.

Manufacturer source:
`https://www.ckswitches.com/media/1394/7000toggle.pdf`

## Architecture discriminator

Direct mounting of Channel, Rumble and Mute on the current main audio PCB is rejected as the **current architecture**.

This is a design downselect, not a claim that every hypothetical elevated-main-board redesign is physically impossible. Direct-main-PCB mounting would make the main-board/carrier Z subordinate to top-cover switch geometry before the carrier-to-cover datum is governed, contrary to the existing serviceable carrier architecture and the rule that PCB/standoffs establish control alignment.

The selected architecture is therefore:

- Channel, Rumble and Mute remain genuine PCB-mounted controls;
- they belong to **distributed local control PCB(s)** near their corresponding signal-chain regions;
- their switch terminals are soldered directly to those local PCBs, so G3-019's no-flying-switch-harness requirement remains satisfied;
- inter-board connection between a local control PCB and the main PCB is a separate B03 interconnect trade and is not itself a flying switch-terminal harness;
- a long central analogue control strip remains prohibited;
- exact partition into one or more local modules remains open and must preserve analogue locality and the front-to-rear control sequence.

## Z-stack boundary

AE-075E deliberately does **not** freeze:

- carrier/main-PCB absolute Z relative to the upper-cover inner face;
- nominal versus as-built top-cover thickness at each aperture;
- exact C&K installed PCB plane;
- local-control-PCB standoff/support architecture;
- rigid board-to-board versus short serviceable inter-board connection;
- the number/outline of C&K local control PCBs.

The C&K manufacturer drawings are component geometry evidence, not authority to invent a panel-to-PCB stack.

## B03 disposition after AE-075E

Resolved/narrowed:

1. Bass/Treble remain on the two channel-local EQ mezzanines selected by AE-075D.
2. Channel/Rumble/Mute direct-main-PCB ownership is rejected as the current architecture.
3. Channel/Rumble/Mute use distributed local control PCB ownership.
4. No operator switch is wired by flying leads.
5. REG-08 remains distributed mechanical-registration authority; no central analogue strip is created.

Still open before final routing:

1. exact carrier/main-PCB Z relative to the upper-cover inner face;
2. exact C&K local-PCB partition and installed panel/PCB stack;
3. mechanical support and inter-board connection for all local control PCBs;
4. switch-local passive ownership and RUN10 parasitic/stability qualification;
5. exact selected-part footprints, pin maps, courtyards and body/3D envelopes;
6. final control XY coordinates, top-cover apertures and keep-outs;
7. physical CAD migration.

No native PCB geometry, final routing, layout freeze, BOM freeze or manufacturing release is authorised by AE-075E.

## Evidence sources

- Littelfuse/C&K A Series 1-4 Pole Rotary Switches datasheet, 2025 revision.
- Littelfuse/C&K 7000 Series Miniature Toggle Switches datasheet, 2025 revision.
- METCASE M5502119 Issue-1 drawing/current product data.
- G3-019 UNICASE interface architecture.
- G3-020 UNICASE sizing/control-stack contract.
- AE-041 Rev A1 top-cover control authority.
- AE-075C exact control hardware reconciliation.
- AE-075D EQ local-mezzanine discriminator.

## Validation result

AE-075E qualification completed against the clean AE-075D governed baseline:

- full regression suite: **698 passed**;
- generated KiCad provenance: PASS, build ID `99a4c56b17067fd0`, 14 immutable files verified;
- native hierarchical ERC: **0 violations**;
- native PCB integrity: PASS;
- routing authority: **false**;
- integrated preflight: PASS;
- decision/configuration authority audit: PASS;
- working-tree `git diff --check`: PASS.

AE071-B03 remains open for carrier/main-PCB Z, exact C&K local-PCB partition and installed stack, local-board support/interconnect, EQ interconnect/passive partition and RUN10 parasitics, exact footprints/pin maps/courtyards/body envelopes, XY keep-outs and final physical CAD migration.

Routing, layout freeze, BOM freeze and manufacturing release remain explicitly unauthorised.
