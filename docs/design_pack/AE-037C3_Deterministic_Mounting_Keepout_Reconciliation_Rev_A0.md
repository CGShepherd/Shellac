# AE-037C3 — Deterministic Mounting Keepout Reconciliation

**Revision:** A0  
**Supersedes:** AE-037C, AE-037C1, AE-037C2  
**Status:** PHYSICAL PLACEMENT RECONCILIATION

## Root cause

AE-037 added two 0805 load/bias resistors to each front cartridge-input cluster.
The added parts increase each input cluster from six to eight PCB components.

With six components, the normal deterministic grid packer fits the cluster. With
eight components, conservative envelope overlap causes the packer to select its
shelf fallback. At the existing 1.5 mm shelf margin, the front JST connector
envelope is too close to the frozen front-corner mounting-hole keepout.

For the left front cluster, using the frozen geometry:

- MH1 centre: (5, 8) mm;
- keepout radius: 4.0 mm;
- shelf-packed H101 nearest-envelope distance at 1.5 mm margin: approximately
  3.54 mm — collision;
- corresponding distance at 2.0 mm margin: approximately 4.12 mm — clear.

The right channel is geometrically symmetric about the board centreline.

## Resolution

Set a **2.0 mm minimum packing margin** for `CLU-101-A` and `CLU-101-C` only.

Apply the rule identically in both deterministic packers:
- normal grid packer;
- shelf fallback packer.

No component receives an arbitrary hand-coded coordinate. The existing packer
remains authoritative and the minimum change is 0.5 mm.

## Test-authority repair

Remaining old `250` population assertions are replaced by relationships to the
live footprint contract where appropriate.

## Tooling cleanup

AE-037C/C1/C2 helper files are removed as superseded. C3 contains no iterative
search loop and no subprocess search.
