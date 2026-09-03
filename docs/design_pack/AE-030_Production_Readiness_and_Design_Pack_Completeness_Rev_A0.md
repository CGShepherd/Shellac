# AE-030 — Production Readiness and Design-Pack Completeness Audit

**Revision:** A0  
**Status:** PRODUCTION CRITICAL-PATH DEFINITION  
**Base:** `develop` at AE-029 baseline

## Executive conclusion

Project Shellac has crossed an important boundary.

The signal-chain architecture is no longer the primary design risk. The current
critical path is:

**control hardware / top-panel mechanics → native four-layer PCB routing →
fabrication release → representative hardware → measured acceptance →
production pack / reproducibility**

This is materially different from the project state earlier in the signal-chain
review.

## What is already closed

### Electrical architecture

AE-023/AE-029 close the principal signal-chain architecture analytically:

- DR-037 complete legacy/RIAA replay architecture;
- DR-038 precision SCH101;
- DR-039 common post-EQ DC block;
- gain/headroom;
- nominal CMRR/noise architecture;
- rumble-filter response;
- channel-mode matrix.

Hardware measurement remains mandatory, but further speculative synthesis is not
justified unless measurements disagree.

### Audio mechanical datum

SR-040 freezes:

- METCASE M5502119 enclosure evidence;
- carrier datum;
- 220 mm × 140 mm audio PCB outline;
- four mounting-hole geometry.

### Placement

SR-041 accepts the manual placement clusters as the routing baseline, with local
refinement authority and explicit manual treatment of critical analogue nets.

## What is not yet production-ready

### Rotary controls / top cover

This is now the leading mechanical blocker.

The live mechanical-control model and top-cover tests still encode the rejected
right-angle Grayhill 71BDF30 devices.

Top-cover machining remains explicitly unreleased.

AE-026/027/028 provide the replacement path:
Lorlin PT preferred, exact gold-contact order codes and sample geometry still open.

### Native PCB routing

The released placement-reference board is deliberately not a routable electrical
board.

The real native KiCad PCB is separately audited. SR-043 treats it as ready to
begin routing only if:

- complete footprint population is present;
- frozen outline is present;
- mounting holes are present;
- it is still unrouted;
- In1.Cu and In2.Cu exist, making a four-layer board.

Production routing, planes, vias and DRC closure are therefore still open.

### Fabrication

There is not yet a production-routed, DRC-closed PCB release with inspected
Gerbers/drill data and a fabrication manifest.

### BOM

The controlled BOM remains partial and still lists the now-rejected Grayhill
rotaries. Final alternates/lifecycle/procurement completeness is open.

### Prototype evidence

AE-029 defines the acceptance programme but the measurements do not yet exist.

### Release/reproducibility

No production-tagged clean-clone reproducibility evidence yet exists.

## Recommended execution order

1. Close Lorlin PT exact MPN + sample geometry.
2. Apply one atomic control-hardware ECO.
3. Re-freeze top-panel machining and switch PCB footprint/datum.
4. Confirm the native board stack is four-layer.
5. Complete native routing under SR-041 rules.
6. DRC/ERC and analogue return-path review.
7. Final BOM/procurement audit.
8. Fabricate representative hardware.
9. Run AE-029 commissioning.
10. Correct only evidence-driven problems.
11. Freeze measured production limits.
12. Complete maintenance and fabrication/release pack.
13. Clean-clone reproducibility audit.
14. Repository hygiene / production tag.
15. Extract Foundry and Generator after Shellac proves the dependency boundary.

## Foundry implication

AE-030 is also a candidate generic Foundry pattern.

The concept of explicit CLOSED / READY / PROTOTYPE EVIDENCE / BLOCKED release
gates, with every blocker having one next action, is reusable beyond Shellac and
should be considered during post-production Foundry extraction.
