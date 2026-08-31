# AE-024 Generated Design Record Reconciliation Audit

Repository: `C:\Users\chris\Dropbox\000_Projects\000_Audio\Shellac`

## Executive summary

- files containing decision/status references: **263**
- decision/status claim lines: **1032**
- baseline declaration lines: **221**
- status-vocabulary findings: **2**
- potential authoritative-status contradictions: **26**

This is an audit report, not an automatic rewrite instruction.

## Status-vocabulary findings

- status vocabulary mismatch: decision_status.yaml=['DEFERRED', 'FROZEN', 'PROPOSED', 'REJECTED', 'SELECTED', 'SUPERSEDED'] vs current_decision_index.yaml=['CURRENT_IMPLEMENTED', 'CURRENT_SELECTED_PENDING_IMPLEMENTATION', 'HISTORICAL', 'REJECTED', 'SUPERSEDED']
- current decision index uses statuses forbidden by decision_status.yaml: ['CURRENT_IMPLEMENTED']

## Potential status contradictions

- DR-038: authoritative=CURRENT_IMPLEMENTED, docs/AE-016A_AE016_Regression_Repair_Rev_A0.md:12 claims SELECTED
- DR-038: authoritative=CURRENT_IMPLEMENTED, docs/AE-019_Generated_Design_Record_Reconciliation.md:21 claims PROPOSED,SELECTED
- DR-038: authoritative=CURRENT_IMPLEMENTED, docs/AE-019_Generated_Design_Record_Reconciliation.md:23 claims SELECTED
- DR-038: authoritative=CURRENT_IMPLEMENTED, docs/AE-019_Generated_Design_Record_Reconciliation.md:24 claims SELECTED
- DR-038: authoritative=CURRENT_IMPLEMENTED, docs/AE-019_Generated_Design_Record_Reconciliation.md:27 claims PROPOSED,SELECTED
- DR-038: authoritative=CURRENT_IMPLEMENTED, docs/AE-019_Generated_Design_Record_Reconciliation.md:33 claims PROPOSED,SELECTED
- DR-038: authoritative=CURRENT_IMPLEMENTED, docs/AE-019_Generated_Design_Record_Reconciliation.md:34 claims SELECTED
- DR-038: authoritative=CURRENT_IMPLEMENTED, docs/AE-019_Generated_Design_Record_Reconciliation.md:37 claims SELECTED
- DR-038: authoritative=CURRENT_IMPLEMENTED, docs/AE-019_Generated_Design_Record_Reconciliation.md:45 claims SELECTED
- DR-038: authoritative=CURRENT_IMPLEMENTED, docs/AE-019_Generated_Design_Record_Reconciliation.md:47 claims SELECTED
- DR-038: authoritative=CURRENT_IMPLEMENTED, docs/AE-020_Decision_Register_Reconciliation_and_Design_Pack_Structure_Rev_A0.md:26 claims CURRENT_SELECTED_PENDING_IMPLEMENTATION
- DR-038: authoritative=CURRENT_IMPLEMENTED, tools/apply_dr038_full_migration.py:61 claims SELECTED
- DR-039: authoritative=CURRENT_IMPLEMENTED, docs/AE-017_Generated_Atomic_Migration_Dependency_Map.md:345 claims SELECTED
- DR-039: authoritative=CURRENT_IMPLEMENTED, docs/AE-019_Generated_Design_Record_Reconciliation.md:23 claims SELECTED
- DR-039: authoritative=CURRENT_IMPLEMENTED, docs/AE-019_Generated_Design_Record_Reconciliation.md:24 claims SELECTED
- DR-039: authoritative=CURRENT_IMPLEMENTED, docs/AE-019_Generated_Design_Record_Reconciliation.md:27 claims PROPOSED,SELECTED
- DR-039: authoritative=CURRENT_IMPLEMENTED, docs/AE-019_Generated_Design_Record_Reconciliation.md:35 claims PROPOSED
- DR-039: authoritative=CURRENT_IMPLEMENTED, docs/AE-019_Generated_Design_Record_Reconciliation.md:36 claims SELECTED
- DR-039: authoritative=CURRENT_IMPLEMENTED, docs/AE-019_Generated_Design_Record_Reconciliation.md:45 claims SELECTED
- DR-039: authoritative=CURRENT_IMPLEMENTED, docs/AE-019_Generated_Design_Record_Reconciliation.md:46 claims SELECTED
- DR-039: authoritative=CURRENT_IMPLEMENTED, docs/AE-019_Generated_Design_Record_Reconciliation.md:47 claims SELECTED
- DR-039: authoritative=CURRENT_IMPLEMENTED, docs/AE-020_Decision_Register_Reconciliation_and_Design_Pack_Structure_Rev_A0.md:27 claims CURRENT_SELECTED_PENDING_IMPLEMENTATION
- DR-039: authoritative=CURRENT_IMPLEMENTED, tools/apply_dr039_full_closure.py:89 claims CURRENT_SELECTED_PENDING_IMPLEMENTATION
- DR-039: authoritative=CURRENT_IMPLEMENTED, docs/updates/AE016B_UPDATE_MANIFEST.md:8 claims SELECTED
- DR-040: authoritative=CURRENT_IMPLEMENTED, docs/AE-019_Generated_Design_Record_Reconciliation.md:37 claims SELECTED
- DR-040: authoritative=CURRENT_IMPLEMENTED, docs/AE-020_Decision_Register_Reconciliation_and_Design_Pack_Structure_Rev_A0.md:28 claims CURRENT_SELECTED_PENDING_IMPLEMENTATION

