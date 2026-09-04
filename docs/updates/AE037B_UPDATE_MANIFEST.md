# AE-037B update manifest

Removes the stale hard-coded board-population value from
`tests/test_preliminary_placement.py`.

The invariant is now relational:

`len(placement.proposals) == len(contract.board_population_refs)`

rather than duplicating a numeric population count in multiple tests.

Run:

`APPLY_AE037B.bat`

If green, continue with:

`build_shellac.bat`

then:

`python -m pytest`
