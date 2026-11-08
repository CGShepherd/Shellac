# Project Shellac — Persistent Working State

## CURRENT — F7H engineering-continuity checkpoint, 8 November 2026

**Classification:** NON-AUTHORITATIVE execution index. No design, PCB, CAD or manufacturing promotion.

### Governed baseline and completed integration

- Verified local `C:\Engineering\Shellac` on clean `develop` at pre-checkpoint HEAD `502ea3e916d61dd6eb882895c2d20ab87a8117f8`; matched `origin/develop` at the last local synchronisation.
- GitHub PR #1 merged into `develop`; merge commit `502ea3e916d61dd6eb882895c2d20ab87a8117f8`. Merge CI run 42394459320 passed.
- F7G evidence regression installed: five changed files; historical U1–U5 reports remain NONBINDING. Historical source register `config/mechanical/ae076f7g_shunt_access_evidence.yaml`.
- Current governed KiCad PCB SHA-256 `6824b2c311173046e0fd8ec782d8a61ba017ca2cc359cc7a17179252b28f81a2`; implemented outline 220 x 140 mm, 256 footprint instances, seven switch footprints not yet implemented.

### F7H authenticated model sources

- Metcase `M5502119.stp`: SHA-256 `9bf09314db1e8ffb596c27cceecb932141d3e43ba8d5ca4998fd4d16411b91fa`; user verified exact local file under `mechanical/mcad/vendor/cache`.
- NKK `NR01105ANG13-2A.stp`: SHA-256 `ede38fcc6f51791ed8f7f5ed2f524df8f6ef7ce1a19778bad2c52d4b380f84cd`; user verified internal STEP in `source_evidence/NKKSWITCHES_NR01105ANG132A.zip`.
- NKK `NR01105ANG13-2C.stp`: SHA-256 `29fecfb6c2b523e49884b4cfcbcbd633b32d0f55a27d15718e3dadca09ceb678`; user verified internal STEP in `source_evidence/NKKSWITCHES_NR01105ANG132C.zip`.
- TE `c-1825537-3-a-3d.stp`: SHA-256 `24e75b2dd8187e63ee200f278dd84016c8e705525980846cd78b37aa4fdeb3d9`; user verified internal STEP in `source_evidence/ENG_CVM_CVM_1825537-3_A.3d_stp (1).zip`.
- Dropbox source root: `000_Projects/000_Audio/Shellac_Engineering_Staging/`. Manufacturer hashes verify source identity, not full assembly fit. FreeCAD 1.1 Python installation was reported present.
- Historical F6H carrier STEP not found in the searched locations; its old 228 x 156 mm PCB assumption is not current product geometry.

### Selected-next mechanical candidate and source chain

- Current controlled support authority remains AE-076B: six PCB-to-removable-upper-cover supports. No formal supersession.
- Selected-next: Metcase G1 independent lower carrier; 220 x 148 x 1.6 mm PCB; six 17 mm M3 PCB supports; separate 1.5 mm TE plate on three independent pillars; four NKK and two C&K toggles direct to the single PCB.
- F4Z verified historical candidate PCB SHA-256 `1199112d3238489c282fb0d078c2effb34e08cf36dda67969114a4a1ecd6fd5f`, under Dropbox `transactions/AE-076F4Z_FIX2_EQUILATERAL_LOCKED_CANDIDATE_NOT_FOR_FAB/`.
- F4Z equilateral TE pattern: centre (125,118), 35 mm radius; MHTE1 (140.343,149.458), MHTE2 (90.085,115.559), MHTE3 (144.572,88.984), coordinates in KiCad XY mm. Earlier F4T non-equilateral pillar coordinates remain historical, not the primary candidate.
- F5A preview SHA-256 `7dcc3911aebf47cd70a998738357ada1c1dfdd97e037f032246e89ba62077f85`: six paired L/R component movements, C7701/C7201, C75094/C70094, TP7504/TP7004. All six original footprint positions independently observed unchanged on current native PCB. Historical 1.638 mm minimum copper-void screen is nominal only.
- F5B preview SHA-256 `c7b4183c0700e3da0c74506eb2dcbfed066916b298288a6ed808b1462337d540`: provisional seven-switch body witnesses.
- F5C preview SHA-256 `a804526e5f8904d1d9f5e5927e249602d190122ee0ea9c95913d258fc3fdd92f`: 67 unnumbered physical-site witnesses. F5E historical report records 51 contact-site registrations without verified vendor numbering/net assignments.
- F5A/F5B/F5C/F5E records are under their named `AE-076F5*` Dropbox transaction folders. They predate current PCB changes and are NOT FOR FAB. None may be promoted without fresh reconciliation.
- U5 historical candidate broad shunt handwell `(145,12)-(211,60)` mm is NONBINDING; no complete-assembly, real finger-grip, structural or harness qualification.

### Outstanding qualification and next action

- Full native FreeCAD assembly on reconciled current-source 220 x 148 mm shadow PCB: authentic Metcase, true seven-switch orientations and manufacturer solids, TE retainer/plate/fasteners, C&K provisional bodies clearly identified, six PCB supports, connector mates and cable envelopes.
- Verify underside/cover registration, mechanical interference, positive worst-case NKK flange clearance, C&K threaded retention, carrier windows/stiffness, G1 capture, hardware access and actual shunt-service motion.
- Preserve true numbered B.Cu switch-contact mapping, electrical parasitic/RUN08–RUN14, four-layer DRC and independent assurance as separate gates.
- Governing holds in `config/release/ae071_prerouting_hold.yaml`: `final_routing=false`, `layout_freeze=false`, `bom_freeze=false`, `manufacturing_release=false`.
- **Next bounded engineering transaction:** current-board-based, read-only F7H native registration/assembly qualification. No older F4Z/F5A–F5E reconstruction or further manufacturer download is required merely to recover known history.

