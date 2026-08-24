# Project Shellac — Controlled Project Status

**Knowledge baseline:** SR-036 reconciliation candidate
**Engineering base:** SR-034 / G3-023
**Current main before SR-036:** `b57aa366ec8e10c5666843820e58fb184d55af09`

## Frozen / closed
- SCH101 gain architecture and internal eight-way DIP selection.
- SCH103 replay EQ architecture and timing-capacitor selection policy.
- SCH107 fourth-order 15 Hz Butterworth rumble filter and 2P2T BBM bypass architecture.
- SCH105 4P4T BBM channel-mode architecture.
- THAT1646 balanced-output architecture; SCH104 unity after integrated gain correction.
- Mechanical input mute ahead of THAT1646.
- Audio and PSU enclosures: METCASE UNICASE 2 M5502119, black RAL 9005.
- PSU mains-entry architecture: SCHURTER KMF1.1121.11.
- PCB/standoffs establish alignment; panel control hardware does not force PCB position.

## Reconciled historical state
- Saved interim BOM used Grayhill 71-series for all three principal rotaries.
- Later project direction revisited Grayhill cost and investigated Lorlin/commonality.
- Exact production rotary MPNs were never formally frozen.
- Old mute-relay BOM content is superseded by AE-008 mechanical mute.
- Panel rail indicators remain two LEDs; current physical direction is flying leads, not light pipes.

## High-priority architecture reconciliation
The separate later RIAA ON/BYPASS straight-through function is recovered/user-reconfirmed prior intent but is not represented clearly enough in current controlled SCH103/SCH109 material. Resolve this before freezing Bass/Treble switch hardware.

## Next engineering package
**G3-024 — Audio Control & Physical-Board Closure.**

Sequence: reconcile/document later RIAA ON/BYPASS; build exact switch truth/contact requirements; compare stocked rotary candidates using Grayhill historical baseline and Lorlin later candidate; freeze exact switch/toggle/LED parts only with electrical + mechanical evidence; reconcile PCB/panel ownership and mounting-hole authority; update BOM/decision/risk records at the same commit as each freeze.

## Manufacturing limitation
Gate 3A PCB output remains a review artefact; no final mounting-hole or drilling release authority yet.
