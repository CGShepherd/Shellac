# G3-022 — PSU Thermal and Mains-Interface Release — Rev A0

## Objective
Force the black METCASE UNICASE 1 **M5501119** PSU decision to a binary release result. Close the exact integrated mains-entry package, then freeze or reject the enclosure on controlled thermal evidence. Do not create another conditional layer.

## Exact mains-entry closure
Selected **SCHURTER KMF1.1121.11**: IEC C14 Class-I inlet, standard 2 A line filter, two-pole 5 x 20 mm fuseholder and two-pole non-illuminated line switch in one panel module.

SCHURTER's KMF manufacturer datasheet gives 40.4 mm behind-panel depth, 50 mm front height, a nominal 28.8 x 47.8 mm panel cut-out, 4.8 x 0.8 mm quick-connect terminals, and stepped snap-in support for 1.0 / 1.5 / 2.0 / 2.5 mm panels. This closes the previously unspecified IEC/filter/fuse/DPST-switch package without inventing separate panel parts.

Against the G3-021 conservative 153 x 85 mm transformer/regulator overlay, the 40.4 mm KMF depth leaves **35.61 mm nominal residual depth**. This is sufficient to show that the mains module itself does not force geometric rejection; final wiring still follows the established rear mains-zone / PE-adjacent architecture.

## Thermal release decision
The repository does not contain controlled worst-case DC rail-current consumption for the complete audio unit, nor a frozen regulator heatsink/chassis thermal resistance. Without those quantities, a release-grade closed-box temperature-rise calculation would require invented assumptions.

G3-022 therefore **REJECTS M5501119** at the binary release gate. This is not a claim that a prototype necessarily overheats. It is a design-freeze decision: the 65 mm enclosure cannot be released with defensible passive-thermal evidence from the controlled baseline, and carrying it as conditional would simply prolong mechanical closure.

## Result
- M5501119 PSU enclosure: **REJECTED**.
- SCHURTER KMF1.1121.11 mains-entry architecture: **FROZEN for the next PSU enclosure assessment**, subject to availability/current-rating review at procurement.
- Next mechanical increment: assess the next larger black UNICASE candidate with explicit thermal margin and close the PSU enclosure rather than reopening M5501119 without new measured/calculated evidence.
- Audio M5502119 freeze is unaffected.
- Audio control-stack and drilling-template work remains deferred.