**Checkpoint verification:** This entry records the pre-transaction baseline. Verify subsequent commit, PR and CI status using Git and GitHub; this document does not certify its own integration.

## HISTORICAL — AE-076F7G evidence-regression checkpoint, 7 November 2026

**Authority:** NON-AUTHORITATIVE execution index only. Current governed design/configuration/release files take precedence. This entry records a reviewed feature branch, not a promoted design or manufacturing baseline.

### Verified Git and qualification

- GitHub PR **#1** (`AE-076F7G — Integrate nonbinding mechanical evidence regression`) is an **open draft** targeting `develop`; it has **not** been merged. The initially verified feature commit is `e12c1d4150d0bcb681b0b7f8b871604d35f3e757` on `feature/ae076f7g-mechanical-evidence-regression`.
- Governed `develop` and `origin/develop` were checked at `4274622e34578a9d9d36761b441ec183dc736c3a`, with the Windows governed checkout reported clean. Do not treat this recorded hash as a substitute for a fresh preflight at the next transaction.
- At commit `e12c1d4`, local isolated-worktree focused pytest **9 passed**, complete pytest **781 passed**; GitHub CI push run **#96** and pull-request run **#97** both passed. Five U1/U2/U3/U4R/U5 historical JSON reports were byte-verified against the staged evidence register on Windows. Ordinary CI does **not** fetch those external reports or rerun FreeCAD.
- PR #1 initially adds four qualification files only: the nonbinding evidence YAML, a fail-closed provenance validator, nine pytest cases and a design-pack qualification-boundary document. The present documentation-only update to this index requires its own CI verification before merger.

### Mechanical configuration and remaining gates

- Current implemented mechanical authority remains **AE-076B** (six PCB-to-removable-upper-cover supports). Current governed native board is **220 × 140 mm**. The independent Metcase G1 reinforced lower carrier, six **17 mm** PCB spacers, TE three-pillar bracket and **220 × 148 mm** PCB are **selected-next, not implemented or approved for fabrication**.
- U5 used historical F6H geometry associated with a **228 × 156 mm** study PCB. Its candidate **R3 66 × 48 mm** gain-shunt handwell `(145, 12)–(211, 60)` mm connected W8/W2 and passed the limited native planar/connected-metal/Metcase screen. It remains **NONBINDING**, without demonstrated real pinch-grip service, full-assembly registration, tolerance/structural acceptance or cable retention.
- Outstanding before a manufacturing baseline: complete correct-board/current-carrier registration; actual seven-switch, cover, support and TE plate stack; native FreeCAD integrated BREP; connector/harness envelopes and strain relief; cable-web/stiffness/fastener assessment; accessible shunt service; governed mechanical architecture supersession; routing/DRC, RUN08–RUN14, hardware evidence and independent design assurance.
- Governing release file remains `config/release/ae071_prerouting_hold.yaml` (AE-076D): `final_routing=false`, `layout_freeze=false`, `bom_freeze=false`, `manufacturing_release=false`. No native PCB, CAD, panel, mechanical manufacturing, routing or BOM promotion is implied by this record.
- **Next bounded transaction:** complete PR #1 review and checks, then deliberately merge the regression-only change if approved. After the updated `develop` baseline and this index are reconciled, undertake integrated 220 × 148 mm PCB/carrier/Metcase registration with durable Tier-1 pytest and separate authenticated native FreeCAD Tier-2 qualification.

### Historical interpretation

Sections below are retained for traceability. Earlier `CURRENT` claims, baseline hashes, PCB dimensions and directions become historical when they conflict with this checkpoint or live governed authority.

---

## HISTORICAL — F7G-D working-state reconciliation, 3 November 2026

**Authority:** NON-AUTHORITATIVE execution index. Current decision/configuration authority and live governed source take precedence. Historical sections below remain provenance, not current execution instructions.

### Governed source and evidence

- Active checkout: `C:\Engineering\Shellac`; previous Dropbox checkout is a procedurally read-only rollback reference.
- Governed `develop` HEAD and independently verified `origin/develop`: `fb273fff59b3e082163d2501ec5a10bebb544a34`.
- F7F correction committed and pushed, with clean working tree verified at F7F-E4.
- F7F-D complete regression: 771 passed, zero failed.
- F7F-E3 established decision/configuration authority audit: PASS.
- No PCB, schematic, physical harness, panel, enclosure, routing or fabrication release resulted from F7F.

### Electrical and harness interfaces

- Regulated rails: +17 V, 0VA, -17 V.
- Preserve R909 0R as the sole intended 0VA-to-CHASSIS bond.
- Five-pole Neutrik DC panel interface: pin 1 0VA; pin 2 +17 V; pin 3 -17 V; pin 4 CHASSIS; pin 5 reserved. Do not bond panel pin 1 to connector shell.
- Separate six-position Molex Mini-Fit Jr. PCB header H901: pin 1 0VA (black AWG18); pin 2 +17VA_IN (red AWG18); pin 3 -17VA_IN (blue AWG18); pin 4 CHASSIS (green/yellow AWG18); pins 5 and 6 unpopulated in mating loom.
- F7E FIX2 authentic native pad/net mapping and F7F governed generator/test correction establish this PCB-side contract. They do not establish completed cable continuity, polarisation, approved mating housing/crimps, strain relief or external PSU polarity.
- F6Z nominal populated-body H901/R909 clearance approximately 5.768 mm with zero solid intersection, not mated-harness qualification; leave R909 at its governed location.

