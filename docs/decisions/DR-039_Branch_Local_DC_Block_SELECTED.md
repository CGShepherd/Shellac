# DR-039 — Branch-local post-EQ DC blocking

**Status:** CURRENT_ARCHITECTURE_QUALIFICATION_OPEN
**Selection authority:** AE-067 / RUN04
**Product-migration authority:** AE-074
**Selected topology:** `BRANCH_LOCAL_DIRECT_BYPASS_BLOCK`

## Decision

The current DR-039 architecture is branch-local DC blocking:

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

## Implemented product migration

AE-074 migrates the selected topology into the live product generator and generated schematic source.

- SCH103 now hands each recovery-amplifier output directly to `POST_EQ_L` / `POST_EQ_R`; there is no common DR-039 capacitor or 330 kOhm return before the SCH107 split.
- SCH107 owns the branch-local DIRECT/BYPASS blocks.
- Existing physical identities are deliberately preserved:
  - left: `C30060` / `R30060`;
  - right: `C35060` / `R35060`.
- The 1 uF PET-film / 63 V / WIMA-MKS2-class footprint contract and 330 kOhm / 1% return are retained.
- The FILTER branch remains the existing two-section SCH107 high-pass and provides intrinsic DC blocking.
- Placement ownership transfers from `CLU-103-HF-L/R` to `CLU-107-L/R` without forcing component renumbering.

The earlier common pre-split implementation record `DR-039_Common_Post_EQ_DC_Block_SELECTED.md` remains historical provenance and is not rewritten.

## Native PCB boundary

AE-074 has completed the controlled native KiCad F8 reconciliation using reference-designator relinking. `C30060/R30060/C35060/R35060` retain their accepted physical positions, are owned by SCH107, and carry the selected branch-local net assignments. The corresponding native-PCB `Function` metadata was reconciled without altering geometry or connectivity. `AE071-B02` is therefore resolved by AE-074.

The board remains intentionally unrouted and AE-074 does not authorise routing, layout freeze, BOM freeze or manufacturing release. Remaining pre-routing blockers and the RUN09/RUN10/RUN12/bench obligations remain authoritative.

## Qualification still open

The following remain open before manufacturing release:

- RUN09 full-system noise;
- RUN10 sensitivity/tolerance and value engineering;
- RUN12 muted/live switching through the balanced output;
- prototype/bench correlation.

## Evidence

- `docs/design_pack/AE-067_RUN04_DR039_SCH107_LF_Trade_Evidence_Rev_A0.md`
- `docs/design_pack/AE-074_DR039_Branch_Local_Product_Migration_Rev_A0.md`
- `simulation/results/run04_lf_trade/ae067_run04.json`
- `simulation/results/run04_lf_trade/ae067_run04.csv`
- `simulation/results/run04_lf_trade/ae067_run04.md`
