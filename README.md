# Shellac AE-058 Rev A4 — numerical correlation closure

This increment addresses the two remaining numerical correlation mismatches
without weakening acceptance tolerances.

Changes:
- removes the artificial 1 GΩ matrix-node load so LTspice correlates the same
  unloaded ideal averaging quantity as AE-055;
- increases DR039 AC sweep density from 200 to 2000 points/decade;
- adds regression assertions for both numerical-contract choices;
- adds AE-058 Rev A2 numerical-closure evidence.

Apply from the Shellac repository root:

    python <extracted-folder>\APPLY_AE058_A4.py

Then run:

    python -m pytest tests/test_ltspice_correlation.py -q
    python -m simulation.scripts.ltspice_correlation
    python -m pytest -q
    git diff --check