### Mechanical authority and selected-next concept

- Current controlled primary PCB support architecture remains AE-076B: six PCB-to-removable-upper-cover supports. This has NOT been superseded.
- AE-076F4T selected-next concept: independent reinforced Metcase G1 rail carrier; six 17 mm M3 PCB supports; proposed 220 x 148 mm PCB; independent 1.5 mm TE three-arm plate supported by three pillars. Physical migration, frame retention, PCB holes, geometry tolerances and fabrication acceptance remain OPEN.
- Earlier F3L 20 mm PCB and 30 mm TE spacer studies and other preliminary pillar XY coordinates remain historical candidate evidence, not the current selected-next geometry.
- Four NKK NR01105ANG13 switches use AT3009 knobs; two C&K 7201SYCBE toggles use direct keyed-cover/two-nut retention; TE MRJE3404 / 1825537-3 is the selected channel-matrix part. Exact physical switch footprints, hole numbers, seating and complete assembly remain unqualified.
- The native production PCB has not been changed by the F7F harness correction.

### Release, risk and execution disposition

- Current routing hold: `config/release/ae071_prerouting_hold.yaml`, AE-076D; `final_routing: false`, `layout_freeze: false`, `bom_freeze: false`, `manufacturing_release: false`.
- Historical SR-039/SR-041/SR-042 release snapshots are explicitly quarantined; historical `ROUTING_RELEASED` does not grant current permission.
- Pre-fabrication holds include RUN08-RUN14 qualification as applicable, RIAA/input tolerance and noise, exact seven-switch footprint/contact mapping, real G1 carrier and mated connector fit, power harness/crimp/polarity, full four-layer DRC, reviewed routing rules and independent design assurance.
- One-off build recoverability rules remain governed by `docs/knowledge/ONE_OFF_BUILD_RECOVERABILITY_STANDARD.md`.
- **Next:** continue F7G root-and-branch requirements/technical-debt reconciliation. Review discrepancies against current decision index and executable source before changing authority. No new layout/routing or fabrication release.

### Historical interpretation rule

The older date-labelled notes, prior Git HEAD claims, early spacer geometries and former critical-path instructions below are preserved as evidence. They must not be used as current instructions without reconciling them against this status, the current decision index and live source.

---


**Purpose:** cross-chat continuity and execution index.
**Authority status:** NON-AUTHORITATIVE SUMMARY. If this file conflicts with controlled current authority, the controlled authority wins and this file must be corrected before further major work.
**Refresh rule:** update after every material engineering review, qualification pass, governed transaction, commit/push, or change to the critical path.

## Mandatory interaction mode - user instruction, 13 October 2026

Project Shellac must continue in a normal ChatGPT chat. Do not use Codex or ChatGPT Work for this project, create or delegate Shellac work to either, or switch the user into either environment.

This restriction remains in force unless the user explicitly revokes the Shellac-specific restriction. Requests such as "continue", "review", "resolve", "promote", or a request involving code, Git, Python, KiCad or other engineering tools do not revoke it.

If this project is opened in Codex or ChatGPT Work, stop project engineering activity, explain this standing instruction, and provide a normal-chat handoff. Do not run project commands or change project files. The only exception is a narrowly scoped administrative handoff or policy update explicitly requested by the user; that is not permission to resume engineering.

Normal ChatGPT may analyse evidence, use connected tools within the user's request, and prepare bounded, fail-closed scripts or patches for the user to run. Preserve controlled design authority and release holds. This interaction policy is a written instruction, not an app-enforced access control.

## AE-076F5Y - KiCad 10 toolchain migration (26 October 2026)

- **Qualified selected toolchain:** KiCad 10.0.7 with version-specific CLI fallback, generator footprint paths and 197 native PCB 3D-model paths; three project STEP references unchanged. Historical `kicad9.py` module name retained.
- **Scope:** five exactly reviewed implementation/regression files plus `docs/maintenance/AE-076F5Y_KiCad_10_Native_Configuration_Migration_Rev_A0.md` and this non-authoritative index. Isolated candidate 771 tests passed, authority audit PASS, KiCad10 ERC/DRC class and STEP topology unchanged.
- **Holds preserved:** 14 ERC findings, 336 DRC findings plus 432 unconnected items, all selected-next mechanical controls/PCB 220x148, routing/fab/BOM and PDR/CDR holds. KiCad9 stays installed until separate dependency review; FreeCAD–KiCad integration remains deferred.

## AE-076F5U - active local workspace (26 October 2026)

