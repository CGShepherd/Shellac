# G3-027 — Independent 3180-us Integration Audit and Foundry BOM Reconciliation

**Revision:** A1 — corrected independent-control interpretation  
**Base:** `e423121b8eba3b66b9f5c01c9e54e2c2f01fcffe`  
**Status:** candidate; electrical integration gate held

## Executive finding

The third RIAA pole is an **independent operator-controlled function**. It is not
interlocked with the Bass or Treble selectors, and G3-027 does not introduce any
logic that attempts to infer a “correct” replay setting.

The operator may therefore select any Bass position, any Treble position, and
optional 3180 us ON or BYPASS in any combination. An unusual combination is not an
electrical fault; it is simply an operator-selected replay curve.

The integration blocker is narrower. The controlled TRUE RIAA bass branch still
contains approximately the 3180 us pole and 318 us zero. G3-026 separately froze an
independent downstream 3180 us stage. If TRUE RIAA Bass is selected and that stage
is ON without changing the legacy branch, the 3180 us pole is applied twice.

Foundry therefore requires the TRUE-RIAA bass contribution to be resynthesised so
it **no longer contains the 3180 us pole**, while preserving the required 318 us
behaviour. The separate G3-026 3180 us stage can then sit later in the common signal
chain and remain completely independent of Bass/Treble selection.

No third Bass-selector pole is required by this interpretation.

## Required G3-028 electrical model

G3-028 should model the full Cartesian control space `Bass × Treble × optional-3180`,
not to prohibit unusual states, but to prove that each selector retains its defined
behaviour, ON contributes exactly one 3180 us term, BYPASS contributes none, TRUE-RIAA
Bass no longer embeds its own 3180 us pole, and no state applies the optional pole twice.

## BOM review

The current controlled BOM is a partial baseline, not a procurement-complete BOM.
A final cost total would therefore be false precision. G3-027 establishes a
procurement framework based on landed basket cost subject to Foundry requirements
and frozen MPNs.

Selected switches are bought at **required quantity only** by default. No routine
spares are purchased merely to reach quantity breaks. This remains valid while the
part is active/recommended for new designs and available without material supply
risk. NRND/EOL/obsolete status or genuine supply risk reopens the question.

## Controlled outcome

Closed: independent third-pole intent, no Bass/Treble interlock, executable
duplicate-3180 audit, required-quantity-only switch policy, partial-BOM status and
landed-cost procurement rules.

Held: TRUE-RIAA Bass resynthesis, SCH103 ECO, complete independent-state regression,
final footprint/machining work and final procurement BOM.
