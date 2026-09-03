# AE-027 — Lorlin PT Exact Procurement Gate

**Revision:** A0  
**Status:** MANUFACTURER CONFIRMATION REQUIRED BEFORE BOM ECO

## Verified facts

Lorlin's current PT datasheet establishes:

- multi-wafer PCB construction;
- adjustable stops;
- BBM/non-shorting available;
- gold flash and gold plate available as options;
- 2.54 mm PCB terminal pitch;
- >999 MΩ initial insulation resistance at 500 VDC;
- <20 mΩ initial contact resistance;
- >10,000-cycle life.

The standard single-wafer metric 30-degree BBM 2P5T part is **PT6004**.

However, PT6004 is a standard silver-contact configuration. The stocked
PT6422/BMH is also a standard silver/Ag-plated construction. Neither shall be
entered into the production BOM as if it were the desired gold-contact part.

## Production configuration required

### Bass and Treble — quantity 2

- PT family;
- vertical PCB mounting;
- metric 6 mm spindle / M10 bush;
- 2 poles;
- 5 positions;
- 30-degree indexing;
- BBM;
- adjustable stop;
- gold plated preferred;
- exact Lorlin non-standard order code: **OPEN**.

### Channel — quantity 1

- PT family;
- same front-panel shaft/bush datum;
- two synchronised 2-pole wafers;
- four positions;
- BBM;
- minimum practical wafer spacing;
- gold plated preferred;
- exact Lorlin multi-wafer order code: **OPEN**.

## Why no guessed MPN is permitted

Lorlin's non-standard ordering system encodes wafer count, indexing, pole/way
configuration, BBM/MBB, plating, shaft geometry, flats and spacers. A plausible-
looking code is not sufficient production evidence.

The exact MPN must therefore come from:

1. Lorlin written quotation/order confirmation; or
2. an authorised distributor listing that exactly matches the required custom
   configuration and manufacturer drawing.

## Stock/price reference only

Farnell currently stocks PT6422/BMH, 2P5T, at approximately £17.29 ex VAT in
single quantity with substantial stock. It is a useful geometry/sample proxy,
not the production gold-contact part.

Production cost remains open until Lorlin quotes the gold-contact assemblies.

## BOM freeze gate

Do not replace the Grayhill entries in the controlled BOM until all of the
following are available:

- exact Lorlin MPNs;
- contact plating confirmation;
- manufacturer outline/PCB drawings;
- shaft length;
- Channel total rear depth;
- prototype quantity price and lead time;
- at least one single-wafer and one two-wafer sample or equivalent dimensional
  confirmation.

At that point the control-hardware ECO can update BOM, footprints, placement and
top-panel geometry atomically.
