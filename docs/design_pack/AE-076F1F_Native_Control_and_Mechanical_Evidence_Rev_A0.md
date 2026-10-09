# AE-076F1F — Native Controls and Mechanical CAD Evidence Disposition — Rev A0

**Date:** 2026-10-09
**Status:** INFORMATIONAL / PRE-LAYOUT PHYSICAL QUALIFICATION OPEN
**Governed source:** AE-076F0 `24899753d05597aedd7a2ced6a482e6e1001c705` (`develop`)
**Authority effect:** NONE. Current six PCB-to-upper-cover primary supports remain selected. Rail carrier remains only a candidate. Routing/layout/BOM/manufacturing HELD.

## Qualified evidence and scope

- AE-076F1D authenticates the Metcase STEP (`9bf09314db1e8ffb596c27cceecb932141d3e43ba8d5ca4998fd4d16411b91fa`) and actual PCB STEP (`84fae4cfe2fa5edc3436a36792f3da41c8f71d29e9cd711f469631b37200fe61`), uses FreeCAD 1.0.2 and corrects the PCB upper-cover datum error in AE-076F1C.
- Nominal cover underside world Y = -33.911678 mm; provisional PCB B.Cu world Y = -46.211678 mm at the selected NKK 12.3 mm panel-to-PCB assumption. These are provisional assembly positions, not frozen manufacturing datums.
- Nominal PCB-substrate to G1 sheet clearance = 17.742547 mm; nominal populated PCB bounding-box to sheet clearance = 7.657547 mm. Omitted NKK/C&K controls, unqualified service-card bodies and hardware invalidate any full fit inference.
- A 239 mm wide, 1.6 mm sheet at the highest G1 guide fits the nominal 236 mm extrusion-face opening and 241 mm back-wall span; nominal centred engagement 1.5 mm per edge and 0.4 mm vertical groove slack. The 234 mm reinforcement nominally approaches zero side clearance at 1 mm lateral shift. These are not tolerance-approved dimensions.
- AE-076F1D sampled carrier-only translation at 5 mm intervals from both ends through 190 mm with the relevant end panel excluded. All sampled positions passed. No continuous swept envelope, populated-PCB assembly path, fastener/tolerance or cover installation qualification is established.
- AE-076F1E authenticates native board SHA-256 `a5b519a21a2bbe2c9f3ad751134d43292a5b32184487100512ab045b6258861c`; **256 current native footprints, all F.Cu**; exactly MH1=(25,28), MH2=(235,28), MH3=(235,152), MH4=(25,152) mm. These four interim footprint holes do NOT implement the selected six supports.
- No native switch footprints were detected. Seven approved control roles (four NKK NR01, one C&K A30403RNCB, two C&K 7201SYCBE) remain part-selected but physically unimplemented. Filename-only CAD search found no dedicated local switch STEP; this does NOT demonstrate absence of manufacturer CAD.

## Evidence file provenance (local Downloads, not yet Git-controlled)

- `SHELLAC_AE076F1D_RAIL_PATH_20261009_145649.json` SHA-256 `582c1d533b159d4ec4fc1009dd014e3f870b57e32bd3ee3f289404fc4a3ae08f`
- `SHELLAC_AE076F1D_RAIL_PATH_20261009_145649.log` SHA-256 `ee4576f3c13c368a5265024ac432e4c02263e1a4692f1b20c8c6420e029c2ef2`
- `SHELLAC_AE076F1E_CONTROL_SUPPORT_INVENTORY_20261009_153621.json` SHA-256 `57a6ed0c37af31cdf8609cd4f291040ac9555c9e97f9ff928e4581e746983eeb`
- `SHELLAC_AE076F1E_CONTROL_SUPPORT_INVENTORY_20261009_153621.log` SHA-256 `a2044e9ca22a4f9727ac7c3cb408cd93bbe49f73738fb7c52016e33c174d7053`

## Mandatory closure before a mechanical selection and PCB placement

1. Acquire and authenticate manufacturer-specific control dimension and terminal/position data for NKK NR01105ANG13-2A/-2C with AT3009, C&K A30403RNCB, and C&K 7201SYCBE; assess exact 3D availability or bounded neutral envelopes. No generic-model substitution as qualified evidence.
2. Establish seven B.Cu board-side pin/pad orientations, physical control locations, shaft axes, panel cut-outs, and C&K common-plane compatibility with NKK 12.3 mm datum. Prove local short EQ switching branches and RUN10 implications before native migration.
3. Overlay current MH1–MH4 and two proposed support points, carrier cut-outs/spacer heads, real F.Cu parts/service cards, harness envelopes, fastener tools and actual bottom-off access. Derive a tolerance budget from manufacturer drawings and a physical rail gauge.
4. Compare the current six-to-upper-cover supports with a rail-engaging sheet and narrower bolted or bonded reinforcement, including actual load path, switch torsion/shaft alignment, bending and racking stiffness, longitudinal/lateral restraint, vibration, assembly/disassembly and galvanic/0VA isolation.
5. Document the one-off CLOSE_BEFORE_FAB / ESCAPE_ROUTE_REQUIRED / BENCH_ONLY_ACCEPTABLE disposition and independent assurance before any architecture supersession.

## Explicit exclusions

- No PCB native edit, new mounting hole, panel drilling or release transition is authorised.
- No completed structural FEA, physical fit gauge, switch force/torque stiffness, cover drop-on path, mated H120/H220 cards or full continuous swept path is claimed.
- AE-076F1C erroneous cover datum Y=-76.914081 mm and resulting negative PCB-sheet clearance are rejected; its independent lateral rail-width sensitivity remains usable as nominal evidence.
- Existing regulated rail authority remains +17.0 V / 0VA / -17.0 V; existing R909 0-ohm bond and C909/D901/D902 DNP options must not be bypassed by carrier hardware.

## Manufacturer data routes for later qualification (not yet imported)

- NKK official NR01105ANG13 product/CAD: https://www.nkkswitches.com/wp-content/themes/impress-blank/search/inc/part.php?part_no=NR01105ANG13
- NKK NR01 family installation PDF: https://www.nkkswitches.com/pdf/NR01%20Rotaries.pdf
- C&K/Littelfuse A rotary series: https://www.littelfuse.com/products/switches/rotary-switches/a-rotary
- C&K 7201SYCBE manufacturer-part catalogue (CAD model download route, not verified): https://www.digikey.co.uk/en/products/detail/c-k/7201SYCBE/40082

**Release:** routing HELD; layout FALSE; BOM FALSE; manufacturing FALSE.
