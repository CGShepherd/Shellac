# AE-076F4B — NKK Flange/Lid Clearance Constraint and Corrected Native Screen — Rev A0

**Date:** 13 October 2026\
**Decision status:** SELECTED GEOMETRIC ACCEPTANCE REQUIREMENT; PHYSICAL IMPLEMENTATION / REQUALIFICATION OPEN\
**Authority effect:** Adds a narrow mechanical acceptance constraint and disposes of incorrect F4A native 2D numbers. Does **not** replace AE-041-A1, AE-076B support authority, the selected C&K A30403RNCB part, or the native PCB.\
**Evidence provenance:** The accepted post-F4A successor package; exact original verified JSON copied verbatim to `docs/design_pack/evidence/` alongside this record. The local source scripts were run before this transaction, not re-executed by this promotion.\
**Source baseline discriminator:** Native PCB SHA-256 `a5b519a21a2bbe2c9f3ad751134d43292a5b32184487100512ab045b6258861c`; F4A screen generator SHA-256 `b64e3216d5d64c646aab07f60eedde749ae3bd11c2d2803041965ec2a2f4a50b`.

## 1. Selected requirement and rejected nominal stack

**F4B-01 — Positive under-lid clearance.** All four NKK NR01105ANG13 controls (two `-2A`, two `-2C`) shall be seated on their authenticated PCB-bearing shoulders. Their Ø16 mm flanged knobs remain beneath the upper-cover panel in the intended installed and removal motions. The **minimum tolerance-inclusive operational flange-to-cover axial clearance must be strictly positive**, allowing for panel/rail/laminate/PCB/spacer/control dimensional variation, fastener seating, relative deflection and service motion. There is **no approved quantitative minimum gap** yet; touching contact, purely nominal zero-clearance and unproven interference are unacceptable.

**F4B-02 — Rejected *as studied*, not globally prohibited.** The **unmodified** G1 lower-bearing-face carrier with direct 18.000 mm PCB supports and directly paired 28.000 mm TE pillars, **without** engineered support-seat offset, panel relief or datum change, is **not an acceptable selectable support-height configuration**: the current nominal flange-to-panel gap is `-0.047488 mm`. Do not freeze those direct lengths or manufacture on an assumption of mere touching fit. Independently engineered 18/28 mm hardware arrangements are not ruled out, but they require a newly qualified datum and whole-assembly/tolerance demonstration.

**F4B-03 — Candidate coordinates retained, not drilling authority.** The corrected KiCad-native 2D screen retains candidates `ADD_A (120,120)`, `ADD_B (150,50)`, `TE_LEFT (143,144)`, `TE_RIGHT (189,124)`, and `TE_FRONT (165,104)` in mm. It does not select exact hole sizes, authorise PCB drilling, freeze the five coordinates, guarantee copper-zone clearance, or prove installed 3D fit. Historical F4A reconstructed-pad clearance figures are **superseded for screening** by the corrected-native JSON; F4A reports remain provenance.

## 2. Evidence and independent nominal checks

### Corrected native KiCad evidence

`docs/design_pack/evidence/AE-076F4B_Corrected_Native_Screen.json` is a byte-for-byte copy of `SHELLAC_POST_F4A_CORRECTED_NATIVE.json`, SHA-256 `ce3817200b3344c090d09732e43017099c67acda610dafee97eae9cec0fb331f`.

- KiCad 10.0.4; 256 footprints; 598 pad objects; zero tracks/vias; 252 cached filled F.CrtYd regions (four interim MH footprints lack front courtyards).
- Corrected rotation reconciles all 598 pad coordinates with native KiCad positions to better than 0.000002 mm; 23 original F4A reconstructed-coordinate discrepancies recorded.
- Candidate `ADD_A/ADD_B/TE_LEFT/TE_RIGHT/TE_FRONT`, respectively, have positive conservative existing-copper gaps `+9.458/+2.859/+2.745/+2.363/+1.055 mm` and filled front-courtyard residual gaps `+6.162/+2.575/+2.645/+0.724/+0.763 mm`.
- Pad-size-circumscribing circles and existing F.CrtYd are only a conservative geometric *screen*. Future planes, 4-layer DRC, real pad edges, mounted controls, connectors, service tools and tolerance remain open.