## Authoritative decision index

| ID | Status | Primary record |
|---|---|---|
| DR-037 | CURRENT_IMPLEMENTED | `docs/DR-037_Restore_Legacy_Complete_RIAA_Architecture_Rev_A0.md` |
| DR-038 | CURRENT_IMPLEMENTED | `docs/decisions/DR-038_SCH101_Precision_Architecture_SELECTED.md` |
| DR-039 | CURRENT_IMPLEMENTED | `docs/decisions/DR-039_Common_Post_EQ_DC_Block_SELECTED.md` |
| DR-040 | CURRENT_IMPLEMENTED | `docs/decisions/DR-040_Precision_CAD_Primitive_Staging_SELECTED.md` |

## Baseline declarations requiring reconciliation

- `APPLY_DECISION_INDEX_RECONCILIATION.py:22` — print("Updated authoritative decision index to the validated DR-038/DR-039 baseline.")
- `manifest.json:5` — "baseline": "sr-027-component-selection-policy / 31809c1",
- `README.md:5` — ## Current controlled baseline
- `README.md:6` — - Release baseline: **SR-034 / G3-023**
- `README.md:16` — Existing report scripts remain authoritative for their respective engineering gates. For the mechanical baseline run `python scripts/report_mechanical_baseline.py`.
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
- `tools/ae024_design_record_audit.py:226` — return "authoritative machine-readable baseline"
- `tools/ae024_design_record_audit.py:256` — f"- baseline declaration lines: **{len(baselines)}**",
- `tools/ae024_design_record_audit.py:274` — lines += ["", "## Baseline declarations requiring reconciliation", ""]
- `tools/ae024_design_record_audit.py:294` — "2. **01 Requirements and architecture** — current functional/electrical/mechanical baseline.",
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
- `docs/design_pack/AE-024_Project_Wide_Design_Record_Reconciliation_Audit_Rev_A0.md:24` — baseline despite substantial later controlled work.
- `docs/design_pack/AE-024_Project_Wide_Design_Record_Reconciliation_Audit_Rev_A0.md:40` — - baseline declarations;
- `docs/design_pack/AE-024_Project_Wide_Design_Record_Reconciliation_Audit_Rev_A0.md:64` — authoritative baseline before we start reconciliation edits.
- `docs/knowledge/DECISION_REGISTER.md:3` — **Baseline:** SR-036 knowledge reconciliation
- `docs/knowledge/DECISION_REGISTER.md:40` — \| DEC-032 \| Foundry FDR-001 is the controlled engineering-governance baseline for evidence, decisions, conflicts and manufacturing release \| SELECTED \| G3_025 \| Git remains au
- `docs/knowledge/DECISION_REGISTER.md:54` — \| DEC-046 \| shellac_bom.yaml remains a controlled partial baseline, not procurement-complete BOM \| SELECTED \| G3_027_REPOSITORY_AUDIT \| Full schematic-derived inventory requir
- `docs/knowledge/DECISION_REGISTER.md:73` — SR-035 incorrectly described Lorlin as the saved prior BOM baseline. Surviving BOM evidence
- `docs/knowledge/DESIGN_PACK_INDEX.md:3` — **Authority:** `main` plus the baseline commit/tag identified in `config/decisions/current_decision_index.yaml`.
- `docs/knowledge/DESIGN_PACK_INDEX.md:5` — This index defines how the repository should be read. Historical documents remain valuable evidence, but the current design is determined by the authoritative decision index and im
- `docs/knowledge/DESIGN_PACK_INDEX.md:7` — ## 1. Current design baseline
- `docs/knowledge/DESIGN_PACK_INDEX.md:15` — - release/baseline tag
- `docs/knowledge/DESIGN_PACK_INDEX.md:56` — - final commissioning limits from the implemented baseline
- `docs/knowledge/DESIGN_RULES.md:3` — **Status:** CONTROLLED BASELINE
- `docs/knowledge/DESIGN_TENETS.md:3` — **Status:** CONTROLLED BASELINE
- `docs/knowledge/PROJECT_STATUS.md:3` — **Knowledge baseline:** SR-036 + Foundry FDR-001
- `docs/knowledge/RECOVERED_BASELINE.md:1` — # Project Shellac — Recovered Architecture & Component Baseline
- `docs/knowledge/RECOVERED_BASELINE.md:4` — **Status:** CONTROLLED RECONCILIATION BASELINE
- `docs/knowledge/RECOVERED_BASELINE.md:31` — Surviving interim BOMs recorded three Grayhill 71-series rotaries, including a 4P4T Mode switch, historically budgeted around £28 each. Later project work questioned that premium u
- `docs/knowledge/RECOVERED_BASELINE.md:38` — ## Mechanical baseline
- `docs/knowledge/RISK_REGISTER.md:17` — \| R-013 \| Engineering method/decision hierarchy existed only implicitly across knowledge files and conversation \| RESOLVED \| FDR-001 Foundry baseline added under configuration 
- `docs/maintenance/MAINTENANCE_GUIDE_SKELETON.md:3` — **Status:** STRUCTURE ONLY — populate from implemented, verified baseline.
- `docs/maintenance/MAINTENANCE_GUIDE_SKELETON.md:6` — Product/revision, PCB revision, firmware/generator baseline if applicable, serial/build record.
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
| `docs/design_pack/AE-024_Project_Wide_Design_Record_Reconciliation_Audit_Rev_A0.md` | design assurance evidence |
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