- **Administrative workspace cutover:** `C:\Engineering\Shellac` is the sole normal active checkout following the governed AE-076F5U commit/push. Use `C:\Engineering\Shellac\.venv\Scripts\python.exe`; GitHub `CGShepherd/Shellac` remains the promoted source authority.
- The previous Dropbox checkout `C:\Users\chris\Dropbox\000_Projects\000_Audio\Shellac` is retained unchanged as a **procedurally read-only rollback reference**, not a second active engineering location. No old-repository rename, deletion, reset or merger is authorised.
- F5P/F5Q/F5R-FIX1/F5S/F5T verified KiCad10 connectivity/3D, generator, local Git checkout, 771 tests and recovered assets. Refer to `docs/maintenance/AE-076F5U_Active_Engineering_Workspace_Cutover_Rev_A0.md` for scope, exact evidence and rollback.
- **Holds unchanged:** KiCad9 library/model variables remain in native source; retain KiCad9 installed pending governed migration. Existing ERC14, DRC336, 432 unconnected, physical-switch, 220 x 148 candidate, routing/fabrication and BOM release holds remain. New-location cloud backup/restoration required before retiring Dropbox rollback.

## Current selected-next mechanical mounting — AE-076F4T (15 October 2026)

- User approved the seven-switch *mounting-method* downselect; native implementation and physical acceptance remain OPEN. TE MRJE3404 / 1825537-3 returns to separate 1.5 mm aluminium plate on three independent pillars; no TE lid nut or custom top-hat. Four NKK NR01105ANG13 -2A/-2C retain standard AT3009 flanged knobs, fully seated PCB mounting. Both C&K 7201SYCBE toggles retain a directly profiled inward-keyed Metcase cover opening and individually adjusted lower/upper retaining nuts; no extra toggle bracket or custom top-hat. Do not reopen these alternatives without contradictory evidence and a new decision.
- AE-076F4R user-run native nominal check PASSED: candidate PCB 220 x 148 x 1.6 mm, six 17 mm M3 supports (existing four plus 110,90 and 110,157), TE plate posts (106,118), (142,92), (142,144), no nominal Metcase substrate or existing-component support hits. These XY, Z, holes and seven control footprints remain SELECTED-NEXT ONLY, NOT DRILLING AUTHORITY. Native PCB remains 220 x 140 with no added switch footprints.
- Controlled AE-076B legacy SIX PCB-TO-UPPER-COVER primary support authority is NOT superseded. AE-076F4B four-NKK flange positive worst-case clearance continues. Mandatory CLOSE_BEFORE_FAB: actual TE bearing/nut/plate assembly and fastening, C&K inner-key panel detail and upper/lower nut/short pin no-preload tolerance, all seven shaft/panel handedness and service lid motion, retained G1 carrier/end stops and connector harness, numbered/mirrored switch footprints and native four-layer DRC/fab acceptance. No routing/layout/BOM/fabrication/PDR/CDR release.
- AE-076F4T selected-next choice record: `docs/design_pack/AE-076F4T_Switch_Mounting_Selection_Rev_A0.md`, indexed as `CURRENT_SELECTED_PENDING_IMPLEMENTATION`. Source Git HEAD on entry: `450ed541d2ab58cd73671df245c8ff071116c236`; verify resulting promotion commit and push separately. Staged F4R evidence remains informational.

## Historical continuation note - 13 October 2026

- **AE-076F4C published selection (13 October 2026):** `develop` HEAD/origin `3ed361dbe90c7ca0c401a1ab8aa4f82ae3f0c3c8`; TE Connectivity/Alcoswitch MRJE3404 / 1825537-3 is the sole current Channel Matrix SW903 part, and C&K A30403RNCB is superseded historical evidence only (NO selected fallback). The 3P4T BBM truth table is unchanged. Exact indexed physical terminal-to-net mapping, separate three-pillar plate, shaft/knob, tolerance stack, PCB holes, RUN10/RUN12 and full MCAD remain CLOSE_BEFORE_FAB. Six upper-cover PCB supports remain the governed architecture until a separate deliberate supersession. ROUTING HELD; layout/BOM/manufacturing freeze and release FALSE. Parent `482c7bb37eb8ccaf3e23d80f6871885bc6273bad`.

- **AE-076F4D information-only drawing/STEP reconciliation (staged, 13 October 2026):** Rev A3 manufacturer PDF SHA-256 `f4319d2a91999bb09c6c9f036ab5e9585ed62f552cd2682d82f9af2bfd90ea6b`; 15 shaft-end drawing terminals match 15 F3O genuine STEP witness positions one-to-one in the existing unmirrored analysis reference (maximum stored-coordinate residual 0.000006 mm). Evidence `Shellac_Engineering_Staging/reports/SHELLAC_AE076F4D_TE_REV_A3_CONTACT_GEOMETRY_READONLY.md/.json`, living handover Rev A9. 30-degree detents and BBM are drawing-supported; CCW/CW stop-to-throw indexing, actual shaft-flat datum, B.Cu mirror, pin/DFM, plate/knob and full assembly remain OPEN. This is not a manufacturing pinout release.

- **AE-076F4B published geometric constraint:** corrected native coordinates reconcile 598 pad centres and preserve five support sites as *unreleased* 2D candidates. Genuine NKK models give 12.300 mm bearing-to-flange height; the unmodified lower-G1 direct 18 mm PCB / 28 mm TE support pair overlaps the lid nominally by 0.047488 mm and must not be frozen. All four NKK flanges require positive tolerance-qualified underside clearance. This requirement does not supersede the six-upper-cover-support architecture or authorise any spacer, hole, panel, PCB, PDR/CDR or release; the **later AE-076F4C matrix part supersession is separate and current**. Decision record: `docs/design_pack/AE-076F4B_NKK_Clearance_and_Corrected_Native_Screen_Rev_A0.md`.

