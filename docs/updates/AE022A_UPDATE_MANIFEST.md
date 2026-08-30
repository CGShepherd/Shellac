# AE-022A update

Apply over the current uncommitted AE-022 migration tree.

Run:
`APPLY_AE022A.bat`

The script applies the full closure, generates the stale-contract audit and runs
the complete pytest suite. Do not commit until pytest and normal build/ERC are clean.
