# Project Shellac — Controlled Design Pack Index

**Working authority:** `develop` plus `config/decisions/current_decision_index.yaml`.

**Production authority:** a tagged `main` release after production/reproducibility gates close.

## 1. Current design baseline

Use first:
- implemented `generator/` source on `develop`;
- `config/decisions/current_decision_index.yaml`;
- `config/decisions/document_authority.yaml`;
- controlled BOM/procurement configuration;
- latest passing regression suite.

Current signal-chain status:
- DR-037: current — complete canonical RIAA retained in SCH103; duplicate independent 3180 us stage removed;
- DR-038: current architecture qualification open — AE-071A migrates the fail-safe gain/service-capacitance topology; AE-075B selects LT5400BIMS8E-7#PBF, implements EP9 to quiet 0VA and selects compatible Samtec TSW/MNT hardware. RUN10 complete-stage tolerance/CMRR, physical shunt pairing/orientation, short-route parasitics and bench qualification remain open;
- DR-039: current architecture qualification open — AE-074 migrates the AE-067 branch-local topology into the live generator while preserving C30060/R30060/C35060/R35060 identities: 1 uF / 330 kOhm only in DIRECT/BYPASS, with intrinsic SCH107 high-pass DC blocking in FILTER; native-PCB F8/net/metadata reconciliation is complete; RUN09/RUN10/RUN12 and bench correlation remain open;
- DR-040: current subject to the live implementation and subsequent assurance records;
- AE-041 Rev A1 + AE-075C hardware + AE-076B: current control architecture — one main audio PCB carries all seven controls directly as an upper-cover service module; six PCB-to-cover supports are selected but MCAD Z/XY/tolerance, exact footprints/3D envelopes, control XY/apertures and physical CAD migration remain B03-open; historical AE-075D/E/F remain provenance; AE-068 RUN05 electrical qualification remains unchanged;
- AE-042 through AE-076B: current assurance chain; AE-071A migrates SCH101, AE-071B hardens board-owned MH1-MH4, AE-074 migrates DR-039, AE-075A closes post-SR043 placement/sense-cap reconciliation, AE-075B closes B06 while narrowing B04/B08, AE-075C freezes exact control hardware, AE-075G closes the SCH108 output-interface migration, AE-076A reconciles +17 V rail authority, and AE-076B selects the one-main-PCB upper-cover service-module architecture while deliberately retaining SR-040/AE-071B MH1-MH4 as interim physical CAD pending AE-076B2 MCAD closure; RUN08-RUN14 and prototype/bench obligations remain open;
- AE-072/AE-073: historical/supporting PSU assurance chain — AE-072 establishes the AIYIMA P1-V reconstruction and AE-073 closes the long-settle discriminator. AE-076A subsequently establishes +17.0 V / 0VA / -17.0 V as current product rail authority and requalifies integrated nominal sanity plus SCH108/PRE90 headroom at that rail condition. Powered PSU set-point/dropout/ripple/startup/thermal qualification remains open;
- prototype measured acceptance: open.

This is not yet a manufacturing baseline. The next intended configuration milestone is the **Shellac Pre-SPICE Architecture Baseline** after repository reconciliation, clean regression and configuration-control closure.

## 2. Decision register

Current status:
- `config/decisions/current_decision_index.yaml`

Status semantics:
- `config/decisions/decision_status.yaml`

Authority classification:
- `config/decisions/document_authority.yaml`

Historical prose is retained as provenance and is not rewritten merely because a later state exists.

## 3. Assurance chain

AE-001 through AE-010: block-level history.
AE-011/012: end-to-end architecture and headroom.
AE-013/014: SCH101 precision redesign.
AE-015: full-chain noise/DC finding.
AE-016/A/B: failed migration and repair history.
AE-017/018: atomic migration and LT5400 physical contract.
AE-019/020: documentation-control structure.
AE-023: implemented production signal-chain analytical closure at that historical state.
AE-024/025: production design-record reconciliation at that historical state.
AE-040B: historical/superseded control-authority state; retained as provenance.
AE-041 Rev A0: superseded intermediate DP4/A20403RNCG matrix authority; retained as historical provenance only.
AE-041 Rev A1: current 3P4T matrix and top-cover control authority.
AE-042: SCH101 pre-SPICE interim design authority.
AE-043: SCH103 pre-SPICE analysis.
AE-044: DR-039 / SCH107 coupled pre-SPICE review establishing that the common pre-split 1 uF / 330 kOhm block is materially loaded by SCH107 and requires architectural requalification.
AE-045: SCH104 pre-SPICE analysis.
AE-046: SCH105 pre-SPICE analysis.
AE-047: system headroom, power and ground pre-SPICE reconciliation.
AE-048: full-system SPICE qualification matrix.
AE-049: SPICE numerical acceptance criteria.
AE-050: SPICE execution package.
AE-051: pre-SPICE non-simulation issue reconciliation.
AE-052: DR-039 / SCH107 pre-SPICE architectural downselect; branch-local direct-path DC block is the preferred SPICE candidate while the existing SCH107 filtered branch provides intrinsic DC blocking. This is a preferred candidate, not implemented authority, until integrated qualification closes.
AE-053: LTspice/Python simulation-toolchain architecture; LTspice is the authoritative integrated analogue solver, Python is the controlled orchestration/extraction/acceptance/reporting layer, and the existing analytical Python remains an independent cross-check. Reference LTspice models shall not be silently rewritten.

