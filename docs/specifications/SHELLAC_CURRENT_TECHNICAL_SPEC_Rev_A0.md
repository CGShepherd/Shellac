# Project Shellac — Current Technical Specification — Rev A0

**Reconciliation:** S35B-S14, 18 November 2026. **Source parent:** `develop` `7f13ac9f71bf4b73ce387c30bef02c42ef433c83`.

**Status:** CONTROLLED SELECTED-NEXT / NOT PHYSICALLY IMPLEMENTED / NOT FOR FABRICATION. The machine-readable companion is `config/decisions/current_spec_manifest.yaml`. This record becomes current selected-next design authority only after governed review, regression and merge. It does not supersede native KiCad, electrical source, safety/release controls or the authoritative current decision index.

## 1. Precedence and evidence rules

1. **Implemented now:** native sources and the implemented-status provisions in `config/decisions/current_decision_index.yaml`; physical PCB and current BOM/generator remain unchanged by S14.
2. **Selected-next:** the values in the companion manifest, which have been selected for development but not implemented. A design preference does not constitute validation.
3. **Superseded:** earlier configuration records remain immutable engineering history. In particular, `AE-007`'s 4P4T matrix, `AE-041`'s original C&K preference, and `AE-076F4T`'s C&K toggle / 17 mm candidate do **not** override later decisions. `AE-076F4C` controls the present TE matrix part identity.
4. **Evidence hierarchy:** actual physical measurements / authenticated native CAD / executed tests with scope and conditions / analyses / unverified development proposals. A generic PASS must always specify the tested predicate.
5. Physical, simulated and system-level validation are different gates. The one-off build is not to depend on a speculative manufacturing respin.

## 2. System configuration and boundaries

- Two-channel playback preamplifier supporting 78 rpm and true RIAA equalisation. One main audio PCB is the selected architecture.
- Regulated analogue supply **+17 V / 0VA / -17 V**, with `R909=0 Ω` the sole intended 0VA–CHASSIS link. No other intentional bond is authorised.
- Governed PCB is presently **220 × 140 mm**. Proposed **220 × 148 × 1.6 mm** board is NOT implemented; all seven physical control footprints and their final mounting holes remain pending native migration.
- Other analogue functional blocks, component tolerances and PSU details remain governed by their own existing decision records. S14 does **not** assert a product-wide requalification of SCH101–SCH108 or the PSU.

## 3. Current Channel Matrix (SCH105)

- Selected TE Connectivity / Alcoswitch **MRJE3404**, TE order **1825537-3**, **3-pole, 4-position, break-before-make**. The incorrect historical 4-pole/3-position verbal description must never be used for this part.
- Operator sequence (CCW to CW): **DUAL L, STEREO, L+R, DUAL R**. Pole A chooses left-buffer input; pole B chooses right-buffer input; pole C joins `MONO_R_LEG` to `MONO_AVG` ONLY in the L+R state.
- Two 4.7 kΩ 0.1% nominal mono resistors; per-channel 2.2 MΩ input returns; dual OPA1656 unity output buffers. No additional matrix gain is intended.

| Mode | Left output | Right output | Pole C |
|---|---|---|---|
| DUAL L | L | L | Open |
| STEREO | L | R | Open |
| L+R | (L+R)/2 | (L+R)/2 | MONO_R_LEG joined to MONO_AVG |
| DUAL R | R | R | Open |

**Verified at model level:** The live `generator/model/mode_matrix.py` and `generator/blocks/mode_matrix.py` implement the 3P4T intention. `AE-068 RUN05` documents a reviewed steady-state simulated pass: worst direct insertion 0.000861 dB; nominal mono insertion −0.018608 dB at 1 kHz; separation under a **hypothetical 5 pF bracket** of 72.00 dB at 20 kHz. These numbers are not physical measured performance and the capacitance is not a switch-specific qualified value.

**Not yet verified:** the exact TE 15-terminal number-to-net allocation; physical detent sequence/direction/BBM; final PCB pin/footprint orientation and solder penetration; switching transients (RUN12) and real-hardware correlation. The user owns an actual MRJE3404, measured approximately 11 mm shoulder-to-pin-tip, 27 mm shoulder-to-shaft-end, 6.5–7 mm threaded bush, plus a small O-ring shoulder. These dimensions are **user-supplied approximate caliper results**, not a released manufacturer tolerance drawing. The next engineering transaction shall map the actual 15 terminals and four detents by continuity before physical footprint release.

