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
| R-010 | Separate later RIAA ON/BYPASS architecture conflicted with the single-RC SCH103 branch | ELECTRICALLY_RESOLVED | G3-026 freezes factorised RC-before-gain OPA1656 realisation and exact DPDT switch; SCH103 integration/verification remains |
| R-011 | Old BOM mute-relay entry conflicts with later AE-008 mechanical input mute | RESOLVED_BY_CONTROLLED_EVIDENCE | AE-008 mechanical input mute controls |
| R-012 | Selected external switch MPNs lack final controlled PCB footprints/3D envelopes | PARTIALLY_MITIGATED | G3-026 closes nominal cover penetration; exact pad geometry, tolerance and complete hardware stack remain before drilling release |
| R-013 | Engineering method/decision hierarchy existed only implicitly across knowledge files and conversation | RESOLVED | FDR-001 Foundry baseline added under configuration control |
| R-014 | Regression evidence depended on manual local console relay | MITIGATED | G3-026 adds GitHub Actions compile/full-pytest workflow; first pushed run still requires confirmation |
| R-015 | Legacy TRUE RIAA branch still contains 3180/318 us while G3-026 adds an independent 3180 us stage | OPEN_BLOCKING | G3-027 audit prevents duplicate 3180 application; resynthesise TRUE-RIAA Bass contribution without 3180 us before SCH103 ECO |
| R-016 | Controlled BOM is not procurement-complete | ACTIVE_MITIGATION | Generate schematic-derived inventory before landed-cost optimisation |
| R-017 | Etched replay-configuration key could diverge from the controlled electrical replay model | OPEN | Generate recommended Bass/Treble/3180-us combinations and final legend content from controlled replay-curve data; verify correspondence by automated test before artwork or machining release |
