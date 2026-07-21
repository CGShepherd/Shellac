# G3-001 — PCB Architecture and Layout Constitution Rev A0

**Status:** Provisional until the audio enclosure, board outline and mounting datums are frozen.

## Purpose

This baseline turns Gate 3 layout intent into a CAD-independent, testable model. It does not place components or emit a KiCad PCB. It defines what a future placement and routing implementation must preserve.

## Provisional stack-up

1. Top — components and critical analogue routing.
2. Inner 1 — continuous 0VA reference plane.
3. Inner 2 — ±18 V distribution with limited non-critical routing.
4. Bottom — supporting analogue and control routing.

Nominal construction is 1.6 mm FR-4 with 1 oz copper. Manufacturer-specific dielectric geometry and impedance values remain open because this design does not require controlled-impedance transmission lines.

## Placement sequence

Input/RF → Replay EQ L/R → Rumble filter → Final gain/mode matrix → Mute/balanced output → output harness.

DC entry and block-level bulk decoupling remain at the output/high-level end, remote from the cartridge input.

## Critical routing policy

Manual-only classes include cartridge inputs, op-amp feedback and frequency-setting nodes, replay-selector RC branches, THAT1646 OUT/SNS loops, 0VA and CHASSIS architecture.

Constrained automation may be used for panel controls and selected ordinary analogue or power routes, but every proposed route remains subject to engineering review.

## Mechanical assumptions

- Minimum usable PCB area: 190 × 125 mm.
- Preferred usable PCB area: 220 × 140 mm.
- Board-edge clearance: 5 mm provisional.
- Mounting-hole keep-out: 10 mm provisional.
- Audio enclosure lid or base must lift vertically after controls are installed.

## Generated evidence

Run:

```cmd
python scripts\report_layout_baseline.py
```

This writes `out/layout/layout_baseline.json`, which is the machine-readable baseline used by future placement and routing tools.
