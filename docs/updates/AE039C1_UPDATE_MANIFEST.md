# AE-039C1 — residual synthetic op-amp 0VA cleanup

Apply directly on top of the current failed AE-039C working tree.

AE-039C correctly removed `0VA` from the real buffer pin contract, but three
builder calls survived because the original patch matched their formatting too
narrowly.

C1:
- removes residual op-amp/buffer `0VA -> 0VA` calls in SCH104/105/107;
- preserves and verifies the AE-039C explicit OUT-to-IN- follower feedback;
- adds a source-level regression preventing the synthetic ground pin from
  returning.

Run:

`APPLY_AE039C1.bat`

If targeted tests pass:

`build_shellac.bat`

then:

`python -m pytest`

Expected physical population remains 246.
