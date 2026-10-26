# AE-076F5U — Active engineering workspace cutover — Rev A0

**Date:** 26 October 2026

**Scope:** Administrative engineering-workspace change only.

**Status:** GOVERNED WORKSPACE DECISION upon successful commit and push.

**Baseline:** `develop` at `1f8293d9de4286850bcaf2df33311416ef410f86` before this transaction.

## Decision

Use `C:\Engineering\Shellac` as the single normal **active** Project Shellac Git checkout.
Its independent virtual environment is `C:\Engineering\Shellac\.venv`.
The Git remote is `https://github.com/CGShepherd/Shellac.git`.

Retain `C:\Users\chris\Dropbox\000_Projects\000_Audio\Shellac` unchanged as a
**procedurally read-only rollback reference**, not as a second active checkout.
Procedural protection is not OS access-control protection. Do not rename, delete,
reset, merge or edit that old checkout as part of this transaction.

This document governs **workspace use only**. It does not modify electrical,
mechanical, CAD, fabrication, BOM, procurement, routing or release authority.

## Verified qualification chain

- F5P: KiCad 9.0.8 / 10.0.7 netlist and native STEP equivalence; full model resolution.
- F5Q: 201 individual exported solids geometrically matched; isolated schematic generator qualified.
- F5R-D1: the abandoned raw-overlay clone was rejected and diagnosed; no promotion.
- F5R-FIX1: Git-native tracked checkout, 811 tracked objects, 752 nontracked assets recovered; 771 tests passed.
- F5S: self-contained Python environment at new location, 771 tests, decision audit and KiCad10 readback passed.
- F5T: both checkouts clean and matching GitHub `develop`; 811 tracked entries and 752 nontracked assets SHA-256 verified in both locations.
- Accepted source PCB SHA-256: `a5b519a21a2bbe2c9f3ad751134d43292a5b32184487100512ab045b6258861c`.
- F5T evidence archive SHA-256: `612cf032c3d5c64e55b33833767c06888f54355cbe45b517bb26f7215d493f0a`.

## Remaining holds and next actions

1. KiCad 10.0.7 is technically qualified for reading, generator execution and 3D equivalence, but the live project still contains `KICAD9_FOOTPRINT_DIR` / `KICAD9_3DMODEL_DIR` references and a KiCad9 CLI fallback. **Retain KiCad 9** pending a separately qualified governed migration.
2. ERC14, DRC336 and 432 unconnected findings are not manufacturing acceptance. Preserve all existing routing/layout/BOM/fabrication/PDR/CDR release holds.
3. Native PCB remains **220 × 140 mm**. The 220 × 148 mm candidate, four NKK controls, two C&K cover-mounted toggles and independent three-pillar TE matrix plate are selected-next/held as previously governed. This workspace change does not supersede their authority or close physical qualification.
4. Source commits must be pushed to GitHub after governed changes; ignored/vendor/STEP and staging evidence require separate independent backup. Before retiring the Dropbox rollback reference, qualify a **new-location backup and a cloud restoration test**.
5. Do not treat the 752 recovered local assets as a uniformly authoritative collection; historical evidence and caches retain their original governance status.
6. Future local commands should run from `C:\Engineering\Shellac` and its `.venv` rather than the Dropbox checkout.

## Recovery

If local repository integrity becomes doubtful, stop engineering edits; preserve the
failed checkout and review its evidence. Recover tracked content from a verified
GitHub commit and essential ignored assets from separately controlled backups.
Do not blindly reconcile or merge the original Dropbox checkout with the active
local checkout.
