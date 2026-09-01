# AE-025A — Authority Reconciliation Regression Repair

**Revision:** A0  
**Status:** REPAIR

AE-025 introduced two regressions:

1. `authoritative_current_status` was written as a YAML block list, but AE-024A's
   deliberately narrow standard-library parser only reads top-level inline lists.
2. `baseline.branch` in the authoritative current decision index was changed from
   `main` to `develop`. That field describes the validated implementation baseline,
   not the working development branch.

AE-025A restores the intended semantics:

- scoped status vocabularies are expressed as inline lists;
- `baseline.branch` remains `main`;
- the temporary `authority_scope` line is removed from the decision index;
- working-on-`develop` guidance remains in README/design-pack documentation rather
  than corrupting baseline provenance.

No circuit, CAD, BOM or assurance model is changed.
