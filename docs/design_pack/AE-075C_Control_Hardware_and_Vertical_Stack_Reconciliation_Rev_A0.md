# AE-075C — Control Hardware and Vertical-Stack Reconciliation — Rev A0

**Project:** Shellac
**Status:** CLOSED — PRE-ROUTING DESIGN IMPLEMENTATION VALIDATED
**Baseline:** `7f95cc578f6fe46f974fc567ddd40f70aef8ba3b`

## Purpose

Narrow routing blocker AE071-B03 by freezing the exact seven operator-control part numbers and reconciling the live mounting semantics before any control footprint, keep-out or drilling coordinate is invented.

## Exact control hardware

- Bass L/R: NKK `NR01105ANG13-2C`, two pieces, red AT3009 flanged knob.
- Treble L/R: NKK `NR01105ANG13-2A`, two pieces, black AT3009 flanged knob.
- Channel matrix: C&K `A30403RNCB`, one piece, existing TE/Alcoswitch `KN900B1/4` knob.
- Rumble: C&K `7201SYCBE`, one piece.
- Mute: C&K `7201SYCBE`, one piece.

The NR01 selection is five-position SP5T, non-shorting/BBM, gold-contact, through-hole PC-pin hardware. Its AT3009 flanged knob registers beneath the panel and the switch has no threaded mounting bushing. This invalidates the stale generic model text inherited from the older Grayhill/Lorlin-era concept.

The C&K A-series matrix and 7000-series toggles retain their threaded-bushing panel-registration semantics.

## Historical/current authority separation

`generator/model/rotary_switch_procurement_gate.py` had remained a live Lorlin PT gate even after AE-041 A1 superseded Lorlin with NKK/C&K hardware. AE-075C reconciles that live module to current NKK authority. Historical AE-026/AE-027 Lorlin design/procurement records remain unchanged provenance.

## B03 vertical-stack finding

The repository freezes:
- METCASE M5502119 enclosure;
- 86.2 mm internal cover-height reference;
- 2 mm removable carrier plate;
- 8 mm main-PCB-to-carrier standoff.

It does **not** currently freeze the carrier/control-PCB Z coordinate relative to the upper-cover inner face or the top-cover thickness at the control apertures. G3-020 itself states that drilling remains gated by the verified cover Z datum and part-specific control stack.

Therefore AE-075C does not claim that the exact switches can be mounted directly on the main audio PCB. It also does not prematurely select a REG-08 control PCB. That ownership downselect must be made from the controlled vertical-stack evidence.

## Remaining AE071-B03 scope

1. Freeze control-plane Z relative to the top cover and the cover thickness.
2. Downselect direct-main-PCB versus REG-08 control-PCB ownership.
3. Create exact footprints/pin maps/courtyards/body envelopes for the selected controls.
4. Freeze control XY coordinates and keep-outs.
5. Verify knob/actuator projection, tool access, anti-rotation features and vertical service removal.
6. Only then migrate the physical switch instances from panel-excluded representation to their final PCB ownership and reconcile native PCB/control-board CAD.

No final routing, layout freeze, BOM freeze or manufacturing release is authorised by AE-075C.

## Manufacturer evidence

- NKK `NR01105ANG13` product specification and NR01 rotary datasheet.
- Littelfuse/C&K A-series rotary-switch datasheet for the A304 family.
- Littelfuse/C&K 7000-series toggle-switch datasheet for `7201SYCBE`.
- METCASE M5502119 Issue-1 dimensional drawing and product data.

## Known provenance debt

The separately documented missing controlled AE-072 design record is unaffected by AE-075C and is not fabricated here.

## Validation result

Final AE-075C qualification completed after historical/current test-architecture reconciliation:

- full regression suite: **689 passed**;
- generated KiCad provenance: PASS, build ID `ad41bc9f4edc05bf`, 14 immutable files verified;
- native hierarchical ERC: **0 violations**;
- native PCB integrity: PASS;
- integrated preflight: PASS;
- decision/configuration authority audit: PASS;
- `git diff --check`: PASS.

AE071-B03 remains intentionally open. AE-075C freezes exact control hardware and mounting semantics only; control-plane Z, upper-cover stack, main-PCB versus REG-08 control-PCB ownership, exact footprints/pin maps/courtyards, XY keep-outs and final physical switch migration remain before routing release.

Routing, layout freeze, BOM freeze and manufacturing release remain explicitly unauthorised.
