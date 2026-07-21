# SR-023A — SCH108 ERC Closure

**Trigger:** SR-023 native ERC: 26 errors and 4 warnings  
**Scope:** SCH108 presentation geometry and hierarchy attachment only

## Root causes

1. Both mute outputs used the same vertical routing lane, creating overlapping
   channel conductors and leaving the switch output pins unresolved in KiCad.
2. Each OUT-to-SNS capacitor routed both terminals back to one common route
   point, electrically shorting the capacitor in the drawing.
3. RFI-capacitor near/far pin selection assumed nominal symbol orientation
   rather than rendered sheet coordinates, causing overlapping branches across
   the capacitor terminals.
4. The four output hierarchy interfaces were not labelled on the real XLR
   conductors, so the hierarchy adapter generated isolated fallback anchors.

## Corrections

- Separate mute output lanes are derived from the channel index.
- Sense capacitor placement lies between its matching OUT and SNS pins, with
  each capacitor terminal routed independently to one driver pin.
- RFI capacitor terminals are selected by actual distance to the signal leg.
- Output hierarchy labels are placed at explicit protected-output branch
  points on the continuous XLR conductors.

The THAT1646 topology, mute function, protection values and XLR assignments
remain unchanged.
