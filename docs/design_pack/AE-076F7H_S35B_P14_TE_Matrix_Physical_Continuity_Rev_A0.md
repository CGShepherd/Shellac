# AE-076F7H S35B-P14 — TE MRJE3404 physical static continuity evidence — Rev A0

**Status:** USER-REPORTED STATIC CONTACT SEQUENCE ACCEPTED; NOT A NATIVE FOOTPRINT OR FABRICATION RELEASE.
**Date:** 18 November 2026.
**Parent controlled baseline:** `develop` `a097987a8ebd1c360defb5e90bad2308e1bd9951` (S14).
**Component:** purchased TE Connectivity / Alcoswitch MRJE3404, manufacturer 1825537-3; 3 poles x 4 throws, four detents.
**Source design:** AE-041 Rev A1 (matrix logic), AE-076F4C (part identity), SHELLAC_CURRENT_TECHNICAL_SPEC_Rev_A0 (selected-next), TE Customer Drawing 1825537 Rev A3.

## Physical evidence and observation classification

User-reported tests were made on the actual, disconnected switch with a conventional two-wire DMM in resistance/continuity mode. No independently witnessed bench log or calibrated low-ohms trace exists.

| Operator detent (view from shaft) | C1 | C2 | C3 |
|---|---|---|---|
| D1 fully counter-clockwise | 1 | 1 | 1 |
| D2 clockwise | 2 | 2 | 2 |
| D3 clockwise | 3 | 3 | 3 |
| D4 fully clockwise | 4 | 4 | 4 |

Each numeral above is the associated pole's selected throw, **not** a global unique pad number. At every detent the other three throws of each pole were reported open-circuit; unselected-throw cross-contacts were also reported open-circuit. User subsequently reported open-circuit common-terminal isolation, interpreted in conversation as C1–C2, C1–C3 and C2–C3; the original wording had a repeated C3 identifier. This is an interpretation to retain in the record, not an invented quantitative insulation result.

Selected-path DMM indication approximately 0.15 ohm, reported by user as probe-limited and uncertain. This establishes continuity; it **does not** qualify the TE manufacturer's 30 milliohm initial contact-resistance limit. The instrument model, zero/lead correction, test current and uncertainty are not recorded.

Manufacturer specifies break-before-make. No dynamic contact-timing measurement was performed or requested. Therefore physical BBM timing remains manufacturer-supported rather than bench-verified; operational procedure stays **MUTE -> MATRIX -> RUN** and RUN12 transient qualification remains open.

## Logical mapping proposed from measured detents (not yet native pin-to-pad authority)

| Physical bank | Common use | Throw 1 / D1 | Throw 2 / D2 | Throw 3 / D3 | Throw 4 / D4 |
|---|---|---|---|---|---|
| C1 | Left OPA1656 mode-buffer input | BUFFERED_L | BUFFERED_L | MONO_AVG | BUFFERED_R |
| C2 | Right OPA1656 mode-buffer input | BUFFERED_L | BUFFERED_R | MONO_AVG | BUFFERED_R |
| C3 | MONO_R_LEG | NC | NC | MONO_AVG | NC |

C3 throw 3 connects the right 4.7 kohm averaging leg only during L+R. C3 throws 1, 2 and 4 shall be physically unconnected, **not** tied to 0VA. The C1/C2/C3 to logical A/B/C assignment is a design mapping supported by the available contact sequence; final footprint must confirm every terminal's physical B.Cu pad number before implementation.

## Photographic evidence — uploaded artefacts

The following images were uploaded within the S35B-P14 chat and are supplied unaltered in this candidate package. Hashes are of the packaged uploaded JPEG bytes, which might not equal independently exported phone originals.

| Image | SHA-256 |
|---|---|
| `PXL_20261118_145740473.jpg` | `E34D215CFD8D73533F34C9CB1AB6AF31921F6A377F53B6245129A678A5ED3C10` |
| `PXL_20261118_145747484.jpg` | `462DD7CBCFC047D766DEDC37DAC2BE12F67AFBEE99815AAA8BD5A984E624A4E2` |
| `PXL_20261118_145833548.MACRO_FOCUS.jpg` | `BF899A39D1DF77C1045F3B92EF1550EC75026BA0F4DA913C389525BD438CEF91` |
| `PXL_20261118_145843732.jpg` | `29BCF5311700FA1D700C7C5FDFFF532409045F0EC436A45A529DF3F31FD1419D` |

Photographs show the shaft and supplied mounting hardware, an axial shaft view, the terminal face and the terminal surround markings. The annotated surround is useful supporting evidence, but the photos are **not** a coordinate-calibrated anti-mirror reference.

## Qualification scope and open conditions

- **Accepted:** purchased-sample static D1..D4 selected-throw progression; inactive-throw open circuit; reported common isolation; compatibility with governed operator sequence DUAL L / STEREO / L+R / DUAL R.
- **Not qualified:** individual contact resistance to 30 milliohm limit; contact bounce or dynamic break-before-make; sample population statistics; final 15 physical pad-to-terminal geometry; shaft-end versus terminal-end parity; B.Cu footprint orientation and copper/solder clearance; completed assembly, transient behaviour, RUN10/RUN12 or bench/system validation.
- **No implementation or release effect:** unchanged generator, BOM, KiCad PCB, manufacturer CAD, and `final_routing=false`, `layout_freeze=false`, `bom_freeze=false`, `manufacturing_release=false`.
- **Next bounded engineering transaction:** reconcile the manufacturer's **3-4** shaft-view PCB hole drawing with numbered contacts and B.Cu orientation, then register actual TE and six other controls in the full seven-control MCAD assembly. Do not repeat the completed switch selection.

**Evidence disposition:** This report is a proposed governed checkpoint. It becomes an installed project record only after local preflight, staged diff review, applicable regression/authority audit, governed commit/PR and verified merge. The photographs are to be retained in the Dropbox evidence archive; the project documentation stores their hashes and provenance rather than binary images.
