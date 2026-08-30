# AE-022H — Final DR-038 Regression Closure

Basis: `temp/dr038-debug-snapshot` at commit `031f431`.

The DR-038 electrical implementation and internal SCH101 audit are already clean.
This closure migrates the final two stale regression assumptions:

1. `PRE_EQ_L/R` now deliberately appear twice: once on the Ux03 output/feedback
   local net and once as the exported sheet interface.
2. LT5400 pin 5 now uses a horizontal 0VA stub so the label is deliberately
   displaced from the shared right-pin column.

No generator, component, electrical-value, symbol, footprint, placement or
decision-record changes are made in AE-022H.