This note records conversation continuity; it does not promote design authority or replace controlled evidence. The older engineering baseline below is retained as provenance and must be reconciled with later evidence before any governed transaction.

- User objective: keep resolving and promoting supported design decisions in bounded controlled updates, then present a frozen candidate to reviewers for PDR/CDR. Avoid repeated general analysis that does not close a decision. No reviewer has been contacted in this handoff.
- User-reported F4A staging succeeded: six information-only artefacts staged, Rev A7 archived, Rev A8 installed. Rev A8 SHA-256: ee78f9bb8408b56c45adf5480d2d1302717c048a8d13a9e809fd61cb2dace27f. The successful staging reported governed Git/PCB/STEP unchanged.
- Two successor studies were reviewed and accepted by the user, but are not staged or promoted: corrected native pad transform, and genuine NKK knob/lid stack interference. Their evidence is in SHELLAC_POST_F4A_SUCCESSOR_REVIEW_PACKAGE.zip and SHELLAC_POST_F4A_CORRECTION_AND_NKK_STACK.md. Carry these into the next normal chat; do not assume automatic cross-chat file access.
- Corrected native screening reconciles all 598 pad centres and retains the five candidate support coordinates. Positive analytical clearances are not full native layout or manufacturing qualification.
- NKK flange height is 12.300 mm above the PCB. The studied 18 mm PCB / 28 mm TE support pair yields 0.047488 mm nominal interference with the lid; genuine-model coupon intersection confirms the issue. Do not freeze these spacer lengths. Reconcile the TE and toggle seating stacks, tolerance allowance and service access before choosing the common datum and obtainable hardware.
- TE MRJE3404 / 1825537-3 is now the **governed sole matrix part** under AE-076F4C, but its independent reinforced G1 lower carrier, six independent PCB supports and three-pillar TE plate remain **selected development direction, not governed mounting authority**. The six-upper-cover-support architecture has not been superseded. Preserve the distinction between selected parts, investigated mechanical concepts and physically implemented hardware.
- Routing HELD; layout freeze, BOM freeze and manufacturing release FALSE. No PDR/CDR completion or release is claimed.
- Engineering stopped for the user's normal-chat handoff. This administrative update changed only PROJECT_GUIDANCE.md and PROJECT_SHELLAC_WORKING_STATE.md. An additional AGENTS.md stop instruction was prepared, but creating it in the repository was denied by the filesystem; it is not installed. No commit or push was performed. Review these intentional documentation changes during the next governed preflight; do not discard or absorb them as unrelated changes. Current Git cleanliness was not verified during this handoff.

## 1. Historical repository baseline (13 October 2026)

- Branch: `develop`
- Last independently verified governed HEAD/origin: `3ed361dbe90c7ca0c401a1ab8aa4f82ae3f0c3c8` (AE-076F4C), published 13 October 2026 after local compilation/770-test promotion reported PASS and a successful fast-forward push/postcheck. Earlier AE-076F3N and AE-076F1F commits are provenance only.
- Current governed subject: `AE-076F4C: select TE matrix and preserve implementation holds`; governed predecessor `482c7bb37eb8ccaf3e23d80f6871885bc6273bad` (AE-076F4B); earlier AE-076F0/AE-076F1F remain historical promoted baselines.
- Promotion parent (historical AE-076E-A): `258751f56f536cc28e836c2d013dbde46aaf4cb6`
- Historical AE-076E-B / AE-076F0 parent: `2a912eac1c63313443f99dc87f86e07232f1a40b`
- Current working phase: `AE-076F — after F4C TE part-selection promotion, F4D informational contact geometry; physical and lower-frame qualification HELD; mechanical authority NOT superseded`.
- Native MCAD/PCB provenance: AE-076F1A–F1E established actual Metcase and intermediate PCB geometry. Later AE-076F4B establishes corrected 598-pad native coordinate screening and the unresolved NKK positive flange-to-cover clearance; AE-076F4D stages authenticated 15-terminal TE drawing-derived geometry. Actual PCB retains 256 footprints, interim MH1–MH4, zero mounted-control footprints and no support-architecture supersession.
- Historical transaction state: AE076E_B_PROMOTED_AE076F_QUALIFICATION_AND_MCAD_HELD — AE-076E-B promotion and AE-076F startup; preserved as continuity provenance.
- Current transaction state: AE076F4C_TE_MATRIX_SELECTED_PHYSICAL_QUALIFICATION_HELD — sole TE MRJE3404 selection published; six-upper-cover-support mechanical authority unchanged; C&K matrix historical only. AE-076F4D drawing evidence is informational, not a numbered PCB footprint or verified CCW/CW detent map. Local AE-076F4C promotion reportedly passed compilation and 770 pytest tests; Git fast-forward publication and clean tree verified. All routing/layout/BOM/manufacturing holds remain.
- Routing: HELD
- Layout freeze: FALSE
- BOM freeze: FALSE
- Manufacturing release: FALSE

## 2. Design essentials and historical candidates (verify current authority)

