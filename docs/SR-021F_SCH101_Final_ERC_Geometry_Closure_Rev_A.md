# SR-021F — SCH101 Final ERC Geometry Closure

**Trigger:** SR-021E native ERC: 8 errors and 6 warnings  
**Scope:** SCH101 routing geometry only

## Root cause

The remaining findings had two causes:

1. Multi-segment feedback and reference conductors contained bend endpoints that KiCad treated as dangling.
2. The reference resistor's leftward 0VA stub landed on the minus-leg output conductor, joining both channel outputs to the common 0VA domain through hierarchy.

## Correction

- Gain-leg feedback base resistors return directly to their op-amp outputs.
- Differential feedback resistor pin 2 connects directly to OUT.
- Differential feedback resistor pin 1 connects directly to IN-.
- Differential reference resistor pin 2 connects directly to IN+.
- Differential reference resistor pin 1 reaches 0VA vertically.
- Tests explicitly reject any 0VA label at U102/U202 output coordinates.

The approved electrical design is unchanged.
