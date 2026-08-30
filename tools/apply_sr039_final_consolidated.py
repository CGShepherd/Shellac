from pathlib import Path
import shutil

EXPECTED_SNAPSHOT = "b393aec8c09dbefb3b781902e747d7ddbde148ce"

print(f"Applying consolidated SR-039 closure for snapshot {EXPECTED_SNAPSHOT}")

# ---------------------------------------------------------------------------
# 1. Replace the authoritative decision index with a structurally correct file.
# ---------------------------------------------------------------------------
index_path = Path("config/decisions/current_decision_index.yaml")
index_text = """schema_version: 1
project: Shellac
authority: This file is the authoritative current decision-status index. Narrative records remain evidence/history.
baseline:
  branch: main
  commit: dce5c0ec36e12f979338d8c46106c44a79c7a023
  tag: sr-038-dr038-dr039-validated-baseline
status_vocabulary:
  - CURRENT_IMPLEMENTED
  - CURRENT_SELECTED_PENDING_IMPLEMENTATION
  - SUPERSEDED
  - REJECTED
  - HISTORICAL
decisions:
  DR-037:
    title: Restore legacy complete-RIAA architecture
    status: CURRENT_IMPLEMENTED
    primary_record: docs/DR-037_Restore_Legacy_Complete_RIAA_Architecture_Rev_A0.md
    evidence:
      - docs/AE-011_End_to_End_Signal_Chain_Closure_Rev_A1.md
      - docs/AE-012_All_State_Gain_Headroom_Closure_Rev_A0.md
    implementation: Legacy TRUE-RIAA 3180/318 us bass branch plus 2121 Hz treble; independent 3180 us stage removed.
    supersedes:
      - G3-025 optional-3180 active architecture
      - G3-026 optional-3180 implementation
      - G3-027 resynthesis requirement
  DR-038:
    title: SCH101 precision architecture
    status: CURRENT_IMPLEMENTED
    primary_record: docs/decisions/DR-038_SCH101_Precision_Architecture_SELECTED.md
    proposal_record: docs/decisions/DR-038_SCH101_Precision_Architecture_PROPOSED.md
    evidence:
      - docs/AE-013_SCH101_Noise_CMRR_Review_Rev_A0.md
      - docs/AE-014_SCH101_Precision_Architecture_Downselect_Rev_A0.md
      - docs/AE-018_Live_Dependency_Disposition_and_Precision_CAD_Primitives_Rev_A0.md
    implementation:
      converter_gain: 4.0
      network: LT5400-7 A-grade
      gain_selection: precision service-link population
      note: DR-038 is implemented in the active SCH101 generator and validated by SR-039.
  DR-039:
    title: Common post-EQ DC block
    status: CURRENT_IMPLEMENTED
    primary_record: docs/decisions/DR-039_Common_Post_EQ_DC_Block_SELECTED.md
    proposal_record: docs/decisions/DR-039_Common_Post_EQ_DC_Block_PROPOSED.md
    evidence:
      - docs/AE-015_Full_Chain_Noise_DC_Review_Rev_A0.md
      - docs/AE-018_Live_Dependency_Disposition_and_Precision_CAD_Primitives_Rev_A0.md
    implementation: SCH103 includes 1uF film / 330k DC block before SCH107 FILTER/BYPASS.
  DR-040:
    title: Precision CAD primitive staging rule
    status: CURRENT_IMPLEMENTED
    primary_record: docs/decisions/DR-040_Precision_CAD_Primitive_Staging_SELECTED.md
    evidence:
      - docs/AE-017_Atomic_Migration_Dependency_Mapping_Gate_Rev_A0.md
      - docs/AE-018_Live_Dependency_Disposition_and_Precision_CAD_Primitives_Rev_A0.md
historical_implementation_events:
  AE-016:
    disposition: SUPERSEDED
    reason: Premature DR-038/DR-039 implementation caused regression failures.
    superseded_by:
      - AE-016A
      - AE-016B
  AE-016A:
    disposition: HISTORICAL
    reason: First regression repair; restored active SCH101 baseline.
  AE-016B:
    disposition: CURRENT_IMPLEMENTATION_STAGING_EVIDENCE
    reason: Restored SCH103 baseline and established atomic migration boundary.
"""
index_path.write_text(index_text, encoding="utf-8")
print("1/5 decision index replaced with valid DR-038 nesting.")

