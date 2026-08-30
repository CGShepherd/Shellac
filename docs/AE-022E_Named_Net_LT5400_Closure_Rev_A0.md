# AE-022E — Named-Net LT5400 Closure

The LT5400/Ux03 converter is now represented using short local stubs plus
explicit named nets for PLUS_SRC, PLUS_SUM, MINUS_SRC, MINUS_SUM and FB_OUT.
The 0VA reference remains local to LT5400 pin 5 and EP9 remains no-connect.

This preserves the DR-038 electrical architecture while removing long graphical
conductors from the converter region, eliminating accidental junctions caused by
crossings or semantic pins lying on route segments.

The SCH101 net tracer now configures its repository import path correctly.
