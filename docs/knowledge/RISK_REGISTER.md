# Project Shellac — Risk and Open-Item Register

| ID | Item | State | Closure |
|---|---|---|---|
| R-001 | Older panel/off-board control representation conflicts with later PCB-established control-stack intent | OPEN | G3-024 ownership ECO/freeze |
| R-002 | Exact Bass/Treble rotary MPNs not frozen; historical Grayhill BOM and later Lorlin direction conflict in provenance | OPEN | G3-024 exact candidate trade using standard-stock parts |
| R-003 | Exact 4P4T Channel Mode implementation not frozen | OPEN | G3-024; four poles remain hard requirement |
| R-004 | Rumble/Mute toggle MPNs not frozen | OPEN | G3-024; maximise useful toggle commonality |
| R-005 | Rail LED electrical design is frozen but physical implementation/MPNs are not | OPEN | G3-024; panel LEDs on flying leads |
| R-006 | Manufacturing mounting-hole authority absent from current review board | OPEN | G3-024 |
| R-007 | Final drilling coordinates/templates intentionally gated | DEFERRED | Close after exact controls/PCB datums |
| R-008 | Closed-box PSU temperature not analytically predicted from controlled load/Rth data | VERIFY_ON_PROTOTYPE | First powered prototype per G3-023 |
| R-009 | Historical BOM/design rationale previously lived partly outside Git | ACTIVE_MITIGATION | SR-035/SR-036 registers; future packages update at decision lock |
| R-010 | Separate later RIAA ON/BYPASS function is recovered intent but not clearly represented in current controlled design | OPEN_HIGH_PRIORITY | Reconcile SCH103/SCH109 before rotary MPN freeze |
| R-011 | Old BOM mute-relay entry conflicts with later AE-008 mechanical input mute | RESOLVED_BY_CONTROLLED_EVIDENCE | AE-008 controls; old BOM retained only as historical provenance |
