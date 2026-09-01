# AE-024 Generated Design Record Reconciliation Audit

Repository: `C:\Users\chris\Dropbox\000_Projects\000_Audio\Shellac`

## Executive summary

- files containing decision/status references: **273**
- decision/status claim lines: **1208**
- baseline declaration lines: **807**
- status-vocabulary findings: **0**
- potential authoritative-status contradictions: **0**

This is an audit report, not an automatic rewrite instruction.

## Status-vocabulary findings

- None detected.

## Potential status contradictions

- None detected.

## Authoritative decision index

| ID | Status | Primary record |
|---|---|---|
| DR-037 | CURRENT_IMPLEMENTED | `docs/DR-037_Restore_Legacy_Complete_RIAA_Architecture_Rev_A0.md` |
| DR-038 | CURRENT_IMPLEMENTED | `docs/decisions/DR-038_SCH101_Precision_Architecture_SELECTED.md` |
| DR-039 | CURRENT_IMPLEMENTED | `docs/decisions/DR-039_Common_Post_EQ_DC_Block_SELECTED.md` |
| DR-040 | CURRENT_IMPLEMENTED | `docs/decisions/DR-040_Precision_CAD_Primitive_Staging_SELECTED.md` |

## Baseline declarations requiring reconciliation

- `APPLY_AE025A_INDEX_REPAIR.py:15` — print("Restored decision-index baseline semantics: branch=main; removed authority_scope.")
- `APPLY_AE025_INDEX_PATCH.py:7` — t=t.replace(needle, needle+"authority_scope: Working design authority is develop until a tagged production baseline is promoted to main.\n")
- `APPLY_DECISION_INDEX_RECONCILIATION.py:22` — print("Updated authoritative decision index to the validated DR-038/DR-039 baseline.")
- `manifest.json:5` — "baseline": "sr-027-component-selection-policy / 31809c1",
- `README.md:10` — - Implemented signal-chain baseline: **DR-037 / DR-038 / DR-039 / DR-040**
- `README.md:52` — tagged production baseline.
- `docs/AE-001_Replay_Equalisation_Synthesis_Rev_A.md:55` — capacitors with a changed resistor baseline, while requiring no exotic
- `docs/AE-003_Full_Band_Replay_Curve_Analysis_Rev_A.md:4` — **Status:** calculation baseline
- `docs/AE-011_End_to_End_Signal_Chain_Closure_Rev_A0.md:5` — **Baseline:** GitHub `main` at commit `4581c49`
- `docs/AE-011_End_to_End_Signal_Chain_Closure_Rev_A0.md:10` — This analysis reconstructs the complete Project Shellac analogue signal-chain assurance that predates the GitHub-controlled baseline. It deliberately does not assume that individua
- `docs/AE-011_End_to_End_Signal_Chain_Closure_Rev_A1.md:6` — **Baseline reviewed:** GitHub `main` at `4581c49`
- `docs/AE-013_SCH101_Noise_CMRR_Review_Rev_A0.md:59` — No previous explicit system CMRR requirement was found in the controlled baseline. A release acceptance value should therefore be created rather than retroactively claimed.
- `docs/AE-014_SCH101_Precision_Architecture_Downselect_Rev_A0.md:146` — These are proposed engineering requirements, not retroactive baseline claims.
- `docs/AE-016A_AE016_Regression_Repair_Rev_A0.md:7` — is valid for the current physical generator baseline and must not simply be
- `docs/AE-016A_AE016_Regression_Repair_Rev_A0.md:11` — - restores `generator/model/balanced_input.py` exactly to the pre-AE016 baseline;
- `docs/AE-016B_Full_Regression_Staging_Repair_Rev_A0.md:7` — AE-016B restores SCH103 to the pre-DR039 physical baseline while retaining the
- `docs/AE-016_DR038_DR039_Implementation_Baseline_Rev_A0.md:1` — # AE-016 — DR-038 / DR-039 Implementation Baseline
- `docs/AE-016_DR038_DR039_Implementation_Baseline_Rev_A0.md:5` — This update converts DR-038 and DR-039 into the controlled electrical baseline.
- `docs/AE-017_Atomic_Migration_Dependency_Mapping_Gate_Rev_A0.md:12` — doing its job: it encodes both the electrical baseline and the rendered CAD
- `docs/AE-017_Atomic_Migration_Dependency_Mapping_Gate_Rev_A0.md:57` — This prevents a second partial-baseline migration.
- `docs/AE-017_Generated_Atomic_Migration_Dependency_Map.md:227` — \| ANALYSIS \| `AE-012` \| `REPAIR_SIGNAL_CHAIN.py` \| 10 \| print("AE-012 signal-chain model is at its pre-DR039 controlled baseline.") \|
- `docs/AE-017_Generated_Atomic_Migration_Dependency_Map.md:236` — \| SCH103_OUTPUT \| `output_end = Point(420` \| `RESTORE_SCH103_BASELINE.py` \| 32 \| baseline = '''    output_end = Point(420, u2_out.y) \|
- `docs/AE-017_Generated_Atomic_Migration_Dependency_Map.md:239` — \| SCH103_OUTPUT \| `replay_eq.py` \| `RESTORE_SCH103_BASELINE.py` \| 44 \| print("Restored replay_eq.py to pre-DR039 physical generator baseline.") \|
- `docs/AE-017_Generated_Atomic_Migration_Dependency_Map.md:240` — \| SCH103_OUTPUT \| `replay_eq.py` \| `RESTORE_SCH103_BASELINE.py` \| 46 \| print("replay_eq.py already at pre-DR039 physical baseline.") \|
- `docs/AE-017_Generated_Atomic_Migration_Dependency_Map.md:289` — \| DR039 \| `DR-039` \| `docs/AE-016_DR038_DR039_Implementation_Baseline_Rev_A0.md` \| 1 \| # AE-016 — DR-038 / DR-039 Implementation Baseline \|
- `docs/AE-017_Generated_Atomic_Migration_Dependency_Map.md:290` — \| DR039 \| `DR-039` \| `docs/AE-016_DR038_DR039_Implementation_Baseline_Rev_A0.md` \| 5 \| This update converts DR-038 and DR-039 into the controlled electrical baseline. \|
- `docs/AE-017_Generated_Atomic_Migration_Dependency_Map.md:343` — \| SCH103_OUTPUT \| `replay_eq.py` \| `docs/updates/AE016B_UPDATE_MANIFEST.md` \| 6 \| - restore `generator/blocks/replay_eq.py` to its pre-DR039 physical baseline; \|
- `docs/AE-019_Design_Record_Reconciliation_Gate_Rev_A0.md:5` — This audit runs in parallel with signal-chain revalidation. It inventories controlled decision and assurance records without rewriting history. The eventual design pack will distin
- `docs/AE-019_Generated_Design_Record_Reconciliation.md:7` — \| `docs/AE-001_Replay_Equalisation_Synthesis_Rev_A.md` \| AE-001, AE-001B, AE-002 \| BASELINE, OPEN, SELECTED, SUPERSEDED \|
- `docs/AE-019_Generated_Design_Record_Reconciliation.md:9` — \| `docs/AE-003_Full_Band_Replay_Curve_Analysis_Rev_A.md` \| AE-003 \| BASELINE \|
- `docs/AE-019_Generated_Design_Record_Reconciliation.md:17` — \| `docs/AE-011_End_to_End_Signal_Chain_Closure_Rev_A0.md` \| AE-010, AE-011 \| BASELINE, CLOSED, OPEN, SELECTED, SUPERSEDED \|
- `docs/AE-019_Generated_Design_Record_Reconciliation.md:18` — \| `docs/AE-011_End_to_End_Signal_Chain_Closure_Rev_A1.md` \| AE-011, DR-037 \| BASELINE, SELECTED, SUPERSEDED \|
- `docs/AE-019_Generated_Design_Record_Reconciliation.md:20` — \| `docs/AE-013_SCH101_Noise_CMRR_Review_Rev_A0.md` \| AE-012, AE-013 \| BASELINE, CLOSED, SELECTED \|
- `docs/AE-019_Generated_Design_Record_Reconciliation.md:21` — \| `docs/AE-014_SCH101_Precision_Architecture_Downselect_Rev_A0.md` \| AE-012, AE-013, AE-014, DR-038 \| BASELINE, PROPOSED, SELECTED \|
- `docs/AE-019_Generated_Design_Record_Reconciliation.md:23` — \| `docs/AE-016A_AE016_Regression_Repair_Rev_A0.md` \| AE-016, AE-016A, DR-038, DR-039 \| BASELINE, SELECTED \|
- `docs/AE-019_Generated_Design_Record_Reconciliation.md:24` — \| `docs/AE-016B_Full_Regression_Staging_Repair_Rev_A0.md` \| AE-016, AE-016A, AE-016B, DR-038, DR-039 \| BASELINE, IMPLEMENTED, SELECTED \|
- `docs/AE-019_Generated_Design_Record_Reconciliation.md:25` — \| `docs/AE-016_DR038_DR039_Implementation_Baseline_Rev_A0.md` \| AE-016, DR-038, DR-039 \| BASELINE \|
- `docs/AE-019_Generated_Design_Record_Reconciliation.md:26` — \| `docs/AE-017_Atomic_Migration_Dependency_Mapping_Gate_Rev_A0.md` \| AE-016, AE-017, DR-038, DR-039 \| BASELINE, CLOSED \|
- `docs/AE-019_Generated_Design_Record_Reconciliation.md:27` — \| `docs/AE-017_Generated_Atomic_Migration_Dependency_Map.md` \| AE-010, AE-011, AE-012, AE-013, AE-014, AE-015, AE-016, AE-016A, AE-017, DR-038, DR-039 \| BASELINE, CLOSED, IMPLEM
- `docs/AE-019_Generated_Design_Record_Reconciliation.md:29` — \| `docs/AE-019_Design_Record_Reconciliation_Gate_Rev_A0.md` \| AE-019 \| BASELINE \|
- `docs/AE-019_Generated_Design_Record_Reconciliation.md:34` — \| `docs/decisions/DR-038_SCH101_Precision_Architecture_SELECTED.md` \| AE-010, AE-012, AE-016, DR-038 \| BASELINE, PENDING, SELECTED \|
- `docs/AE-019_Generated_Design_Record_Reconciliation.md:38` — \| `docs/knowledge/DECISION_REGISTER.md` \| AE-005, AE-007, AE-008, AE-009, AE-010 \| BASELINE, CLOSED, OPEN, SELECTED \|
- `docs/AE-019_Generated_Design_Record_Reconciliation.md:39` — \| `docs/knowledge/RECOVERED_BASELINE.md` \| AE-007, AE-008, AE-009 \| BASELINE, OPEN, REJECTED, SELECTED, SUPERSEDED \|
- `docs/AE-019_Generated_Design_Record_Reconciliation.md:40` — \| `docs/knowledge/RISK_REGISTER.md` \| AE-008 \| BASELINE, CLOSED, OPEN, SELECTED \|
- `docs/AE-019_Generated_Design_Record_Reconciliation.md:46` — \| `docs/updates/AE016B_UPDATE_MANIFEST.md` \| AE-012, AE-016, AE-016A, AE-016B, DR-039 \| BASELINE, PENDING, SELECTED \|
- `docs/AE-019_Generated_Design_Record_Reconciliation.md:47` — \| `docs/updates/AE016_UPDATE_MANIFEST.md` \| AE-016, DR-038, DR-039 \| BASELINE, SELECTED \|
- `docs/AE-019_Generated_Design_Record_Reconciliation.md:48` — \| `docs/updates/AE017_UPDATE_MANIFEST.md` \| AE-017, DR-038, DR-039 \| BASELINE \|
- `docs/AE-019_Generated_Design_Record_Reconciliation.md:50` — \| `docs/updates/AE019_UPDATE_MANIFEST.md` \| AE-019 \| BASELINE \|
- `docs/AE-019_Generated_Design_Record_Reconciliation.md:57` — - Assurance evidence identifies the baseline it analysed.
- `docs/AE-019_Generated_Design_Record_Reconciliation.md:58` — - Current design baseline separated from historical evidence.
- `docs/AE-020_Decision_Register_Reconciliation_and_Design_Pack_Structure_Rev_A0.md:5` — **Baseline:** `main` at `1ebb04d`
- `docs/AE-023_Production_Signal_Chain_Assurance_Closure_Rev_A0.md:12` — ## Implemented baseline verified
- `docs/AE-023_Production_Signal_Chain_Assurance_Closure_Rev_A0.md:127` — 3. mechanical/PCB production-baseline closure;
- `docs/G3-001_PCB_Architecture_and_Layout_Constitution_Rev_A0.md:7` — This baseline turns Gate 3 layout intent into a CAD-independent, testable model. It does not place components or emit a KiCad PCB. It defines what a future placement and routing im
- `docs/G3-001_PCB_Architecture_and_Layout_Constitution_Rev_A0.md:46` — This writes `out/layout/layout_baseline.json`, which is the machine-readable baseline used by future placement and routing tools.
- `docs/G3-002_Quantitative_Performance_and_Critical_Loop_Baseline_Rev_A0.md:1` — # G3-002 — Quantitative Performance and Critical-Loop Baseline
- `docs/G3-003_Mechanical_Datum_and_Preliminary_Placement_Baseline_Rev_A0.md:1` — # G3-003 — Mechanical Datum and Preliminary Placement Baseline
- `docs/G3-004_Commissioning_and_Verification_Baseline_Rev_A0.md:1` — # G3-004 — Commissioning and Verification Baseline Rev A0
- `docs/G3-004_Commissioning_and_Verification_Baseline_Rev_A0.md:10` — The baseline is intentionally conservative: no stage may be bypassed after a
- `docs/G3-005_Component_Cluster_Placement_Baseline_Rev_A0.md:1` — # G3-005 — Component-Cluster Placement Baseline Rev A0
- `docs/G3-009_Schematic_to_PCB_Footprint_Contract_Rev_A0.md:11` — native ERC baseline remain unchanged.
- `docs/G3-013A_G3-014_KiCad_Parser_and_Native_Pipeline_Rev_A0.md:1` — # G3-013A / G3-014 — KiCad PCB Parser Closure and Native Pipeline Baseline
- `docs/G3-015_Gate_3A_Macro_Acceptance_and_CLU-106_Refinement_Rev_A0.md:5` — The 220 mm x 140 mm board architecture and right-to-left functional flow were visually reviewed in KiCad and accepted as the Gate 3A macro-placement baseline.
- `docs/G3-022_PSU_Thermal_Mains_Release_Rev_A0.md:16` — G3-022 therefore **REJECTS M5501119** at the binary release gate. This is not a claim that a prototype necessarily overheats. It is a design-freeze decision: the 65 mm enclosure ca
- `docs/G3-025_Foundry_RIAA_Physical_Closure_Rev_A0.md:68` — - Foundry baseline exists in Git and is machine-readable;
- `docs/G3-027_RIAA_Integration_Audit_and_BOM_Reconciliation_Rev_A1.md:38` — The current controlled BOM is a partial baseline, not a procurement-complete BOM.
- `docs/SR-001_Schematic_Generation_Readiness_Audit_Rev_A.md:15` — schematic baseline.
- `docs/SR-001_Schematic_Generation_Readiness_Audit_Rev_A.md:70` — 7. Correct genuine ERC findings and freeze the schematic baseline.
- `docs/SR-014_Legacy_Sheet_Pin_Aware_Closure_Rev_A.md:44` — - Native KiCad hierarchical ERC: 286 findings, reduced from the accepted SR-013 baseline of 600.
- `docs/SR-015_ERC_and_Deterministic_Build_Closure_Rev_A.md:34` — The accepted SR-014 baseline reported 286 native KiCad findings. SR-015 closes all of them through renderer, library and connectivity corrections. No analogue engineering decision 
- `docs/SR-021B_Canonical_Grid_and_Electrical_Integrity_Foundation_Rev_A.md:4` — **Parent:** accepted SR-021 baseline
- `docs/SR-021B_Canonical_Grid_and_Electrical_Integrity_Foundation_Rev_A.md:81` — accepted baseline only after the new report has been reviewed. No analogue
- `docs/SR-021D_ERC_Branch_Topology_Closure_Rev_A.md:3` — **Parent baseline:** SR-021C
- `docs/SR-021G_Schematic_Baseline_Acceptance_and_Provenance_Policy_Rev_A.md:1` — # SR-021G — Schematic Baseline Acceptance and Provenance Policy
- `docs/SR-021G_Schematic_Baseline_Acceptance_and_Provenance_Policy_Rev_A.md:8` — baseline. Provenance now distinguishes immutable generated design artifacts
- `docs/SR-021_SCH107_Human_Reviewable_Conversion_Rev_A.md:59` — Gate 2A machine readiness: PASS on the accepted SR-020 baseline
- `docs/SR-023_SCH108_Human_Reviewable_Rev_A.md:5` — **Parent:** accepted SR-022 baseline
- `docs/SR-039_Schematic_to_Layout_Release_Gate_Rev_A0.md:7` — Validated baseline:
- `docs/SR-039_Schematic_to_Layout_Release_Gate_Rev_A0.md:35` — The controlled BOM remains a partial high-level baseline rather than a full
- `docs/SR-041_Critical_Placement_and_Routing_Release_Rev_A0.md:42` — All manual-authority clusters are accepted as the routing baseline subject to
- `foundry/FOUNDRY_BASELINE.md:1` — # FDR-001 — Project Shellac Foundry Baseline
- `foundry/README.md:17` — Foundry baseline: **FDR-001 / G3-025**.
- `scripts/report_commissioning_baseline.py:20` — print(f"Project Shellac commissioning baseline: {model.identifier} {model.revision}")
- `scripts/report_interface_architecture.py:36` — print(f"Mechanical baseline: {mechanical.status}")
- `scripts/report_kicad_native_pipeline.py:13` — baseline = write_kicad_native_pipeline_baseline(out)
- `scripts/report_kicad_native_pipeline.py:15` — print(f"Status: {baseline.status}")
- `scripts/report_kicad_native_pipeline.py:16` — print(f"PCB owner: {baseline.pcb_owner}")
- `scripts/report_kicad_native_pipeline.py:17` — print(f"Placement intent items: {baseline.footprint_count}")
- `scripts/report_kicad_native_pipeline.py:18` — print(f"Accepted / review: {baseline.accepted_count} / {baseline.review_count}")
- `scripts/report_kicad_native_pipeline.py:19` — print(f"Manufacturing holes frozen: {baseline.manufacturing_holes_frozen}")
- `scripts/report_layout_baseline.py:1` — """Report the provisional Gate 3 PCB architecture baseline."""
- `scripts/report_layout_baseline.py:18` — baseline = build_layout_baseline()
- `scripts/report_layout_baseline.py:21` — json_path.write_text(json.dumps(baseline.to_dict(), indent=2) + "\n", encoding="utf-8")
- `scripts/report_layout_baseline.py:23` — print(f"{baseline.identifier} — {baseline.revision}")
- `scripts/report_layout_baseline.py:24` — print(baseline.status)
- `scripts/report_layout_baseline.py:25` — print(f"Stack-up: {baseline.stackup.layer_count} layers")
- `scripts/report_layout_baseline.py:26` — print(f"Functional regions: {len(baseline.regions)}")
- `scripts/report_layout_baseline.py:27` — print(f"Critical-net classes: {len(baseline.critical_nets)}")
- `scripts/report_layout_baseline.py:28` — print(f"Manual-only net classes: {sum(n.routing_policy.value == 'manual_only' for n in baseline.critical_nets)}")
- `scripts/report_performance_baseline.py:13` — baseline = build_performance_baseline()
- `scripts/report_performance_baseline.py:14` — print(f"{baseline.identifier} — {baseline.revision}")
- `scripts/report_performance_baseline.py:15` — print(baseline.status)
- `scripts/report_performance_baseline.py:18` — for row in baseline.gain_settings:
- `scripts/report_performance_baseline.py:22` — for row in baseline.margins:
- `scripts/report_performance_baseline.py:25` — print(f"\nCriticality records: {len(baseline.criticality)}")
- `scripts/report_performance_baseline.py:26` — print(f"Placement constraints: {len(baseline.placement_constraints)}")
- `scripts/report_performance_baseline.py:27` — print(f"Open measurements: {len(baseline.open_measurements)}")
- `scripts/report_performance_baseline.py:32` — path.write_text(json.dumps(baseline.to_dict(), indent=2), encoding="utf-8")
- `tests/test_enclosure_decision_baseline.py:21` — baseline = build_mechanical_baseline()
- `tests/test_enclosure_decision_baseline.py:22` — candidate = next(item for item in baseline.candidates if item.identifier == "ENC-A03")
- `tests/test_enclosure_decision_baseline.py:23` — findings = decision_findings(candidate, baseline, DrawingEvidence(False, False, False, False, False, None))
- `tests/test_kicad_native_pipeline.py:8` — baseline = build_kicad_native_pipeline_baseline()
- `tests/test_kicad_native_pipeline.py:9` — assert baseline.pcb_owner == "KiCad native document"
- `tests/test_kicad_native_pipeline.py:10` — assert baseline.intent_owner == "Project Shellac engineering model"
- `tests/test_kicad_native_pipeline.py:11` — assert baseline.manufacturing_holes_frozen is False
- `tests/test_kicad_native_pipeline.py:12` — assert validate_kicad_native_pipeline_baseline(baseline) == []
- `tests/test_kicad_native_pipeline.py:16` — baseline = build_kicad_native_pipeline_baseline()
- `tests/test_kicad_native_pipeline.py:17` — assert baseline.footprint_count == 250
- `tests/test_kicad_native_pipeline.py:18` — assert baseline.accepted_count + baseline.review_count == 250
- `tests/test_kicad_native_pipeline.py:19` — assert len({item["reference"] for item in baseline.placement_items}) == 250
- `tests/test_kicad_native_pipeline.py:23` — baseline = build_kicad_native_pipeline_baseline()
- `tests/test_kicad_native_pipeline.py:24` — manual = [i for i in baseline.placement_items if not i["accepted"]]
- `tests/test_layout_baseline.py:5` — baseline = build_layout_baseline()
- `tests/test_layout_baseline.py:6` — assert baseline.stackup.layer_count == 4
- `tests/test_layout_baseline.py:7` — assert "Continuous 0VA" in baseline.stackup.inner_1_role
- `tests/test_layout_baseline.py:11` — baseline = build_layout_baseline()
- `tests/test_layout_baseline.py:12` — assert len({r.identifier for r in baseline.regions}) == len(baseline.regions)
- `tests/test_layout_baseline.py:13` — assert len({r.sequence for r in baseline.regions}) == len(baseline.regions)
- `tests/test_layout_baseline.py:14` — assert [r.sequence for r in baseline.regions] == sorted(r.sequence for r in baseline.regions)
- `tests/test_layout_baseline.py:18` — baseline = build_layout_baseline()
- `tests/test_layout_baseline.py:19` — assert len({n.identifier for n in baseline.critical_nets}) == len(baseline.critical_nets)
- `tests/test_layout_baseline.py:20` — assert all(n.verification.strip() for n in baseline.critical_nets)
- `tests/test_layout_baseline.py:24` — baseline = build_layout_baseline()
- `tests/test_layout_baseline.py:26` — for net in baseline.critical_nets:
- `tests/test_layout_baseline.py:32` — baseline = build_layout_baseline()
- `tests/test_layout_baseline.py:33` — for net in baseline.critical_nets:
- `tests/test_performance_baseline.py:15` — baseline = build_performance_baseline()
- `tests/test_performance_baseline.py:16` — for row in baseline.gain_settings:
- `tests/test_performance_baseline.py:17` — assert abs(row.nominal_5mv_output_rms_v - baseline.nominal_cartridge_rms_v * row.input_stage_gain_linear) < 1e-12
- `tests/test_performance_baseline.py:46` — baseline = build_performance_baseline()
- `tests/test_performance_baseline.py:47` — joined = " ".join(baseline.open_measurements).lower()
- `tools/ae019_design_record_reconcile.py:3` — DR=re.compile(r"\b(DR-\d{3})\b",re.I); AE=re.compile(r"\b(AE-\d{3}[A-Z]?)\b",re.I); ST=re.compile(r"\b(PROPOSED\|SELECTED\|CLOSED\|SUPERSEDED\|REJECTED\|OPEN\|PENDING\|IMPLEMENTED\
- `tools/ae019_design_record_reconcile.py:14` — lines += ["","## Reconciliation gates","","- One authoritative current status per decision.","- Superseded decisions retained with explicit successor links.","- Assurance evidence 
- `tools/ae024_design_record_audit.py:25` — BASELINE_RE = re.compile(r"(?i)\b(?:current controlled baseline\|release baseline\|baseline)\b")
- `tools/ae024_design_record_audit.py:246` — return "authoritative machine-readable baseline"
- `tools/ae024_design_record_audit.py:276` — f"- baseline declaration lines: **{len(baselines)}**",
- `tools/ae024_design_record_audit.py:294` — lines += ["", "## Baseline declarations requiring reconciliation", ""]
- `tools/ae024_design_record_audit.py:314` — "2. **01 Requirements and architecture** — current functional/electrical/mechanical baseline.",
- `tools/apply_ae021c_population_closure.py:4` — "tests/test_kicad_native_pipeline.py": [("assert baseline.footprint_count == 243", "assert baseline.footprint_count == 249")],
- `tools/apply_ae022a_closure.py:79` — print("AE-013 historical baseline: isolated")
- `tools/apply_dr039_full_closure.py:10` — raise SystemExit(label + ": expected baseline text not found")
- `tools/apply_sr039_final_consolidated.py:15` — baseline:
- `tools/apply_sr039_final_consolidated.py:18` — tag: sr-038-dr038-dr039-validated-baseline
- `tools/apply_sr039_final_consolidated.py:77` — reason: First regression repair; restored active SCH101 baseline.
- `tools/apply_sr039_final_consolidated.py:80` — reason: Restored SCH103 baseline and established atomic migration boundary.
- `tools/audit_current_decision_index.py:18` — # Narrow guard for the currently implemented DR-038/039 production baseline.
- `generator/commissioning/model.py:1` — """G3-004 staged commissioning and verification baseline.
- `generator/commissioning/model.py:77` — ("Any undocumented substitution in a performance-defining component.", "Any mismatch between fitted hardware and frozen baseline."),
- `generator/commissioning/model.py:160` — _m("M-0801", "End-to-end noise", "Inputs terminated with representative cartridge model", "Balanced outputs", "No hum spur or broadband anomaly; establish baseline", "Numeric limit
- `generator/commissioning/model.py:166` — ("Noise spectra", "THD+N table", "Headroom map", "Final measured baseline JSON/CSV"),
- `generator/layout/constraints.py:1` — """Gate 3 PCB architecture baseline.
- `generator/layout/kicad_native_pipeline.py:118` — baseline = build_kicad_native_pipeline_baseline()
- `generator/layout/kicad_native_pipeline.py:119` — issues = validate_kicad_native_pipeline_baseline(baseline)
- `generator/layout/kicad_native_pipeline.py:121` — raise ValueError("invalid KiCad-native pipeline baseline: " + "; ".join(issues))
- `generator/layout/kicad_native_pipeline.py:123` — path.write_text(json.dumps(asdict(baseline), indent=2) + "\n", encoding="utf-8")
- `generator/layout/kicad_native_pipeline.py:124` — return baseline
- `generator/layout/performance.py:1` — """Gate 3 quantitative performance and design-margin baseline.
- `generator/layout/performance.py:209` — status="CALCULATED BASELINE — noise and distortion close after device/source models and bench correlation",
- `generator/layout/placement_clusters.py:275` — raise ValueError("invalid cluster placement baseline: " + "; ".join(issues))
- `generator/layout/schematic_release_gate.py:46` — blockers.append("Manufacturing release blocked until the controlled BOM is expanded from the partial high-level baseline to the full schematic population with exact purchasable ide
- `generator/layout/schematic_release_gate.py:60` — "Validated baseline evidence: 374/374 Python tests and native KiCad ERC 0 errors / 0 warnings on 30 August 2026.",
- `generator/layout/sr041_routing_release.py:104` — "Schematic electrical baseline validated before SR-040.",
- `generator/layout/sr041_routing_release.py:107` — "Critical/manual clusters accepted as routing baseline with controlled local refinement.",
- `generator/mechanical/freeze.py:75` — baseline: MechanicalBaseline,
- `generator/mechanical/freeze.py:79` — baseline.audio_requirement
- `generator/mechanical/freeze.py:81` — else baseline.psu_requirement
- `generator/mechanical/freeze.py:134` — baseline = build_mechanical_baseline()
- `generator/mechanical/freeze.py:138` — eligible = [candidate for candidate in baseline.candidates if candidate.role is role]
- `generator/mechanical/freeze.py:141` — findings = decision_findings(candidate, baseline, evidence) if candidate else ["no candidate available"]
- `generator/mechanical/placement.py:69` — baseline = build_layout_baseline()
- `generator/mechanical/placement.py:70` — if width_mm < baseline.envelope.minimum_usable_width_mm or depth_mm < baseline.envelope.minimum_usable_depth_mm:
- `generator/mechanical/placement.py:73` — edge = baseline.envelope.board_edge_clearance_mm
- `generator/mechanical/psu_release.py:90` — "A release-grade passive thermal proof cannot be calculated from the project baseline: authoritative worst-case DC rail current and regulator-to-ambient thermal resistance/heatsink
- `generator/mechanical/sr040_audio_freeze.py:43` — baseline=build_mechanical_baseline()
- `generator/mechanical/sr040_audio_freeze.py:44` — candidate=next(c for c in baseline.candidates if c.identifier=="ENC-A04")
- `generator/model/production_cmrr.py:3` — Uses the implemented DR-038 values, not the earlier candidate baseline.
- `generator/model/shellac.py:1` — """Project Shellac engineering-model baseline, Revision A.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:9` — - baseline declaration lines: **673**
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:32` — ## Baseline declarations requiring reconciliation
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:34` — - `APPLY_AE025A_INDEX_REPAIR.py:15` — print("Restored decision-index baseline semantics: branch=main; removed authority_scope.")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:35` — - `APPLY_AE025_INDEX_PATCH.py:7` — t=t.replace(needle, needle+"authority_scope: Working design authority is develop until a tagged production baseline is promoted to main.\n")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:36` — - `APPLY_DECISION_INDEX_RECONCILIATION.py:22` — print("Updated authoritative decision index to the validated DR-038/DR-039 baseline.")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:37` — - `manifest.json:5` — "baseline": "sr-027-component-selection-policy / 31809c1",
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:38` — - `README.md:10` — - Implemented signal-chain baseline: **DR-037 / DR-038 / DR-039 / DR-040**
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:39` — - `README.md:52` — tagged production baseline.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:40` — - `docs/AE-001_Replay_Equalisation_Synthesis_Rev_A.md:55` — capacitors with a changed resistor baseline, while requiring no exotic
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:41` — - `docs/AE-003_Full_Band_Replay_Curve_Analysis_Rev_A.md:4` — **Status:** calculation baseline
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:42` — - `docs/AE-011_End_to_End_Signal_Chain_Closure_Rev_A0.md:5` — **Baseline:** GitHub `main` at commit `4581c49`
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:43` — - `docs/AE-011_End_to_End_Signal_Chain_Closure_Rev_A0.md:10` — This analysis reconstructs the complete Project Shellac analogue signal-chain assurance that predates the GitHub-cont
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:44` — - `docs/AE-011_End_to_End_Signal_Chain_Closure_Rev_A1.md:6` — **Baseline reviewed:** GitHub `main` at `4581c49`
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:45` — - `docs/AE-013_SCH101_Noise_CMRR_Review_Rev_A0.md:59` — No previous explicit system CMRR requirement was found in the controlled baseline. A release acceptance value should therefo
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:46` — - `docs/AE-014_SCH101_Precision_Architecture_Downselect_Rev_A0.md:146` — These are proposed engineering requirements, not retroactive baseline claims.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:47` — - `docs/AE-016A_AE016_Regression_Repair_Rev_A0.md:7` — is valid for the current physical generator baseline and must not simply be
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:48` — - `docs/AE-016A_AE016_Regression_Repair_Rev_A0.md:11` — - restores `generator/model/balanced_input.py` exactly to the pre-AE016 baseline;
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:49` — - `docs/AE-016B_Full_Regression_Staging_Repair_Rev_A0.md:7` — AE-016B restores SCH103 to the pre-DR039 physical baseline while retaining the
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:50` — - `docs/AE-016_DR038_DR039_Implementation_Baseline_Rev_A0.md:1` — # AE-016 — DR-038 / DR-039 Implementation Baseline
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:51` — - `docs/AE-016_DR038_DR039_Implementation_Baseline_Rev_A0.md:5` — This update converts DR-038 and DR-039 into the controlled electrical baseline.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:52` — - `docs/AE-017_Atomic_Migration_Dependency_Mapping_Gate_Rev_A0.md:12` — doing its job: it encodes both the electrical baseline and the rendered CAD
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:53` — - `docs/AE-017_Atomic_Migration_Dependency_Mapping_Gate_Rev_A0.md:57` — This prevents a second partial-baseline migration.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:54` — - `docs/AE-017_Generated_Atomic_Migration_Dependency_Map.md:227` — \\| ANALYSIS \\| `AE-012` \\| `REPAIR_SIGNAL_CHAIN.py` \\| 10 \\| print("AE-012 signal-chain model is at its pre-
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:55` — - `docs/AE-017_Generated_Atomic_Migration_Dependency_Map.md:236` — \\| SCH103_OUTPUT \\| `output_end = Point(420` \\| `RESTORE_SCH103_BASELINE.py` \\| 32 \\| baseline = '''    outp
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:56` — - `docs/AE-017_Generated_Atomic_Migration_Dependency_Map.md:239` — \\| SCH103_OUTPUT \\| `replay_eq.py` \\| `RESTORE_SCH103_BASELINE.py` \\| 44 \\| print("Restored replay_eq.py to 
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:57` — - `docs/AE-017_Generated_Atomic_Migration_Dependency_Map.md:240` — \\| SCH103_OUTPUT \\| `replay_eq.py` \\| `RESTORE_SCH103_BASELINE.py` \\| 46 \\| print("replay_eq.py already at p
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:58` — - `docs/AE-017_Generated_Atomic_Migration_Dependency_Map.md:289` — \\| DR039 \\| `DR-039` \\| `docs/AE-016_DR038_DR039_Implementation_Baseline_Rev_A0.md` \\| 1 \\| # AE-016 — DR-03
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:59` — - `docs/AE-017_Generated_Atomic_Migration_Dependency_Map.md:290` — \\| DR039 \\| `DR-039` \\| `docs/AE-016_DR038_DR039_Implementation_Baseline_Rev_A0.md` \\| 5 \\| This update conv
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:60` — - `docs/AE-017_Generated_Atomic_Migration_Dependency_Map.md:343` — \\| SCH103_OUTPUT \\| `replay_eq.py` \\| `docs/updates/AE016B_UPDATE_MANIFEST.md` \\| 6 \\| - restore `generator/
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:62` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:7` — \\| `docs/AE-001_Replay_Equalisation_Synthesis_Rev_A.md` \\| AE-001, AE-001B, AE-002 \\| BASELINE, OPEN, SELECTED, SUP
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:63` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:9` — \\| `docs/AE-003_Full_Band_Replay_Curve_Analysis_Rev_A.md` \\| AE-003 \\| BASELINE \\|
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:64` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:17` — \\| `docs/AE-011_End_to_End_Signal_Chain_Closure_Rev_A0.md` \\| AE-010, AE-011 \\| BASELINE, CLOSED, OPEN, SELECTED, 
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:65` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:18` — \\| `docs/AE-011_End_to_End_Signal_Chain_Closure_Rev_A1.md` \\| AE-011, DR-037 \\| BASELINE, SELECTED, SUPERSEDED \\|
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:66` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:20` — \\| `docs/AE-013_SCH101_Noise_CMRR_Review_Rev_A0.md` \\| AE-012, AE-013 \\| BASELINE, CLOSED, SELECTED \\|
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:67` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:21` — \\| `docs/AE-014_SCH101_Precision_Architecture_Downselect_Rev_A0.md` \\| AE-012, AE-013, AE-014, DR-038 \\| BASELINE,
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:68` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:23` — \\| `docs/AE-016A_AE016_Regression_Repair_Rev_A0.md` \\| AE-016, AE-016A, DR-038, DR-039 \\| BASELINE, SELECTED \\|
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:69` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:24` — \\| `docs/AE-016B_Full_Regression_Staging_Repair_Rev_A0.md` \\| AE-016, AE-016A, AE-016B, DR-038, DR-039 \\| BASELINE
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:70` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:25` — \\| `docs/AE-016_DR038_DR039_Implementation_Baseline_Rev_A0.md` \\| AE-016, DR-038, DR-039 \\| BASELINE \\|
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:71` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:26` — \\| `docs/AE-017_Atomic_Migration_Dependency_Mapping_Gate_Rev_A0.md` \\| AE-016, AE-017, DR-038, DR-039 \\| BASELINE,
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:72` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:27` — \\| `docs/AE-017_Generated_Atomic_Migration_Dependency_Map.md` \\| AE-010, AE-011, AE-012, AE-013, AE-014, AE-015, AE
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:73` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:29` — \\| `docs/AE-019_Design_Record_Reconciliation_Gate_Rev_A0.md` \\| AE-019 \\| BASELINE \\|
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:74` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:34` — \\| `docs/decisions/DR-038_SCH101_Precision_Architecture_SELECTED.md` \\| AE-010, AE-012, AE-016, DR-038 \\| BASELINE
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:75` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:38` — \\| `docs/knowledge/DECISION_REGISTER.md` \\| AE-005, AE-007, AE-008, AE-009, AE-010 \\| BASELINE, CLOSED, OPEN, SELE
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:76` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:39` — \\| `docs/knowledge/RECOVERED_BASELINE.md` \\| AE-007, AE-008, AE-009 \\| BASELINE, OPEN, REJECTED, SELECTED, SUPERSE
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:77` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:40` — \\| `docs/knowledge/RISK_REGISTER.md` \\| AE-008 \\| BASELINE, CLOSED, OPEN, SELECTED \\|
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:78` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:46` — \\| `docs/updates/AE016B_UPDATE_MANIFEST.md` \\| AE-012, AE-016, AE-016A, AE-016B, DR-039 \\| BASELINE, PENDING, SELE
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:79` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:47` — \\| `docs/updates/AE016_UPDATE_MANIFEST.md` \\| AE-016, DR-038, DR-039 \\| BASELINE, SELECTED \\|
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:80` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:48` — \\| `docs/updates/AE017_UPDATE_MANIFEST.md` \\| AE-017, DR-038, DR-039 \\| BASELINE \\|
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:81` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:50` — \\| `docs/updates/AE019_UPDATE_MANIFEST.md` \\| AE-019 \\| BASELINE \\|
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:82` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:57` — - Assurance evidence identifies the baseline it analysed.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:83` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:58` — - Current design baseline separated from historical evidence.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:84` — - `docs/AE-020_Decision_Register_Reconciliation_and_Design_Pack_Structure_Rev_A0.md:5` — **Baseline:** `main` at `1ebb04d`
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:85` — - `docs/AE-023_Production_Signal_Chain_Assurance_Closure_Rev_A0.md:12` — ## Implemented baseline verified
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:86` — - `docs/AE-023_Production_Signal_Chain_Assurance_Closure_Rev_A0.md:127` — 3. mechanical/PCB production-baseline closure;
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:87` — - `docs/G3-001_PCB_Architecture_and_Layout_Constitution_Rev_A0.md:7` — This baseline turns Gate 3 layout intent into a CAD-independent, testable model. It does not place components
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:88` — - `docs/G3-001_PCB_Architecture_and_Layout_Constitution_Rev_A0.md:46` — This writes `out/layout/layout_baseline.json`, which is the machine-readable baseline used by future placeme
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:89` — - `docs/G3-002_Quantitative_Performance_and_Critical_Loop_Baseline_Rev_A0.md:1` — # G3-002 — Quantitative Performance and Critical-Loop Baseline
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:90` — - `docs/G3-003_Mechanical_Datum_and_Preliminary_Placement_Baseline_Rev_A0.md:1` — # G3-003 — Mechanical Datum and Preliminary Placement Baseline
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:91` — - `docs/G3-004_Commissioning_and_Verification_Baseline_Rev_A0.md:1` — # G3-004 — Commissioning and Verification Baseline Rev A0
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:92` — - `docs/G3-004_Commissioning_and_Verification_Baseline_Rev_A0.md:10` — The baseline is intentionally conservative: no stage may be bypassed after a
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:93` — - `docs/G3-005_Component_Cluster_Placement_Baseline_Rev_A0.md:1` — # G3-005 — Component-Cluster Placement Baseline Rev A0
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:94` — - `docs/G3-009_Schematic_to_PCB_Footprint_Contract_Rev_A0.md:11` — native ERC baseline remain unchanged.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:95` — - `docs/G3-013A_G3-014_KiCad_Parser_and_Native_Pipeline_Rev_A0.md:1` — # G3-013A / G3-014 — KiCad PCB Parser Closure and Native Pipeline Baseline
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:96` — - `docs/G3-015_Gate_3A_Macro_Acceptance_and_CLU-106_Refinement_Rev_A0.md:5` — The 220 mm x 140 mm board architecture and right-to-left functional flow were visually reviewed in KiC
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:98` — - `docs/G3-025_Foundry_RIAA_Physical_Closure_Rev_A0.md:68` — - Foundry baseline exists in Git and is machine-readable;
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:99` — - `docs/G3-027_RIAA_Integration_Audit_and_BOM_Reconciliation_Rev_A1.md:38` — The current controlled BOM is a partial baseline, not a procurement-complete BOM.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:100` — - `docs/SR-001_Schematic_Generation_Readiness_Audit_Rev_A.md:15` — schematic baseline.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:101` — - `docs/SR-001_Schematic_Generation_Readiness_Audit_Rev_A.md:70` — 7. Correct genuine ERC findings and freeze the schematic baseline.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:102` — - `docs/SR-014_Legacy_Sheet_Pin_Aware_Closure_Rev_A.md:44` — - Native KiCad hierarchical ERC: 286 findings, reduced from the accepted SR-013 baseline of 600.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:103` — - `docs/SR-015_ERC_and_Deterministic_Build_Closure_Rev_A.md:34` — The accepted SR-014 baseline reported 286 native KiCad findings. SR-015 closes all of them through renderer, libra
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:104` — - `docs/SR-021B_Canonical_Grid_and_Electrical_Integrity_Foundation_Rev_A.md:4` — **Parent:** accepted SR-021 baseline
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:105` — - `docs/SR-021B_Canonical_Grid_and_Electrical_Integrity_Foundation_Rev_A.md:81` — accepted baseline only after the new report has been reviewed. No analogue
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:106` — - `docs/SR-021D_ERC_Branch_Topology_Closure_Rev_A.md:3` — **Parent baseline:** SR-021C
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:107` — - `docs/SR-021G_Schematic_Baseline_Acceptance_and_Provenance_Policy_Rev_A.md:1` — # SR-021G — Schematic Baseline Acceptance and Provenance Policy
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:108` — - `docs/SR-021G_Schematic_Baseline_Acceptance_and_Provenance_Policy_Rev_A.md:8` — baseline. Provenance now distinguishes immutable generated design artifacts
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:109` — - `docs/SR-021_SCH107_Human_Reviewable_Conversion_Rev_A.md:59` — Gate 2A machine readiness: PASS on the accepted SR-020 baseline
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:110` — - `docs/SR-023_SCH108_Human_Reviewable_Rev_A.md:5` — **Parent:** accepted SR-022 baseline
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:111` — - `docs/SR-039_Schematic_to_Layout_Release_Gate_Rev_A0.md:7` — Validated baseline:
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:112` — - `docs/SR-039_Schematic_to_Layout_Release_Gate_Rev_A0.md:35` — The controlled BOM remains a partial high-level baseline rather than a full
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:113` — - `docs/SR-041_Critical_Placement_and_Routing_Release_Rev_A0.md:42` — All manual-authority clusters are accepted as the routing baseline subject to
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:114` — - `foundry/FOUNDRY_BASELINE.md:1` — # FDR-001 — Project Shellac Foundry Baseline
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:115` — - `foundry/README.md:17` — Foundry baseline: **FDR-001 / G3-025**.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:116` — - `scripts/report_commissioning_baseline.py:20` — print(f"Project Shellac commissioning baseline: {model.identifier} {model.revision}")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:117` — - `scripts/report_interface_architecture.py:36` — print(f"Mechanical baseline: {mechanical.status}")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:118` — - `scripts/report_kicad_native_pipeline.py:13` — baseline = write_kicad_native_pipeline_baseline(out)
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:119` — - `scripts/report_kicad_native_pipeline.py:15` — print(f"Status: {baseline.status}")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:120` — - `scripts/report_kicad_native_pipeline.py:16` — print(f"PCB owner: {baseline.pcb_owner}")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:121` — - `scripts/report_kicad_native_pipeline.py:17` — print(f"Placement intent items: {baseline.footprint_count}")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:122` — - `scripts/report_kicad_native_pipeline.py:18` — print(f"Accepted / review: {baseline.accepted_count} / {baseline.review_count}")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:123` — - `scripts/report_kicad_native_pipeline.py:19` — print(f"Manufacturing holes frozen: {baseline.manufacturing_holes_frozen}")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:124` — - `scripts/report_layout_baseline.py:1` — """Report the provisional Gate 3 PCB architecture baseline."""
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:125` — - `scripts/report_layout_baseline.py:18` — baseline = build_layout_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:126` — - `scripts/report_layout_baseline.py:21` — json_path.write_text(json.dumps(baseline.to_dict(), indent=2) + "\n", encoding="utf-8")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:127` — - `scripts/report_layout_baseline.py:23` — print(f"{baseline.identifier} — {baseline.revision}")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:128` — - `scripts/report_layout_baseline.py:24` — print(baseline.status)
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:129` — - `scripts/report_layout_baseline.py:25` — print(f"Stack-up: {baseline.stackup.layer_count} layers")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:130` — - `scripts/report_layout_baseline.py:26` — print(f"Functional regions: {len(baseline.regions)}")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:131` — - `scripts/report_layout_baseline.py:27` — print(f"Critical-net classes: {len(baseline.critical_nets)}")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:132` — - `scripts/report_layout_baseline.py:28` — print(f"Manual-only net classes: {sum(n.routing_policy.value == 'manual_only' for n in baseline.critical_nets)}")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:133` — - `scripts/report_performance_baseline.py:13` — baseline = build_performance_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:134` — - `scripts/report_performance_baseline.py:14` — print(f"{baseline.identifier} — {baseline.revision}")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:135` — - `scripts/report_performance_baseline.py:15` — print(baseline.status)
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:136` — - `scripts/report_performance_baseline.py:18` — for row in baseline.gain_settings:
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:137` — - `scripts/report_performance_baseline.py:22` — for row in baseline.margins:
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:138` — - `scripts/report_performance_baseline.py:25` — print(f"\nCriticality records: {len(baseline.criticality)}")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:139` — - `scripts/report_performance_baseline.py:26` — print(f"Placement constraints: {len(baseline.placement_constraints)}")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:140` — - `scripts/report_performance_baseline.py:27` — print(f"Open measurements: {len(baseline.open_measurements)}")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:141` — - `scripts/report_performance_baseline.py:32` — path.write_text(json.dumps(baseline.to_dict(), indent=2), encoding="utf-8")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:142` — - `tests/test_enclosure_decision_baseline.py:21` — baseline = build_mechanical_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:143` — - `tests/test_enclosure_decision_baseline.py:22` — candidate = next(item for item in baseline.candidates if item.identifier == "ENC-A03")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:144` — - `tests/test_enclosure_decision_baseline.py:23` — findings = decision_findings(candidate, baseline, DrawingEvidence(False, False, False, False, False, None))
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:145` — - `tests/test_kicad_native_pipeline.py:8` — baseline = build_kicad_native_pipeline_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:146` — - `tests/test_kicad_native_pipeline.py:9` — assert baseline.pcb_owner == "KiCad native document"
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:147` — - `tests/test_kicad_native_pipeline.py:10` — assert baseline.intent_owner == "Project Shellac engineering model"
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:148` — - `tests/test_kicad_native_pipeline.py:11` — assert baseline.manufacturing_holes_frozen is False
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:149` — - `tests/test_kicad_native_pipeline.py:12` — assert validate_kicad_native_pipeline_baseline(baseline) == []
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:150` — - `tests/test_kicad_native_pipeline.py:16` — baseline = build_kicad_native_pipeline_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:151` — - `tests/test_kicad_native_pipeline.py:17` — assert baseline.footprint_count == 250
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:152` — - `tests/test_kicad_native_pipeline.py:18` — assert baseline.accepted_count + baseline.review_count == 250
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:153` — - `tests/test_kicad_native_pipeline.py:19` — assert len({item["reference"] for item in baseline.placement_items}) == 250
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:154` — - `tests/test_kicad_native_pipeline.py:23` — baseline = build_kicad_native_pipeline_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:155` — - `tests/test_kicad_native_pipeline.py:24` — manual = [i for i in baseline.placement_items if not i["accepted"]]
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:156` — - `tests/test_layout_baseline.py:5` — baseline = build_layout_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:157` — - `tests/test_layout_baseline.py:6` — assert baseline.stackup.layer_count == 4
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:158` — - `tests/test_layout_baseline.py:7` — assert "Continuous 0VA" in baseline.stackup.inner_1_role
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:159` — - `tests/test_layout_baseline.py:11` — baseline = build_layout_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:160` — - `tests/test_layout_baseline.py:12` — assert len({r.identifier for r in baseline.regions}) == len(baseline.regions)
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:161` — - `tests/test_layout_baseline.py:13` — assert len({r.sequence for r in baseline.regions}) == len(baseline.regions)
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:162` — - `tests/test_layout_baseline.py:14` — assert [r.sequence for r in baseline.regions] == sorted(r.sequence for r in baseline.regions)
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:163` — - `tests/test_layout_baseline.py:18` — baseline = build_layout_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:164` — - `tests/test_layout_baseline.py:19` — assert len({n.identifier for n in baseline.critical_nets}) == len(baseline.critical_nets)
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:165` — - `tests/test_layout_baseline.py:20` — assert all(n.verification.strip() for n in baseline.critical_nets)
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:166` — - `tests/test_layout_baseline.py:24` — baseline = build_layout_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:167` — - `tests/test_layout_baseline.py:26` — for net in baseline.critical_nets:
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:168` — - `tests/test_layout_baseline.py:32` — baseline = build_layout_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:169` — - `tests/test_layout_baseline.py:33` — for net in baseline.critical_nets:
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:170` — - `tests/test_performance_baseline.py:15` — baseline = build_performance_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:171` — - `tests/test_performance_baseline.py:16` — for row in baseline.gain_settings:
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:172` — - `tests/test_performance_baseline.py:17` — assert abs(row.nominal_5mv_output_rms_v - baseline.nominal_cartridge_rms_v * row.input_stage_gain_linear) < 1e-12
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:173` — - `tests/test_performance_baseline.py:46` — baseline = build_performance_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:174` — - `tests/test_performance_baseline.py:47` — joined = " ".join(baseline.open_measurements).lower()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:177` — - `tools/ae024_design_record_audit.py:25` — BASELINE_RE = re.compile(r"(?i)\b(?:current controlled baseline\\|release baseline\\|baseline)\b")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:178` — - `tools/ae024_design_record_audit.py:246` — return "authoritative machine-readable baseline"
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:179` — - `tools/ae024_design_record_audit.py:276` — f"- baseline declaration lines: **{len(baselines)}**",
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:180` — - `tools/ae024_design_record_audit.py:294` — lines += ["", "## Baseline declarations requiring reconciliation", ""]
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:181` — - `tools/ae024_design_record_audit.py:314` — "2. **01 Requirements and architecture** — current functional/electrical/mechanical baseline.",
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:182` — - `tools/apply_ae021c_population_closure.py:4` — "tests/test_kicad_native_pipeline.py": [("assert baseline.footprint_count == 243", "assert baseline.footprint_count == 249")],
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:183` — - `tools/apply_ae022a_closure.py:79` — print("AE-013 historical baseline: isolated")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:184` — - `tools/apply_dr039_full_closure.py:10` — raise SystemExit(label + ": expected baseline text not found")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:185` — - `tools/apply_sr039_final_consolidated.py:15` — baseline:
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:186` — - `tools/apply_sr039_final_consolidated.py:18` — tag: sr-038-dr038-dr039-validated-baseline
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:187` — - `tools/apply_sr039_final_consolidated.py:77` — reason: First regression repair; restored active SCH101 baseline.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:188` — - `tools/apply_sr039_final_consolidated.py:80` — reason: Restored SCH103 baseline and established atomic migration boundary.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:189` — - `tools/audit_current_decision_index.py:18` — # Narrow guard for the currently implemented DR-038/039 production baseline.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:190` — - `generator/commissioning/model.py:1` — """G3-004 staged commissioning and verification baseline.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:191` — - `generator/commissioning/model.py:77` — ("Any undocumented substitution in a performance-defining component.", "Any mismatch between fitted hardware and frozen baseline."),
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:192` — - `generator/commissioning/model.py:160` — _m("M-0801", "End-to-end noise", "Inputs terminated with representative cartridge model", "Balanced outputs", "No hum spur or broadband a
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:193` — - `generator/commissioning/model.py:166` — ("Noise spectra", "THD+N table", "Headroom map", "Final measured baseline JSON/CSV"),
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:194` — - `generator/layout/constraints.py:1` — """Gate 3 PCB architecture baseline.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:195` — - `generator/layout/kicad_native_pipeline.py:118` — baseline = build_kicad_native_pipeline_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:196` — - `generator/layout/kicad_native_pipeline.py:119` — issues = validate_kicad_native_pipeline_baseline(baseline)
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:197` — - `generator/layout/kicad_native_pipeline.py:121` — raise ValueError("invalid KiCad-native pipeline baseline: " + "; ".join(issues))
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:198` — - `generator/layout/kicad_native_pipeline.py:123` — path.write_text(json.dumps(asdict(baseline), indent=2) + "\n", encoding="utf-8")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:199` — - `generator/layout/kicad_native_pipeline.py:124` — return baseline
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:200` — - `generator/layout/performance.py:1` — """Gate 3 quantitative performance and design-margin baseline.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:201` — - `generator/layout/performance.py:209` — status="CALCULATED BASELINE — noise and distortion close after device/source models and bench correlation",
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:202` — - `generator/layout/placement_clusters.py:275` — raise ValueError("invalid cluster placement baseline: " + "; ".join(issues))
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:203` — - `generator/layout/schematic_release_gate.py:46` — blockers.append("Manufacturing release blocked until the controlled BOM is expanded from the partial high-level baseline to the 
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:204` — - `generator/layout/schematic_release_gate.py:60` — "Validated baseline evidence: 374/374 Python tests and native KiCad ERC 0 errors / 0 warnings on 30 August 2026.",
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:205` — - `generator/layout/sr041_routing_release.py:104` — "Schematic electrical baseline validated before SR-040.",
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:206` — - `generator/layout/sr041_routing_release.py:107` — "Critical/manual clusters accepted as routing baseline with controlled local refinement.",
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:207` — - `generator/mechanical/freeze.py:75` — baseline: MechanicalBaseline,
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:208` — - `generator/mechanical/freeze.py:79` — baseline.audio_requirement
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:209` — - `generator/mechanical/freeze.py:81` — else baseline.psu_requirement
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:210` — - `generator/mechanical/freeze.py:134` — baseline = build_mechanical_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:211` — - `generator/mechanical/freeze.py:138` — eligible = [candidate for candidate in baseline.candidates if candidate.role is role]
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:212` — - `generator/mechanical/freeze.py:141` — findings = decision_findings(candidate, baseline, evidence) if candidate else ["no candidate available"]
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:213` — - `generator/mechanical/placement.py:69` — baseline = build_layout_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:214` — - `generator/mechanical/placement.py:70` — if width_mm < baseline.envelope.minimum_usable_width_mm or depth_mm < baseline.envelope.minimum_usable_depth_mm:
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:215` — - `generator/mechanical/placement.py:73` — edge = baseline.envelope.board_edge_clearance_mm
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:216` — - `generator/mechanical/psu_release.py:90` — "A release-grade passive thermal proof cannot be calculated from the project baseline: authoritative worst-case DC rail current and reg
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:217` — - `generator/mechanical/sr040_audio_freeze.py:43` — baseline=build_mechanical_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:218` — - `generator/mechanical/sr040_audio_freeze.py:44` — candidate=next(c for c in baseline.candidates if c.identifier=="ENC-A04")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:219` — - `generator/model/production_cmrr.py:3` — Uses the implemented DR-038 values, not the earlier candidate baseline.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:220` — - `generator/model/shellac.py:1` — """Project Shellac engineering-model baseline, Revision A.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:221` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:9` — - baseline declaration lines: **450**
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:222` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:33` — ## Baseline declarations requiring reconciliation
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:223` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:35` — - `APPLY_AE025_INDEX_PATCH.py:7` — t=t.replace(needle, needle+"authority_scope: Working design auth
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:224` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:36` — - `APPLY_DECISION_INDEX_RECONCILIATION.py:22` — print("Updated authoritative decision index to the 
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:225` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:37` — - `manifest.json:5` — "baseline": "sr-027-component-selection-policy / 31809c1",
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:226` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:38` — - `README.md:10` — - Implemented signal-chain baseline: **DR-037 / DR-038 / DR-039 / DR-040**
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:227` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:39` — - `README.md:52` — tagged production baseline.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:228` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:40` — - `docs/AE-001_Replay_Equalisation_Synthesis_Rev_A.md:55` — capacitors with a changed resistor base
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:229` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:41` — - `docs/AE-003_Full_Band_Replay_Curve_Analysis_Rev_A.md:4` — **Status:** calculation baseline
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:230` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:42` — - `docs/AE-011_End_to_End_Signal_Chain_Closure_Rev_A0.md:5` — **Baseline:** GitHub `main` at commit
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:232` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:44` — - `docs/AE-011_End_to_End_Signal_Chain_Closure_Rev_A1.md:6` — **Baseline reviewed:** GitHub `main` 
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:233` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:45` — - `docs/AE-013_SCH101_Noise_CMRR_Review_Rev_A0.md:59` — No previous explicit system CMRR requiremen
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:234` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:46` — - `docs/AE-014_SCH101_Precision_Architecture_Downselect_Rev_A0.md:146` — These are proposed enginee
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:235` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:47` — - `docs/AE-016A_AE016_Regression_Repair_Rev_A0.md:7` — is valid for the current physical generator 
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:236` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:48` — - `docs/AE-016A_AE016_Regression_Repair_Rev_A0.md:11` — - restores `generator/model/balanced_input.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:237` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:49` — - `docs/AE-016B_Full_Regression_Staging_Repair_Rev_A0.md:7` — AE-016B restores SCH103 to the pre-DR
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:238` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:50` — - `docs/AE-016_DR038_DR039_Implementation_Baseline_Rev_A0.md:1` — # AE-016 — DR-038 / DR-039 Implem
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:239` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:51` — - `docs/AE-016_DR038_DR039_Implementation_Baseline_Rev_A0.md:5` — This update converts DR-038 and D
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:240` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:52` — - `docs/AE-017_Atomic_Migration_Dependency_Mapping_Gate_Rev_A0.md:12` — doing its job: it encodes b
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:241` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:53` — - `docs/AE-017_Atomic_Migration_Dependency_Mapping_Gate_Rev_A0.md:57` — This prevents a second part
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:243` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:55` — - `docs/AE-017_Generated_Atomic_Migration_Dependency_Map.md:236` — \\\| SCH103_OUTPUT \\\| `output_
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:249` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:62` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:7` — \\\| `docs/AE-001_Replay_Equalisation
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:250` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:63` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:9` — \\\| `docs/AE-003_Full_Band_Replay_Cu
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:251` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:64` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:17` — \\\| `docs/AE-011_End_to_End_Signal_
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:252` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:65` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:18` — \\\| `docs/AE-011_End_to_End_Signal_
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:253` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:66` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:20` — \\\| `docs/AE-013_SCH101_Noise_CMRR_
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:254` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:67` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:21` — \\\| `docs/AE-014_SCH101_Precision_A
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:255` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:68` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:23` — \\\| `docs/AE-016A_AE016_Regression_
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:256` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:69` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:24` — \\\| `docs/AE-016B_Full_Regression_S
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:257` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:70` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:25` — \\\| `docs/AE-016_DR038_DR039_Implem
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:258` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:71` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:26` — \\\| `docs/AE-017_Atomic_Migration_D
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:260` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:73` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:29` — \\\| `docs/AE-019_Design_Record_Reco
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:261` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:74` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:34` — \\\| `docs/decisions/DR-038_SCH101_P
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:262` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:75` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:38` — \\\| `docs/knowledge/DECISION_REGIST
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:263` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:76` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:39` — \\\| `docs/knowledge/RECOVERED_BASEL
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:264` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:77` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:40` — \\\| `docs/knowledge/RISK_REGISTER.m
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:265` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:78` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:46` — \\\| `docs/updates/AE016B_UPDATE_MAN
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:266` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:79` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:47` — \\\| `docs/updates/AE016_UPDATE_MANI
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:267` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:80` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:48` — \\\| `docs/updates/AE017_UPDATE_MANI
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:268` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:81` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:50` — \\\| `docs/updates/AE019_UPDATE_MANI
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:269` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:82` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:57` — - Assurance evidence identifies the 
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:270` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:83` — - `docs/AE-019_Generated_Design_Record_Reconciliation.md:58` — - Current design baseline separated 
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:271` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:84` — - `docs/AE-020_Decision_Register_Reconciliation_and_Design_Pack_Structure_Rev_A0.md:5` — **Baseline
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:272` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:85` — - `docs/AE-023_Production_Signal_Chain_Assurance_Closure_Rev_A0.md:12` — ## Implemented baseline ve
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:273` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:86` — - `docs/AE-023_Production_Signal_Chain_Assurance_Closure_Rev_A0.md:127` — 3. mechanical/PCB product
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:274` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:87` — - `docs/G3-001_PCB_Architecture_and_Layout_Constitution_Rev_A0.md:7` — This baseline turns Gate 3 l
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:275` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:88` — - `docs/G3-001_PCB_Architecture_and_Layout_Constitution_Rev_A0.md:46` — This writes `out/layout/lay
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:276` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:89` — - `docs/G3-002_Quantitative_Performance_and_Critical_Loop_Baseline_Rev_A0.md:1` — # G3-002 — Quanti
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:277` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:90` — - `docs/G3-003_Mechanical_Datum_and_Preliminary_Placement_Baseline_Rev_A0.md:1` — # G3-003 — Mechan
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:278` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:91` — - `docs/G3-004_Commissioning_and_Verification_Baseline_Rev_A0.md:1` — # G3-004 — Commissioning and 
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:279` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:92` — - `docs/G3-004_Commissioning_and_Verification_Baseline_Rev_A0.md:10` — The baseline is intentionall
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:280` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:93` — - `docs/G3-005_Component_Cluster_Placement_Baseline_Rev_A0.md:1` — # G3-005 — Component-Cluster Pla
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:281` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:94` — - `docs/G3-009_Schematic_to_PCB_Footprint_Contract_Rev_A0.md:11` — native ERC baseline remain uncha
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:282` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:95` — - `docs/G3-013A_G3-014_KiCad_Parser_and_Native_Pipeline_Rev_A0.md:1` — # G3-013A / G3-014 — KiCad P
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:284` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:98` — - `docs/G3-025_Foundry_RIAA_Physical_Closure_Rev_A0.md:68` — - Foundry baseline exists in Git and i
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:285` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:99` — - `docs/G3-027_RIAA_Integration_Audit_and_BOM_Reconciliation_Rev_A1.md:38` — The current controlled
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:286` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:100` — - `docs/SR-001_Schematic_Generation_Readiness_Audit_Rev_A.md:15` — schematic baseline.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:287` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:101` — - `docs/SR-001_Schematic_Generation_Readiness_Audit_Rev_A.md:70` — 7. Correct genuine ERC findings
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:288` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:102` — - `docs/SR-014_Legacy_Sheet_Pin_Aware_Closure_Rev_A.md:44` — - Native KiCad hierarchical ERC: 286 
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:289` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:103` — - `docs/SR-015_ERC_and_Deterministic_Build_Closure_Rev_A.md:34` — The accepted SR-014 baseline rep
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:290` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:104` — - `docs/SR-021B_Canonical_Grid_and_Electrical_Integrity_Foundation_Rev_A.md:4` — **Parent:** accep
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:291` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:105` — - `docs/SR-021B_Canonical_Grid_and_Electrical_Integrity_Foundation_Rev_A.md:81` — accepted baselin
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:292` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:106` — - `docs/SR-021D_ERC_Branch_Topology_Closure_Rev_A.md:3` — **Parent baseline:** SR-021C
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:293` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:107` — - `docs/SR-021G_Schematic_Baseline_Acceptance_and_Provenance_Policy_Rev_A.md:1` — # SR-021G — Sche
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:294` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:108` — - `docs/SR-021G_Schematic_Baseline_Acceptance_and_Provenance_Policy_Rev_A.md:8` — baseline. Proven
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:295` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:109` — - `docs/SR-021_SCH107_Human_Reviewable_Conversion_Rev_A.md:59` — Gate 2A machine readiness: PASS o
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:296` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:110` — - `docs/SR-023_SCH108_Human_Reviewable_Rev_A.md:5` — **Parent:** accepted SR-022 baseline
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:297` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:111` — - `docs/SR-039_Schematic_to_Layout_Release_Gate_Rev_A0.md:7` — Validated baseline:
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:298` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:112` — - `docs/SR-039_Schematic_to_Layout_Release_Gate_Rev_A0.md:35` — The controlled BOM remains a parti
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:299` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:113` — - `docs/SR-041_Critical_Placement_and_Routing_Release_Rev_A0.md:42` — All manual-authority cluster
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:300` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:114` — - `foundry/FOUNDRY_BASELINE.md:1` — # FDR-001 — Project Shellac Foundry Baseline
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:301` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:115` — - `foundry/README.md:17` — Foundry baseline: **FDR-001 / G3-025**.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:302` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:116` — - `scripts/report_commissioning_baseline.py:20` — print(f"Project Shellac commissioning baseline: 
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:303` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:117` — - `scripts/report_interface_architecture.py:36` — print(f"Mechanical baseline: {mechanical.status}
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:304` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:118` — - `scripts/report_kicad_native_pipeline.py:13` — baseline = write_kicad_native_pipeline_baseline(o
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:305` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:119` — - `scripts/report_kicad_native_pipeline.py:15` — print(f"Status: {baseline.status}")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:306` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:120` — - `scripts/report_kicad_native_pipeline.py:16` — print(f"PCB owner: {baseline.pcb_owner}")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:307` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:121` — - `scripts/report_kicad_native_pipeline.py:17` — print(f"Placement intent items: {baseline.footpri
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:308` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:122` — - `scripts/report_kicad_native_pipeline.py:18` — print(f"Accepted / review: {baseline.accepted_cou
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:309` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:123` — - `scripts/report_kicad_native_pipeline.py:19` — print(f"Manufacturing holes frozen: {baseline.man
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:310` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:124` — - `scripts/report_layout_baseline.py:1` — """Report the provisional Gate 3 PCB architecture baseli
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:311` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:125` — - `scripts/report_layout_baseline.py:18` — baseline = build_layout_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:312` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:126` — - `scripts/report_layout_baseline.py:21` — json_path.write_text(json.dumps(baseline.to_dict(), ind
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:313` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:127` — - `scripts/report_layout_baseline.py:23` — print(f"{baseline.identifier} — {baseline.revision}")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:314` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:128` — - `scripts/report_layout_baseline.py:24` — print(baseline.status)
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:315` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:129` — - `scripts/report_layout_baseline.py:25` — print(f"Stack-up: {baseline.stackup.layer_count} layers
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:316` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:130` — - `scripts/report_layout_baseline.py:26` — print(f"Functional regions: {len(baseline.regions)}")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:317` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:131` — - `scripts/report_layout_baseline.py:27` — print(f"Critical-net classes: {len(baseline.critical_ne
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:318` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:132` — - `scripts/report_layout_baseline.py:28` — print(f"Manual-only net classes: {sum(n.routing_policy.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:319` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:133` — - `scripts/report_performance_baseline.py:13` — baseline = build_performance_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:320` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:134` — - `scripts/report_performance_baseline.py:14` — print(f"{baseline.identifier} — {baseline.revision
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:321` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:135` — - `scripts/report_performance_baseline.py:15` — print(baseline.status)
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:322` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:136` — - `scripts/report_performance_baseline.py:18` — for row in baseline.gain_settings:
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:323` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:137` — - `scripts/report_performance_baseline.py:22` — for row in baseline.margins:
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:324` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:138` — - `scripts/report_performance_baseline.py:25` — print(f"\nCriticality records: {len(baseline.criti
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:325` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:139` — - `scripts/report_performance_baseline.py:26` — print(f"Placement constraints: {len(baseline.place
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:326` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:140` — - `scripts/report_performance_baseline.py:27` — print(f"Open measurements: {len(baseline.open_meas
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:327` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:141` — - `scripts/report_performance_baseline.py:32` — path.write_text(json.dumps(baseline.to_dict(), ind
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:328` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:142` — - `tests/test_enclosure_decision_baseline.py:21` — baseline = build_mechanical_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:329` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:143` — - `tests/test_enclosure_decision_baseline.py:22` — candidate = next(item for item in baseline.cand
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:330` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:144` — - `tests/test_enclosure_decision_baseline.py:23` — findings = decision_findings(candidate, baselin
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:331` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:145` — - `tests/test_kicad_native_pipeline.py:8` — baseline = build_kicad_native_pipeline_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:332` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:146` — - `tests/test_kicad_native_pipeline.py:9` — assert baseline.pcb_owner == "KiCad native document"
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:333` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:147` — - `tests/test_kicad_native_pipeline.py:10` — assert baseline.intent_owner == "Project Shellac engi
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:334` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:148` — - `tests/test_kicad_native_pipeline.py:11` — assert baseline.manufacturing_holes_frozen is False
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:335` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:149` — - `tests/test_kicad_native_pipeline.py:12` — assert validate_kicad_native_pipeline_baseline(baseli
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:336` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:150` — - `tests/test_kicad_native_pipeline.py:16` — baseline = build_kicad_native_pipeline_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:337` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:151` — - `tests/test_kicad_native_pipeline.py:17` — assert baseline.footprint_count == 250
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:338` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:152` — - `tests/test_kicad_native_pipeline.py:18` — assert baseline.accepted_count + baseline.review_coun
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:339` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:153` — - `tests/test_kicad_native_pipeline.py:19` — assert len({item["reference"] for item in baseline.pl
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:340` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:154` — - `tests/test_kicad_native_pipeline.py:23` — baseline = build_kicad_native_pipeline_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:341` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:155` — - `tests/test_kicad_native_pipeline.py:24` — manual = [i for i in baseline.placement_items if not 
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:342` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:156` — - `tests/test_layout_baseline.py:5` — baseline = build_layout_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:343` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:157` — - `tests/test_layout_baseline.py:6` — assert baseline.stackup.layer_count == 4
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:344` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:158` — - `tests/test_layout_baseline.py:7` — assert "Continuous 0VA" in baseline.stackup.inner_1_role
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:345` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:159` — - `tests/test_layout_baseline.py:11` — baseline = build_layout_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:346` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:160` — - `tests/test_layout_baseline.py:12` — assert len({r.identifier for r in baseline.regions}) == len
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:347` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:161` — - `tests/test_layout_baseline.py:13` — assert len({r.sequence for r in baseline.regions}) == len(b
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:348` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:162` — - `tests/test_layout_baseline.py:14` — assert [r.sequence for r in baseline.regions] == sorted(r.s
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:349` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:163` — - `tests/test_layout_baseline.py:18` — baseline = build_layout_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:350` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:164` — - `tests/test_layout_baseline.py:19` — assert len({n.identifier for n in baseline.critical_nets}) 
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:351` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:165` — - `tests/test_layout_baseline.py:20` — assert all(n.verification.strip() for n in baseline.critica
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:352` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:166` — - `tests/test_layout_baseline.py:24` — baseline = build_layout_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:353` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:167` — - `tests/test_layout_baseline.py:26` — for net in baseline.critical_nets:
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:354` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:168` — - `tests/test_layout_baseline.py:32` — baseline = build_layout_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:355` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:169` — - `tests/test_layout_baseline.py:33` — for net in baseline.critical_nets:
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:356` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:170` — - `tests/test_performance_baseline.py:15` — baseline = build_performance_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:357` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:171` — - `tests/test_performance_baseline.py:16` — for row in baseline.gain_settings:
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:358` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:172` — - `tests/test_performance_baseline.py:17` — assert abs(row.nominal_5mv_output_rms_v - baseline.nom
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:359` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:173` — - `tests/test_performance_baseline.py:46` — baseline = build_performance_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:360` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:174` — - `tests/test_performance_baseline.py:47` — joined = " ".join(baseline.open_measurements).lower()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:361` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:177` — - `tools/ae024_design_record_audit.py:25` — BASELINE_RE = re.compile(r"(?i)\b(?:current controlled
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:362` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:178` — - `tools/ae024_design_record_audit.py:246` — return "authoritative machine-readable baseline"
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:363` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:179` — - `tools/ae024_design_record_audit.py:276` — f"- baseline declaration lines: **{len(baselines)}**"
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:364` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:180` — - `tools/ae024_design_record_audit.py:294` — lines += ["", "## Baseline declarations requiring rec
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:365` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:181` — - `tools/ae024_design_record_audit.py:314` — "2. **01 Requirements and architecture** — current fu
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:366` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:182` — - `tools/apply_ae021c_population_closure.py:4` — "tests/test_kicad_native_pipeline.py": [("assert 
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:367` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:183` — - `tools/apply_ae022a_closure.py:79` — print("AE-013 historical baseline: isolated")
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:368` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:184` — - `tools/apply_dr039_full_closure.py:10` — raise SystemExit(label + ": expected baseline text not 
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:369` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:185` — - `tools/apply_sr039_final_consolidated.py:15` — baseline:
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:370` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:186` — - `tools/apply_sr039_final_consolidated.py:18` — tag: sr-038-dr038-dr039-validated-baseline
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:371` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:187` — - `tools/apply_sr039_final_consolidated.py:77` — reason: First regression repair; restored active 
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:372` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:188` — - `tools/apply_sr039_final_consolidated.py:80` — reason: Restored SCH103 baseline and established 
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:373` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:189` — - `tools/audit_current_decision_index.py:18` — # Narrow guard for the currently implemented DR-038
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:374` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:190` — - `generator/commissioning/model.py:1` — """G3-004 staged commissioning and verification baseline.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:375` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:191` — - `generator/commissioning/model.py:77` — ("Any undocumented substitution in a performance-definin
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:377` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:193` — - `generator/commissioning/model.py:166` — ("Noise spectra", "THD+N table", "Headroom map", "Final
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:378` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:194` — - `generator/layout/constraints.py:1` — """Gate 3 PCB architecture baseline.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:379` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:195` — - `generator/layout/kicad_native_pipeline.py:118` — baseline = build_kicad_native_pipeline_baselin
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:380` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:196` — - `generator/layout/kicad_native_pipeline.py:119` — issues = validate_kicad_native_pipeline_baseli
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:381` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:197` — - `generator/layout/kicad_native_pipeline.py:121` — raise ValueError("invalid KiCad-native pipelin
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:382` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:198` — - `generator/layout/kicad_native_pipeline.py:123` — path.write_text(json.dumps(asdict(baseline), i
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:383` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:199` — - `generator/layout/kicad_native_pipeline.py:124` — return baseline
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:384` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:200` — - `generator/layout/performance.py:1` — """Gate 3 quantitative performance and design-margin basel
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:385` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:201` — - `generator/layout/performance.py:209` — status="CALCULATED BASELINE — noise and distortion close
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:386` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:202` — - `generator/layout/placement_clusters.py:275` — raise ValueError("invalid cluster placement basel
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:387` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:203` — - `generator/layout/schematic_release_gate.py:46` — blockers.append("Manufacturing release blocked
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:388` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:204` — - `generator/layout/schematic_release_gate.py:60` — "Validated baseline evidence: 374/374 Python t
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:389` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:205` — - `generator/layout/sr041_routing_release.py:104` — "Schematic electrical baseline validated befor
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:390` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:206` — - `generator/layout/sr041_routing_release.py:107` — "Critical/manual clusters accepted as routing 
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:391` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:207` — - `generator/mechanical/freeze.py:75` — baseline: MechanicalBaseline,
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:392` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:208` — - `generator/mechanical/freeze.py:79` — baseline.audio_requirement
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:393` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:209` — - `generator/mechanical/freeze.py:81` — else baseline.psu_requirement
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:394` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:210` — - `generator/mechanical/freeze.py:134` — baseline = build_mechanical_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:395` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:211` — - `generator/mechanical/freeze.py:138` — eligible = [candidate for candidate in baseline.candidate
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:396` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:212` — - `generator/mechanical/freeze.py:141` — findings = decision_findings(candidate, baseline, evidenc
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:397` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:213` — - `generator/mechanical/placement.py:69` — baseline = build_layout_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:398` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:214` — - `generator/mechanical/placement.py:70` — if width_mm < baseline.envelope.minimum_usable_width_mm
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:399` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:215` — - `generator/mechanical/placement.py:73` — edge = baseline.envelope.board_edge_clearance_mm
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:400` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:216` — - `generator/mechanical/psu_release.py:90` — "A release-grade passive thermal proof cannot be calc
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:401` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:217` — - `generator/mechanical/sr040_audio_freeze.py:43` — baseline=build_mechanical_baseline()
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:402` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:218` — - `generator/mechanical/sr040_audio_freeze.py:44` — candidate=next(c for c in baseline.candidates 
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:403` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:219` — - `generator/model/production_cmrr.py:3` — Uses the implemented DR-038 values, not the earlier can
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:404` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:220` — - `generator/model/shellac.py:1` — """Project Shellac engineering-model baseline, Revision A.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:405` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:221` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:9` — - baseline declara
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:406` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:222` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:58` — ## Baseline decla
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:408` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:224` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:61` — - `manifest.json:
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:409` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:225` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:62` — - `README.md:5` —
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:410` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:226` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:63` — - `README.md:6` —
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:413` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:229` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:66` — - `docs/AE-003_Fu
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:414` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:230` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:67` — - `docs/AE-011_En
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:415` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:232` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:69` — - `docs/AE-011_En
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:446` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:270` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:108` — - `docs/AE-019_G
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:448` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:272` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:110` — - `docs/AE-023_P
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:450` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:274` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:112` — - `docs/G3-001_P
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:455` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:279` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:117` — - `docs/G3-004_C
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:457` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:281` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:119` — - `docs/G3-009_S
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:459` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:284` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:123` — - `docs/G3-025_F
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:461` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:286` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:125` — - `docs/SR-001_S
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:464` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:289` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:128` — - `docs/SR-015_E
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:467` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:292` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:131` — - `docs/SR-021D_
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:469` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:294` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:133` — - `docs/SR-021G_
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:471` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:296` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:135` — - `docs/SR-023_S
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:472` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:297` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:136` — - `docs/SR-039_S
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:475` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:300` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:139` — - `foundry/FOUND
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:476` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:301` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:140` — - `foundry/READM
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:477` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:302` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:141` — - `scripts/repor
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:478` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:303` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:142` — - `scripts/repor
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:479` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:304` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:143` — - `scripts/repor
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:480` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:305` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:144` — - `scripts/repor
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:481` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:306` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:145` — - `scripts/repor
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:482` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:307` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:146` — - `scripts/repor
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:483` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:308` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:147` — - `scripts/repor
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:484` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:309` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:148` — - `scripts/repor
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:486` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:311` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:150` — - `scripts/repor
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:487` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:312` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:151` — - `scripts/repor
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:488` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:313` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:152` — - `scripts/repor
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:489` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:314` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:153` — - `scripts/repor
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:490` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:315` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:154` — - `scripts/repor
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:491` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:316` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:155` — - `scripts/repor
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:492` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:317` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:156` — - `scripts/repor
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:494` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:319` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:158` — - `scripts/repor
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:495` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:320` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:159` — - `scripts/repor
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:496` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:321` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:160` — - `scripts/repor
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:497` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:322` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:161` — - `scripts/repor
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:498` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:323` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:162` — - `scripts/repor
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:499` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:324` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:163` — - `scripts/repor
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:500` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:325` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:164` — - `scripts/repor
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:501` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:326` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:165` — - `scripts/repor
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:502` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:327` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:166` — - `scripts/repor
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:503` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:328` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:167` — - `tests/test_en
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:504` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:329` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:168` — - `tests/test_en
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:506` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:331` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:170` — - `tests/test_ki
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:507` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:332` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:171` — - `tests/test_ki
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:508` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:333` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:172` — - `tests/test_ki
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:509` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:334` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:173` — - `tests/test_ki
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:511` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:336` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:175` — - `tests/test_ki
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:512` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:337` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:176` — - `tests/test_ki
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:513` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:338` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:177` — - `tests/test_ki
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:514` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:339` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:178` — - `tests/test_ki
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:515` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:340` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:179` — - `tests/test_ki
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:516` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:341` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:180` — - `tests/test_ki
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:517` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:342` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:181` — - `tests/test_la
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:518` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:343` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:182` — - `tests/test_la
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:519` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:344` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:183` — - `tests/test_la
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:520` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:345` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:184` — - `tests/test_la
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:521` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:346` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:185` — - `tests/test_la
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:522` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:347` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:186` — - `tests/test_la
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:523` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:348` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:187` — - `tests/test_la
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:524` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:349` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:188` — - `tests/test_la
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:525` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:350` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:189` — - `tests/test_la
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:526` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:351` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:190` — - `tests/test_la
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:527` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:352` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:191` — - `tests/test_la
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:528` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:353` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:192` — - `tests/test_la
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:529` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:354` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:193` — - `tests/test_la
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:530` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:355` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:194` — - `tests/test_la
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:531` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:356` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:195` — - `tests/test_pe
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:532` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:357` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:196` — - `tests/test_pe
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:533` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:358` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:197` — - `tests/test_pe
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:534` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:359` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:198` — - `tests/test_pe
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:535` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:360` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:199` — - `tests/test_pe
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:537` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:362` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:203` — - `tools/ae024_d
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:538` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:363` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:204` — - `tools/ae024_d
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:539` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:364` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:205` — - `tools/ae024_d
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:542` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:367` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:208` — - `tools/apply_a
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:543` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:368` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:209` — - `tools/apply_d
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:544` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:369` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:210` — - `tools/apply_s
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:545` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:370` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:211` — - `tools/apply_s
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:547` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:372` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:213` — - `tools/apply_s
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:549` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:374` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:215` — - `generator/com
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:552` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:378` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:219` — - `generator/lay
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:553` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:379` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:220` — - `generator/lay
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:556` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:382` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:223` — - `generator/lay
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:557` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:383` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:224` — - `generator/lay
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:559` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:385` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:226` — - `generator/lay
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:562` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:388` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:229` — - `generator/lay
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:563` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:389` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:230` — - `generator/lay
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:565` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:391` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:232` — - `generator/mec
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:566` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:392` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:233` — - `generator/mec
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:567` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:393` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:234` — - `generator/mec
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:568` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:394` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:235` — - `generator/mec
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:569` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:395` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:236` — - `generator/mec
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:570` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:396` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:237` — - `generator/mec
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:571` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:397` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:238` — - `generator/mec
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:572` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:398` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:239` — - `generator/mec
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:573` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:399` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:240` — - `generator/mec
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:575` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:401` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:242` — - `generator/mec
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:576` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:402` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:243` — - `generator/mec
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:578` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:404` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:245` — - `generator/mod
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:582` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:408` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:249` — - `docs/knowledg
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:586` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:412` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:253` — - `docs/knowledg
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:587` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:413` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:255` — - `docs/knowledg
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:588` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:414` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:256` — - `docs/knowledg
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:590` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:416` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:258` — - `docs/knowledg
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:591` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:417` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:259` — - `docs/knowledg
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:592` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:418` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:260` — - `docs/knowledg
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:594` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:420` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:262` — - `docs/knowledg
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:595` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:421` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:264` — - `docs/knowledg
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:601` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:428` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:271` — - `docs/updates/
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:602` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:429` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:272` — - `docs/updates/
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:607` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:434` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:277` — - `config/decisi
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:608` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:435` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:278` — - `config/decisi
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:610` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:437` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:280` — - `config/decisi
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:611` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:438` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:291` — \\\| `config/bom
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:612` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:439` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:292` — \\\| `config/dec
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:613` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:440` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:293` — \\\| `config/dec
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:614` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:441` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:294` — \\\| `config/fou
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:616` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:443` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:296` — \\\| `config/pro
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:618` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:445` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:298` — \\\| `config/rel
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:619` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:446` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:299` — \\\| `config/rel
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:620` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:447` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:300` — \\\| `config/rel
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:621` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:448` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:301` — \\\| `config/rel
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:622` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:449` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:553` — 2. **01 Requirem
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:623` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:450` — - `docs/design_pack/AE-024_Project_Wide_Design_Record_Reconciliation_Audit_Rev_A0.md:24` — baselin
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:624` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:451` — - `docs/design_pack/AE-024_Project_Wide_Design_Record_Reconciliation_Audit_Rev_A0.md:40` — - basel
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:625` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:452` — - `docs/design_pack/AE-024_Project_Wide_Design_Record_Reconciliation_Audit_Rev_A0.md:64` — authori
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:626` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:453` — - `docs/design_pack/AE-025_Current_Authority_and_Design_Pack_Reconciliation_Rev_A0.md:13` — - upda
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:627` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:454` — - `docs/design_pack/AE-025_Current_Authority_and_Design_Pack_Reconciliation_Rev_A0.md:23` — - nume
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:628` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:455` — - `docs/design_pack/AE-025_Current_Authority_and_Design_Pack_Reconciliation_Rev_A0.md:24` — record
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:629` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:456` — - `docs/knowledge/DECISION_REGISTER.md:3` — **Baseline:** SR-036 knowledge reconciliation
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:630` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:457` — - `docs/knowledge/DECISION_REGISTER.md:40` — \\\| DEC-032 \\\| Foundry FDR-001 is the controlled e
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:631` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:458` — - `docs/knowledge/DECISION_REGISTER.md:54` — \\\| DEC-046 \\\| shellac_bom.yaml remains a controll
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:632` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:459` — - `docs/knowledge/DECISION_REGISTER.md:73` — SR-035 incorrectly described Lorlin as the saved prio
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:633` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:460` — - `docs/knowledge/DESIGN_PACK_INDEX.md:7` — ## 1. Current design baseline
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:634` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:461` — - `docs/knowledge/DESIGN_PACK_INDEX.md:61` — Current signal-chain baseline:
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:635` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:462` — - `docs/knowledge/DESIGN_RULES.md:3` — **Status:** CONTROLLED BASELINE
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:636` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:463` — - `docs/knowledge/DESIGN_TENETS.md:3` — **Status:** CONTROLLED BASELINE
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:637` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:464` — - `docs/knowledge/PROJECT_STATUS.md:3` — **Knowledge baseline:** SR-036 + Foundry FDR-001
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:638` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:465` — - `docs/knowledge/RECOVERED_BASELINE.md:1` — # Project Shellac — Recovered Architecture & Componen
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:639` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:466` — - `docs/knowledge/RECOVERED_BASELINE.md:4` — **Status:** CONTROLLED RECONCILIATION BASELINE
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:640` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:468` — - `docs/knowledge/RECOVERED_BASELINE.md:38` — ## Mechanical baseline
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:642` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:470` — - `docs/maintenance/MAINTENANCE_GUIDE_SKELETON.md:6` — Product/revision, PCB revision, release tag
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:643` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:471` — - `docs/maintenance/Signal_Chain_Commissioning_and_Maintenance_Baseline_Rev_A0.md:1` — # Project S
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:644` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:472` — - `docs/maintenance/Signal_Chain_Commissioning_and_Maintenance_Baseline_Rev_A0.md:3` — **Status:**
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:645` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:473` — - `docs/updates/AE016B_UPDATE_MANIFEST.md:6` — - restore `generator/blocks/replay_eq.py` to its pr
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:646` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:474` — - `docs/updates/AE016_UPDATE_MANIFEST.md:12` — - AE-016 implementation baseline
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:647` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:475` — - `docs/updates/AE017_UPDATE_MANIFEST.md:11` — No active circuit, CAD, BOM, or analysis baseline i
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:648` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:476` — - `docs/updates/AE019_UPDATE_MANIFEST.md:3` — Adds a read-only documentation reconciliation scanne
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:649` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:477` — - `docs/updates/AE023_UPDATE_MANIFEST.md:27` — `git commit -m "analysis(signal-chain): close produ
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:650` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:478` — - `docs/updates/SR039_UPDATE_MANIFEST.md:8` — - records the validated 374/374 + native ERC 0/0 ele
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:651` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:479` — - `docs/updates/SR041_UPDATE_MANIFEST.md:6` — - accepts deterministic manual-authority clusters as
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:652` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:480` — - `config/decisions/current_decision_index.yaml:4` — authority_scope: Working design authority is 
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:653` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:481` — - `config/decisions/current_decision_index.yaml:5` — baseline:
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:654` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:482` — - `config/decisions/current_decision_index.yaml:8` — tag: sr-038-dr038-dr039-validated-baseline
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:655` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:483` — - `config/decisions/current_decision_index.yaml:67` — reason: First regression repair; restored ac
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:656` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:484` — - `config/decisions/current_decision_index.yaml:70` — reason: Restored SCH103 baseline and establi
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:657` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:496` — \\| `config/bom/shellac_bom.yaml` \\| authoritative machine-readable baseline \\|
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:658` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:497` — \\| `config/decisions/current_decision_index.yaml` \\| authoritative machine-readable baseline \\|
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:659` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:498` — \\| `config/decisions/decision_status.yaml` \\| authoritative machine-readable baseline \\|
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:660` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:499` — \\| `config/foundry/foundry.yaml` \\| authoritative machine-readable baseline \\|
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:661` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:500` — \\| `config/mechanical/sr040_audio_mechanical_freeze.yaml` \\| authoritative machine-readable base
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:662` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:501` — \\| `config/procurement/policy.yaml` \\| authoritative machine-readable baseline \\|
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:663` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:502` — \\| `config/procurement/sourcing_snapshot_2026-08-24.yaml` \\| authoritative machine-readable base
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:664` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:503` — \\| `config/release/sr039_schematic_to_layout.yaml` \\| authoritative machine-readable baseline \\
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:665` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:504` — \\| `config/release/sr041_routing_release.yaml` \\| authoritative machine-readable baseline \\|
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:666` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:505` — \\| `config/release/sr042_native_kicad_bootstrap.yaml` \\| authoritative machine-readable baseline
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:667` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:506` — \\| `config/release/sr043_native_board.yaml` \\| authoritative machine-readable baseline \\|
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:668` — - `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:762` — 2. **01 Requirements and architecture** — current functional/electrical/mechanical baseline.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:669` — - `docs/design_pack/AE-024_Project_Wide_Design_Record_Reconciliation_Audit_Rev_A0.md:24` — baseline despite substantial later controlled work.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:670` — - `docs/design_pack/AE-024_Project_Wide_Design_Record_Reconciliation_Audit_Rev_A0.md:40` — - baseline declarations;
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:671` — - `docs/design_pack/AE-024_Project_Wide_Design_Record_Reconciliation_Audit_Rev_A0.md:64` — authoritative baseline before we start reconciliation edits.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:672` — - `docs/design_pack/AE-025A_Authority_Reconciliation_Regression_Repair_Rev_A0.md:10` — 2. `baseline.branch` in the authoritative current decision index was changed from
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:673` — - `docs/design_pack/AE-025A_Authority_Reconciliation_Regression_Repair_Rev_A0.md:11` — `main` to `develop`. That field describes the validated implementation baseline,
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:674` — - `docs/design_pack/AE-025A_Authority_Reconciliation_Regression_Repair_Rev_A0.md:17` — - `baseline.branch` remains `main`;
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:675` — - `docs/design_pack/AE-025A_Authority_Reconciliation_Regression_Repair_Rev_A0.md:20` — than corrupting baseline provenance.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:676` — - `docs/design_pack/AE-025_Current_Authority_and_Design_Pack_Reconciliation_Rev_A0.md:13` — - updates README from stale SR-034/G3-023 baseline language;
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:677` — - `docs/design_pack/AE-025_Current_Authority_and_Design_Pack_Reconciliation_Rev_A0.md:23` — - numerous baseline keyword hits may remain because historical analyses correctly
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:678` — - `docs/design_pack/AE-025_Current_Authority_and_Design_Pack_Reconciliation_Rev_A0.md:24` — record the baseline they examined.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:679` — - `docs/knowledge/DECISION_REGISTER.md:3` — **Baseline:** SR-036 knowledge reconciliation
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:680` — - `docs/knowledge/DECISION_REGISTER.md:40` — \\| DEC-032 \\| Foundry FDR-001 is the controlled engineering-governance baseline for evidence, decisions, conflicts and manufacturing 
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:681` — - `docs/knowledge/DECISION_REGISTER.md:54` — \\| DEC-046 \\| shellac_bom.yaml remains a controlled partial baseline, not procurement-complete BOM \\| SELECTED \\| G3_027_REPOSITORY
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:682` — - `docs/knowledge/DECISION_REGISTER.md:73` — SR-035 incorrectly described Lorlin as the saved prior BOM baseline. Surviving BOM evidence
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:683` — - `docs/knowledge/DESIGN_PACK_INDEX.md:7` — ## 1. Current design baseline
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:684` — - `docs/knowledge/DESIGN_PACK_INDEX.md:61` — Current signal-chain baseline:
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:685` — - `docs/knowledge/DESIGN_RULES.md:3` — **Status:** CONTROLLED BASELINE
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:686` — - `docs/knowledge/DESIGN_TENETS.md:3` — **Status:** CONTROLLED BASELINE
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:687` — - `docs/knowledge/PROJECT_STATUS.md:3` — **Knowledge baseline:** SR-036 + Foundry FDR-001
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:688` — - `docs/knowledge/RECOVERED_BASELINE.md:1` — # Project Shellac — Recovered Architecture & Component Baseline
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:689` — - `docs/knowledge/RECOVERED_BASELINE.md:4` — **Status:** CONTROLLED RECONCILIATION BASELINE
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:691` — - `docs/knowledge/RECOVERED_BASELINE.md:38` — ## Mechanical baseline
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:692` — - `docs/knowledge/RISK_REGISTER.md:17` — \\| R-013 \\| Engineering method/decision hierarchy existed only implicitly across knowledge files and conversation \\| RESOLVED \\| FDR-00
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:693` — - `docs/maintenance/MAINTENANCE_GUIDE_SKELETON.md:6` — Product/revision, PCB revision, release tag, toolchain baseline, build record.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:694` — - `docs/maintenance/Signal_Chain_Commissioning_and_Maintenance_Baseline_Rev_A0.md:1` — # Project Shellac — Signal-Chain Commissioning and Maintenance Baseline
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:695` — - `docs/maintenance/Signal_Chain_Commissioning_and_Maintenance_Baseline_Rev_A0.md:3` — **Status:** PRE-PRODUCTION MAINTENANCE BASELINE
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:696` — - `docs/updates/AE016B_UPDATE_MANIFEST.md:6` — - restore `generator/blocks/replay_eq.py` to its pre-DR039 physical baseline;
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:697` — - `docs/updates/AE016_UPDATE_MANIFEST.md:12` — - AE-016 implementation baseline
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:698` — - `docs/updates/AE017_UPDATE_MANIFEST.md:11` — No active circuit, CAD, BOM, or analysis baseline is modified.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:699` — - `docs/updates/AE019_UPDATE_MANIFEST.md:3` — Adds a read-only documentation reconciliation scanner and test. No circuit/CAD baseline changes.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:700` — - `docs/updates/AE023_UPDATE_MANIFEST.md:27` — `git commit -m "analysis(signal-chain): close production assurance baseline"`
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:701` — - `docs/updates/SR039_UPDATE_MANIFEST.md:8` — - records the validated 374/374 + native ERC 0/0 electrical baseline;
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:702` — - `docs/updates/SR041_UPDATE_MANIFEST.md:6` — - accepts deterministic manual-authority clusters as routing baseline;
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:703` — - `config/decisions/current_decision_index.yaml:4` — baseline:
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:704` — - `config/decisions/current_decision_index.yaml:7` — tag: sr-038-dr038-dr039-validated-baseline
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:705` — - `config/decisions/current_decision_index.yaml:66` — reason: First regression repair; restored active SCH101 baseline.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:706` — - `config/decisions/current_decision_index.yaml:69` — reason: Restored SCH103 baseline and established atomic migration boundary.
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:718` — \| `config/bom/shellac_bom.yaml` \| authoritative machine-readable baseline \|
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:719` — \| `config/decisions/current_decision_index.yaml` \| authoritative machine-readable baseline \|
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:720` — \| `config/decisions/decision_status.yaml` \| authoritative machine-readable baseline \|
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:721` — \| `config/foundry/foundry.yaml` \| authoritative machine-readable baseline \|
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:722` — \| `config/mechanical/sr040_audio_mechanical_freeze.yaml` \| authoritative machine-readable baseline \|
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:723` — \| `config/procurement/policy.yaml` \| authoritative machine-readable baseline \|
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:724` — \| `config/procurement/sourcing_snapshot_2026-08-24.yaml` \| authoritative machine-readable baseline \|
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:725` — \| `config/release/sr039_schematic_to_layout.yaml` \| authoritative machine-readable baseline \|
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:726` — \| `config/release/sr041_routing_release.yaml` \| authoritative machine-readable baseline \|
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:727` — \| `config/release/sr042_native_kicad_bootstrap.yaml` \| authoritative machine-readable baseline \|
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:728` — \| `config/release/sr043_native_board.yaml` \| authoritative machine-readable baseline \|
- `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md:987` — 2. **01 Requirements and architecture** — current functional/electrical/mechanical baseline.
- `docs/design_pack/AE-024_Project_Wide_Design_Record_Reconciliation_Audit_Rev_A0.md:24` — baseline despite substantial later controlled work.
- `docs/design_pack/AE-024_Project_Wide_Design_Record_Reconciliation_Audit_Rev_A0.md:40` — - baseline declarations;
- `docs/design_pack/AE-024_Project_Wide_Design_Record_Reconciliation_Audit_Rev_A0.md:64` — authoritative baseline before we start reconciliation edits.
- `docs/design_pack/AE-025A_Authority_Reconciliation_Regression_Repair_Rev_A0.md:10` — 2. `baseline.branch` in the authoritative current decision index was changed from
- `docs/design_pack/AE-025A_Authority_Reconciliation_Regression_Repair_Rev_A0.md:11` — `main` to `develop`. That field describes the validated implementation baseline,
- `docs/design_pack/AE-025A_Authority_Reconciliation_Regression_Repair_Rev_A0.md:17` — - `baseline.branch` remains `main`;
- `docs/design_pack/AE-025A_Authority_Reconciliation_Regression_Repair_Rev_A0.md:20` — than corrupting baseline provenance.
- `docs/design_pack/AE-025_Current_Authority_and_Design_Pack_Reconciliation_Rev_A0.md:13` — - updates README from stale SR-034/G3-023 baseline language;
- `docs/design_pack/AE-025_Current_Authority_and_Design_Pack_Reconciliation_Rev_A0.md:23` — - numerous baseline keyword hits may remain because historical analyses correctly
- `docs/design_pack/AE-025_Current_Authority_and_Design_Pack_Reconciliation_Rev_A0.md:24` — record the baseline they examined.
- `docs/knowledge/DECISION_REGISTER.md:3` — **Baseline:** SR-036 knowledge reconciliation
- `docs/knowledge/DECISION_REGISTER.md:40` — \| DEC-032 \| Foundry FDR-001 is the controlled engineering-governance baseline for evidence, decisions, conflicts and manufacturing release \| SELECTED \| G3_025 \| Git remains au
- `docs/knowledge/DECISION_REGISTER.md:54` — \| DEC-046 \| shellac_bom.yaml remains a controlled partial baseline, not procurement-complete BOM \| SELECTED \| G3_027_REPOSITORY_AUDIT \| Full schematic-derived inventory requir
- `docs/knowledge/DECISION_REGISTER.md:73` — SR-035 incorrectly described Lorlin as the saved prior BOM baseline. Surviving BOM evidence
- `docs/knowledge/DESIGN_PACK_INDEX.md:7` — ## 1. Current design baseline
- `docs/knowledge/DESIGN_PACK_INDEX.md:61` — Current signal-chain baseline:
- `docs/knowledge/DESIGN_RULES.md:3` — **Status:** CONTROLLED BASELINE
- `docs/knowledge/DESIGN_TENETS.md:3` — **Status:** CONTROLLED BASELINE
- `docs/knowledge/PROJECT_STATUS.md:3` — **Knowledge baseline:** SR-036 + Foundry FDR-001
- `docs/knowledge/RECOVERED_BASELINE.md:1` — # Project Shellac — Recovered Architecture & Component Baseline
- `docs/knowledge/RECOVERED_BASELINE.md:4` — **Status:** CONTROLLED RECONCILIATION BASELINE
- `docs/knowledge/RECOVERED_BASELINE.md:31` — Surviving interim BOMs recorded three Grayhill 71-series rotaries, including a 4P4T Mode switch, historically budgeted around £28 each. Later project work questioned that premium u
- `docs/knowledge/RECOVERED_BASELINE.md:38` — ## Mechanical baseline
- `docs/knowledge/RISK_REGISTER.md:17` — \| R-013 \| Engineering method/decision hierarchy existed only implicitly across knowledge files and conversation \| RESOLVED \| FDR-001 Foundry baseline added under configuration 
- `docs/maintenance/MAINTENANCE_GUIDE_SKELETON.md:6` — Product/revision, PCB revision, release tag, toolchain baseline, build record.
- `docs/maintenance/Signal_Chain_Commissioning_and_Maintenance_Baseline_Rev_A0.md:1` — # Project Shellac — Signal-Chain Commissioning and Maintenance Baseline
- `docs/maintenance/Signal_Chain_Commissioning_and_Maintenance_Baseline_Rev_A0.md:3` — **Status:** PRE-PRODUCTION MAINTENANCE BASELINE
- `docs/updates/AE016B_UPDATE_MANIFEST.md:6` — - restore `generator/blocks/replay_eq.py` to its pre-DR039 physical baseline;
- `docs/updates/AE016_UPDATE_MANIFEST.md:12` — - AE-016 implementation baseline
- `docs/updates/AE017_UPDATE_MANIFEST.md:11` — No active circuit, CAD, BOM, or analysis baseline is modified.
- `docs/updates/AE019_UPDATE_MANIFEST.md:3` — Adds a read-only documentation reconciliation scanner and test. No circuit/CAD baseline changes.
- `docs/updates/AE023_UPDATE_MANIFEST.md:27` — `git commit -m "analysis(signal-chain): close production assurance baseline"`
- `docs/updates/SR039_UPDATE_MANIFEST.md:8` — - records the validated 374/374 + native ERC 0/0 electrical baseline;
- `docs/updates/SR041_UPDATE_MANIFEST.md:6` — - accepts deterministic manual-authority clusters as routing baseline;
- `config/decisions/current_decision_index.yaml:4` — baseline:
- `config/decisions/current_decision_index.yaml:7` — tag: sr-038-dr038-dr039-validated-baseline
- `config/decisions/current_decision_index.yaml:66` — reason: First regression repair; restored active SCH101 baseline.
- `config/decisions/current_decision_index.yaml:69` — reason: Restored SCH103 baseline and established atomic migration boundary.

## Design-pack document inventory

| File | Proposed production-pack role |
|---|---|
| `AE020A_README.md` | supporting/history |
| `APPLY_AE025_AUDIT_PATCH.py` | supporting/history |
| `APPLY_DECISION_INDEX_RECONCILIATION.py` | supporting/history |
| `APPLY_UPDATE.bat` | supporting/history |
| `README.md` | project entry point |
| `README_G3_016.md` | supporting/history |
| `config/bom/shellac_bom.yaml` | authoritative machine-readable baseline |
| `config/decisions/current_decision_index.yaml` | authoritative machine-readable baseline |
| `config/decisions/decision_status.yaml` | authoritative machine-readable baseline |
| `config/foundry/foundry.yaml` | authoritative machine-readable baseline |
| `config/mechanical/sr040_audio_mechanical_freeze.yaml` | authoritative machine-readable baseline |
| `config/procurement/policy.yaml` | authoritative machine-readable baseline |
| `config/procurement/sourcing_snapshot_2026-08-24.yaml` | authoritative machine-readable baseline |
| `config/release/sr039_schematic_to_layout.yaml` | authoritative machine-readable baseline |
| `config/release/sr041_routing_release.yaml` | authoritative machine-readable baseline |
| `config/release/sr042_native_kicad_bootstrap.yaml` | authoritative machine-readable baseline |
| `config/release/sr043_native_board.yaml` | authoritative machine-readable baseline |
| `docs/AE-001_Replay_Equalisation_Synthesis_Rev_A.md` | design assurance evidence |
| `docs/AE-002_Transfer_Function_Engine_Rev_A.md` | design assurance evidence |
| `docs/AE-003_Full_Band_Replay_Curve_Analysis_Rev_A.md` | design assurance evidence |
| `docs/AE-004_SCH103_Electrical_Closure_Rev_A.md` | design assurance evidence |
| `docs/AE-005_SCH107_Rumble_Filter_Rev_A.md` | design assurance evidence |
| `docs/AE-006_SCH104_Final_Gain_Rev_A.md` | design assurance evidence |
| `docs/AE-007_SCH105_Channel_Mode_Matrix_Rev_A.md` | design assurance evidence |
| `docs/AE-008_SCH108_Balanced_Output_Rev_A.md` | design assurance evidence |
| `docs/AE-009_SCH109_Controls_UI_Rev_A.md` | design assurance evidence |
| `docs/AE-010_SCH101_Gain_Selector_Closure_Rev_A.md` | design assurance evidence |
| `docs/AE-011_End_to_End_Signal_Chain_Closure_Rev_A0.md` | design assurance evidence |
| `docs/AE-011_End_to_End_Signal_Chain_Closure_Rev_A1.md` | design assurance evidence |
| `docs/AE-012_All_State_Gain_Headroom_Closure_Rev_A0.md` | design assurance evidence |
| `docs/AE-013_SCH101_Noise_CMRR_Review_Rev_A0.md` | design assurance evidence |
| `docs/AE-014_SCH101_Precision_Architecture_Downselect_Rev_A0.md` | design assurance evidence |
| `docs/AE-015_Full_Chain_Noise_DC_Review_Rev_A0.md` | design assurance evidence |
| `docs/AE-016A_AE016_Regression_Repair_Rev_A0.md` | design assurance evidence |
| `docs/AE-016B_Full_Regression_Staging_Repair_Rev_A0.md` | design assurance evidence |
| `docs/AE-016_DR038_DR039_Implementation_Baseline_Rev_A0.md` | design assurance evidence |
| `docs/AE-017_Atomic_Migration_Dependency_Mapping_Gate_Rev_A0.md` | design assurance evidence |
| `docs/AE-017_Generated_Atomic_Migration_Dependency_Map.md` | design assurance evidence |
| `docs/AE-018_Live_Dependency_Disposition_and_Precision_CAD_Primitives_Rev_A0.md` | design assurance evidence |
| `docs/AE-019_Design_Record_Reconciliation_Gate_Rev_A0.md` | design assurance evidence |
| `docs/AE-019_Generated_Design_Record_Reconciliation.md` | design assurance evidence |
| `docs/AE-020_Decision_Register_Reconciliation_and_Design_Pack_Structure_Rev_A0.md` | design assurance evidence |
| `docs/AE-021_DR039_Full_Implementation_and_Schematic_Rework_Acceleration_Rev_A0.md` | design assurance evidence |
| `docs/AE-022A_DR038_Migration_Closure_Rev_A0.md` | design assurance evidence |
| `docs/AE-022A_Generated_Stale_SCH101_Contract_Audit.md` | design assurance evidence |
| `docs/AE-022B_LT5400_Converter_Routing_Closure_Rev_A0.md` | design assurance evidence |
| `docs/AE-022C_LT5400_Pin_Crossing_Closure_Rev_A0.md` | design assurance evidence |
| `docs/AE-022D_Exact_Net_Conflict_Closure_Rev_A0.md` | design assurance evidence |
| `docs/AE-022E_Named_Net_LT5400_Closure_Rev_A0.md` | design assurance evidence |
| `docs/AE-022F_LT5400_Symbol_Contract_Closure_Rev_A0.md` | design assurance evidence |
| `docs/AE-022G_DR038_Definitive_Snapshot_Closure_Rev_A0.md` | design assurance evidence |
| `docs/AE-022H_Final_Regression_Closure_Rev_A0.md` | design assurance evidence |
| `docs/AE-022_DR038_Full_SCH101_Precision_Migration_Rev_A0.md` | design assurance evidence |
| `docs/AE-023_Production_Signal_Chain_Assurance_Closure_Rev_A0.md` | design assurance evidence |
| `docs/DR-037_Restore_Legacy_Complete_RIAA_Architecture_Rev_A0.md` | supporting/history |
| `docs/G3-001_PCB_Architecture_and_Layout_Constitution_Rev_A0.md` | gate/history evidence |
| `docs/G3-002_Quantitative_Performance_and_Critical_Loop_Baseline_Rev_A0.md` | gate/history evidence |
| `docs/G3-003_Mechanical_Datum_and_Preliminary_Placement_Baseline_Rev_A0.md` | gate/history evidence |
| `docs/G3-004_Commissioning_and_Verification_Baseline_Rev_A0.md` | gate/history evidence |
| `docs/G3-005_Component_Cluster_Placement_Baseline_Rev_A0.md` | gate/history evidence |
| `docs/G3-006_Enclosure_Decision_and_Carrier_Plate_Freeze_Rev_A0.md` | gate/history evidence |
| `docs/G3-007_Board_Outline_Mounting_Hole_Synthesis_Rev_A0.md` | gate/history evidence |
| `docs/G3-008_PCB_Coordinate_Frame_KiCad_Board_Skeleton_Rev_A0.md` | gate/history evidence |
| `docs/G3-009_Schematic_to_PCB_Footprint_Contract_Rev_A0.md` | gate/history evidence |
| `docs/G3-010_Interconnect_Harness_Architecture_Rev_A0.md` | gate/history evidence |
| `docs/G3-013A_G3-014_KiCad_Parser_and_Native_Pipeline_Rev_A0.md` | gate/history evidence |
| `docs/G3-013_Gate_3A_Populated_Review_Board_Rev_A0.md` | gate/history evidence |
| `docs/G3-015_Gate_3A_Macro_Acceptance_and_CLU-106_Refinement_Rev_A0.md` | gate/history evidence |
| `docs/G3-016_Real_Footprint_Audit_and_Capacitor_ECO_Blockers_Rev_A0.md` | gate/history evidence |
| `docs/G3-018_Detailed_Placement_Readiness_Rev_A0.md` | gate/history evidence |
| `docs/G3-019_UNICASE_Front_to_Rear_Interface_Architecture_Rev_A0.md` | gate/history evidence |
| `docs/G3-020_UNICASE_Sizing_Control_Stack_Rev_A0.md` | gate/history evidence |
| `docs/G3-021_PSU_UNICASE_Component_Fit_Closure_Rev_A0.md` | gate/history evidence |
| `docs/G3-022_PSU_Thermal_Mains_Release_Rev_A0.md` | gate/history evidence |
| `docs/G3-023_PSU_UNICASE2_Freeze_Rev_A0.md` | gate/history evidence |
| `docs/G3-024_Audio_Control_Subsystem_Hardware_Closure_Rev_A0.md` | gate/history evidence |
| `docs/G3-025_Foundry_RIAA_Physical_Closure_Rev_A0.md` | gate/history evidence |
| `docs/G3-026_Optional_RIAA_Circuit_and_Manufacturing_Geometry_Rev_A0.md` | gate/history evidence |
| `docs/G3-027_RIAA_Integration_Audit_and_BOM_Reconciliation_Rev_A1.md` | gate/history evidence |
| `docs/SR-001_Schematic_Generation_Readiness_Audit_Rev_A.md` | review/closure evidence |
| `docs/SR-002_Pin_Aware_Renderer_Foundation_Rev_A.md` | review/closure evidence |
| `docs/SR-003_SCH105_Pin_Aware_Conversion_Rev_A.md` | review/closure evidence |
| `docs/SR-004_SCH107_Pin_Aware_Conversion_Rev_A.md` | review/closure evidence |
| `docs/SR-005_SCH108_Pin_Aware_Conversion_Rev_A.md` | review/closure evidence |
| `docs/SR-006_SCH101_DIP_Switch_Closure_Rev_A.md` | review/closure evidence |
| `docs/SR-007_SCH109_Pin_Aware_Conversion_Rev_A.md` | review/closure evidence |
| `docs/SR-008_SCH103_Pin_Aware_Conversion_Rev_A.md` | review/closure evidence |
| `docs/SR-009_Root_Hierarchical_Schematic_Rev_A.md` | review/closure evidence |
| `docs/SR-010_Annotation_and_Symbol_Closure_Rev_A.md` | review/closure evidence |
| `docs/SR-011_Hierarchical_ERC_Execution_Rev_A.md` | review/closure evidence |
| `docs/SR-012_Electrical_Grid_Alignment_Rev_A.md` | review/closure evidence |
| `docs/SR-013_Pin_Coordinate_Contract_Closure_Rev_A.md` | review/closure evidence |
| `docs/SR-014_Legacy_Sheet_Pin_Aware_Closure_Rev_A.md` | review/closure evidence |
| `docs/SR-015_ERC_and_Deterministic_Build_Closure_Rev_A.md` | review/closure evidence |
| `docs/SR-016_Schematic_Capture_Review_Preparation_Rev_A.md` | review/closure evidence |
| `docs/SR-017_Standalone_Annotation_and_Human_Review_Proof_Rev_A.md` | review/closure evidence |
| `docs/SR-018_SCH101_Human_Reviewable_Conversion_Rev_A.md` | review/closure evidence |
| `docs/SR-019_Deterministic_Junction_Dots_Rev_A.md` | review/closure evidence |
| `docs/SR-020_SCH106_Human_Reviewable_Conversion_Rev_A.md` | review/closure evidence |
| `docs/SR-021B_Canonical_Grid_and_Electrical_Integrity_Foundation_Rev_A.md` | review/closure evidence |
| `docs/SR-021_SCH107_Human_Reviewable_Conversion_Rev_A.md` | review/closure evidence |
| `docs/SR-023A_SCH108_ERC_Closure_Rev_A.md` | review/closure evidence |
| `docs/SR-023_SCH108_Human_Reviewable_Rev_A.md` | review/closure evidence |
| `docs/SR-024_SCH103_Human_Reviewable_Rev_A.md` | review/closure evidence |
| `docs/SR-025A_Gate_2B_Native_ERC_Closure_Rev_A.md` | review/closure evidence |
| `docs/SR-025_SCH109_Human_Reviewable_and_Gate_2B_Rev_A.md` | review/closure evidence |
| `docs/SR-039_Schematic_to_Layout_Release_Gate_Rev_A0.md` | review/closure evidence |
| `docs/SR-040_Mechanical_BOM_Placement_Closure_Rev_A0.md` | review/closure evidence |
| `docs/SR-041_Critical_Placement_and_Routing_Release_Rev_A0.md` | review/closure evidence |
| `docs/SR-042_Native_KiCad_Board_Bootstrap_Rev_A0.md` | review/closure evidence |
| `docs/SR-043_Native_Board_Placement_and_Stackup_Gate_Rev_A0.md` | review/closure evidence |
| `docs/decisions/DR-038_SCH101_Precision_Architecture_PROPOSED.md` | decision evidence |
| `docs/decisions/DR-038_SCH101_Precision_Architecture_SELECTED.md` | decision evidence |
| `docs/decisions/DR-039_Common_Post_EQ_DC_Block_PROPOSED.md` | decision evidence |
| `docs/decisions/DR-039_Common_Post_EQ_DC_Block_SELECTED.md` | decision evidence |
| `docs/decisions/DR-040_Precision_CAD_Primitive_Staging_SELECTED.md` | decision evidence |
| `docs/design_pack/AE-024A_Standard_Library_Audit_Repair_Rev_A0.md` | design assurance evidence |
| `docs/design_pack/AE-024_Generated_Design_Record_Reconciliation_Audit.md` | design assurance evidence |
| `docs/design_pack/AE-024_Project_Wide_Design_Record_Reconciliation_Audit_Rev_A0.md` | design assurance evidence |
| `docs/design_pack/AE-025A_Authority_Reconciliation_Regression_Repair_Rev_A0.md` | design assurance evidence |
| `docs/design_pack/AE-025B_Test_Fixture_Repair_Rev_A0.md` | design assurance evidence |
| `docs/design_pack/AE-025_Current_Authority_and_Design_Pack_Reconciliation_Rev_A0.md` | design assurance evidence |
| `docs/knowledge/CONFIGURATION_CONTROL.md` | knowledge summary |
| `docs/knowledge/DECISION_REGISTER.md` | knowledge summary |
| `docs/knowledge/DESIGN_PACK_INDEX.md` | knowledge summary |
| `docs/knowledge/DESIGN_RULES.md` | knowledge summary |
| `docs/knowledge/DESIGN_TENETS.md` | knowledge summary |
| `docs/knowledge/PROJECT_STATUS.md` | knowledge summary |
| `docs/knowledge/RECOVERED_BASELINE.md` | knowledge summary |
| `docs/knowledge/RISK_REGISTER.md` | knowledge summary |
| `docs/maintenance/DR038_SCH101_PRECISION_FRONT_END.md` | maintenance/commissioning |
| `docs/maintenance/DR039_POST_EQ_DC_BLOCK.md` | maintenance/commissioning |
| `docs/maintenance/MAINTENANCE_GUIDE_SKELETON.md` | maintenance/commissioning |
| `docs/maintenance/Signal_Chain_Commissioning_and_Maintenance_Baseline_Rev_A0.md` | maintenance/commissioning |
| `docs/updates/AE012_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/AE013_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/AE014_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/AE015_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/AE016A_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/AE016B_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/AE016_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/AE017_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/AE018_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/AE019_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/AE020_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/AE021B_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/AE021C_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/AE021_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/AE022A_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/AE022B_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/AE022C_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/AE022D_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/AE022E_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/AE022F_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/AE022G_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/AE022H_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/AE022_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/AE023_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/AE024A_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/AE024_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/AE025A_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/AE025B_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/AE025_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/DR037_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/SR039_FINAL_CONSOLIDATED_CLOSURE.md` | supporting/history |
| `docs/updates/SR039_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/SR040_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/SR041A_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/SR041_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/SR042_UPDATE_MANIFEST.md` | supporting/history |
| `docs/updates/SR043_UPDATE_MANIFEST.md` | supporting/history |
| `foundry/FOUNDRY_BASELINE.md` | supporting/history |
| `foundry/README.md` | supporting/history |
| `generator/blocks/balanced_input.py` | supporting/history |
| `generator/blocks/final_gain.py` | supporting/history |
| `generator/blocks/power_entry.py` | supporting/history |
| `generator/blocks/replay_eq.py` | supporting/history |
| `generator/blocks/rumble_filter.py` | supporting/history |
| `generator/commissioning/model.py` | supporting/history |
| `generator/core/components.py` | supporting/history |
| `generator/layout/constraints.py` | supporting/history |
| `generator/layout/detailed_placement_readiness.py` | supporting/history |
| `generator/layout/footprint_contract.py` | supporting/history |
| `generator/layout/ghost_placement.py` | supporting/history |
| `generator/layout/interconnect_architecture.py` | supporting/history |
| `generator/layout/preliminary_placement.py` | supporting/history |
| `generator/layout/schematic_release_gate.py` | supporting/history |
| `generator/layout/sr040_routing_readiness.py` | supporting/history |
| `generator/layout/sr041_routing_release.py` | supporting/history |
| `generator/layout/sr042_native_routing_bootstrap.py` | supporting/history |
| `generator/mechanical/board_outline.py` | supporting/history |
| `generator/mechanical/board_skeleton.py` | supporting/history |
| `generator/mechanical/control_hardware.py` | supporting/history |
| `generator/mechanical/freeze.py` | supporting/history |
| `generator/mechanical/interface_architecture.py` | supporting/history |
| `generator/mechanical/model.py` | supporting/history |
| `generator/mechanical/placement.py` | supporting/history |
| `generator/mechanical/populated_board.py` | supporting/history |
| `generator/mechanical/psu_enclosure_freeze.py` | supporting/history |
| `generator/mechanical/psu_fit.py` | supporting/history |
| `generator/mechanical/psu_release.py` | supporting/history |
| `generator/mechanical/released_placement_board.py` | supporting/history |
| `generator/mechanical/sr040_audio_freeze.py` | supporting/history |
| `generator/mechanical/top_cover_stack.py` | supporting/history |
| `generator/mechanical/unicase_fit.py` | supporting/history |
| `generator/model/controls.py` | supporting/history |
| `generator/model/final_gain.py` | supporting/history |
| `generator/model/mode_matrix.py` | supporting/history |
| `generator/model/mode_matrix_analysis.py` | supporting/history |
| `generator/model/output_driver.py` | supporting/history |
| `generator/model/post_eq_dc_block.py` | supporting/history |
| `generator/model/precision_cad_contract.py` | supporting/history |
| `generator/model/production_cmrr.py` | supporting/history |
| `generator/model/production_signal_chain_closure.py` | supporting/history |
| `generator/model/replay_eq_electrical.py` | supporting/history |
| `generator/model/replay_eq_synthesis.py` | supporting/history |
| `generator/model/replay_eq_transfer.py` | supporting/history |
| `generator/model/rumble_filter.py` | supporting/history |
| `generator/model/rumble_filter_analysis.py` | supporting/history |
| `generator/model/sch101_precision_analysis.py` | supporting/history |
| `generator/model/sch101_precision_candidate.py` | supporting/history |
| `generator/model/signal_chain_analysis.py` | supporting/history |
| `generator/model/signal_chain_noise_dc.py` | supporting/history |
| `generator/procurement/full_bom_census.py` | supporting/history |
| `generator/signal_chain_analysis_A1.py` | supporting/history |
| `generator/writers/kicad9.py` | supporting/history |
| `manifest.json` | supporting/history |
| `payload/balanced_input_builder.py` | supporting/history |
| `scripts/build_populated_review_board.py` | supporting/history |
| `scripts/report_enclosure_decision_baseline.py` | supporting/history |
| `scripts/report_footprint_contract.py` | supporting/history |
| `scripts/report_ghost_placement.py` | supporting/history |
| `scripts/report_real_footprint_audit.py` | supporting/history |
| `tests/test_ae017_dependency_map.py` | supporting/history |
| `tests/test_ae019_design_record_reconcile.py` | supporting/history |
| `tests/test_ae024_design_record_audit.py` | supporting/history |
| `tests/test_ae025_authority_reconciliation.py` | supporting/history |
| `tests/test_ae025a_regression_repair.py` | supporting/history |
| `tests/test_balanced_input.py` | supporting/history |
| `tests/test_board_outline_baseline.py` | supporting/history |
| `tests/test_current_decision_index.py` | supporting/history |
| `tests/test_decision_index_status_audit.py` | supporting/history |
| `tests/test_dr039_full_closure.py` | supporting/history |
| `tests/test_psu_enclosure_freeze.py` | supporting/history |
| `tests/test_psu_release.py` | supporting/history |
| `tests/test_sr039_schematic_to_layout_release.py` | supporting/history |
| `tests/test_sr040_mechanical_bom_placement.py` | supporting/history |
| `tests/test_unicase_fit.py` | supporting/history |
| `tools/ae017_dependency_map.py` | supporting/history |
| `tools/ae019_design_record_reconcile.py` | supporting/history |
| `tools/ae024_design_record_audit.py` | supporting/history |
| `tools/apply_ae021b_atomic_repair.py` | supporting/history |
| `tools/apply_ae021c_population_closure.py` | supporting/history |
| `tools/apply_ae022a_closure.py` | supporting/history |
| `tools/apply_ae022b_routing_closure.py` | supporting/history |
| `tools/apply_ae022c_pin_crossing_closure.py` | supporting/history |
| `tools/apply_ae022d_exact_fix.py` | supporting/history |
| `tools/apply_ae022d_regression.py` | supporting/history |
| `tools/apply_ae022e_named_net_converter.py` | supporting/history |
| `tools/apply_ae022e_regressions.py` | supporting/history |
| `tools/apply_ae022f_symbol_contract.py` | supporting/history |
| `tools/apply_ae022h_final_regression_closure.py` | supporting/history |
| `tools/apply_dr038_definitive_fix.py` | supporting/history |
| `tools/apply_dr038_full_migration.py` | supporting/history |
| `tools/apply_dr039_full_closure.py` | supporting/history |
| `tools/apply_sr039_final_consolidated.py` | supporting/history |
| `tools/apply_sr040.py` | supporting/history |
| `tools/apply_sr041a_mounting_clearance.py` | supporting/history |
| `tools/apply_sr043_native_board.py` | supporting/history |
| `tools/audit_current_decision_index.py` | supporting/history |
| `tools/report_sr040.py` | supporting/history |
| `tools/report_sr041.py` | supporting/history |
| `tools/report_sr042.py` | supporting/history |

## Required production design-pack structure

1. **00 Release authority** — release manifest, version/tag, toolchain pins.
2. **01 Requirements and architecture** — current functional/electrical/mechanical baseline.
3. **02 Decision register** — one authoritative status per decision plus supersession links.
4. **03 Schematics and PCB** — production source and fabrication outputs.
5. **04 BOM and procurement** — controlled BOM, alternates, sourcing policy.
6. **05 Design assurance** — AE/SR evidence, simulations, margins, validation.
7. **06 Commissioning and acceptance** — production tests and measured limits.
8. **07 Maintenance guide** — test points, expected values, service configuration, fault isolation.
9. **08 Build/reproducibility** — clean-clone build instructions and pinned dependencies.
10. **99 Historical evidence** — superseded analyses retained but clearly non-authoritative.
