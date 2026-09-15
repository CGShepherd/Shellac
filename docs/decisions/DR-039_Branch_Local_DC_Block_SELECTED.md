# DR-039 — Branch-local post-EQ DC blocking

**Status:** CURRENT_SELECTED_PENDING_IMPLEMENTATION
**Selection authority:** AE-067 / RUN04
**Selected topology:** `BRANCH_LOCAL_DIRECT_BYPASS_BLOCK`

## Decision

The current selected DR-039 architecture is branch-local DC blocking:

- DIRECT/BYPASS branch: retain a dedicated 1.0 uF series capacitor and 330 kOhm downstream return to 0VA;
- FILTER branch: do not add a second common DC-block network; use the intrinsic DC blocking already provided by SCH107;
- the DC-block network shall not be placed as a common pre-split element ahead of the FILTER/BYPASS branch point;
- the DC-block network shall not be moved to one common post-selector element.

AE-067 RUN04 provides the selection evidence. At nominal values the branch-local candidate gives approximately:

- direct-path loss at 20 Hz: -0.002524 dB;
- SCH107 -3 dB frequency: 15.044700 Hz;
- SCH107 response at 20 Hz: -0.460963 dB;
- internal RUN04 selector transient: 3.788 mV;
- conservative 250 mV DC-step direct-path settling to 1%: 1.592235 s.

## Rejected alternatives

`CURRENT_COMMON_PRE_SPLIT` is rejected because loading by SCH107 materially changes both the direct and filtered LF response and fails the AE-049 RUN04 acceptance criteria.

`POST_SWITCH_COMMON` is rejected because the common capacitor retains charge across selector transitions and produces an approximately 249.5 mV internal selector transient in the RUN04 discriminator.

`RUMBLE_SCALE10_COMMON_1P2UF` is rejected because it does not preserve the preferred direct-path LF target and adds approximately 1.658 dB integrated filter-path noise relative to the branch-local reference without compensating system benefit.

## Implementation boundary

This decision is **selected but not yet implemented in the live product generator**.

The existing live generator may still contain the earlier common pre-split implementation described by `DR-039_Common_Post_EQ_DC_Block_SELECTED.md`. That document remains historical provenance for the previously implemented state; it is superseded as current DR-039 design authority by this record and AE-067.

Controlled product-generator/CAD/BOM migration must be performed as a separate implementation event. AE-067 by itself does not authorise a manufacturing baseline.

## Qualification still open

The following remain open before manufacturing release:

- RUN09 full-system noise;
- RUN10 sensitivity/tolerance and value engineering;
- RUN12 muted/live switching through the balanced output;
- prototype/bench correlation.

## Evidence

- `docs/design_pack/AE-067_RUN04_DR039_SCH107_LF_Trade_Evidence_Rev_A0.md`
- `simulation/results/run04_lf_trade/ae067_run04.json`
- `simulation/results/run04_lf_trade/ae067_run04.csv`
- `simulation/results/run04_lf_trade/ae067_run04.md`
