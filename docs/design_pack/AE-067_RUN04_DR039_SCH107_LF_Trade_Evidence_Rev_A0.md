# AE-067 — RUN04 DR039/SCH107 LF Trade Evidence — Rev A0

**Project:** Shellac
**Status:** REVIEWED / BRANCH-LOCAL SELECTED / IMPLEMENTATION AND FOLLOW-ON QUALIFICATION OPEN
**Execution baseline:** `c29bbadaff34ee8f05668701d5031994f9243a5a`

## Purpose
Execute the AE-050 RUN04 candidate comparison without migrating any candidate into the product generator.

## Scope
Four candidates are compared: current common pre-split block, post-switch common block, AE-052 branch-local direct block, and the x10 SCH107 / 1.2 uF common-block reference.

Each candidate receives separate AC, noise, DC-offset-step and selector-transition analyses. RUN04 switching is an internal candidate discriminator only; balanced-output switching remains RUN12.

## Evidence summary

| Candidate | LF hard | LF preferred | Filter noise delta | Selector peak |
|---|---|---|---:|---:|
| CURRENT_COMMON_PRE_SPLIT | FAIL | REVIEW | +0.099 dB | 3.79 mV |
| POST_SWITCH_COMMON | PASS | PASS | +0.000 dB | 249.50 mV |
| BRANCH_LOCAL_DIRECT_BYPASS_BLOCK | PASS | PASS | +0.000 dB | 3.79 mV |
| RUMBLE_SCALE10_COMMON_1P2UF | FAIL | REVIEW | +1.658 dB | 3.79 mV |

## Reviewed disposition

**SELECT:** `BRANCH_LOCAL_DIRECT_BYPASS_BLOCK` for controlled implementation.

- direct-path loss at 20 Hz: -0.002524 dB;
- SCH107 -3 dB frequency: 15.044700 Hz;
- SCH107 response at 20 Hz: -0.460963 dB;
- RUN04 internal selector transient: 3.788 mV;
- conservative 250 mV DC-step direct-path settling to 1%: 1.592235 s.

**REJECT:** `CURRENT_COMMON_PRE_SPLIT` because it fails the AE-049 LF criteria.

**REJECT:** `POST_SWITCH_COMMON` because the RUN04 selector discriminator produces a 249.50 mV charge transient.

**REJECT:** `RUMBLE_SCALE10_COMMON_1P2UF` because it misses the preferred direct-path LF target and adds +1.658 dB integrated filter-path noise with no compensating system benefit.

The raw Phase-A result intentionally retains `EVIDENCE_COMPLETE_REVIEW_REQUIRED` and no automatic topology promotion; this reviewed design record and controlled configuration registers carry the reviewed selection. The live product generator is not changed by AE-067.

## Open qualification

- RUN09 full-system noise;
- RUN10 sensitivity/tolerance and timing-capacitor value engineering;
- RUN12 muted/live selector switching to the balanced output;
- prototype/bench correlation.

## Evidence

- `simulation/results/run04_lf_trade/ae067_run04.json`
- `simulation/results/run04_lf_trade/ae067_run04.csv`
- `simulation/results/run04_lf_trade/ae067_run04.md`
