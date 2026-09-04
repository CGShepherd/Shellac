# AE-037A update manifest

Run from repository root:

`python tools/apply_ae037a_placement_reconciliation.py`

Then targeted validation:

`python -m pytest tests/test_ae037a_placement_reconciliation.py tests/test_cluster_placement_baseline.py tests/test_preliminary_placement.py tests/test_real_footprint_audit.py -v`

If green:

`build_shellac.bat`

Then:

`python -m pytest`

No manual source editing is required.
