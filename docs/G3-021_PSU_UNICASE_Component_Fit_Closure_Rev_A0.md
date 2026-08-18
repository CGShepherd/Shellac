# G3-021 — PSU UNICASE Component-Fit Closure — Rev A0

## Objective
Close the known-component geometry for black METCASE UNICASE 1 **M5501119** and reduce the enclosure decision to evidence that genuinely remains unknown. Do not select arbitrary mains hardware or release drilling data.

## Manufacturer drawing evidence
The M5501119 drawing supplies the internal dimensions that G3-020 deliberately left open: **181.00 mm inside face-to-inside face, 161.01 mm internal floor dimension and 61.20 mm internal height**. The published base-PCB guide envelope remains 166 x 159 mm; component-fit work uses the larger physical internal envelope only where the drawing explicitly supports it.

## Known component overlay
- Toroid TI-69043-ME / TA030-15 conservative envelope: **78 x 78 x 36 mm**.
- Existing LM317/LM337 regulator module envelope: **75 x 85 x 31 mm**.
- Side-by-side rectangular overlay: **153 x 85 mm**.
- Residual internal floor before allocating mains-entry hardware or segregation zones: **28 mm lateral, 76.01 mm depth**.
- Both known component heights are below the 61.20 mm internal-height datum.

This is a conservative envelope proof, not a released placement. Transformer fastener geometry, wire exits, touch protection, creepage/clearance, service loops and thermal behaviour remain design constraints.

## Decision
**M5501119 is not rejected by the known transformer/regulator geometry, but remains RELEASE_BLOCKED rather than frozen.** Freezing it now would require inventing evidence that does not yet exist.

Only two release blockers remain for the PSU enclosure decision:
1. Select the exact filtered IEC/fuse/DPST-switch hardware and prove rear-panel depth, terminals, touch protection, mains/SELV segregation and wiring bend space.
2. Complete the passive thermal calculation/measurement for transformer plus LM317/LM337 dissipation in the closed 65 mm enclosure.

No arbitrary IEC inlet, fuse holder, switch, heatsink, hole position or drilling template is selected in G3-021.