# ---------------------------------------------------------------------------
# 2. Complete the intended SR-039 layout-constraint migration.
# ---------------------------------------------------------------------------
constraints_path = Path("generator/layout/constraints.py")
text = constraints_path.read_text(encoding="utf-8")

text = text.replace(
    'status="PROVISIONAL — enclosure and board outline not frozen",',
    'status="SCHEMATIC RELEASED — provisional placement allowed; final routing/manufacture blocked pending mechanical datum freeze",'
)
text = text.replace(
    'status="Provisional until audio enclosure trade study closes.",',
    'status="Provisional mechanical keep-in; exact outline/mounting/keep-outs require verified enclosure/carrier datums.",'
)

if 'CriticalNet("NET-011"' not in text:
    marker = '        CriticalNet("NET-010", "OUTPUT_[LR]_(POS|NEG)", NetClass.BALANCED_OUTPUT, RoutingPolicy.ASSISTED_REVIEW_REQUIRED, 1, "0VA plane", "Route from output protection directly to the output harness region.", "Maintain pair adjacency and avoid the input region.", "Pair geometry and output-continuity audit."),\n'
    if marker not in text:
        raise SystemExit("SR-039 FINAL: exact NET-010 insertion point not found; refusing partial modification.")
    additions = marker + (
        '        CriticalNet("NET-011", "SCH101_[LR]_LT5400_(PLUS_SRC|PLUS_SUM|MINUS_SRC|MINUS_SUM)", NetClass.FEEDBACK, RoutingPolicy.MANUAL_ONLY, 0, "continuous 0VA plane", "Keep each LT5400 network immediately adjacent to its OPA1656 converter and associated precision gain legs.", "Short direct routes only; no control/power crossing through the summing region; preserve left/right symmetry.", "LT5400 locality, via-count and return-path audit."),\n'
        '        CriticalNet("NET-012", "PRE_EQ_[LR]", NetClass.FEEDBACK, RoutingPolicy.MANUAL_ONLY, 0, "continuous 0VA plane", "Keep the LT5400 feedback/output node local to the differential converter before SCH103 hand-off.", "No unrelated branch or via in the local feedback/output connection.", "Feedback locality and net-continuity audit."),\n'
        '        CriticalNet("NET-013", "POST_EQ_[LR]", NetClass.ANALOG, RoutingPolicy.MANUAL_ONLY, 0, "local 0VA return", "Place the DR-039 1u film capacitor and 330k bias resistor at the SCH103 recovery output / SCH107 hand-off.", "Keep raw-EQ to capacitor and capacitor to POST_EQ paths short; bias return directly to quiet 0VA.", "DC-block locality and continuity audit."),\n'
    )
    text = text.replace(marker, additions, 1)

constraints_path.write_text(text, encoding="utf-8")
print("2/5 layout constraints completed, including NET-011..NET-013.")

