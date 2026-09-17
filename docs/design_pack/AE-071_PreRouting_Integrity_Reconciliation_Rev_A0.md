# AE-071 — Pre-Routing Integrity Reconciliation — Rev A0

**Project:** Shellac
**Baseline:** `67b2101474bc1db10deb7784a0cc7131ed20e2ef` (AE-070)
**Status:** PHYSICAL CAD DEFECTS CORRECTED / ROUTING HELD

## Purpose

AE-071 reconciles build-critical physical-CAD defects discovered by the post-RUN07 independent design-assurance review. It deliberately does not migrate selected-next signal architectures or make unresolved procurement/mechanical decisions.

## Corrected defects

- SCH101 now has local 100 nF rail bypassing for all four physical op-amp packages.
- SCH101 differential-converter annotation now matches the physical OPA1655 allocation.
- SCH103 and SCH108 negative-rail polarized bulk capacitors place the positive capacitor terminal at 0VA and the negative terminal at -18V.
- SCH107 470 nF frequency-setting film capacitors use a real 7.2 x 3.5 mm, 5 mm-pitch THT film footprint rather than generic 0805.
- The generated KiCad project exposes the `Capacitor_THT` footprint library.
- The live SCH101/BOM representation no longer claims a nonexistent LT5400-7 A-grade part. B-grade -7 is the procurement-feasible candidate family, while RUN10 retains tolerance/CMRR acceptance and final MPN authority.
- The engineering-model hierarchy now carries independent `BASS_L_SELECT`, `BASS_R_SELECT`, `TREBLE_L_SELECT` and `TREBLE_R_SELECT` signals between SCH109 and SCH103 rather than collapsing them into generic control nets.
- `MONO_AVG` and `MONO_R_LEG` are explicit cross-sheet analogue interfaces from SCH104 to SCH105, matching the AE-041 Rev A1 switched-summing authority.
- The hierarchy reconciliation changes the controlled readiness census from 66 to 74 hierarchical pins and from 19 to 23 cross-sheet signals; native KiCad ERC closes at zero errors and zero warnings.
- The eight SCH101 local bypass capacitors (`C191`-`C194`, `C291`-`C294`) are explicitly owned by the existing left/right gain-and-differential-converter placement clusters, preserving local supply-pin adjacency and a complete 255-reference current PCB population.

## Explicit non-decisions

AE-071 does not migrate AE-042 SCH101 or AE-067 DR-039 selected-next electrical implementations; choose final control footprints; choose LT5400 exposed-pad implementation; freeze the THAT1646 sense capacitor or output ferrite; approve the cartridge harness contact system; define final XLR pin-1 geometry; qualify the external PSU; or correct the THAT1646 25-ohm-per-leg / 50-ohm-balanced model semantics.

## Routing disposition

Historical SR-041 remains unchanged as provenance for its original base commit and is not current routing authority. Current disposition is `ROUTING_HELD_PENDING_PRODUCT_RECONCILIATION`. Final routing, layout freeze, BOM freeze and manufacturing release remain prohibited until the controlled blockers in `config/release/ae071_prerouting_hold.yaml` close. AE-072 Final Design Assurance is mandatory before layout/BOM/manufacturing freeze.

## Validation requirement

AE-071 must rebuild generated KiCad output, run native hierarchical ERC, run focused and full regressions, integrated preflight, decision-authority audit and `git diff --check`. Any native ERC violation remains a review blocker rather than being silently waived.

## Validation evidence

The reconciled implementation passes the AE-071 focused regression set and the complete repository regression suite. Deterministic KiCad generation produces build ID `a103d9c34573f492`; native KiCad ERC reports zero errors and zero warnings. Integrated preflight remains coherent through AE-070/RUN07, the decision/configuration authority audit passes, and `git diff --check` is clean apart from non-failing working-tree line-ending notices where Git is configured to normalise CRLF to LF.
