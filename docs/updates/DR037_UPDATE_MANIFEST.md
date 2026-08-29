# DR-037 implementation package

Base branch: `feature/dr-037-riaa-rollback`
Verified remote branch tree: `8257c1a986ff240eafce25add0ff141346694155`

## Purpose

Implement DR-037 in the active repository state:

- retain legacy complete RIAA in SCH103;
- remove the later optional independent 3180 us engineering implementation;
- remove its BOM/procurement entries;
- correct AE-011 executable model from the accidentally pushed A0 version to A1;
- add regression tests for restored complete RIAA.

## Files replaced

- `generator/model/signal_chain_analysis.py`
- `config/bom/shellac_bom.yaml`
- `config/procurement/sourcing_snapshot_2026-08-24.yaml`

## Files added

- `tests/test_signal_chain_analysis.py`

## Files deleted by APPLY_UPDATE.bat

- `generator/model/riaa_optional_pole.py`
- `generator/model/riaa_optional_pole_realisation.py`
- `generator/model/riaa_integration_audit.py`
- `tests/test_riaa_optional_pole.py`
- `tests/test_riaa_optional_pole_realisation.py`
- `tests/test_riaa_integration_audit.py`

The G3-025/G3-026/G3-027 documentation remains untouched as historical evidence.

## Important verification result

The active root engineering model and dispatcher already use the direct
`SCH101 -> SCH103 -> SCH107 -> SCH104 -> SCH105 -> SCH108` architecture and
never registered an independent 3180 us functional block. SCH109 also contains
only Bass, Treble, Mode, Rumble and Mute controls. No root-hierarchy or control
rewrite is required.

## Apply

Extract this ZIP into the Shellac repository root and run:

`APPLY_UPDATE.bat`

The script copies/replaces the packaged files and removes the superseded optional-RIAA model/test files.

Then run:

`python -m pytest`

and, if clean:

`git status`
`git add -A`
`git commit -m "feat(riaa): implement DR-037 legacy complete-RIAA rollback"`
`git push`

