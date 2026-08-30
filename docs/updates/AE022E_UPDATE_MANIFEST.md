# AE-022E update

Apply over the current uncommitted AE-022 through AE-022D tree.

Run:
`APPLY_AE022E.bat`

The batch rewrites the converter with named nets, updates regressions, runs the
connectivity tracer, then executes the full pytest suite.

If green, run the normal Shellac build/native ERC before committing DR-038.
