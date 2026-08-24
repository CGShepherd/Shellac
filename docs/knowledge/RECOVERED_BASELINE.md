# Project Shellac — Recovered Architecture & Component Baseline

**Revision:** A  
**Status:** CONTROLLED RECONCILIATION BASELINE  
**Introduced:** SR-036

## Purpose
Preserve recoverable Shellac engineering intent, distinguish evidence from reconstruction, and give G3-024 a trustworthy starting point.

## Signal chain
Controlled order: `SCH101 -> SCH103 -> SCH107 -> SCH104 -> SCH105 -> SCH108`. SCH104 is unity after AE-008 because THAT1646 supplies the final 2x differential gain.

## Replay EQ / RIAA
Controlled: Bass and Treble are linked-stereo 2P5 BBM selectors. Bass positions are Flat / 200 / 400 / 500-Hz 78 / True RIAA. Treble positions are Flat / 1600 / 2121-RIAA / 3400 / 5800. True RIAA uses Bass=True RIAA plus Treble=2121 Hz RIAA with no mechanical interlock.

Recovered intent needing formal closure: a separate downstream RIAA ON/BYPASS switching function inserts the additional RIAA function when ON and is straight-through when bypassed. This was intended to avoid complicating the Bass rotary with an extra pole. The current controlled repository does not preserve this rationale clearly enough; G3-024 must reconcile it explicitly.

## Rumble
Frozen: fourth-order Butterworth high-pass, nominal 15 Hz, OPA1656, 470 nF film capacitors, linked stereo 2P2T BBM Filter/Bypass. Filter input remains driven during bypass to avoid floating nodes and switching transients.

## Channel mode
Frozen: 4P4T BBM; Stereo / Dual Left / Dual Right / L+R Mono. Two poles route outputs and two connect the mono summing branches only in Mono. AE-007 rejected relay routing, passive-only matrix and a bridged 2P4T solution. Four poles are therefore a hard requirement unless SCH105 is deliberately reopened and superseded.

## Output and mute
Frozen: THAT1646 per channel on ±18 V; SCH104 unity isolation; stereo 2PDT BBM input mute ahead of THAT1646; full-size panel male XLRs; pin 1 to CHASSIS. Old relay-mute BOM content is historical and superseded by AE-008.

## Controls / indicators
Electrical requirements: Bass 2P5 BBM; Treble 2P5 BBM; Channel 4P4T BBM; Rumble 2P2T BBM; Mute 2P2T BBM; two rail LEDs with 8.2 kΩ series resistors. Current physical direction: panel LEDs on short flying leads; no light pipes.

## Rotary procurement history
Surviving interim BOMs recorded three Grayhill 71-series rotaries, including a 4P4T Mode switch, historically budgeted around £28 each. Later project work questioned that premium under Affordable Performance and investigated lower-cost commonality, with Lorlin becoming a leading candidate. That later direction was not written back into the saved BOM. Therefore Grayhill is the historical BOM baseline; Lorlin is a later candidate/direction; exact production MPNs remain open.

For G3-024, evaluate standard-stock authorised-reseller parts, not impractical custom-only variants. Gold-contact Lorlin variants count only if realistically available in sensible quantities. Compare quantity breaks where the saving is material.

## Historical component evidence
Early BOMs recorded THAT1512A08-U balanced input devices, OPA1656 processing/filter devices, THAT1646 balanced output drivers, Neutrik panel XLRs, Panasonic FR reservoir/bulk capacitors, MUR820 rectifiers and an older Omron G5V-2-H1 mute-relay concept. These are historical evidence, not automatic current freezes. Controlled AE/G3 documents supersede older architecture where they conflict.

## Mechanical baseline
Frozen: both audio and PSU enclosures use black METCASE UNICASE 2 M5502119; PSU mains entry is SCHURTER KMF1.1121.11; PCB/standoffs establish board position; control hardware must not pull PCB/panel into alignment; drilling coordinates require exact frozen hardware and board coordinates.

Open: exact control MPNs/footprints/shaft stack, real PCB mounting-hole authority and released drilling templates.

## Recovered design rules
Affordable Performance; optimise the whole BOM; prefer useful commonality; use quantity breaks when they create meaningful savings; do not force commonality through hard requirements; prefer simple/proven architectures; preserve serviceability/manual assembly/testability; freeze only with evidence; supersede frozen decisions explicitly.

## Contradictions requiring closure
1. Saved rotary BOM = Grayhill; later intended direction = Lorlin/commonality.
2. AE-009 says switches are currently off-board/top-panel; later G3 mechanics points toward PCB-established control geometry.
3. Separate later RIAA ON/BYPASS is recovered intent but not clearly represented in controlled SCH103/SCH109.
4. Old mute-relay BOM is superseded by AE-008 mechanical input mute.
5. LED electrical architecture is frozen; exact physical LED/wiring parts remain open.

## Rotary-switch closure after reconciliation

Grayhill Series 71 is selected for all three principal rotary controls.

- SW901 Bass: `71BDF30-01-2-AJN`, stop at 5 positions.
- SW902 Treble: `71BDF30-01-2-AJN`, stop at 5 positions.
- SW903 Channel Mode: `71BDF30-02-2-AJN`, stop at 4 positions.

The decision follows a re-run comparison against C&K, Lorlin and alternative Grayhill configurations. The Series 71 solution preserves BBM/non-shorting operation, PCB termination, threaded panel bushings, adjustable stops and a common front mechanical datum. The two-deck Mode switch adds rearward depth without changing the intended PCB-to-panel interface.

PCB standoffs define PCB position. The threaded bushings provide intentional secondary structural connections and carry operating loads after natural alignment; they must not pull a misaligned PCB into position.

