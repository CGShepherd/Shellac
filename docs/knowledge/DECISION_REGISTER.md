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
| DEC-026 | Separate later RIAA ON/BYPASS straight-through function retained; do not add a third Bass pole merely to implement it | SELECTED_ARCHITECTURE | USER_RECONFIRMED_PLUS_G3_025_ANALYSIS | Dedicated stereo 3180 us section; exact RC/gain realisation and MPN remain open |
| DEC-027 | SW904 Rumble and SW905 Mute use the same C&K 7201SYCBE DPDT ON-ON gold-contact PC-pin toggle with threaded panel bushing | SELECTED | NEW_ANALYSIS | Common low-level toggle family; exact PCB footprint still requires controlled verification |
| DEC-028 | LED901/LED902 use Vishay TLLG4401 low-current diffused green 3 mm LEDs in Arcolectric/Bulgin A104700BLACK black-brass bezels; retain 8.2 kΩ resistors | SELECTED | NEW_ANALYSIS | Approximately 1.90 mA using 2.4 V design Vf; intentionally subdued indicator |
| DEC-029 | Rail indicators are fitted only to the audio chassis, on the top-cover central longitudinal spine, as a symmetric +18/-18 pair on short flying leads | SELECTED | USER_RECONFIRMED_AND_NEW_ANALYSIS | PSU receives no duplicate rail LEDs |
| DEC-030 | All five external switches are PCB-through-hole controls whose threaded bushings pass through the top cover as intentional secondary structural connections; standoffs remain the primary PCB datum/support | SELECTED | RECOVERED_AND_REVALIDATED | Schematic interface symbols remain non-placement authority until verified footprints are released |
| DEC-031 | G3-024 did not invent the internal 3180 us RIAA switch topology | SUPERSEDED_BY_G3_025 | REPOSITORY_EVIDENCE_PLUS_RECOVERED_INTENT | Architecture-level reconciliation completed by DEC-033/DEC-034 |
| DEC-032 | Foundry FDR-001 is the controlled engineering-governance baseline for evidence, decisions, conflicts and manufacturing release | SELECTED | G3_025 | Git remains authoritative project memory |
| DEC-033 | The current single-RC SCH103 active branch couples the 3180 us pole and 318 us zero; changing/bypassing its capacitor cannot independently bypass only the 3180 us term | FROZEN_ANALYSIS | DERIVED_AND_TESTED | Pole and zero both scale as 1/C |
| DEC-034 | Optional 3180 us architecture is factorised as invariant 318/75 core times a dedicated 3180 us section; internal BYPASS is straight-through around only that section in both channels | SELECTED | DERIVED_AND_TESTED | Minimum two linked signal paths; exact circuit values/MPN not yet frozen |
| DEC-035 | G3-025 records control mechanical evidence but does not convert catalogue dimensions into manufacturing authority | SELECTED | FOUNDRY_RULE | Final pad geometry, top-cover Z stack and drilling remain gated |
| DEC-036 | Panel-bezel rail LEDs on short flying leads explicitly supersede stale light-pipe/no-flying-indicator assumptions | SELECTED | CONTROLLED_DECISIONS_024_029 | External switches remain PCB-mounted |

## Rotary selection rationale

The Grayhill Series 71 selection is based on engineering fit rather than prestige. The one-deck
and two-deck PC-mount adjustable variants share the same front shaft/bushing architecture,
while the extra Mode deck grows rearward. This preserves a common PCB-to-panel datum across all
three controls.

Selected parts:
- SW901 Bass: `71BDF30-01-2-AJN`, stop set to 5.
- SW902 Treble: `71BDF30-01-2-AJN`, stop set to 5.
- SW903 Mode: `71BDF30-02-2-AJN`, stop set to 4.

All are non-shorting/BBM, PCB-mount, threaded-bushing Series 71 controls.

## Provenance correction

SR-035 incorrectly described Lorlin as the saved prior BOM baseline. Surviving BOM evidence
shows Grayhill Series 71 was the recorded historical choice. Later cost/commonality work
considered Lorlin and C&K, but the re-run trade selects Grayhill Series 71 because the shared
mechanical datum, PCB mounting, adjustable stops and contact system justify the modest premium.

## G3-024 control-hardware closure

External operating controls now have selected physical hardware. This does not release final PCB
footprints, drilling coordinates or enclosure machining. The internal later RIAA ON/BYPASS
function is intentionally excluded from this hardware freeze until SCH103 node-level
implementation is reconciled.
