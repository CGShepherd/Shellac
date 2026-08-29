# AE-016 update manifest

Base commit: `21a7bbe208147802e57de5be75157c7d5c326a86`

Replaces:
- generator/model/balanced_input.py

Adds:
- generator/model/post_eq_dc_block.py
- tests/test_dr038_dr039.py
- selected DR-038 / DR-039 decision records
- AE-016 implementation baseline

Patch scripts update:
- generator/blocks/replay_eq.py
- generator/model/signal_chain_analysis.py

Apply:
`APPLY_UPDATE.bat`
`python -m pytest`

Suggested commit:
`git add -A`
`git commit -m "feat(signal-chain): implement DR-038 precision gain and DR-039 DC block"`
`git push`
