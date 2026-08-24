# Project Shellac — Decision Register

**Baseline:** SR-036 knowledge reconciliation
**Engineering base:** SR-034 / G3-023
**Git base for reconciliation:** `b57aa366ec8e10c5666843820e58fb184d55af09`

| ID | Decision | Status | Provenance | Evidence / note |
|---|---|---|---|---|
| DEC-001 | Affordable-performance / whole-BOM optimisation governs component selection | SELECTED | RECONSTRUCTED_PRIOR_INTENT | Retained from SR-035 |
| DEC-002 | Prefer component-family commonality and meaningful quantity-break economies where hard requirements remain satisfied | SELECTED | RECONSTRUCTED_PRIOR_INTENT | Quantity breaks matter most on material-cost items |
| DEC-003 | Replay timing capacitors: C0G/NP0, 1%, >=50 V; <27 nF 0805, >=27 nF 1206 | FROZEN | REPOSITORY_EVIDENCE | generator/component_selection.py |
| DEC-004 | SCH101 internal gain selector uses an eight-way DIP bank | FROZEN | REPOSITORY_EVIDENCE | AE-010 |
| DEC-005 | Audio enclosure: black METCASE UNICASE 2 M5502119 | FROZEN | REPOSITORY_EVIDENCE | G3-020/G3-023 |
| DEC-006 | PSU enclosure: black METCASE UNICASE 2 M5502119 | FROZEN | REPOSITORY_EVIDENCE | G3-023 |
| DEC-007 | PSU mains-entry architecture uses SCHURTER KMF1.1121.11 | FROZEN | REPOSITORY_EVIDENCE | G3-022/G3-023 |
| DEC-008 | PCB/standoffs establish position; control nuts/bushings must not pull a misaligned PCB into position | FROZEN | REPOSITORY_EVIDENCE | G3-019/G3-020 |
| DEC-009 | Bass/Treble require linked-stereo 2P5 functions; analogue switches BBM/non-shorting | FROZEN | REPOSITORY_EVIDENCE | AE-009 |
| DEC-010 | Channel Mode requires 4P4T BBM: Stereo/Dual Left/Dual Right/L+R Mono | FROZEN | REPOSITORY_EVIDENCE | AE-007/AE-009 |
| DEC-011 | Historical saved BOM used Grayhill 71-series rotaries for the three principal rotary controls | HISTORICAL_BASELINE | REPOSITORY_EVIDENCE | Surviving interim BOMs |
| DEC-012 | Principal rotary family is Grayhill Series 71 | SELECTED | RECOVERED_AND_REVALIDATED | Re-run trade: signal suitability + common mechanical datum |
| DEC-013 | SW901 Bass and SW902 Treble use Grayhill 71BDF30-01-2-AJN, adjustable stop set to 5 positions | SELECTED | NEW_ANALYSIS | Same exact MPN, PCB mount, BBM |
| DEC-014 | SW903 Channel Mode uses Grayhill 71BDF30-02-2-AJN, adjustable stop set to 4 positions | SELECTED | NEW_ANALYSIS | Two decks provide four poles total; PCB mount, BBM |
| DEC-015 | Rotary bushings are intentional secondary structural connections to the top cover; PCB standoffs remain primary board support | SELECTED | RECOVERED_AND_REVALIDATED | Common Series 71 front datum avoids mixed-height integration |
| DEC-016 | Release drilling templates only after exact hardware and PCB/control coordinates are frozen | FROZEN | REPOSITORY_EVIDENCE | G3-019/G3-020 |
| DEC-017 | First powered PSU prototype requires closed-box thermal verification | FROZEN | REPOSITORY_EVIDENCE | G3-023 |
| DEC-018 | SCH107 rumble filter uses linked stereo 2P2T BBM Filter/Bypass switching | FROZEN | REPOSITORY_EVIDENCE | AE-005 |
| DEC-019 | SCH105 four-pole switching is intrinsic to mono-network isolation | FROZEN | REPOSITORY_EVIDENCE | AE-007 |
| DEC-020 | THAT1646 supplies final +6.021 dB differential gain; SCH104 is unity isolation buffer | FROZEN | REPOSITORY_EVIDENCE | AE-008 |
| DEC-021 | Output mute is stereo 2PDT BBM ahead of THAT1646 inputs | FROZEN | REPOSITORY_EVIDENCE | AE-008 |
| DEC-022 | XLR outputs are full-size panel-mounted male connectors; pin 1 is CHASSIS | FROZEN | REPOSITORY_EVIDENCE | AE-008 |
| DEC-023 | +18 V/-18 V indicators are two independent panel LEDs with 8.2 kΩ resistors | FROZEN_ELECTRICAL | REPOSITORY_EVIDENCE | AE-009 |
| DEC-024 | Indicator physical implementation uses panel LEDs on flying leads, not light pipes | SELECTED | USER_RECONFIRMED_PRIOR_INTENT | Exact LED MPN open |
| DEC-025 | True RIAA uses Bass=True RIAA plus Treble=2121 Hz RIAA; no mechanical interlock required | FROZEN | REPOSITORY_EVIDENCE | AE-009 |
| DEC-026 | Separate later RIAA ON/BYPASS straight-through function retained as recovered intent; do not add a third Bass pole merely to implement it | RECOVERED_INTENT_PENDING_REPOSITORY_CLOSURE | USER_RECONFIRMED_PRIOR_INTENT | Exact switch topology still open |

## Rotary selection rationale

The Grayhill Series 71 selection is based on engineering fit rather than prestige. The one-deck and two-deck PC-mount adjustable variants share the same front shaft/bushing architecture, while the extra Mode deck grows rearward. This preserves a common PCB-to-panel datum across all three controls.

Selected parts:
- SW901 Bass: `71BDF30-01-2-AJN`, stop set to 5.
- SW902 Treble: `71BDF30-01-2-AJN`, stop set to 5.
- SW903 Mode: `71BDF30-02-2-AJN`, stop set to 4.

All are non-shorting/BBM, PCB-mount, threaded-bushing Series 71 controls.

## Provenance correction

SR-035 incorrectly described Lorlin as the saved prior BOM baseline. Surviving BOM evidence shows Grayhill Series 71 was the recorded historical choice. Later cost/commonality work considered Lorlin and C&K, but the re-run trade selects Grayhill Series 71 because the shared mechanical datum, PCB mounting, adjustable stops and contact system justify the modest premium.