## 4. Seven-control mechanical selected-next, unimplemented

| Feature | Selected-next value | Remaining acceptance condition |
|---|---|---|
| Four Bass/Treble controls | Two `NR01105ANG13-2C` and two `NR01105ANG13-2A`, standard AT3009 knobs | Native apertures, assembly tolerances, control footprint orientation |
| Rumble/Mute | Two `UB226SKG03N-5C`, PCB-mounted without local raisers | Native pad/terminal map, button travel/access and cover aperture |
| UB2 apertures | 16.5 mm square **candidate only** | Prove corner radii, tolerance, panel machining and fingertip use |
| Main board | 220 × 148 × 1.6 mm **candidate** | Genuine native KiCad implementation, support sites, clearance/DRC |
| Main board support | Six M3 pillars; nominal **16 mm**; adjustable until proved | Full side-groove-to-cover and underside tolerance stack |
| Carrier | G1 lower-groove sliding 1.5 mm aluminium sheet, separate 2 mm reinforcement | Bearing/retention, stiffness, service withdrawal, insulation/grounding |
| Carrier retention | **Option B:** removable groove stops; **Option A fallback:** extended side members | Actual groove fixing detail and end-panel wiring clearance |
| Matrix mounting | Three independent pillars and 1.5 mm aluminium spider plate | Height, plate position, TE hardware, pin-root/solder relief and shaft engagement |
| H802 | Candidate B `(148.100001,125.7291)` mm | Exact mated connector, harness and extraction, 3D fit, native migration |
| Carrier relief | Local voids allowed **if a clash is demonstrated** | Load paths around M3 supports, PCB underside and actuation forces |

Selected seven-centre positions in candidate KiCad XY: Bass L/R `(76,53)/(184,53)`; Treble L/R `(76,86)/(184,86)`; Rumble `(130,86)`; Matrix `(130,118)`; Mute `(130,153)`. Positions are **not drill authority**.

The S35B-P06 FreeCAD survey was user-run: TE/Metcase/NKK model geometry was imported in earlier gates; P06 confirmed 4 UB2 solids and 42 Metcase G1 solids. P10–P13 were subsequent non-governed native-development screens. They do not supersede a registered fully populated physical assembly, nor imply cover/retention acceptance. **No complete seven-control installed 3D qualification has passed.**

## 5. Verification, simulation and validation ladder

| Gate | Present status | Required release evidence |
|---|---|---|
| Correct TE part, logical 3P4T design | Documentary/source consistency confirmed | No reversal without a governed new decision |
| Actual TE switch continuity | OPEN | Three commons, four throws per pole, terminal numbering and CCW/CW/BBM test |
| Matrix RUN05 steady state | REVIEWED PASS for model and 5 pF bracket | Preserve scope and model version |
| RUN08–RUN14 including RUN10 and RUN12 | OPEN/PARTIAL | Numerical accepted simulations with correct ±17 V source and parasitic assumptions |
| Exact switch footprints, native PCB and routing | HELD | Net-to-pin parity, DRC/DFM, copper/fastener clearance |
| Full G1/carrier/switch native assembly | OPEN | Installed transformations, collision/clearance, tolerances, serviceability |
| Physical hardware validation | NOT STARTED | Real operating and performance acceptance (gain, EQ, noise, THD, fault handling) |

Before fabrication, unresolved findings must be classified as `CLOSE_BEFORE_FAB`, `ESCAPE_ROUTE_REQUIRED` or `BENCH_ONLY_ACCEPTABLE` under the existing one-off build recoverability standard. No blanket deferral of mechanical respin risk is permitted.

## 6. Controlled invariants

`final_routing=false`, `layout_freeze=false`, `bom_freeze=false`, `manufacturing_release=false`. No BOM quantity/purchasing or panel drilling approval follows from this specification. No governed design or source file is physically migrated by S14.

## 7. Exact next transaction after S14 merge

**P14: map the real MRJE3404 in all four detents against manufacturer 15-terminal nomenclature, using low-energy continuity testing, and produce one accepted contact truth table. BBM transition timing remains a separate manufacturer/dynamic-test qualification, not something a static multimeter continuity test proves.** Do not revisit the now-reconciled 3P4T part selection. Then continue registered seven-control MCAD, with the selected 16 mm candidate and no UB2 raisers.