- Regulated rails: `+17.0 V / 0VA / -17.0 V`.
- One main audio PCB carries all seven controls directly.
- PCB orientation: F.Cu down / B.Cu up toward removable upper cover.
- **Current controlled support authority:** six PCB-to-removable-upper-cover primary supports; exact XY/Z/hardware/tolerances open, native footprint migration unauthorised. **Selected-next engineering concept (AE-076F3L, not authority):** stiffened open rail-engaged lower frame, independently supported main PCB on 20 mm M3 spacers, and flat three-arm TE switch plate on three separate 30 mm M3 metal pillars passing freely through three provisional PCB clearance holes. Conceptual carrier fit, actual holes and all control CAD remain CLOSE_BEFORE_FAB; no formal support supersession authorised.
- Bass: NKK `NR01105ANG13-2C` x2.
- Treble: NKK `NR01105ANG13-2A` x2.
- Channel Matrix production part: TE/Alcoswitch `MRJE3404` / `1825537-3` selected under AE-076F4C; C&K `A30403RNCB` superseded historical only.
- Rumble/Mute: C&K `7201SYCBE`.
- SCH101 LT5400: `LT5400BIMS8E-7#PBF`; EP9 to quiet 0VA implemented.
- Gain programming: TSW-104-07-G-D / MNT-104-BK-G, approximately 14/18/22 dB; no LOW/HIGH shunt = fail-safe ~18 dB.
- Cartridge loading: live dual per-channel main-board sockets, separate service cards remain qualification-open; no card=BASE; matched +47 pF and +100 pF L/R service pairs; audio path does not pass through card.
- AE-076E-A exact primitive: Samtec `SLW-102-01-G-D`, controlled 2x2 PTH footprint, pins 1/4=POS and 2/3=NEG; no generic 3D model substituted.
- Live generator and native PCB now implement per-channel H120/H220; H121/H122/C103/C104/C203/C204 are absent from the PCB, while H120 retains pins 1/4=POS and 2/3=NEG.
- DR-039 current implementation: branch-local 1 uF / 330 kOhm only in DIRECT/BYPASS; FILTER uses intrinsic SCH107 high-pass DC blocking.
- Grounding population: R909=0 ohm fitted; C909/D901/D902 DNP.
- H801/H802 output harness is HOT/COLD only with no 0VA conductor.
- Five-pole regulated-DC interface: pin1=0VA, pin2=+17 V, pin3=-17 V, pin4=CHASSIS, pin5 NC_RESERVED; pin1-shell bond prohibited.

## 3. Current one-off build philosophy

Shellac is expected to be a one-off build, not an iterative prototype-to-production programme.

Before fabrication, unresolved items must be classified as:
- `CLOSE_BEFORE_FAB`;
- `ESCAPE_ROUTE_REQUIRED`;
- `BENCH_ONLY_ACCEPTABLE`.

Where a residual uncertainty could otherwise require board or mechanical respin, provide a controlled low-impact recovery mechanism when technically sensible. Do not add speculative flexibility, especially in the cartridge/SCH101 low-level region.

Controlled standard:
`docs/knowledge/ONE_OFF_BUILD_RECOVERABILITY_STANDARD.md`

## 4. Historical pre-layout critical path (superseded as execution order)

1. Verified current published AE-076F4C baseline is `3ed361dbe90c7ca0c401a1ab8aa4f82ae3f0c3c8` on `develop`; TE is the selected matrix part, and the six-upper-cover-support architecture remains current mechanical authority. AE-076F4D drawing review and F3O terminal-site correlation are informational; neither is a numbered pinout/detent qualification or a physical implementation. Historical F3-series analyses remain supporting evidence, not design authority.
2. Perform bounded preliminary RUN10 design-driving tolerance/parasitic assessment at current `+17.0 V / 0VA / -17.0 V`, especially LT5400/CMRR, gain shunts, Grado 78C cable/loading and H120/H220 service-card parasitics, and SCH103 timing-component source/value choices. This is not full RUN10 closure.
3. Qualify the F3L preferred-next stiffened/open rail-engaged lower subframe and independent TE plate/pillar concept against authenticated Metcase and populated PCB models: measure G1 groove throat, check ~2.257 mm nominal downstand from G1 sheet-top to proposed frame bearing face, all switches/fasteners, H802/H120/H220 service envelopes, underside access, chassis capture/stiffness, tolerances, cover installation and grounding. The earlier six-cover-support concept remains CURRENT CONTROLLED authority pending deliberate supersession; no carrier geometry is yet released.
4. Complete RUN08-RUN14 under the current AE-076D qualification delta; preserve the AE-070 vendor THAT1646 full-chain AC model composition limit and prohibit transferring AC surrogate validity to nonlinear/noise/fault gates.
5. Resolve RUN10-driven SCH103 timing-cap decomposition and SCH108 ferrite selection before layout as justified; retain bench correlation where defensible.
6. Qualify the **selected** TE MRJE3404 alongside the four NKK and two C&K 7201SYCBE controls: determine actual CCW/CW detent-to-throw order, keyed/shaft-flat datum, terminal-to-B.Cu pad mirroring/rotation, solderability, real seven-control Metcase assembly and lid apertures. AE-076F4D informational Rev A3 drawing supplies a provisional 15-terminal shaft-end polar map; independent F3O STEP-centre comparison yields 15/15 unique nominal positions (maximum stored-coordinate residual 0.000006 mm), but this does not certify physical indexing or release a footprint. Screen three TE plate-pillar holes (investigative Ø7.0 mm NPTH / Ø9.5 mm all-layer voids) and six-plus independent PCB supports. No native PCB/panel alteration, routing or support supersession before controlled qualification.
7. Qualify ±17 V physical PSU set-point/dropout/ripple/startup/thermal behaviour, system rail fault-energy response and deliberate CHASSIS/0VA interfaces before system sign-off.
8. Freeze bounded four-layer fabrication stack, quantitative DRC/netclasses and instantiate/audit In1 0VA plane.
9. Conduct block-by-block independent design assurance, with explicit one-off recoverability classifications and documented dissent.
10. Consider routing release only after every relevant design-driving HOLD is resolved and a controlled permission transition is authorised.

