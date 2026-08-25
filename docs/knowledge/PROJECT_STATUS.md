# Project Shellac — Controlled Project Status

**Knowledge baseline:** SR-036 + Foundry FDR-001
**Engineering package:** G3-027 independent-3180 integration audit / BOM reconciliation candidate
**Base commit:** `e423121b8eba3b66b9f5c01c9e54e2c2f01fcffe`

## G3-027 electrical finding
- Third 3180 us RIAA pole is an independent operator-controlled ON/BYPASS stage.
- No Bass/Treble interlock or state-detection logic is required.
- Any Bass × Treble × 3180 state is allowed.
- SCH103 integration is blocked only because current TRUE-RIAA Bass still contains an approximately 3180 us pole.
- Remove that legacy 3180 us term so G3-026 is the sole 3180 us source when ON.

## Procurement
- Landed whole-BOM cost is the optimisation objective subject to Foundry.
- Selected switches: required quantity only by default, no routine spares.
- Primary pool: DigiKey UK, Mouser UK, Farnell UK, CPC UK.
- Challenger pool: RS, TME, LCSC.
- Controlled BOM remains partial rather than procurement-complete.

## Held
- TRUE-RIAA Bass resynthesis without embedded 3180 us.
- SCH103 ECO and complete independent-state regression.
- Final footprints/Z datum/machining.
- Purchase-order BOM until full schematic-derived inventory is reconciled.

## Next package
**G3-028 — Independent-RIAA Core Resynthesis and Full Procurement-BOM Build**

No PCB fabrication or enclosure machining release.