# ---------------------------------------------------------------------------
# 3. Replace brittle decision-index regression with exact semantic checks.
# ---------------------------------------------------------------------------
test_index = """from pathlib import Path
import re

INDEX = Path("config/decisions/current_decision_index.yaml")

def _text():
    return INDEX.read_text(encoding="utf-8")

def _decision_block(decision_id, next_id=None):
    text = _text()
    start = f"  {decision_id}:"
    assert start in text, f"Missing decision {decision_id}"
    block = text.split(start, 1)[1]
    if next_id is not None:
        block = block.split(f"  {next_id}:", 1)[0]
    elif "historical_implementation_events:" in block:
        block = block.split("historical_implementation_events:", 1)[0]
    return block

def _decision_status(decision_id, next_id=None):
    block = _decision_block(decision_id, next_id)
    m = re.search(r"(?m)^    status:\\s*([^\\n]+)$", block)
    assert m, f"Missing status for {decision_id}"
    return m.group(1).strip()

def test_authoritative_decision_index_is_well_formed():
    text = _text()
    assert re.search(r"(?m)^  branch:\\s*main\\s*$", text)
    assert "commit: dce5c0ec36e12f979338d8c46106c44a79c7a023" in text
    assert _decision_status("DR-037", "DR-038") == "CURRENT_IMPLEMENTED"
    assert _decision_status("DR-038", "DR-039") == "CURRENT_IMPLEMENTED"
    assert _decision_status("DR-039", "DR-040") == "CURRENT_IMPLEMENTED"
    assert _decision_status("DR-040") == "CURRENT_IMPLEMENTED"

def test_dr038_dr039_are_claimed_as_implemented():
    dr038 = _decision_block("DR-038", "DR-039")
    assert "    implementation:" in dr038
    assert "      converter_gain: 4.0" in dr038
    assert "      network: LT5400-7 A-grade" in dr038
    assert "      gain_selection: precision service-link population" in dr038
    assert "pre-DR038 implementation" not in dr038

    dr039 = _decision_block("DR-039", "DR-040")
    assert "status: CURRENT_IMPLEMENTED" in dr039
    assert "SCH103 includes 1uF film / 330k DC block" in dr039

def test_design_pack_and_maintenance_structure_exist():
    assert Path("docs/knowledge/DESIGN_PACK_INDEX.md").exists()
    assert Path("docs/maintenance/MAINTENANCE_GUIDE_SKELETON.md").exists()
"""
Path("tests/test_current_decision_index.py").write_text(test_index, encoding="utf-8")
print("3/5 decision-index tests replaced with structure-aware checks.")

# Strengthen existing SR-039 release test without increasing test count.
sr_test = Path("tests/test_sr039_schematic_to_layout_release.py")
sr = sr_test.read_text(encoding="utf-8")
needle = '    assert gate.disposition.manufacturing_release.startswith("BLOCKED")\n'
addition = needle + (
    '    from generator.layout.constraints import build_layout_baseline\n'
    '    critical_ids={item.identifier for item in build_layout_baseline().critical_nets}\n'
    '    assert {"NET-011","NET-012","NET-013"} <= critical_ids\n'
)
if 'assert {"NET-011","NET-012","NET-013"} <= critical_ids' not in sr:
    if needle not in sr:
        raise SystemExit("SR-039 FINAL: release-test insertion point not found.")
    sr = sr.replace(needle, addition, 1)
sr_test.write_text(sr, encoding="utf-8")
print("4/5 SR-039 test now proves layout-critical constraints are installed.")

# ---------------------------------------------------------------------------
# 4. Remove failed patch scaffolding so the repo retains one final state,
#    not a chain of known-broken installers.
# ---------------------------------------------------------------------------
obsolete = [
    "APPLY_SR039.bat",
    "APPLY_SR039A.bat",
    "APPLY_SR039B.bat",
    "APPLY_SR039C.bat",
    "README_CI_FIX.txt",
    "tools/apply_sr039_release_gate.py",
    "tools/apply_sr039a_no_pyyaml.py",
    "tools/apply_sr039b_installer_fix.py",
    "tools/apply_sr039c_decision_test.py",
    "docs/updates/SR039A_UPDATE_MANIFEST.md",
    "docs/updates/SR039B_UPDATE_MANIFEST.md",
    "docs/updates/SR039C_UPDATE_MANIFEST.md",
    "payload/DR038_SELECTED.md",
    "payload/DR039_SELECTED.md",
    "payload/DR040_SELECTED.md",
    "payload/schematic_release_gate.py",
]
for item in obsolete:
    path = Path(item)
    if path.exists():
        path.unlink()

payload = Path("payload")
if payload.exists() and not any(payload.iterdir()):
    payload.rmdir()

print("5/5 obsolete SR-039 patch scaffolding removed.")
print("Consolidated SR-039 closure applied successfully.")
