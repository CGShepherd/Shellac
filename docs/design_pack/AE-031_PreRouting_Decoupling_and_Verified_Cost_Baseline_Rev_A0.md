# AE-031 — Pre-Routing Decoupling and Verified Cost Baseline

**Revision:** A0  
**Status:** PRE-ROUTING / COST BASELINE

## Purpose

AE-031 clears work that can proceed before the Lorlin PT sample/MPNs arrive and
establishes the first evidence-backed running BOM subtotal.

## Verified running BOM snapshot — 3 September 2026

Current verified design-BOM subtotal:

**£233.67 ex VAT**

This includes:

- two METCASE M5502119 enclosures: £187.10;
- two C&K 7201SYCBE toggles: £23.82;
- one SCHURTER KMF1.1121.11: £22.75.

The Lorlin rotary set remains UNQUOTED and is therefore excluded from the
subtotal rather than treated as zero cost.

This is not yet a complete Shellac BOM: electronics, PCB fabrication,
connectors/wiring and miscellaneous hardware still require pricing.

## Cost implication

The two enclosures alone are approximately 80% of the currently priced subtotal.
That is a useful whole-system finding: further penny-level optimisation of
ordinary passives is unlikely to dominate total unit cost.

Cost optimisation should therefore focus on:
1. rotary-control quote;
2. PCB fabrication;
3. connectors/interconnect;
4. PSU/transformer/regulator hardware;
5. semiconductors and precision networks;
before low-value passive optimisation.

## Grayhill decoupling

The rejected Grayhill 71BDF30 devices remain in live files because they currently
provide dimensional/history evidence.

AE-031 does not delete or falsify that evidence.

Instead:
- no new production contract may select Grayhill;
- the running cost ledger uses Lorlin PT as the current rotary platform and keeps
  it UNQUOTED;
- exact rotary footprint/keep-out/top-panel dimensions remain gated by AE-027/028;
- the later control ECO will atomically replace current BOM/mechanical authority.

## Four-layer routing work that can proceed now

The following do not depend on final rotary geometry:
- four-layer stack definition;
- continuous In1.Cu 0VA reference-plane intent;
- In2.Cu rail/power-spine intent;
- SCH101 differential symmetry;
- LT5400 local precision routing;
- THAT1646 output symmetry;
- decoupling placement/loop minimisation;
- prohibition on precision routes crossing reference-plane discontinuities.

The only routing areas held are the final EQ-selector endpoints/keep-outs and
other geometry directly constrained by the PT assemblies.

## Next activity

After AE-031:
1. configure/verify the native board as four-layer;
2. establish plane/routing classes and critical-net manual-routing rules;
3. route geometry-independent critical analogue paths;
4. hold rotary-specific regions until sample evidence closes;
5. continue BOM pricing toward full coverage.
