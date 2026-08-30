# AE-022G definitive snapshot fix

Apply to the exact working state represented by
`temp/dr038-debug-snapshot` commit `6c9290e`.

Run:

`APPLY_DR038_DEFINITIVE_FIX.bat`

The batch applies the fix, prints the SCH101 audit result, and runs the complete
pytest suite.

Do not merge to main yet. If green, run the normal Shellac build/native ERC,
then push the corrected development state for review.
