# AE-016A — AE-016 Regression Repair

AE-016 caused broad regressions by replacing the authoritative central SCH101
model before the LT5400 CAD implementation and dependent tests had been migrated.

The existing suite explicitly freezes the active converter at 3.48x. That test
is valid for the current physical generator baseline and must not simply be
weakened.

AE-016A therefore:
- restores `generator/model/balanced_input.py` exactly to the pre-AE016 baseline;
- retains DR-038 as SELECTED, but stages it for an atomic CAD/test migration;
- retains DR-039 as the implementable independent change;
- removes the AE016 patch to `signal_chain_analysis.py` from the apply process;
- makes the SCH103 DR-039 patch idempotent.

After AE-016A the active SCH101 generator should again satisfy the historical
regression suite, while the 4x precision candidate remains preserved in
`sch101_precision_candidate.py` for the next controlled migration.