AE-054 through AE-058 establish implemented LTspice/Python execution and analytical-correlation infrastructure. AE-059 reconciles configuration-control semantics without implementing AE-042 or AE-052.

AE-060 establishes the fail-closed integrated-model contract and model-source preflight. It does not claim that SHELLAC_TOP is yet implemented or qualified.

AE-061 establishes controlled model-source provenance, corrects the primary Grado cartridge identity to Prestige 78C, and keeps model ingestion fail-closed until artefacts are captured and verified.

AE-062 qualifies the locally acquired OPA1656, OPA161x/OPA1612, LT5400-7 and THAT1646 model sources against controlled hashes, exact subcircuit interfaces and LTspice smoke execution. Vendor payloads remain external to the repository pending redistribution review; 1N4004 provenance remains open.

AE-063 reconciles the live SCH108 clamp identity from generic axial 1N4004 to Vishay S1G, matching the existing SMA footprint, and qualifies the manufacturer S1G SPICE model as a controlled external reference. System phantom-fault qualification remains open.

AE-064 qualifies controlled behavioural electrical source equivalents for Grado Prestige 78C and Audio-Technica AT-VM95SP, adds a non-gating Grado Gold/8MZ compatibility model, and closes the integrated model-source gate. Cartridge body/return bench verification remains open and SHELLAC_TOP itself is not yet implemented.

AE-065 implements the first genuine selected-next `SHELLAC_TOP` integrated candidate-analysis model and passes nominal RUN00 structural/DC sanity. It does not migrate AE-042/AE-052 into the live product generator; RUN01-RUN14 and R-024 remain open.

AE-066 executes integrated AC RUN01-RUN03. RUN01 resolves the loading matrix while retaining the Grado 78C 20-50 kHz behavioural-model validity finding; RUN02 qualifies nominal SCH101 gain/CMRR; RUN03 qualifies all 25 nominal SCH103 Bass x Treble states with close independent analytical correlation. AE-066 also consolidates simulator infrastructure and prepares controlled component/model candidates for RUN04-RUN06. No product-generator migration is implied; RUN04-RUN14, tolerance/Monte Carlo and bench correlation remain open.

AE-067 executes RUN04 and closes the DR-039/SCH107 architectural down-select. The branch-local direct-path 1 uF / 330 kOhm block passes the AE-049 LF criteria with nominal SCH107 values, adds no material noise penalty relative to the post-switch alternative, and limits the internal selector transient to about 3.79 mV under the RUN04 discriminator. The current common pre-split topology fails LF criteria; the post-switch common topology is rejected by its approximately 249.5 mV charge transient; and the x10-scaled alternative is rejected by LF/noise/value-engineering evidence. The topology is selected pending product-generator implementation; RUN09, RUN10, RUN12 and bench correlation remain open.

AE-068 executes RUN05 for SCH104/SCH105. All four matrix states are exercised with L-only, R-only, equal, unequal and opposite-phase stimuli. Direct insertion, mono insertion/weighting and stereo crosstalk pass AE-049. A 5 pF lumped selector/PCB parasitic bracket gives approximately 98 dB separation at 1 kHz and 72 dB at 20 kHz; even 10 pF remains above the 60 dB 20 kHz minimum. The 2.2 MOhm returns are retained. The existing AE-041 A1 4.7 kOhm / 0.1% mono-resistor implementation remains current; RUN05 derives <=0.10% preferred / <=0.25% maximum pair mismatch as an input to RUN10 tolerance/value engineering, not as an AE-068 BOM relaxation. RUN09/RUN10/RUN12 and bench switch/parasitic correlation remain open.