## 5. Formal block-review sequence

Review in this order:
1. cartridge / input XLR / harness;
2. SCH101 RF, loading, gain and precision front end;
3. SCH103 replay EQ;
4. SCH107 rumble/direct path/DC blocking;
5. SCH104 isolation and mono preparation;
6. SCH105 channel Matrix;
7. SCH108 mute, THAT1646, ferrites, clamps and output interface;
8. 0VA / CHASSIS / earthing;
9. +17 V / 0VA / -17 V distribution;
10. external PSU: mains inlet through transformer, rectification, regulation, protection and DC cable.

Each block must end as:
- `PASS_FOR_LAYOUT`;
- `PASS_WITH_CONTROLLED_RECOVERY`;
- `HOLD`.

For every block review: implementation, evidence, component authority, PCB/MCAD, interfaces, FMEA/fault behaviour, procurement, serviceability, recovery path and residual qualification must be explicit.

## 6. Known open design-driving items

- AE-076F preliminary RUN10, full RUN08-RUN14, and full Metcase/PCB/seven-switch dimensional implementation of selected-next lower-subframe/TE-spider concept; AE-076E-B promotion is complete;
- exact SLW/TSW mated mechanical envelope and RUN10 interface parasitics/matching;
- exact component-specific capacitor body/mechanical fit and full MCAD collision assessment after successful H901/C30060/C35060 solid STEP export;
- gain-shunt physical pairing/orientation;
- RUN08 overload/clipping/recovery;
- RUN09 full-system noise;
- RUN10 tolerance/sensitivity/value engineering/parasitics;
- RUN11 Monte Carlo;
- RUN12 switching transients;
- RUN13 rail variation/ripple/start-up;
- RUN14 phantom/fault energy;
- SCH103 timing-cap source/value decomposition;
- SCH108 ferrite selection;
- exact seven-control B.Cu pin/pad/orientation mapping;
- controlled six-upper-cover-support authority supersession pending full MCAD and independent assurance; F3L three-point flat plate / independent 20/30 mm spacer alternative downselected for development only; TE retention/15-pin map/knob, PCB holes/all-layer copper/DRC, G1 rail downstand, full-chassis assembly, fasteners and service clearances remain CLOSE_BEFORE_FAB;
- bounded fabrication stack, In1 plane and quantitative DRC/netclasses;
- Grado 20-50 kHz model-validity/measurement disposition;
- PSU powered set-point/dropout/ripple/startup/thermal qualification.

## 7. Explicitly deferred to build/commissioning where presently acceptable

These remain subject to the recoverability standard and may move back to pre-fabrication closure if review shows respin risk:

- physical harness/crimp continuity;
- actual cartridge body/return continuity measurement;
- measured noise/CMRR/distortion correlation where no PCB change is expected;
- final hum/grounding confirmation with controlled R909/C909/D901/D902 population options;
- thermal measurements with the final assembled enclosure;
- load/cable stability and high-level PRE90 confirmation where design margin/recovery remains adequate.

## 8. Validation

- AE-076C governed baseline full suite: 743 passed.
- AE-076D governed baseline commit: `4975fba11a12f25744e35ea61e11578c66f3d50f`; promotion validated with 754 tests.
- AE-076E-A governed baseline: `258751f56f536cc28e836c2d013dbde46aaf4cb6`; promotion verified with 761 tests.
- AE-076E-B source-phase focused validation: PASS — 64 tests; current-decision audit and generated-SCH101 discriminator PASS.
- AE-076E-B native board SHA-256 `a5b519a21a2bbe2c9f3ad751134d43292a5b32184487100512ab045b6258861c`; H901 model `40cd349dcd35a3aa04844d09e13f92a40d90f1a664e1ad8baec2cd010259e87a`; capacitor model `35659ae3b9a50ddeb0aa5add4edfaea1770d99f3a8c2db7320eb8fb13be8ee1b`; actual-board STEP `84fae4cfe2fa5edc3436a36792f3da41c8f71d29e9cd711f469631b37200fe61`; KiCad CLI rc0 and no missing models, DNP excluded.
- AE-076E-B intermediate regression history: 764 passed/1 failed at superseded pre-F8 board assertion; subsequent 766 passed/1 failed at obsolete DR-038 wording. Both test contracts were reconciled to the live implementation.
- Full AE-076E-B governance-candidate regression on 2026-10-08: 767 passed in 45.34 seconds; decision/configuration authority audit PASS. Promoted Git `develop` baseline `2a912eac1c63313443f99dc87f86e07232f1a40b` was subsequently verified by read-only AE-076F startup on 2026-10-09: 767 passed in 47.46 seconds, authority audit PASS, hashes matched, local HEAD=origin/develop, clean index/tree. No routing/layout/BOM/manufacturing authorisation conferred.
- Reproducibility: the governed native PCB remains CRLF and SHA-256-pinned; .gitattributes uses a single-file -text -eol whitespace=cr-at-eol exception so staged/checked-out bytes remain identical without weakening Git whitespace verification.