### NKK STEP and lid coupon evidence

`docs/design_pack/evidence/AE-076F4B_NKK_Flange_Stack_Probe.json` copies `SHELLAC_NKK_LID_PROBE_VERIFIED.json`, SHA-256 `afc49e9d5147d3aa040e8132931ec0ab4b0ad415bf711658484ffb1cbe9c5d2e`.

- Genuine source STEP hashes: `NR01105ANG13-2A.stp` `ede38fcc6f51791ed8f7f5ed2f524df8f6ef7ce1a19778bad2c52d4b380f84cd`; `NR01105ANG13-2C.stp` `29fecfb6c2b523e49884b4cfcbcbd633b32d0f55a27d15718e3dadca09ceb678`.
- Four planar PCB-bearing shoulders per genuine model at local Y = `-9.992 mm`; Ø16 mm flanged knob upper face at Y = `+2.308 mm`; nominal bearing-to-flange height `12.300 mm`.
- Current G1 lower-lip face depth `31.852512 mm` below lid, direct PCB support `18.000 mm`, board thickness `1.600 mm`: B.Cu-to-lid `31.852512 - 18 - 1.6 = 12.252512 mm`, flange gap `12.252512 - 12.300 = -0.047488 mm`.
- Genuine-model intersection with an **analytical coupon**, assumed Ø12.4 mm test aperture and 2 mm panel, gives `3.813244 mm³` collision for each variant, matching `π × (8² − 6.2²) × 0.047488` to numerical precision. This confirms nominal interference under the stated placement; it is **not** a seven-control lid/assembly fit result or an approved panel aperture.
- Spacer sensitivity at the unchanged G1 face: nominal flange gap in mm = `17.952512 − direct PCB spacer length`. Do **not** infer a selected spacer from this sensitivity formula.

## 3. Current authority and migration boundary

- **Remain current:** one main PCB with seven direct controls; F.Cu down and B.Cu up; current six-primary-support PCB-to-removable-upper-cover mechanical selection; C&K `A30403RNCB` matrix selection; functional passive 3P4T BBM matrix, operator mode order, and all +17 V / 0VA / −17 V power/earthing authority.
- **Retain as selected *development direction*, not implemented product authority:** independent reinforced single-G1 rail carrier with six PCB supports; separately supported three-pillar TE `MRJE3404`/`1825537-3` matrix plate. No physical stack or specific spacer sizes selected for manufacture by F4B.
- **Prohibited by this promotion:** editing seven-control footprints or native PCB supports; introducing the five candidate holes; freezing switch/panel XY/Z or nut geometry; changing the BOM to TE; superseding historical controls/supports; energising routing; declaring the mechanical design PDR/CDR-complete.

## 4. Conditions before the next configuration downselect

1. Establish TE 1825537-3 shoulder, retention, washer/nut, pin root/tip and shaft/knob seating at the candidate common control height; verify terminal numbering and B.Cu contact transform from exact manufacturer data.
2. Establish both C&K `7201SYCBE` toggle seated bushing/terminal dimensions and actual access/reach. The accepted temporary upright lever-handling procedure remains, but is not an electrical OFF position.
3. Build worst-case dimensional stack from available spacer/sheet/PCB, rail, panel, NKK/TE/C&K manufacturing tolerances; choose a strictly positive *quantified* required clearance after allowable motion and deflection. Check obtainable hardware and screw engagement.
4. Qualify true seven-control lid lowering/lifting, knob flange capture, panel holes, mated service connectors/cards, harness/bend radii, fastener/tool access and lower-side component envelope.
5. Independently verify single-guide rail insertion, carrier rigidity, frame retention/centering/end stops and 0VA–CHASSIS isolation. The only intended link remains R909=0Ω.
6. Qualify final native numbered footprints, all-layer copper/plane voids, mask/annulus/hole tolerance, physical DRC and manufacturing enquiry **before** any PCB/panel/fabrication migration.
7. Complete RUN08–RUN14 and independent design assurance for later PDR/CDR candidacy; this F4B constraint does not close those gates.

**Gate state after F4B:** ROUTING HELD; layout freeze FALSE; BOM freeze FALSE; manufacturing release FALSE; PDR/CDR candidate freeze FALSE. No product implementation or physical fabrication authorised.
