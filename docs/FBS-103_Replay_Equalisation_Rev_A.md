# FBS-103 — Replay Equalisation

**Revision:** A  
**Status:** Implemented to controlled-switch-network level  
**External source:** Elliott Sound Products Project 91, retrieved 14 July 2026  
**Source URL:** https://sound-au.com/project91.htm

## Purpose

SCH103 implements selectable replay equalisation for 78 rpm records while retaining true RIAA selections for LP use. The agreed architecture uses the ESP Project 91 adaptation of the Project 06 separate active-bass and passive-treble equalisation sections, with LM4562 devices and nominal ±18 V rails.

## Controlled selections

### Bass / C1

| Position | Selection | C1 |
|---:|---|---:|
| 1 | Flat | 0 nF — switch short |
| 2 | 200 Hz | 56 nF |
| 3 | 400 Hz | 27 nF |
| 4 | 500 Hz, RIAA | 22 nF |

### Treble / C4

| Position | Selection | C4 |
|---:|---|---:|
| 1 | Flat | 0 nF — switch open |
| 2 | 1,600 Hz | 120 nF |
| 3 | 2,121 Hz, RIAA | 82 nF |
| 4 | 3,400 Hz | 56 nF |
| 5 | 5,800 Hz | 33 nF |

## Implementation constraints

- Use one ganged control per EQ function so both channels select the same curve.
- Keep switch wiring electrically short; the switch common shall connect to the sensitive PCB node, with the capacitor ends returned to the low-impedance destinations prescribed by P91.
- Prefer close channel matching over nominal tolerance alone.
- Use stable film capacitors; 1206 is preferred where the required values and voltage ratings are practical.
- Provide test points at EQ input, active-core output and final EQ output for each channel.
- Nominal supply rails are +18 V and -18 V.
- The fitted third RIAA pole remains bypassable as previously agreed; its detailed implementation is not introduced by this patch.

## Deliberate boundary of Rev A

The P91 selection values are frozen and generated. The underlying P06 resistor and gain network is represented as an explicit LM4562 functional block until its exact integration values are reconciled with Shellac's preceding differential gain and following buffer. No resistor or gain value is guessed.

## Verification

- Confirm all four bass and five treble positions against the controlled table.
- Confirm left/right capacitor matching before assembly.
- Sweep each selection and record turnover/roll-off response.
- Confirm RIAA selections at 500 Hz and 2,121 Hz.
- Confirm no oscillation or measurable response shift due to switch wiring.
