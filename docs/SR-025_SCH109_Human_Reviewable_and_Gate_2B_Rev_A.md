# SR-025 — SCH109 Human-Reviewable Conversion and Gate 2B Candidate

**Scope:** controls and indicators presentation only

## Presentation

- BASS, TREBLE, MODE, RUMBLE and MUTE appear as explicit panel-state interfaces.
- +18 V and -18 V indicators are complete series branches.
- Indicator test points tap the resistor/LED junction with horizontal conductors.
- Both LED returns terminate at a clearly labelled 0VA node below the device.
- Internal LED-drive net labels are not used.

## Design preservation

The five control inventories, positions and switching behaviour are unchanged.
Both indicators retain 8.2 kΩ series resistors and approximately 1.95 mA nominal
current.

A clean native KiCad ERC on the combined SR-024/SR-025 build is required before
Gate 2B is accepted.
