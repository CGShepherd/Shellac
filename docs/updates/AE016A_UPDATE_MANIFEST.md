# AE-016A repair manifest

Apply over an **uncommitted AE-016 working tree**.

Restores:
- generator/model/balanced_input.py

Replaces:
- tests/test_dr038_dr039.py
- DR-038 selected decision staging text

Retains:
- generator/model/post_eq_dc_block.py
- DR-039 SCH103 physical patch

Does NOT apply:
- AE-016 `signal_chain_analysis.py` modification.

If AE-016 already modified `signal_chain_analysis.py`, run the repair script
included in this package.

Then run:
`python -m pytest`
