# SR-021G1 — Legacy Provenance Migration

**Scope:** provenance verification only

## Defect

SR-021G introduced the correct immutable/mutable distinction but assumed the
existing `build_provenance.json` already used the new structure. Accepted
SR-021F repositories still used the previous schema, producing:

- `missing=ProjectShellac.kicad_pro`
- a mismatched Build ID

## Correction

During verification, legacy `.kicad_pro` entries are moved from `files` to
`mutable_files` in memory and the immutable Build ID is recalculated. The
on-disk provenance document remains untouched. A future successful build
naturally writes the current schema.

This is a compatibility migration, not a relaxation of schematic integrity.
