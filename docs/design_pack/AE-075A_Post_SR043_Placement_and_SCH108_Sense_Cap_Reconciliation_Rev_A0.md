# AE-075A — Post-SR043 Placement and SCH108 Sense-Cap Reconciliation — Rev A0

**Project:** Shellac
**Baseline:** 046af25cb7866198304f4142c46725a5e4181f5d
**Status:** CLOSED — PRE-ROUTING DESIGN IMPLEMENTATION VALIDATED

## Scope

AE-075A repairs two physical-CAD defects discovered during final pre-routing assurance without authorising routing.

1. Twenty-three PCB-owned references introduced after the SR-043 placement freeze remained at KiCad/F8 staging coordinates outside the 220 x 140 mm Edge.Cuts rectangle.
2. SCH108 common-mode feedback capacitors had the correct 10 uF non-polar / 35 V electrical intent and 2.0 mm lead pitch but an understated 5 mm body-height footprint.

The native-board audit is also hardened so product footprint origins outside Edge.Cuts become an integrity failure.

## Placement reconciliation

The SR-042 released placement population did not regress. All out-of-board references were later additions. AE-075A moves only those identified references to their current deterministic board-local placement proposals translated into the native KiCad +20/+20 mm frame.

This is placement reconciliation, not routing acceptance. Manual-authority analogue clusters and courtyard-proximity reviews remain subject to the normal placement review gate.

## SCH108 sense capacitor

Selected part: Panasonic ECEA1VN100U.

Controlled physical contract:
- 10 uF;
- 35 V;
- bipolar/non-polar aluminium electrolytic;
- 5.0 mm body diameter;
- 11.0 mm body height;
- 2.0 mm lead pitch;
- four parts: C80010, C80011, C90010 and C90011.

The controlled ProjectShellac footprint captures the PCB diameter/pitch and carries the 11.0 mm assembly-height requirement on F.Fab and in generator/BOM metadata.

## Permanent regression guard

`sr043_native_board_audit.py` now includes every current PCB-owned product footprint origin lying within Edge.Cuts as a native-board integrity condition. Future F8 additions therefore cannot silently remain outside the board.

## Explicit non-decisions

AE-075A does not close B03, B04, B06 or B08; does not authorise final routing; and does not freeze enclosure Z-clearance or manufacturing drilling.

## Validation result

- current detailed-placement readiness: zero geometric blockers;
- native-board audit: footprint origins inside Edge.Cuts PASS;
- exact four SCH108 sense-cap footprints present on native PCB;
- generated-project rebuild/provenance PASS;
- native hierarchical ERC zero violations;
- full pytest PASS;
- integrated preflight PASS;
- git diff --check PASS.
