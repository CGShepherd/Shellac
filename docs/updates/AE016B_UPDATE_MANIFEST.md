# AE-016B repair manifest

Apply over the current uncommitted AE-016 + AE-016A working tree.

Changes:
- restore `generator/blocks/replay_eq.py` to its pre-DR039 physical baseline;
- retain `generator/model/post_eq_dc_block.py`;
- restage DR-039 as SELECTED / CAD migration pending;
- replace `tests/test_dr038_dr039.py` with staging-safe assertions;
- restore the AE-012 signal-chain calculation if it is still patched.

Run:
`APPLY_UPDATE.bat`
`python -m pytest`
