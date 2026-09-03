# AE-028 — Lorlin PT Mechanical Sample Validation Gate

**Revision:** A0  
**Status:** SAMPLE / MECHANICAL VALIDATION

## Purpose

The production gold-contact PT order codes remain open pending Lorlin confirmation.
Mechanical validation can proceed independently because Lorlin PT uses a common
front-panel/shaft/PCB architecture across standard and custom contact finishes.

## Recommended sample basket

1. One standard Lorlin PT 2-pole / 5-position switch, e.g. **PT6534** or equivalent
   available PT 2P5T mechanical proxy.
2. One **PT6528 spacer kit**.
3. One compatible PT additional wafer, e.g. **PT602-003 / PT602-011** as available.

These parts are **mechanical proxies only**. Their standard silver contacts do not
qualify them as production audio-path parts.

## Current indicative UK cost

- PT 2P5T proxy: about £17.14 ex VAT.
- PT6528 spacer kit: about £4.56 ex VAT.
- PT additional wafer: about £4.49–£6.09 ex VAT.

Expected sample basket: approximately **£26–28 ex VAT**, before carriage.

## Measurements to capture

### Front-panel datum
- shaft diameter;
- usable shaft length above panel;
- bush thread and bush length;
- washer/nut stack;
- required top-panel hole;
- anti-rotation provision if any;
- knob clearance.

### PCB datum
- panel-to-PCB distance with bush tightened;
- terminal insertion depth;
- terminal pitch and orientation;
- body footprint and keep-out;
- solder-side clearance.

### Single-wafer switch
- overall body width/depth;
- centreline tolerance;
- rotational stop operation;
- shaft axial/radial play.

### Two-wafer simulation
Using the spacer kit and extra wafer:
- total rearward depth;
- added wafer spacing;
- tie-rod/retainer envelope;
- PCB routing access around the rear wafer;
- whether the assembly remains mechanically square when panel and PCB both constrain it.

## Acceptance criteria

The PT platform passes this gate if:
1. shaft axis is normal to PCB within practical assembly tolerance;
2. all three rotary control positions can share one panel drilling datum;
3. panel and PCB can constrain the switch without inducing visible shaft tilt;
4. Channel two-wafer depth fits the enclosure/control keep-out;
5. PCB terminals are directly solderable without wire links;
6. knob and nut stack are compatible with the selected top-panel thickness;
7. no special mechanical bracket is required beyond PCB + panel support.

## Production consequence

If the sample passes, PCB/panel geometry may be based on PT-family mechanics
while the exact gold-contact manufacturer order codes remain open.

If it fails, the PT family is rejected before the BOM/PCB ECO.
