# Project Shellac — One-Off Build Recoverability Standard

**Status:** CURRENT ENGINEERING STANDARD
**Applies from:** AE-076D pre-layout closure onward
**Product intent:** one-off / very-low-volume personal build, not a prototype intended to converge through repeated PCB revisions.

## 1. Purpose

Shellac should be designed to work correctly on the first fabricated unit. Residual uncertainty is not accepted merely because a future prototype could reveal it. Where an uncertainty cannot reasonably be closed before fabrication, the design shall include a deliberate, low-risk recovery path when a board respin would otherwise be the likely remedy.

Recoverability is not permission to add speculative features or uncontrolled options. Every escape route must be justified by a specific identified uncertainty.

## 2. Mandatory uncertainty classification before fabrication

Every unresolved design item that could affect the fabricated unit shall be classified as exactly one of:

- **CLOSE_BEFORE_FAB** — evidence must be obtained and the design frozen before PCB/mechanical fabrication;
- **ESCAPE_ROUTE_REQUIRED** — the primary design is evidence-based but residual uncertainty remains large enough that a reversible recovery mechanism is required in the one-off unit;
- **BENCH_ONLY_ACCEPTABLE** — residual uncertainty may remain until commissioning because a failed bench result can be corrected without PCB/mechanical respin or unacceptable degradation.

No item may remain merely `OPEN` at fabrication release without one of these dispositions.

## 3. Escape-route record

For each `ESCAPE_ROUTE_REQUIRED` item, controlled design evidence shall state:

1. uncertainty and failure consequence;
2. evidence supporting the default implementation;
3. default fitted/DNP state;
4. physical/electrical escape mechanism;
5. trigger measurement or observation for invoking it;
6. rework method and required access;
7. expected parasitic, noise, reliability, mechanical and service penalty;
8. verification after rework;
9. conditions under which the escape route can be removed from later documentation.

## 4. Preferred mechanisms

Use the least intrusive mechanism that solves the identified problem. Candidates include:

- DNP population options where the unused footprint has negligible impact;
- alternative passive values using the same production footprint;
- deliberately placed 0-ohm links or solder links where series/contact resistance is irrelevant;
- selectable grounding/protection/ferrite networks where the alternative is already analytically justified;
- accessible test points at block boundaries;
- service connectors or daughterboards where serviceability benefit outweighs contact/parasitic risk;
- physical clearance for a bounded larger/taller alternative component;
- mechanical slots, removable brackets or replaceable looms where uncertainty is mechanical rather than electrical.

## 5. Low-level analogue restrictions

The cartridge/SCH101 region is capacitance-, leakage-, symmetry- and noise-sensitive. Do not add spare connector positions, long stubs, generic jumpers, oversized multi-option pad fields or unnecessary test pads merely for flexibility.

An escape route in this region must have quantified or bounded capacitance/leakage/mismatch impact and must be included in RUN10 or equivalent analytical/bench acceptance.

The selected per-channel passive cartridge-personality interface is an example of a justified serviceable mechanism because it changes only the differential shunt load and the audio path does not traverse the card.

## 6. One-off fabrication release criterion

Before fabrication/layout freeze:

- all design-driving uncertainties are either closed or explicitly classified;
- every `ESCAPE_ROUTE_REQUIRED` item has a controlled implementation and verification plan;
- no HIGH-severity uncertainty relies on a future PCB respin as its normal mitigation;
- escape routes do not materially compromise nominal performance, reliability or serviceability;
- block-level review records explicitly state `PASS_FOR_LAYOUT`, `PASS_WITH_CONTROLLED_RECOVERY`, or `HOLD`.

A `PASS_WITH_CONTROLLED_RECOVERY` is acceptable for a one-off unit only when the recovery action is realistically executable on the assembled hardware.

## 7. Review discipline

Recoverability shall be reviewed per functional block rather than as a final blanket check. The final pre-routing review must challenge both sides:

- has an uncertainty been deferred when it should have been closed?
- has unnecessary flexibility been added where the escape mechanism itself creates more risk than it removes?
