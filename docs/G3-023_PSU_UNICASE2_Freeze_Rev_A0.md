# G3-023 — PSU UNICASE 2 Freeze — Rev A0

## Objective
Close the replacement PSU enclosure decision after G3-022 rejected black UNICASE 1 M5501119. The outcome must be binary: freeze or reject the next larger black UNICASE candidate without creating another conditional layer.

## Decision
**FREEZE METCASE UNICASE 2 M5502119, black RAL 9005, for the PSU enclosure.** This is the same order code already frozen for the audio enclosure.

The manufacturer M5502119 data gives 260 x 250 x 90 mm nominal external size and a 241 x 229 mm base-PCB envelope. The controlled project drawing data already records the usable inside-face envelope as 256 x 236 x 86.2 mm with 2.0 mm end panels.

## Packaging reserve
The conservative G3-021 transformer/regulator overlay remains 153 x 85 mm. Carrying forward the exact SCHURTER KMF1.1121.11 mains-entry depth of 40.4 mm, M5502119 leaves:

- 103.0 mm residual width beyond the side-by-side transformer/regulator envelopes;
- 110.6 mm residual depth after the 85 mm overlay and 40.4 mm rear mains module;
- 50.2 mm headroom above the conservative transformer envelope;
- 55.2 mm headroom above the existing regulator-module envelope.

The enclosure therefore satisfies the established 120 x 180 x 80 mm PSU screening gate with substantial service, wiring-bend, segregation and heatsink reserve.

## Passive-thermal reserve
A release-grade temperature prediction is still not possible without controlled worst-case rail current and regulator-to-ambient thermal resistance. G3-023 does not fabricate those quantities.

Instead, enclosure selection uses explicit reserve relative to the rejected M5501119: approximately **2.92x usable internal volume** and **1.95x nominal external surface area**, while restoring the historical >=80 mm internal-height gate. This is sufficient to freeze enclosure size while retaining closed-box temperature measurement as a first-prototype verification activity.

A failed prototype temperature test reopens the regulator heatsinking/thermal path first; it does not automatically invalidate the enclosure freeze unless measured evidence shows that the reserved passive-thermal architecture cannot close.

## Result
- Audio enclosure: **M5502119 FROZEN**.
- PSU enclosure: **M5502119 FROZEN**.
- Both enclosures: black RAL 9005 METCASE UNICASE 2.
- PSU mains entry: SCHURTER **KMF1.1121.11** carried forward.
- M5501119 remains rejected and is not reopened.
- Prototype closed-box thermal verification remains required.
- Audio control selection and released drilling templates remain deferred to their own increments.
