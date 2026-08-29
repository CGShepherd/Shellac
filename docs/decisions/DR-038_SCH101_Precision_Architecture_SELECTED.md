# DR-038 — SCH101 precision architecture

**Status:** SELECTED — CAD/DEPENDENCY MIGRATION PENDING

The 4.00x LT5400-7 / low-impedance architecture remains the selected next SCH101
implementation. It is intentionally **not yet substituted into the active
`balanced_input.py` baseline**.

Reason: the current generator, schematic builder, AE-010/AE-012 regressions and
precision/noise assurance suite are mutually coupled to the proven 3.48x
implementation. DR-038 shall be migrated atomically when the correct LT5400
MSOP-8 CAD component and precision service-link implementation are available.

This staging rule supersedes the over-eager AE-016 attempt to replace the
central model before its dependent CAD/tests were migrated.
