# Project Shellac — Controlled Project Status

**Knowledge baseline:** SR-036
**Engineering package:** G3-024 control-subsystem closure candidate
**Base commit:** `2728729f96166abf521d332aec886016555fd057`

## Frozen / selected
- SW901/SW902: Grayhill 71BDF30-01-2-AJN, five stops.
- SW903: Grayhill 71BDF30-02-2-AJN, four stops.
- SW904/SW905: C&K 7201SYCBE common DPDT toggle.
- LED901/LED902: Vishay TLLG4401 in black-brass A104700BLACK bezels, audio top-cover centre spine, flying leads.
- External-switch bushings are secondary structural connections; PCB standoffs remain primary datum/support.
- Previously frozen electrical/enclosure/PSU decisions remain unchanged.

## Deliberately open
- Exact node-level topology and MPN for the recovered internal 3180 us RIAA ON/BYPASS switch.
- Verified controlled PCB footprints/3D envelopes for the five selected external switches.
- Final board mounting-hole authority and top-cover drilling coordinates.

## Next package
**G3-025 — Control Footprint, RIAA-switch and Top-Cover Datum Closure**
1. Reconcile the later 3180 us RIAA ON/BYPASS function into SCH103 at node level.
2. Build/verify controlled footprints and mechanical envelopes from manufacturer drawings.
3. Resolve generic SCH109 interface symbols versus physical PCB ownership without disturbing electrical hierarchy.
4. Synthesize control coordinates, mounting holes and centre-spine LED coordinates.
5. Release drilling information only after stack-up/tolerance checks pass.

## Manufacturing limitation
G3-024 selects control hardware but does not authorise final PCB fabrication or top-cover machining.
