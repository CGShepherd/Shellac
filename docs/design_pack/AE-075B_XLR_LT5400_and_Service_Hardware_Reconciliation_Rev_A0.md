# AE-075B — XLR, LT5400 and Service-Hardware Reconciliation — Rev A0

**Project:** Shellac
**Status:** CLOSED — PRE-ROUTING DESIGN IMPLEMENTATION VALIDATED
**Baseline:** `5b51964c2282083c7d767f330966905d34fe47e6`

## Purpose

Resolve the low-risk pre-routing hardware authority that can be closed without conflating it with B03 control-stack mechanical CAD or with RUN10 complete-stage qualification.

## B06 — XLR pin-1/local-chassis closure

Selected panel connectors:
- input: Neutrik `NC3FD-L-B-1`, female, solder cup, black metal, gold contacts;
- output: Neutrik `NC3MD-L-B-1`, male, solder cup, black metal, gold contacts.

Contract:
- pin 1 -> `CHASSIS`;
- separate shell/front-panel ground contact -> `CHASSIS` by explicit local bond;
- no connector-local `0VA` connection;
- do not rely on anodised-panel incidental contact;
- shell/pin-1/chassis continuity remains a manufacturing/commissioning inspection.

This closes AE071-B06 at pre-routing design level.

## B04 — LT5400 partial closure

Selected exact part: `LT5400BIMS8E-7#PBF` (B grade, -7 ratio, industrial temperature range).

The exposed pad (pin 9) is bonded to quiet `0VA`. This follows the LT5400 manufacturer guidance to use a quiet AC ground as an electrostatic/AC shield and avoids noisy ground injection.

B-grade CMRR-matching limit: ±0.015%. For the -7 ratio, R2/R1 = R3/R4 = 0.25. Applying the manufacturer difference-amplifier CMRR contribution expression gives a worst-case resistor-network residual of `0.00006000`, equivalent to `84.44 dB`.

This is a network-only bound. It exceeds the AE-049 mid-band design objective of 75 dB, but it does not close RUN10. Complete-stage op-amp, source impedance, PCB parasitic and 20 kHz behaviour remain subject to RUN10:
- >=70 dB, 20 Hz to 1 kHz;
- >=60 dB at 20 kHz;
- objective >=75 dB mid-band.

AE071-B04 therefore remains a routing blocker, narrowed to complete-stage RUN10 tolerance/CMRR/parasitic acceptance.

## B08 — service hardware narrowing

Selected compatible hardware:
- gain headers: Samtec `TSW-104-07-G-D`;
- gain shunt: Samtec `MNT-104-BK-G`;
- load headers: Samtec `TSW-102-07-G-D`;
- load shunt: Samtec `MNT-102-BK-G`.

The manufacturer material corroborates the pitch/family/mating selection, but does not provide sufficiently unambiguous electrical evidence to waive physical continuity/orientation verification for the movable multi-position shunts.

B08 remains open only for:
1. physical continuity/pairing/orientation confirmation on production-representative samples;
2. pin-1/orientation marking in final CAD/service documentation;
3. short, symmetric routing and service-header parasitic/layout verification.

## Explicit non-decisions

- B03 control footprints/keep-outs are not modified. The NKK NR01 EQ rotary mechanics require a dedicated control-stack reconciliation rather than reuse of the generic threaded-bushing model.
- RUN10 is not claimed complete.
- No final routing, layout freeze, BOM freeze or manufacturing release is authorised.

## Configuration-control debt reconciliation

AE-075B qualification exposed stale mutable-current assertions embedded in older regression modules and drift between current authority registries. The reconciliation therefore also updates current-state tests, advances the routing-hold header, cross-registers AE-075A/B, strengthens cross-registry audit coverage, and makes the governed native-PCB ignore exception explicit.

Historical AE-071/AE-074 design records remain unchanged. Known provenance debt is not fabricated: current-facing PSU narrative refers to AE-072, but no controlled AE-072 design-record file exists in the live design-pack tree.

## Validation result

Final AE-075B qualification completed after configuration-control debt reconciliation:

- full regression suite: **682 passed**;
- generated KiCad provenance: PASS, build ID `f764fff879a708d4`, 14 immutable files verified;
- native hierarchical ERC: **0 violations**;
- native PCB integrity: PASS;
- integrated preflight: PASS;
- decision/configuration authority audit: PASS;
- `git diff --check`: PASS.

Routing remains explicitly unauthorised. The remaining pre-routing blockers are AE071-B03, AE071-B04 and AE071-B08. The controlled AE-072 design-record provenance gap remains documented and is not fabricated by AE-075B.
