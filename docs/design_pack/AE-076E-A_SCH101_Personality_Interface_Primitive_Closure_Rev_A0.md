# AE-076E-A — SCH101 Personality Interface Primitive Closure — Rev A0

**Parent governed baseline:** `4975fba11a12f25744e35ea61e11578c66f3d50f`
**Parent authority:** AE-076D
**Status:** EXACT INTERFACE PRIMITIVE IMPLEMENTED — LIVE SCH101 / NATIVE PCB MIGRATION OPEN
**Release effect:** NONE — routing/layout/BOM/manufacturing permissions remain FALSE

## 1. Purpose

AE-076E-A creates the exact CAD/electrical primitive required by the AE-076C
per-channel passive cartridge-personality architecture without creating an
intermediate mismatch between the generated schematic and native PCB.

The live product circuit is deliberately unchanged by this increment.
AE-076E-B will replace the current ganged H120/H121/H122 plus
C103/C104/C203/C204 implementation with local H120/H220 personality sockets
and reconcile the native KiCad board by guarded F8.

## 2. Read-only baseline evidence

The pre-implementation probe confirmed:

- `develop`, HEAD and `origin/develop` all at
  `4975fba11a12f25744e35ea61e11578c66f3d50f`;
- no staged or tracked working changes;
- native board SHA-256
  `2e8934d9357f85cda82a47e7a19524c5fd76b1d8357f6c2a95cfaa559b0b1417`;
- 0 routed segments and 0 vias;
- In1.Cu and In2.Cu are present;
- live H120/H121/H122 and C103/C104/C203/C204 are present;
- H220 is absent;
- generator board population is 257;
- H120/H121/H122 are owned by CLU-101-F;
- C103/C104 are owned by CLU-101-A and C203/C204 by CLU-101-C.

These facts define the AE-076E-B discriminator.

## 3. Exact interface primitive

Main-board socket:

- Samtec `SLW-102-01-G-D`;
- 2 rows x 2 positions;
- 2.54 mm pitch and row spacing;
- through-hole;
- manufacturer recommended 0.86 mm PTH;
- mating card header `TSW-102-07-G-D`.

Controlled footprint:

`ProjectShellac:Samtec_SLW-102-01-G-D_2x02_P2.54mm_Vertical`

Manufacturer footprint source reviewed:

`https://suddendocs.samtec.com/prints/slw-1xx-01-x-x-footprint.pdf`

## 4. Pin contract

| Pin | Node |
|---|---|
| 1 | POS |
| 2 | NEG |
| 3 | NEG |
| 4 | POS |

A 180-degree rotation exchanges 1<->4 and 2<->3, preserving both nodes.

Generated semantic pin names are `POS_A`, `NEG_A`, `NEG_B`, `POS_B`.

## 5. Fail-safe behaviour

The card is a differential shunt only. The cartridge signal does not pass in
series through it. No card therefore remains BASE and cannot interrupt signal
continuity.

Service-card capacitor value/tolerance/matching and connector/card parasitic
capacitance remain RUN10 / pre-fabrication work.

## 6. 3D boundary

AE-076E-A attaches no generic 2x2 3D model to the exact SLW footprint. Exact
SLW/TSW mated geometry remains an AE-076E-B/full-MCAD item.

The read-only probe also disproved the earlier assumption that the local KiCad
9 installation contains the H901 Mini-Fit Jr model at the canonical
`.wrl`/`.step` path. H901 closure is therefore deferred to AE-076E-B and must
not be represented as a simple extension substitution.

The C30060/C35060 capacitor WRL is locally present and matches the controlled
AE-076B2C hash, but its native binding is likewise outside AE-076E-A.

## 7. Live state after AE-076E-A

Intentionally unchanged:

- H120/H121/H122 remain live;
- C103/C104/C203/C204 remain live;
- H220 remains absent;
- AE-076C remains `CURRENT_SELECTED_PENDING_IMPLEMENTATION`;
- RUN10 interface parasitic/matching work remains open;
- all release permissions remain FALSE.

## 8. AE-076E-B entry conditions

AE-076E-B must atomically close:

1. live H120/H220 source migration;
2. removal of C103/C104/C203/C204/H121/H122;
3. placement ownership migration to CLU-101-A / CLU-101-C;
4. BOM/current-authority reconciliation;
5. guarded KiCad F8;
6. Edge.Cuts and MH1-MH4 preservation;
7. H120/H220 pad/net proof;
8. H901 and C30060/C35060 model-path resolution;
9. native audit and STEP evidence.

## 9. Disposition

**AE-076E-A interface primitive:** PASS FOR GOVERNED CHECKPOINT.
**Live personality migration:** OPEN — AE-076E-B.
**Routing/layout:** HOLD.
**Manufacturing:** HOLD.
