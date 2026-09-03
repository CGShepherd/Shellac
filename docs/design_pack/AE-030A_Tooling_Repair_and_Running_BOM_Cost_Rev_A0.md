# AE-030A — Tooling Repair and Running BOM Cost

**Revision:** A0  
**Status:** PROCESS / COST-CONTROL INFRASTRUCTURE

## Purpose

AE-030A integrates running product cost into the Shellac production-closure
process and repairs AE-030's direct-script import defect.

## Cost views

Shellac shall maintain three product-cost views:

1. **Design BOM cost** — current best unit-price estimate for one complete system.
2. **One-build acquisition cost** — realistic purchase cost including MOQ/package effects.
3. **10-unit production reference** — modest-volume reference for future build decisions.

All values are GBP ex VAT unless explicitly marked otherwise.

## Evidence discipline

A price line must carry a procurement state and confidence. Unknown prices are
`UNQUOTED`; they are never silently converted to zero-cost parts.

The dashboard therefore reports both subtotal and coverage. A £100 subtotal at
25% coverage is not represented as a £100 product BOM.

## Cost categories

The ledger should grow to cover:
- active/passive audio electronics;
- controls;
- PCB fabrication;
- connectors and wiring;
- enclosure/mechanics;
- PSU;
- fasteners/miscellaneous hardware.

## NRE separation

Prototype switch samples, fixtures, test jigs and other development purchases are
recorded separately from product unit cost.

Existing laboratory instruments are excluded.

## ECO rule

Every future ECO changing a physical part should state:
- old design cost;
- new design cost;
- estimated unit delta;
- confidence/source date;
- whether the delta buys a material electrical, mechanical, reliability,
  procurement or serviceability benefit.

## Immediate cost priorities

The highest-value price-resolution work is:
1. Lorlin PT exact production rotary quotation;
2. current C&K toggle pricing;
3. both METCASE enclosures;
4. PCB fabrication at prototype and 10-unit quantities;
5. final controlled BOM population.

This sequencing concentrates effort on the largest and least-certain cost blocks.
