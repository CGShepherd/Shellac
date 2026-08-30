# AE-022B — LT5400 Converter Routing Closure

AE-022A exposed a real generated-schematic short between 0VA and PRE_EQ_L/R.
AE-022B removes the long diagonal LT5400 feedback route and separates the plus,
minus, reference and feedback connections into explicit non-crossing Manhattan
corridors. EP9 remains explicit no-connect.

The regression suite is strengthened so SCH101 must have no named-net conflicts
and no unterminated pins.
