# AE-039B1 — SCH103 Allocation Reference Correction

AE-039A used `U301/U302` and `U351/U352` for SCH103. The live replay-EQ builder
actually generates `U3001/U3002` and `U3501/U3502`.

That mismatch meant AE-039B absorbed only six of the intended eight pseudo-
packages, yielding 248 rather than 246 physical PCB items.

Correct physical allocation:
- U3001A / U3001B = logical U3001 / U3002, OPA1612
- U3501A / U3501B = logical U3501 / U3502, OPA1612

Expected board population after AE-039B/B1: **246**.

A new cross-layer regression requires the allocation authority to match the
actual generated op-amp references exactly.
