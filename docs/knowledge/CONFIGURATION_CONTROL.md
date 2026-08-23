# Project Shellac — Knowledge and Configuration Control

**Status:** ACTIVE  
**Introduced:** SR-035

## Authority hierarchy
1. Frozen versioned engineering evidence and machine-readable configuration in Git.
2. Selected/proposed versioned decisions in Git.
3. Reconstructed historical intent recorded in Git with explicit provenance.
4. Conversation history, supplier browsing and interim working notes.

A lower level cannot silently override a higher level.

## Decision lifecycle
`PROPOSED` → `SELECTED` → `FROZEN`; also `DEFERRED`, `REJECTED`, and `SUPERSEDED`.

## Provenance
- `REPOSITORY_EVIDENCE` — directly supported by an existing controlled artefact.
- `RECONSTRUCTED_PRIOR_INTENT` — recovered from earlier project/BOM work but not previously promoted into Git.
- `NEW_ANALYSIS` — introduced by the current package.
- `PROCUREMENT_SNAPSHOT` — dated volatile price/stock/source evidence.

Reconstructed intent must not be described as historically frozen unless repository evidence proves that status.

## Package acceptance
A material package updates, where applicable, the decision register, controlled BOM, project status, risk/open-item register, detailed evidence and deterministic validation/tests.

## Superseding a frozen decision
Record the old decision ID, reason for reopening, new evidence, affected interfaces, risk impact, migration consequences and replacement decision. Preserve the old record as `SUPERSEDED`.