- AE-076F0 governed commit `24899753d05597aedd7a2ced6a482e6e1001c705` promoted after 767 tests/decision audit; later read-only AE-076F1E reverified GitHub `develop` and clean index/tree.
- AE-076F1D authenticated Metcase and populated-PCB STEP models (FreeCAD 1.0.2), corrected the cover underside Y to -33.911678 mm, reported nominal populated-board-to-G1-carrier clearance 7.657547 mm, and sampled unobstructed carrier-only insertion with relevant end panel removed. No complete installation qualification.
- AE-076F1E controlled native PCB SHA-256 `a5b519a21a2bbe2c9f3ad751134d43292a5b32184487100512ab045b6258861c`: 256 F.Cu footprints; MH1–MH4 at (25,28), (235,28), (235,152), (25,152) mm; no physical seven-control footprints and no dedicated control CAD discovered by filename. Informational disposition `docs/design_pack/AE-076F1F_Native_Control_and_Mechanical_Evidence_Rev_A0.md`. Release held.

## 9. AE-076F3J–F3L mechanical implementation status (INFORMATIONAL, 2026-10-12)

- **Native baseline reverified by user-run F3J FIX2:** 1.60 mm board, SHA-256 `a5b519a21a2bbe2c9f3ad751134d43292a5b32184487100512ab045b6258861c`; 256 F.Cu footprints; 598 pads, comprising 592 other pads, four Ø3.2 mm interim MH1–MH4 NPTH supports and two Ø3.0 mm H901 connector locator NPTH holes; 12 F.Cu route/pour keepouts, no routed tracks or vias. Report/JSON/SVG staged outside Git under `Shellac_Engineering_Staging`; this is not layout or manufacturing approval.
- **Three-point mechanical downselect, user delegated:** TE candidate centre `(165,126) mm`; independent metal-post candidate centres LEFT `(143,144)`, RIGHT `(189,124)`, FRONT `(165,104) mm`. F3J native 2D Ø8 mm hypothetical hardware-to-nearest-courtyard gaps: +3.390 / +1.4705 / +1.506 mm. These are NOT authorised drill coordinates or 3D fastener/copper clearance.
- **F3L concept (non-governed):** 1.5 mm flat aluminium three-arm spider; TE MRJE3404 preferred development candidate mounted to three independent 30 mm M3 female/female pillars through provisional Ø7 mm non-plated PCB openings, with provisional Ø9.5 mm all-layer copper keepouts. Main 220×140×1.60 mm PCB independently supported by 20 mm M3 hex spacers at separate board fixing positions (4 perimeter plus at least 2 independently screened additional supports is an investigative target, NOT installed). Actual Harwin drawings, threads, spacing tolerances and procurement unqualified.
- **Nominal stack at cover underside datum 0:** PCB B.Cu +12.30 mm, F.Cu +13.90 mm; frame face +33.90 mm; 30 mm matrix pillars put plate lower surface / TE shoulder at +3.90 mm and 1.5 mm plate top +2.40 mm; TE housing gap 2.40 mm, pin-root gap 0.78 mm, pin tip projection 1.176 mm beyond F.Cu. These are conceptual model arithmetic, not qualified manufacturer solder/fastener/tolerance limits. Nominal G1 frame face ~2.257 mm below earlier guide-sheet top: unresolved true chassis fit.
- **Selected concept only, NOT full physical closure:** earlier bent top-hat, stacked-nut and PCB-clamping/shared-stud constructions no longer lead development unless contradictory evidence arises. The 3J real native 2D screen and F3L synthetic CadQuery coupon/STEP checks do not amount to a complete Metcase + true TE + real hardware + all seven controls assembly or electrical footprint acceptance.
- **Already resolved handling procedure:** C&K `7201SYCBE` Rumble/Mute toggle levers temporarily held upright during cover fitting/removal; do not reopen the tilted-lever clearance concern without contradictory physical evidence. This handling decision does NOT certify every other cover collision/fastener clearance.
- **Required CLOSE_BEFORE_FAB:** true TE 15 numbered pin/clockwise mode map; TE MRJE3404 procurement/stock evidence (part selection already CLOSED under AE-076F4C); TE real retaining nut, shaft/knob and plate clearances; board holes/4-layer copper/mask/DFM with full DRC; full authentic chassis STEP plus populated PCB and all seven switch/mated harness 3D fit; G1 bearing/rail stiffness and retention; neutral assembly/shim design; measured fastener tolerances and safe 0VA/CHASSIS isolation. Release gates remain ROUTING HELD, LAYOUT/BOM FREEZE FALSE, MANUFACTURING RELEASE FALSE. Sole intended 0VA–CHASSIS link remains `R909=0Ω`.
- **Authority boundary (reconciled AE-076F4C):** the six removable-upper-cover PCB supports remain the current governed mechanical architecture; TE `MRJE3404` / `1825537-3` is the current governed matrix *part* and C&K `A30403RNCB` is superseded historical evidence, not a fallback. Controlled current-facing BOM/configuration records were reconciled by AE-076F4C; neither the G1 carrier nor the TE plate, numbered footprint, PCB holes or panel has been authorised for implementation. The earlier F3L package remains historical informational concept evidence.

## 10. Continuity rule

Do not begin a major new Shellac phase from conversation memory alone.

At the start of a new chat:
1. read this file in full;
2. read `PROJECT_GUIDANCE.md`;
3. verify Git branch/HEAD/origin/working-tree state;
4. inspect the current authority files referenced by this summary for the task at hand;
5. update this file again before the next major phase transition.

This file is an index, not a substitute for controlled design records.
