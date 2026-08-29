# AE-017 update manifest

Base commit: `6d34fa0b6c808b541576b79f6f1ba6b8313c6fad`

Adds only:
- `tools/ae017_dependency_map.py`
- `tests/test_ae017_dependency_map.py`
- `docs/AE-017_Atomic_Migration_Dependency_Mapping_Gate_Rev_A0.md`
- `docs/updates/AE017_UPDATE_MANIFEST.md`

No active circuit, CAD, BOM, or analysis baseline is modified.

Run:
`python tools/ae017_dependency_map.py`
`python -m pytest`

If clean, inspect:
`docs/AE-017_Generated_Atomic_Migration_Dependency_Map.md`

Suggested commit after generation:
`git add -A`
`git commit -m "analysis(migration): map DR-038 and DR-039 atomic dependencies"`
`git push`
