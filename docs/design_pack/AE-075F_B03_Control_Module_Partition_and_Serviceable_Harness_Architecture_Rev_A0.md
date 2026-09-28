# AE-075F — B03 Control-Module Partition and Serviceable Harness Architecture — Rev A0

**Project:** Shellac
**Status:** CLOSED — PRE-ROUTING DESIGN IMPLEMENTATION VALIDATED
**Baseline:** `b2229860369c6be87b8d411ef6be8ba25f7747f9`

## Purpose

Continue AE071-B03 after AE-075E by freezing the number/function partition of the local control PCBs and the inter-board connection architecture without prematurely freezing exact connector footprints, top-cover Z/support hardware or the RUN10-dependent EQ passive partition.

## Selected control-module partition

Shellac shall use four local control PCBs:

1. `EQ_L` — left Bass + left Treble NKK controls.
2. `EQ_R` — right Bass + right Treble NKK controls.
3. `RUMBLE` — SW904 C&K 7201SYCBE.
4. `MATRIX_MUTE` — SW903 C&K A30403RNCB plus SW905 C&K 7201SYCBE.

Combining Matrix and Mute is selected because their signal-chain regions are adjacent and the matrix L/R outputs can feed the mute locally on the same PCB. This reduces the combined downstream main-board interface to seven unique external nets: `BUFFERED_L`, `BUFFERED_R`, `MONO_AVG`, `MONO_R_LEG`, `0VA`, and the two post-mute THAT1646 input feeds.

Rumble remains separate because its six switched nets belong to the SCH107 direct/filter selection region and should not be extended rearward merely to reduce PCB count.

## Interconnect architecture

Rigid board-to-board coupling between a local control PCB and the main audio PCB is rejected as the current architecture.

Each local control PCB shall instead use a **short detachable wire harness** to the main PCB. This decouples control-plane tolerance from the main-board/carrier datum and preserves removable-cover serviceability.

The switch pins themselves remain soldered to their local PCB. Therefore the selected harness is an **inter-board** harness and does not violate the G3-019 prohibition on flying switch/potentiometer terminals.

## Connector-family selection

The selected family is **Molex Micro-Lock Plus 2.00 mm**.

Controlled family-level attributes:

- positive-lock wire-to-board system;
- single-row 2–16-circuit options;
- vertical `505575` and right-angle `505578` PCB-header series;
- `505570` receptacle housing series;
- existing Shellac-selected female crimp terminal `5055721200`;
- gold-plated PCB-header options are available.

This reuses the connector ecosystem already selected for the Shellac cartridge-input harness.

Exact header orientation/order code and final circuit count are not frozen by AE-075F because they depend on final Z/XY and the EQ passive-partition discriminator.

Manufacturer sources:
- `https://www.molex.com/en-us/products/series-chart/505575`
- `https://www.molex.com/en-us/products/series-chart/505578`
- `https://www.molex.com/en-us/products/series-chart/505570`
- `https://www.molex.com/content/dam/molex/molex-dot-com/en_us/pdf/datasheets/987651-4888.pdf`

## Interface census

- `RUMBLE`: six unique external switched nets; six circuits is the functional minimum before optional guard/spare conductors.
- `MATRIX_MUTE`: seven unique external nets with Matrix-to-Mute routing local to the module; eight circuits is the natural minimum family size if one spare/guard position is retained.
- `EQ_L` / `EQ_R`: exact count intentionally remains open. Migrating the switch-local Bass R-C branches and Treble shunt capacitors onto each EQ mezzanine reduces the main-board interface to four unique nets per channel, but that physical passive partition remains subject to the B03/RUN10 parasitic discriminator.

## Mechanical boundary

AE-075F selects detachable harness coupling but does not freeze how the local PCBs are supported relative to the upper cover. PCB/standoffs must still establish each local-board datum before C&K bushings are tightened; NKK installed-panel geometry remains governed by its 12.3 mm datum.

The exact local-board standoffs/brackets, cover thickness, C&K installed PCB planes, connector orientation and harness lengths remain open.

## B03 disposition after AE-075F

Resolved/narrowed:

- exact control MPNs;
- local PCB ownership;
- four-module partition;
- combined Matrix+Mute downstream module;
- Rumble separate local module;
- detachable short inter-board harness architecture;
- Molex Micro-Lock Plus 2.00 mm family selected;
- rigid board-to-board control coupling rejected as the current architecture.

Still open:

1. main-PCB/carrier Z relative to upper cover;
2. local-control-board installed stack and mechanical support;
3. exact Micro-Lock Plus header variants, circuit counts, footprints and pin maps;
4. EQ switch-local passive ownership and RUN10 parasitic/stability acceptance;
5. exact control footprints/courtyards/body envelopes;
6. control XY/keep-outs and top-cover apertures;
7. physical CAD migration.

Routing, layout freeze, BOM freeze and manufacturing release remain unauthorised.

## Validation result

AE-075F qualification completed against the clean AE-075E governed baseline:

- full regression suite: **703 passed**;
- generated KiCad provenance: PASS, build ID `cdc403ccf951d4d8`, 14 immutable files verified;
- native hierarchical ERC: **0 violations**;
- native PCB integrity: PASS;
- routing authority: **false**;
- integrated preflight: PASS;
- decision/configuration authority audit: PASS;
- historical provenance regression for AE-071A and AE-075B: PASS;
- working-tree `git diff --check`: PASS.

AE071-B03 remains open for main-PCB/carrier Z, local-board installed stack/support, exact Micro-Lock Plus variants/circuit counts/footprints, EQ passive ownership and RUN10 parasitic/stability acceptance, exact control footprints/courtyards/body envelopes, XY keep-outs and physical CAD migration.

Routing, layout freeze, BOM freeze and manufacturing release remain explicitly unauthorised.
