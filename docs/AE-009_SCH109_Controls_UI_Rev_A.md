# Project Shellac — AE-009 SCH109 Controls and User Interface

**Revision:** A  
**Status:** electrically closed  
**Date:** 14 July 2026

## External operating controls

| Control | Hardware | Positions |
|---|---|---|
| Bass characteristic | Linked stereo 2P5 rotary | Flat, 200 Hz, 400 Hz, 500 Hz 78, True RIAA |
| Treble characteristic | Linked stereo 2P5 rotary | Flat, 1600 Hz, 2121 Hz RIAA, 3400 Hz, 5800 Hz |
| Channel mode | 4P4T rotary | Stereo, Dual Left, Dual Right, L+R Mono |
| Rumble filter | Stereo 2P2T toggle | Filter, Bypass |
| Output mute | Stereo 2P2T toggle | Play, Mute |

All analogue switches are break-before-make.

The true-RIAA operating combination is:

```text
BASS = TRUE RIAA
TREBLE = 2121 Hz RIAA
```

No mechanical interlock is required; the panel and operating guide shall make
the combination explicit.

## Rail indicators

Two independent panel LEDs indicate the presence of +18 V and -18 V.

Each LED uses an 8.2 kΩ series resistor. With an assumed 2.0 V forward drop,
nominal current is approximately 1.95 mA. The electrical design tolerates
ordinary low-current indicators with roughly 1.8–2.4 V forward voltage.

The negative-rail LED is wired with its anode at 0VA and cathode through its
series resistor to -18 V.

## Mechanical and wiring constraints

- Controls and LEDs are top-panel mounted.
- Switches are off-board in the current generated representation.
- Bass and treble switch wiring shall be kept especially short.
- Left/right wiring shall be symmetrical.
- Control bodies and panel nuts shall not be relied upon as the sole PCB
  support unless the final mechanical design explicitly validates that method.
- Aluminium knobs shall have a visible index line.
- Panel legends shall use the exact position names in this document.

## Internal gain selection

The previously agreed internal gain-selection requirement belongs to SCH101,
not SCH109. The current SCH101 generated implementation does not yet expose
that selector. AE-009 does not invent a control connection without a resolved
SCH101 topology; this remains an explicit SCH101 closure item.

## Corrections captured

AE-009 also corrects two stale engineering-model statements:

- SCH103 now has independent BASS_SELECT and TREBLE_SELECT interfaces rather
  than one generic CURVE_SELECT.
- SCH104 is recorded as unity gain following AE-008; THAT1646 supplies the
  final 2× differential gain.
