# AE-021 — DR-039 Full Implementation and Schematic-Rework Acceleration

This phase closes DR-039 as an implemented subsystem rather than another analysis increment. SCH103 gains a common 1 µF PET-film / 330 kΩ DC block per channel before the SCH107 FILTER/BYPASS split, with raw and post-block test points. The nominal pole is approximately 0.48 Hz and is negligible at 20 Hz.

Physical capture uses the WIMA MKS2 1 µF / 63 V class, 5 mm lead pitch, approximately 7.2 × 5 × 10 mm.

After this phase, the only major signal-chain schematic rework before layout is DR-038 SCH101 precision migration. The next phase is intentionally large: LT5400-7 CAD representation, 4x converter, 1 kΩ gain ladder, hard service links, RF matching, SCH101 capture rewrite, placement/BOM updates, and CMRR/noise/headroom regression.
