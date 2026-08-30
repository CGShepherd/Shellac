from pathlib import Path
import shutil

shutil.copyfile("payload/schematic_release_gate.py","generator/layout/schematic_release_gate.py")
Path("config/release").mkdir(parents=True,exist_ok=True)
shutil.copyfile("payload/DR038_SELECTED.md","docs/decisions/DR-038_SCH101_Precision_Architecture_SELECTED.md")
shutil.copyfile("payload/DR039_SELECTED.md","docs/decisions/DR-039_Common_Post_EQ_DC_Block_SELECTED.md")
shutil.copyfile("payload/DR040_SELECTED.md","docs/decisions/DR-040_Precision_CAD_Primitive_Staging_SELECTED.md")

p=Path("config/decisions/current_decision_index.yaml")
t=p.read_text(encoding="utf-8")
t=t.replace(
"baseline:\\n  branch: main\\n  commit: 1ebb04d078aec05e370c0a899607d5e46ad25958\\n  tag: sr-037-signal-chain-revalidation-baseline",
"baseline:\\n  branch: main\\n  commit: dce5c0ec36e12f979338d8c46106c44a79c7a023\\n  tag: sr-038-dr038-dr039-validated-baseline"
)
t=t.replace(
"    implemented_baseline_still:\\n      converter_gain: 4.0\\n      note: Active SCH101 remains the pre-DR038 implementation until atomic CAD migration.",
"    implementation:\\n      converter_gain: 4.0\\n      network: LT5400-7 A-grade\\n      gain_selection: precision service-link population\\n      note: DR-038 is implemented in the active SCH101 generator and validated by SR-039."
)
p.write_text(t,encoding="utf-8")

p=Path("generator/layout/constraints.py")
t=p.read_text(encoding="utf-8")
t=t.replace(
'status="PROVISIONAL — enclosure and board outline not frozen",',
'status="SCHEMATIC RELEASED — provisional placement allowed; final routing/manufacture blocked pending mechanical datum freeze",'
)
t=t.replace(
'status="Provisional until audio enclosure trade study closes.",',
'status="Provisional mechanical keep-in; exact outline/mounting/keep-outs require verified enclosure/carrier datums.",'
)
anchor='        CriticalNet("NET-010", "OUTPUT_[LR]_(POS|NEG)", NetClass.BALANCED_OUTPUT, RoutingPolicy.ASSISTED_REVIEW_REQUIRED, 1, "0VA plane", "Route from output protection directly to the output harness region.", "Maintain pair adjacency and avoid the input region.", "Pair geometry and output-continuity audit."),\\n'
if "NET-011" not in t:
    addition=anchor
    addition+='        CriticalNet("NET-011", "SCH101_[LR]_LT5400_(PLUS_SRC|PLUS_SUM|MINUS_SRC|MINUS_SUM)", NetClass.FEEDBACK, RoutingPolicy.MANUAL_ONLY, 0, "continuous 0VA plane", "Keep each LT5400 network immediately adjacent to its OPA1656 converter and associated precision gain legs.", "Short direct routes only; no control/power crossing through the summing region; preserve left/right symmetry.", "LT5400 locality, via-count and return-path audit."),\\n'
    addition+='        CriticalNet("NET-012", "PRE_EQ_[LR]", NetClass.FEEDBACK, RoutingPolicy.MANUAL_ONLY, 0, "continuous 0VA plane", "Keep the LT5400 feedback/output node local to the differential converter before SCH103 hand-off.", "No unrelated branch or via in the local feedback/output connection.", "Feedback locality and net-continuity audit."),\\n'
    addition+='        CriticalNet("NET-013", "POST_EQ_[LR]", NetClass.ANALOG, RoutingPolicy.MANUAL_ONLY, 0, "local 0VA return", "Place the DR-039 1u film capacitor and 330k bias resistor at the SCH103 recovery output / SCH107 hand-off.", "Keep raw-EQ to capacitor and capacitor to POST_EQ paths short; bias return directly to quiet 0VA.", "DC-block locality and continuity audit."),\\n'
    if anchor not in t:
        raise SystemExit("Could not find NET-010 anchor")
    t=t.replace(anchor,addition,1)
p.write_text(t,encoding="utf-8")
print("SR-039 release-gate migration applied.")
