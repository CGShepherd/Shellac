# AE-018 update manifest

Base commit: `e26ce0959e98a49be90468629ea55d2e3f616768`

Adds only:
- `generator/model/precision_cad_contract.py`
- `tests/test_precision_cad_contract.py`
- `docs/AE-018_Live_Dependency_Disposition_and_Precision_CAD_Primitives_Rev_A0.md`
- `docs/decisions/DR-040_Precision_CAD_Primitive_Staging_SELECTED.md`
- `docs/updates/AE018_UPDATE_MANIFEST.md`

No active SCH101/SCH103 circuit or CAD builder is changed.

Validate:
`python -m pytest`

Suggested commit:
`git add -A`
`git commit -m "analysis(cad): freeze LT5400 precision primitive contract"`
`git push`
