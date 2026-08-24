# Project Shellac — Risk and Open-Item Register

| ID | Item | State | Closure |
|---|---|---|---|
| R-001 | Older panel/off-board control representation conflicts with PCB-established control-stack intent | MITIGATED | G3-024 engineering model carries PCB/panel ownership; generic schematic interface symbols remain non-placement authority until footprint ECO |
| R-002 | Bass/Treble rotary MPNs not frozen | RESOLVED | Grayhill 71BDF30-01-2-AJN selected for both, five stops |
| R-003 | Exact 4P4T Channel Mode implementation not frozen | RESOLVED | Grayhill 71BDF30-02-2-AJN selected, four stops |
| R-004 | Rumble/Mute toggle MPNs not frozen | RESOLVED | Common C&K 7201SYCBE selected |
| R-005 | Rail LED physical implementation/MPNs not frozen | RESOLVED | Vishay TLLG4401 + A104700BLACK; audio top-cover centre spine |
| R-006 | Manufacturing mounting-hole authority absent from current review board | OPEN | Next physical-board package: verified footprints + mounting-hole synthesis |
| R-007 | Final drilling coordinates/templates intentionally gated | DEFERRED | Release after verified controls/PCB datums |
| R-008 | Closed-box PSU temperature not analytically predicted from controlled load/Rth data | VERIFY_ON_PROTOTYPE | First powered prototype per G3-023 |
| R-009 | Historical BOM/design rationale previously lived partly outside Git | ACTIVE_MITIGATION | Controlled registers/BOM updated with each decision lock |
| R-010 | Separate later RIAA ON/BYPASS function lacks controlled node-level implementation | OPEN_HIGH_PRIORITY | Reconcile SCH103 switching topology; do not infer pole count/MPN |
| R-011 | Old BOM mute-relay entry conflicts with later AE-008 mechanical input mute | RESOLVED_BY_CONTROLLED_EVIDENCE | AE-008 mechanical input mute controls |
| R-012 | Selected external switch MPNs do not yet have verified controlled PCB footprints/3D envelopes | OPEN_HIGH_PRIORITY | Build/verify custom footprints from manufacturer drawings before placement/drilling release |