AE-069 executes RUN06 for SCH108. Normal 100 kOhm / 20 kOhm / 10 kOhm load gain variation and passband peaking pass AE-049, DC-offset limits pass, and the 600 Ohm stress case records approximately -0.688 dB gain droop. The 3.21 Vrms severe-input 10 kOhm case retains approximately 3.91 dB margin to the 10 Vrms design ceiling. Official Murata small-signal ferrite models are hash-controlled for exact-topology 1-100 MHz AC evidence. The combined THAT1646/Murata/S1G transient stack is not reproducibly convergent, so transient load stability is not claimed from SPICE; prototype load/cable stability remains mandatory. Dynamic large-signal THD likewise remains a bench gate because the controlled THAT1646 macro does not support reproducible periodic large-signal analysis. No ferrite, sense capacitor mechanical implementation or product-generator change is frozen by AE-069.

AE-070 executes RUN07 for representative end-to-end nominal states. Historical 78 and RIAA replay accuracy, integrated rumble response and nominal mono insertion pass AE-049. L/R comparison is nominal model symmetry only; tolerance tracking remains RUN10/RUN11. The controlled THAT1646 output pair and complete upstream chain each solve independently, while the full integrated composition reproducibly times out; RUN07 therefore uses an explicit qualification-only small-signal AC surrogate after controlled composition discrimination plus magnitude/load and isolated phase correlation. The surrogate cannot support DC/common-mode, transient stability, distortion, overload/recovery, switching or phantom/fault claims. No ferrite or product-generator migration is selected by AE-070.

AE-071 performs the post-RUN07 pre-routing integrity reconciliation. It corrects SCH101 local package bypassing and OPA1655/LT5400 physical identity, SCH103/SCH108 negative-bulk polarity representation, SCH107 470 nF film footprints and generated Capacitor_THT exposure. Native hierarchical ERC then exposed six genuine engineering-model hierarchy omissions: four dual-mono EQ control signals plus MONO_AVG and MONO_R_LEG. AE-071 carries those signals explicitly across SCH103/SCH109 and SCH104/SCH105, reconciles the resulting 74 hierarchical pins / 23 cross-sheet signals, and assigns the eight new SCH101 bypass capacitors to their existing gain/converter placement clusters. Historical SR-041 remains provenance only; current routing authority is held by config/release/ae071_prerouting_hold.yaml until the listed product, procurement, mechanical and interface blockers close.

AE-071A migrates the AE-042 SCH101 selected-next topology into the live product generator after AE-066 nominal evidence. The eight old 0-ohm service links are removed; six PCB service headers and two additional load capacitors preserve the 255-reference population while changing its identity set. Production Samtec shunt pairing/orientation and cartridge-load header parasitic/layout behaviour remain routing blockers; RUN10 retains tolerance/CMRR authority.

AE-071B closes the native-PCB mechanical-ownership defect exposed during AE-071A F8 reconciliation. MH1-MH4 remain at the frozen SR-040/SR-043 identity and coordinates, but are now explicitly board-only, locked and excluded from BOM/POS output so future delete-unused-footprint updates cannot remove them.

AE-072 establishes the physically reconstructed AIYIMA P1-V PSU authority and qualifies controlled RUN00 manufacturer-macromodel execution. It does not constitute powered hardware qualification or change the Shellac nominal rail requirement.

AE-073 executes the long-settle RUN01 discriminator and confirms that the exploratory 400 ms apparent ~±15.6 V ceiling is a startup-settling artefact. The target-17 investigation settles to about +16.843 V / -16.804 V with the LF353 outputs near zero. Powered set-point, dropout, ripple, startup and thermal qualification remain open, and no rail-authority change is made.

AE-074 migrates the AE-067 DR-039 branch-local topology into the live product generator and generated schematic source while preserving C30060/R30060/C35060/R35060 physical identities. The common SCH103 pre-split block is removed; the same 1 uF / 330 kOhm networks exist only in the SCH107 DIRECT/BYPASS branches, while FILTER uses its intrinsic high-pass capacitors. AE-074 closes native-PCB F8 reference relink, net and metadata reconciliation and resolves AE071-B02; RUN09/RUN10/RUN12 and bench correlation remain open.

AE-075G closes the SCH108 balanced-output connector electrical/native migration with exact Molex 5055780221 H801/H802 headers, HOT/COLD-only harnesses and no PCB-to-panel 0VA conductor. It corrects the live THAT1646 source-impedance semantics to 25 Ohm per leg / 50 Ohm differential, resolving AE071-S01. A separate application-specific PRE90 2 kOhm discriminator records 0.209239 dB worst insertion loss and negligible audio-band peaking; the worst high-gain representative state is about 9.098 V rms, only 0.190 dB below the published 9.3 V rms input-sensitivity figure, so high-level hardware/operating correlation remains mandatory. Historical AE-069 RUN06 evidence and its bench gates are unchanged. H801/H802 imported XY is explicitly provisional pending manual placement reconciliation.

