# AE-037A — SCH101 Placement Reconciliation

**Revision:** A0  
**Parent:** AE-037  
**Status:** PHYSICAL-MODEL RECONCILIATION

AE-037 added four real 23.7 kΩ cartridge-load / OPA1656 DC-return resistors:
`R104`, `R105`, `R204`, `R205`.

The electrical and footprint models correctly treated those as approved PCB
components, increasing board population from 250 to 254, but the existing Gate 3
placement-cluster authority had not been updated. This caused the subsequent
placement/routing-gate failures through an unowned `R104`.

## Resolution

- `R104`, `R105` belong to `CLU-101-A`, Left input RF and connector interface.
- `R204`, `R205` belong to `CLU-101-C`, Right input RF and connector interface.
- Existing input-region span/keepout is retained.
- Existing deterministic real-footprint packer remains authoritative; its shelf
  fallback is allowed to accommodate the two additional 0805 resistors.
- Real-footprint audit population baseline becomes 254.

No electrical value or topology is changed by AE-037A.

## New invariant

Every electrically introduced approved PCB component must acquire exactly one
physical placement-cluster owner in the same design increment.
