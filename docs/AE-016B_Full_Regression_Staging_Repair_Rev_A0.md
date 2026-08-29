# AE-016B — Full Regression Staging Repair

AE-016 caused two premature implementation migrations: DR-038 in the central
SCH101 model and DR-039 in the SCH103 physical builder. AE-016A repaired the
first class and reduced failures from 24 to 17.

AE-016B restores SCH103 to the pre-DR039 physical baseline while retaining the
DR-039 analytical model and selected decision. Both DR-038 and DR-039 will be
implemented later as atomic CAD/dependency migrations.

Apply with `APPLY_UPDATE.bat`, then run `python -m pytest`. Do not commit unless
the suite is clean.