AE-076A closes the nominal rail-authority drift by making +17.0 V / 0VA / -17.0 V current across the live generator, current simulation contract, commissioning model and native PCB net identities. Fresh integrated RUN00 and SCH108/PRE90 rail/headroom evidence passes at ±17 V. Historical ±18 V records remain immutable; RUN06 bench gates, RUN08, RUN10, RUN13, RUN14 and powered PSU qualification remain open.

AE-076B supersedes the current AE-075D/E/F local-control-board/carrier ownership architecture with one main audio PCB carrying all seven controls directly as part of the removable upper-cover service module. Six PCB-to-cover supports are selected but their XY/Z/hardware/tolerance stack is open. NKK 12.3 mm installation evidence remains controlled; C&K fit must be proven by AE-076B2 MCAD. SR-040/AE-071B MH1-MH4 geometry remains unchanged as interim physical CAD; no placement/routing release is implied.

AE-076B2A records the 261 F.Cu / 0 B.Cu native audit and selects F.Cu-down electronics with B.Cu-up direct controls. The four 11 mm SCH108 sense capacitors therefore leave the NKK 12.3 mm upper-cover stack. Exact B.Cu control footprints/pin maps, C&K common-plane fit, six-support geometry and full MCAD clearance/service review remain open; native geometry is unchanged.

AE-076B2B hash-controls the public official M5502119 drawing, four official Neutrik panel STEP models and a source-bound KiCad PCB STEP. The authenticated M5502119 STEP is ingested and hash-controlled; drawing-to-STEP dimensional reconciliation remains open. The five-pole DC interface is NC5FD-LX-B at the PSU source and NC5MD-LX-B at the audio chassis; pin 1 remains 0VA, pin 4/shell CHASSIS, and the optional pin1-shell bond is prohibited.

AE-042 through AE-076B2B, including AE-071A/AE-071B and the AE-072/AE-073 PSU assurance narrative, are assurance/evidence records. They do not by themselves constitute manufacturing release authority.

AE-048 and AE-050 remain the qualification and execution authorities for the simulation campaign. AE-049 remains the historical numerical-acceptance basis; AE-076A narrowly supersedes its nominal-RUN00 rail criterion for the current +17 V / 0VA / -17 V product authority and records targeted rail/headroom requalification. AE-053 remains the toolchain architecture.

## 4. Production/commissioning

Still required:
- completion of integrated RUN08-RUN14 under AE-048/049/050, plus the still-open RUN06 prototype load/cable-stability and dynamic-THD bench gates and the open Grado extended-band model/bench finding;
- integrated full-system configuration qualification following AE-059 reconciliation;
- Shellac Pre-SPICE Architecture Baseline configuration milestone;
- full-system LTspice qualification and sensitivity/value-engineering work;
- measured CMRR/noise/DC/overload/transient acceptance;
- cartridge terminal/isolation bench confirmation where required;
- grounding-population and phantom-energy closure;
- final PCB/mechanical release;
- manufacturing release checklist;
- fabrication outputs frozen to a release commit;
- complete commissioning sheet;
- clean-clone reproducibility evidence.

The intended simulation implementation sequence begins with toolchain implementation, RUN00 model sanity and analytical correlation before Monte Carlo or value engineering.

## 5. Maintenance

Current signal-chain baseline:
`docs/maintenance/Signal_Chain_Commissioning_and_Maintenance_Baseline_Rev_A0.md`

Maintenance documentation must be reconciled to the final electrically qualified implementation before manufacturing release.

## 6. Historical evidence rule

Superseded/staging records remain provenance and do not determine current hardware.

In particular, historical linked-stereo Lorlin/Grayhill control concepts and the historical 4P4 matrix must not override AE-041 Rev A1 or the current generator/BOM architecture.

## 7. Change-control rule

Future implemented changes must update source/CAD, tests, current decision index,
assurance evidence, BOM/procurement and maintenance information together where applicable.

No implemented functionality may exist without an explicit requirement or controlled design decision, and no controlled design decision may be treated as implemented without corresponding implementation evidence.

Reference LTspice models and vendor macro-models are controlled evidence inputs. They must not be silently rewritten; any wrapper, substitution, patch or behavioural replacement must be explicit, traceable and justified.
