# SR-023B — SCH108 Sense-Loop ERC Closure

**Trigger:** SR-023A native ERC: 10 errors, 6 warnings.

All findings were confined to the four THAT1646 common-mode capacitors.  The
previous orthogonal routes used two wire segments per terminal.  KiCad treated
the bend segments as dangling.  Each terminal now uses one direct conductor
between the driver pin and capacitor pin.  The electrical topology is unchanged.
