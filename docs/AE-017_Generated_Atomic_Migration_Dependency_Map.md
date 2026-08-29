# AE-017 Generated DR-038 / DR-039 Dependency Map

Repository scanned: `C:\Users\chris\Dropbox\000_Projects\000_Audio\Shellac`

## Summary

- matched files: **80**
- matched references: **505**

This report is evidence for an atomic migration. A file appearing here is
not automatically changed; it is a review surface that must be dispositioned.

## SCH101_NUMERIC

| File | Contract class | References |
|---|---|---:|
| `docs/AE-010_SCH101_Gain_Selector_Closure_Rev_A.md` | controlled documentation | 2 |
| `docs/AE-011_End_to_End_Signal_Chain_Closure_Rev_A0.md` | controlled documentation | 1 |
| `docs/AE-013_SCH101_Noise_CMRR_Review_Rev_A0.md` | controlled documentation | 1 |
| `docs/AE-014_SCH101_Precision_Architecture_Downselect_Rev_A0.md` | controlled documentation | 7 |
| `docs/AE-016A_AE016_Regression_Repair_Rev_A0.md` | controlled documentation | 1 |
| `docs/AE-017_Atomic_Migration_Dependency_Mapping_Gate_Rev_A0.md` | controlled documentation | 4 |
| `docs/decisions/DR-038_SCH101_Precision_Architecture_SELECTED.md` | controlled documentation | 1 |
| `generator/blocks/balanced_input.py` | CAD builder | 12 |
| `generator/core/components.py` | CAD infrastructure | 1 |
| `generator/model/balanced_input.py` | electrical/analysis model | 13 |
| `generator/model/sch101_precision_analysis.py` | electrical/analysis model | 4 |
| `generator/model/sch101_precision_candidate.py` | electrical/analysis model | 1 |
| `out/kicad/ProjectShellac_SCH101.kicad_sch` | repository/support | 18 |
| `out/kicad/ProjectShellac_SCH103.kicad_sch` | repository/support | 1 |
| `out/layout/footprint_contract.json` | repository/support | 14 |
| `out/layout/kicad_native_pipeline.json` | repository/support | 14 |
| `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | repository/support | 14 |
| `scripts/report_balanced_input_gain.py` | repository/support | 4 |
| `tests/test_ae017_dependency_map.py` | regression contract | 5 |
| `tests/test_balanced_input.py` | regression contract | 5 |
| `tests/test_balanced_input_gain.py` | regression contract | 3 |
| `tests/test_dr038_dr039.py` | regression contract | 3 |
| `tools/ae017_dependency_map.py` | repository/support | 12 |

## SCH101_CAD

| File | Contract class | References |
|---|---|---:|
| `docs/AE-017_Atomic_Migration_Dependency_Mapping_Gate_Rev_A0.md` | controlled documentation | 4 |
| `docs/SR-006_SCH101_DIP_Switch_Closure_Rev_A.md` | controlled documentation | 1 |
| `generator/blocks/balanced_input.py` | CAD builder | 5 |
| `generator/core/components.py` | CAD infrastructure | 1 |
| `generator/core/pins.py` | CAD infrastructure | 1 |
| `generator/layout/placement_clusters.py` | layout | 4 |
| `generator/writers/kicad9.py` | repository/support | 4 |
| `out/kicad/ProjectShellac.kicad_sym` | repository/support | 2 |
| `out/kicad/ProjectShellac_SCH101.kicad_sch` | repository/support | 20 |
| `out/kicad/ProjectShellac_SCH103.kicad_sch` | repository/support | 2 |
| `out/kicad/ProjectShellac_SCH104.kicad_sch` | repository/support | 2 |
| `out/kicad/ProjectShellac_SCH105.kicad_sch` | repository/support | 2 |
| `out/kicad/ProjectShellac_SCH106.kicad_sch` | repository/support | 2 |
| `out/kicad/ProjectShellac_SCH107.kicad_sch` | repository/support | 2 |
| `out/kicad/ProjectShellac_SCH108.kicad_sch` | repository/support | 2 |
| `out/kicad/ProjectShellac_SCH109.kicad_sch` | repository/support | 2 |
| `out/layout/cluster_placement_baseline.json` | repository/support | 4 |
| `out/layout/detailed_placement_readiness.json` | repository/support | 8 |
| `out/layout/footprint_contract.json` | repository/support | 10 |
| `out/layout/kicad_native_pipeline.json` | repository/support | 5 |
| `out/layout/preliminary_placement_baseline.json` | repository/support | 4 |
| `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | repository/support | 5 |
| `tests/test_ae017_dependency_map.py` | regression contract | 4 |
| `tests/test_balanced_input.py` | regression contract | 7 |
| `tests/test_kicad_writer_instances.py` | regression contract | 2 |
| `tests/test_pin_connectivity.py` | regression contract | 1 |
| `tests/test_root_hierarchy.py` | regression contract | 1 |
| `tools/ae017_dependency_map.py` | repository/support | 8 |

## SCH103_OUTPUT

| File | Contract class | References |
|---|---|---:|
| `APPLY_DR039_PATCH.py` | repository/support | 8 |
| `RESTORE_SCH103_BASELINE.py` | repository/support | 8 |
| `docs/AE-015_Full_Chain_Noise_DC_Review_Rev_A0.md` | controlled documentation | 2 |
| `docs/SR-004_SCH107_Pin_Aware_Conversion_Rev_A.md` | controlled documentation | 1 |
| `docs/SR-021_SCH107_Human_Reviewable_Conversion_Rev_A.md` | controlled documentation | 1 |
| `docs/SR-024_SCH103_Human_Reviewable_Rev_A.md` | controlled documentation | 1 |
| `docs/updates/AE016B_UPDATE_MANIFEST.md` | controlled documentation | 1 |
| `docs/updates/AE016_UPDATE_MANIFEST.md` | controlled documentation | 1 |
| `generator/blocks/replay_eq.py` | CAD builder | 6 |
| `generator/blocks/rumble_filter.py` | CAD builder | 2 |
| `generator/commissioning/model.py` | repository/support | 4 |
| `generator/model/shellac.py` | electrical/analysis model | 6 |
| `manifest.json` | repository/support | 1 |
| `out/commissioning/commissioning_baseline.json` | repository/support | 4 |
| `out/kicad/ProjectShellac.kicad_sch` | repository/support | 8 |
| `out/kicad/ProjectShellac_SCH103.kicad_sch` | repository/support | 8 |
| `out/kicad/ProjectShellac_SCH107.kicad_sch` | repository/support | 2 |
| `out/layout/footprint_contract.json` | repository/support | 6 |
| `out/layout/kicad_native_pipeline.json` | repository/support | 6 |
| `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | repository/support | 6 |
| `tests/test_pin_connectivity.py` | regression contract | 2 |
| `tests/test_sch103_human_readable.py` | regression contract | 1 |
| `tests/test_sch107_human_readable.py` | regression contract | 1 |
| `tools/ae017_dependency_map.py` | repository/support | 5 |

## DR039

| File | Contract class | References |
|---|---|---:|
| `APPLY_DR039_PATCH.py` | repository/support | 8 |
| `APPLY_SIGNAL_CHAIN_PATCH.py` | repository/support | 3 |
| `REPAIR_SIGNAL_CHAIN.py` | repository/support | 1 |
| `RESTORE_SCH103_BASELINE.py` | repository/support | 5 |
| `docs/AE-015_Full_Chain_Noise_DC_Review_Rev_A0.md` | controlled documentation | 7 |
| `docs/AE-016A_AE016_Regression_Repair_Rev_A0.md` | controlled documentation | 2 |
| `docs/AE-016B_Full_Regression_Staging_Repair_Rev_A0.md` | controlled documentation | 2 |
| `docs/AE-016_DR038_DR039_Implementation_Baseline_Rev_A0.md` | controlled documentation | 4 |
| `docs/AE-017_Atomic_Migration_Dependency_Mapping_Gate_Rev_A0.md` | controlled documentation | 3 |
| `docs/decisions/DR-039_Common_Post_EQ_DC_Block_PROPOSED.md` | controlled documentation | 3 |
| `docs/decisions/DR-039_Common_Post_EQ_DC_Block_SELECTED.md` | controlled documentation | 4 |
| `docs/updates/AE015_UPDATE_MANIFEST.md` | controlled documentation | 1 |
| `docs/updates/AE016A_UPDATE_MANIFEST.md` | controlled documentation | 2 |
| `docs/updates/AE016B_UPDATE_MANIFEST.md` | controlled documentation | 2 |
| `docs/updates/AE016_UPDATE_MANIFEST.md` | controlled documentation | 3 |
| `docs/updates/AE017_UPDATE_MANIFEST.md` | controlled documentation | 1 |
| `generator/blocks/power_entry.py` | CAD builder | 4 |
| `generator/model/post_eq_dc_block.py` | electrical/analysis model | 2 |
| `generator/model/signal_chain_noise_dc.py` | electrical/analysis model | 2 |
| `out/kicad/ProjectShellac_SCH106.kicad_sch` | repository/support | 2 |
| `out/layout/footprint_contract.json` | repository/support | 2 |
| `out/layout/kicad_native_pipeline.json` | repository/support | 2 |
| `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | repository/support | 2 |
| `tests/test_ae017_dependency_map.py` | regression contract | 1 |
| `tests/test_dr038_dr039.py` | regression contract | 2 |
| `tests/test_signal_chain_noise_dc.py` | regression contract | 1 |
| `tools/ae017_dependency_map.py` | repository/support | 10 |

## ANALYSIS

| File | Contract class | References |
|---|---|---:|
| `APPLY_SIGNAL_CHAIN_PATCH.py` | repository/support | 2 |
| `REPAIR_SIGNAL_CHAIN.py` | repository/support | 2 |
| `docs/AE-012_All_State_Gain_Headroom_Closure_Rev_A0.md` | controlled documentation | 2 |
| `docs/AE-013_SCH101_Noise_CMRR_Review_Rev_A0.md` | controlled documentation | 5 |
| `docs/AE-014_SCH101_Precision_Architecture_Downselect_Rev_A0.md` | controlled documentation | 10 |
| `docs/AE-015_Full_Chain_Noise_DC_Review_Rev_A0.md` | controlled documentation | 4 |
| `docs/AE-016A_AE016_Regression_Repair_Rev_A0.md` | controlled documentation | 2 |
| `docs/decisions/DR-038_SCH101_Precision_Architecture_PROPOSED.md` | controlled documentation | 4 |
| `docs/decisions/DR-038_SCH101_Precision_Architecture_SELECTED.md` | controlled documentation | 1 |
| `docs/decisions/DR-039_Common_Post_EQ_DC_Block_PROPOSED.md` | controlled documentation | 1 |
| `docs/updates/AE012_UPDATE_MANIFEST.md` | controlled documentation | 4 |
| `docs/updates/AE013_UPDATE_MANIFEST.md` | controlled documentation | 4 |
| `docs/updates/AE014_UPDATE_MANIFEST.md` | controlled documentation | 4 |
| `docs/updates/AE015_UPDATE_MANIFEST.md` | controlled documentation | 4 |
| `docs/updates/AE016A_UPDATE_MANIFEST.md` | controlled documentation | 2 |
| `docs/updates/AE016B_UPDATE_MANIFEST.md` | controlled documentation | 1 |
| `docs/updates/AE016_UPDATE_MANIFEST.md` | controlled documentation | 1 |
| `docs/updates/DR037_UPDATE_MANIFEST.md` | controlled documentation | 2 |
| `generator/model/sch101_precision_analysis.py` | electrical/analysis model | 1 |
| `generator/model/sch101_precision_candidate.py` | electrical/analysis model | 1 |
| `generator/model/signal_chain_analysis.py` | electrical/analysis model | 1 |
| `generator/model/signal_chain_noise_dc.py` | electrical/analysis model | 2 |
| `tests/test_dr038_dr039.py` | regression contract | 1 |
| `tests/test_sch101_precision_analysis.py` | regression contract | 1 |
| `tests/test_sch101_precision_candidate.py` | regression contract | 1 |
| `tests/test_signal_chain_analysis.py` | regression contract | 1 |
| `tests/test_signal_chain_noise_dc.py` | regression contract | 1 |
| `tools/ae017_dependency_map.py` | repository/support | 12 |

## Atomic migration gates

### DR-038 / SCH101

The migration is not complete until all of these move together:

1. electrical constants and gain settings;
2. physical LT5400-7 component/symbol/footprint representation;
3. removal/replacement of the ordinary DIP gain selector;
4. precision service-link implementation;
5. SCH101 builder values and annotations;
6. component/BOM/procurement records;
7. numeric gain regressions;
8. rendered-CAD/refdes regressions;
9. AE-012 headroom regression;
10. AE-013/014 noise/CMRR regression.

### DR-039 / SCH103

The migration is not complete until all of these move together:

1. post-EQ DC-block electrical model;
2. SCH103 output builder and test-point allocation;
3. physical film-capacitor selection/footprint;
4. PCB placement allowance;
5. component-count/refdes contracts;
6. replay-curve regression including the ~0.48 Hz pole;
7. AE-012 headroom update;
8. AE-015 DC/noise update;
9. rumble bypass/filter switching transient tests;
10. power-up/power-down transient acceptance.

## Detailed hits

| Category | Token | File | Line | Context |
|---|---|---|---:|---|
| SCH103_OUTPUT | `replay_eq.py` | `APPLY_DR039_PATCH.py` | 2 | path=Path("generator/blocks/replay_eq.py") |
| DR039 | `DR-039` | `APPLY_DR039_PATCH.py` | 4 | if "DR-039 common post-EQ DC block" in text: |
| DR039 | `DR-039` | `APPLY_DR039_PATCH.py` | 5 | print("replay_eq.py already contains DR-039; no change.") |
| SCH103_OUTPUT | `replay_eq.py` | `APPLY_DR039_PATCH.py` | 5 | print("replay_eq.py already contains DR-039; no change.") |
| SCH103_OUTPUT | `output_end = Point(420` | `APPLY_DR039_PATCH.py` | 7 | old = '''    output_end = Point(420, u2_out.y) |
| SCH103_OUTPUT | `TP{base}4` | `APPLY_DR039_PATCH.py` | 9 | f"TP{base}4", f"{channel}_EQ_OUT", Point(395, u2_out.y + 5.08) |
| SCH103_OUTPUT | `_EQ_OUT` | `APPLY_DR039_PATCH.py` | 9 | f"TP{base}4", f"{channel}_EQ_OUT", Point(395, u2_out.y + 5.08) |
| DR039 | `DR-039` | `APPLY_DR039_PATCH.py` | 15 | new = '''    # DR-039 common post-EQ DC block before the SCH107 filter/bypass split. |
| SCH103_OUTPUT | `TP{base}4` | `APPLY_DR039_PATCH.py` | 17 | f"TP{base}4", f"{channel}_EQ_RAW", Point(395, u2_out.y + 5.08) |
| DR039 | `1u` | `APPLY_DR039_PATCH.py` | 20 | f"C{base}60", "1u", Point(425, u2_out.y), |
| DR039 | `DR-039` | `APPLY_DR039_PATCH.py` | 22 | function="DR-039 common post-EQ DC block", |
| DR039 | `330k` | `APPLY_DR039_PATCH.py` | 27 | f"R{base}60", "330k", Point(455, u2_out.y + 15), |
| DR039 | `DR-039` | `APPLY_DR039_PATCH.py` | 28 | tolerance="1%", function="DR-039 downstream DC reference" |
| SCH103_OUTPUT | `_EQ_OUT` | `APPLY_DR039_PATCH.py` | 31 | f"TP{base}5", f"{channel}_EQ_OUT", Point(455, u2_out.y + 5.08) |
| DR039 | `DR-039` | `APPLY_DR039_PATCH.py` | 43 | print("Patched replay_eq.py for DR-039") |
| SCH103_OUTPUT | `replay_eq.py` | `APPLY_DR039_PATCH.py` | 43 | print("Patched replay_eq.py for DR-039") |
| ANALYSIS | `signal_chain_analysis` | `APPLY_SIGNAL_CHAIN_PATCH.py` | 2 | p=Path("generator/model/signal_chain_analysis.py") |
| DR039 | `post_eq_dc_block` | `APPLY_SIGNAL_CHAIN_PATCH.py` | 4 | if "post_eq_dc_block" not in t: |
| DR039 | `post_eq_dc_block` | `APPLY_SIGNAL_CHAIN_PATCH.py` | 7 | "from .output_driver import DIFFERENTIAL_GAIN_LINEAR, DESIGN_OUTPUT_RMS_V\nfrom .post_eq_dc_block import magnitude as post_eq_dc_magnitude" |
| ANALYSIS | `signal_chain_analysis` | `APPLY_SIGNAL_CHAIN_PATCH.py` | 14 | print("Patched signal_chain_analysis.py for DR-039") |
| DR039 | `DR-039` | `APPLY_SIGNAL_CHAIN_PATCH.py` | 14 | print("Patched signal_chain_analysis.py for DR-039") |
| ANALYSIS | `signal_chain_analysis` | `REPAIR_SIGNAL_CHAIN.py` | 2 | p = Path("generator/model/signal_chain_analysis.py") |
| DR039 | `post_eq_dc_block` | `REPAIR_SIGNAL_CHAIN.py` | 4 | t = t.replace("\nfrom .post_eq_dc_block import magnitude as post_eq_dc_magnitude", "") |
| ANALYSIS | `AE-012` | `REPAIR_SIGNAL_CHAIN.py` | 10 | print("AE-012 signal-chain model is at its pre-DR039 controlled baseline.") |
| SCH103_OUTPUT | `replay_eq.py` | `RESTORE_SCH103_BASELINE.py` | 3 | path = Path("generator/blocks/replay_eq.py") |
| DR039 | `DR-039` | `RESTORE_SCH103_BASELINE.py` | 6 | dr039 = '''    # DR-039 common post-EQ DC block before the SCH107 filter/bypass split. |
| SCH103_OUTPUT | `TP{base}4` | `RESTORE_SCH103_BASELINE.py` | 8 | f"TP{base}4", f"{channel}_EQ_RAW", Point(395, u2_out.y + 5.08) |
| DR039 | `1u` | `RESTORE_SCH103_BASELINE.py` | 11 | f"C{base}60", "1u", Point(425, u2_out.y), |
| DR039 | `DR-039` | `RESTORE_SCH103_BASELINE.py` | 13 | function="DR-039 common post-EQ DC block", |
| DR039 | `330k` | `RESTORE_SCH103_BASELINE.py` | 18 | f"R{base}60", "330k", Point(455, u2_out.y + 15), |
| DR039 | `DR-039` | `RESTORE_SCH103_BASELINE.py` | 19 | tolerance="1%", function="DR-039 downstream DC reference" |
| SCH103_OUTPUT | `_EQ_OUT` | `RESTORE_SCH103_BASELINE.py` | 22 | f"TP{base}5", f"{channel}_EQ_OUT", Point(455, u2_out.y + 5.08) |
| SCH103_OUTPUT | `output_end = Point(420` | `RESTORE_SCH103_BASELINE.py` | 32 | baseline = '''    output_end = Point(420, u2_out.y) |
| SCH103_OUTPUT | `TP{base}4` | `RESTORE_SCH103_BASELINE.py` | 34 | f"TP{base}4", f"{channel}_EQ_OUT", Point(395, u2_out.y + 5.08) |
| SCH103_OUTPUT | `_EQ_OUT` | `RESTORE_SCH103_BASELINE.py` | 34 | f"TP{base}4", f"{channel}_EQ_OUT", Point(395, u2_out.y + 5.08) |
| SCH103_OUTPUT | `replay_eq.py` | `RESTORE_SCH103_BASELINE.py` | 44 | print("Restored replay_eq.py to pre-DR039 physical generator baseline.") |
| SCH103_OUTPUT | `replay_eq.py` | `RESTORE_SCH103_BASELINE.py` | 46 | print("replay_eq.py already at pre-DR039 physical baseline.") |
| SCH101_NUMERIC | `3.48` | `docs/AE-010_SCH101_Gain_Selector_Closure_Rev_A.md` | 10 | followed by a fixed 3.48× differential converter. That implied 13.92× total |
| SCH101_NUMERIC | `3.48` | `docs/AE-010_SCH101_Gain_Selector_Closure_Rev_A.md` | 23 | 3. fixed 3.48× precision differential converter; |
| SCH101_NUMERIC | `3.48` | `docs/AE-011_End_to_End_Signal_Chain_Closure_Rev_A0.md` | 37 | - fixed 3.48x differential conversion; |
| ANALYSIS | `AE-012` | `docs/AE-012_All_State_Gain_Headroom_Closure_Rev_A0.md` | 1 | # AE-012 — Project Shellac All-State Gain and Headroom Closure |
| ANALYSIS | `AE-012` | `docs/AE-012_All_State_Gain_Headroom_Closure_Rev_A0.md` | 11 | AE-012 performs a dense end-to-end gain/headroom sweep of: |
| ANALYSIS | `AE-013` | `docs/AE-013_SCH101_Noise_CMRR_Review_Rev_A0.md` | 1 | # AE-013 — SCH101 Noise and CMRR Design-Assurance Review |
| ANALYSIS | `AE-012` | `docs/AE-013_SCH101_Noise_CMRR_Review_Rev_A0.md` | 10 | AE-012 closed the end-to-end gain/headroom envelope. The next assurance step was integrated noise and common-mode rejection. |
| SCH101_NUMERIC | `3.48` | `docs/AE-013_SCH101_Noise_CMRR_Review_Rev_A0.md` | 92 | - differential converter: 10 kΩ / 34.8 kΩ -> approximately 1 kΩ / 3.48 kΩ. |
| ANALYSIS | `AE-013` | `docs/AE-013_SCH101_Noise_CMRR_Review_Rev_A0.md` | 109 | A matched thin-film resistor network or networks are likely preferable to eight independent precision resistors, but component down-selection is deliberately no |
| ANALYSIS | `AE-013` | `docs/AE-013_SCH101_Noise_CMRR_Review_Rev_A0.md` | 113 | AE-013 does **not** alter SCH101 component values or footprints. |
| ANALYSIS | `AE-012` | `docs/AE-013_SCH101_Noise_CMRR_Review_Rev_A0.md` | 119 | - AE-012 gain/headroom: remains GREEN. |
| ANALYSIS | `AE-014` | `docs/AE-014_SCH101_Precision_Architecture_Downselect_Rev_A0.md` | 1 | # AE-014 — SCH101 Precision Architecture Down-Selection |
| ANALYSIS | `AE-013` | `docs/AE-014_SCH101_Precision_Architecture_Downselect_Rev_A0.md` | 10 | AE-013 identified two coupled weaknesses in the controlled SCH101 implementation: resistor-network Johnson noise and tolerance-limited CMRR. |
| ANALYSIS | `AE-014` | `docs/AE-014_SCH101_Precision_Architecture_Downselect_Rev_A0.md` | 12 | AE-014 recommends solving both without changing the fundamental balanced-input topology or the established 14/18/22 dB user gain choices. |
| SCH101_NUMERIC | `3.48` | `docs/AE-014_SCH101_Precision_Architecture_Downselect_Rev_A0.md` | 18 | 3. change the differential converter from the non-standard 3.48 ratio to a precision **4.000 ratio**; |
| SCH101_NUMERIC | `3.48` | `docs/AE-014_SCH101_Precision_Architecture_Downselect_Rev_A0.md` | 26 | ## 1. Why 4.00x rather than retaining 3.48x |
| SCH101_NUMERIC | `3.48` | `docs/AE-014_SCH101_Precision_Architecture_Downselect_Rev_A0.md` | 28 | The controlled 3.48x converter uses 10 kΩ / 34.8 kΩ. It is electrically valid but awkward as a high-precision monolithic ratio. |
| ANALYSIS | `AE-014` | `docs/AE-014_SCH101_Precision_Architecture_Downselect_Rev_A0.md` | 86 | **B — practical prototype solution:** individually selected 0.01% thin-film resistors for the 249 Ω / 750 Ω / 1.91 kΩ segments, placed as geometrically and ther |
| SCH101_NUMERIC | `3.48` | `docs/AE-014_SCH101_Precision_Architecture_Downselect_Rev_A0.md` | 90 | ## 5. Alternative considered: preserve 3.48x |
| SCH101_NUMERIC | `3.48` | `docs/AE-014_SCH101_Precision_Architecture_Downselect_Rev_A0.md` | 92 | Retaining 3.48x would minimise mathematical change, but it forces either: |
| SCH101_NUMERIC | `3.48` | `docs/AE-014_SCH101_Precision_Architecture_Downselect_Rev_A0.md` | 100 | **Recommendation: reject the 3.48x converter for the next SCH101 revision.** |
| ANALYSIS | `AE-013` | `docs/AE-014_SCH101_Precision_Architecture_Downselect_Rev_A0.md` | 104 | AE-013 estimated the current DEFAULT front end at roughly 18 nV/√Hz input-referred. |
| ANALYSIS | `AE-014` | `docs/AE-014_SCH101_Precision_Architecture_Downselect_Rev_A0.md` | 106 | The AE-014 candidate is below 9.5 nV/√Hz in the same first-order model. The improvement is approximately 6 dB and comes mainly from lowering the feedback/differ |
| ANALYSIS | `AE-013` | `docs/AE-014_SCH101_Precision_Architecture_Downselect_Rev_A0.md` | 138 | AE-013 found no controlled system CMRR requirement. AE-014 therefore proposes requirements for formal adoption: |
| ANALYSIS | `AE-014` | `docs/AE-014_SCH101_Precision_Architecture_Downselect_Rev_A0.md` | 138 | AE-013 found no controlled system CMRR requirement. AE-014 therefore proposes requirements for formal adoption: |
| SCH101_NUMERIC | `3.48` | `docs/AE-014_SCH101_Precision_Architecture_Downselect_Rev_A0.md` | 153 | - replace 3.48x converter with 4.00x precision converter; |
| ANALYSIS | `AE-012` | `docs/AE-014_SCH101_Precision_Architecture_Downselect_Rev_A0.md` | 170 | 5. rerun AE-012 headroom regression; |
| ANALYSIS | `AE-013` | `docs/AE-014_SCH101_Precision_Architecture_Downselect_Rev_A0.md` | 171 | 6. rerun AE-013/014 noise regression; |
| ANALYSIS | `AE-015` | `docs/AE-015_Full_Chain_Noise_DC_Review_Rev_A0.md` | 1 | # AE-015 — Full-Chain Noise and DC-Offset Review |
| ANALYSIS | `AE-015` | `docs/AE-015_Full_Chain_Noise_DC_Review_Rev_A0.md` | 11 | AE-015 extends the end-to-end review beyond gain/headroom into: |
| SCH103_OUTPUT | `POST_EQ` | `docs/AE-015_Full_Chain_Noise_DC_Review_Rev_A0.md` | 77 | The non-flat SCH103 path can then produce approximately **1.7 V DC at POST_EQ**, and the direct-coupled complete chain can exceed **3 V differential DC at the X |
| DR039 | `1.0 µF` | `docs/AE-015_Full_Chain_Noise_DC_Review_Rev_A0.md` | 100 | - series capacitor: **1.0 µF film**; |
| DR039 | `0.48 Hz` | `docs/AE-015_Full_Chain_Noise_DC_Review_Rev_A0.md` | 102 | - first-order corner: approximately **0.48 Hz**. |
| DR039 | `0.48 Hz` | `docs/AE-015_Full_Chain_Noise_DC_Review_Rev_A0.md` | 130 | The proposed 0.48 Hz high-pass pole is more than an order of magnitude below the existing 15 Hz rumble filter and about two orders below the 50 Hz RIAA low-freq |
| ANALYSIS | `AE-012` | `docs/AE-015_Full_Chain_Noise_DC_Review_Rev_A0.md` | 137 | - AE-012 headroom; |
| ANALYSIS | `AE-015` | `docs/AE-015_Full_Chain_Noise_DC_Review_Rev_A0.md` | 138 | - AE-015 noise; |
| DR039 | `DR-039` | `docs/AE-015_Full_Chain_Noise_DC_Review_Rev_A0.md` | 146 | Therefore DR-039 must be implemented together with: |
| SCH103_OUTPUT | `POST_EQ` | `docs/AE-015_Full_Chain_Noise_DC_Review_Rev_A0.md` | 166 | - direct-coupled POST_EQ -> rumble-bypass -> output DC path. |
| DR039 | `DR-039` | `docs/AE-015_Full_Chain_Noise_DC_Review_Rev_A0.md` | 170 | **DR-039 — Common post-EQ DC block** |
| DR039 | `1.0 µF` | `docs/AE-015_Full_Chain_Noise_DC_Review_Rev_A0.md` | 172 | Add a 1.0 µF film / 330 kΩ first-order DC block per channel immediately after SCH103 and before the SCH107 bypass split. |
| DR039 | `DR-039` | `docs/AE-015_Full_Chain_Noise_DC_Review_Rev_A0.md` | 178 | 1. implement DR-039 in the controlled model and SCH103/SCH107 interface; |
| SCH101_NUMERIC | `3.48` | `docs/AE-016A_AE016_Regression_Repair_Rev_A0.md` | 6 | The existing suite explicitly freezes the active converter at 3.48x. That test |
| DR039 | `DR-039` | `docs/AE-016A_AE016_Regression_Repair_Rev_A0.md` | 13 | - retains DR-039 as the implementable independent change; |
| ANALYSIS | `signal_chain_analysis` | `docs/AE-016A_AE016_Regression_Repair_Rev_A0.md` | 14 | - removes the AE016 patch to `signal_chain_analysis.py` from the apply process; |
| DR039 | `DR-039` | `docs/AE-016A_AE016_Regression_Repair_Rev_A0.md` | 15 | - makes the SCH103 DR-039 patch idempotent. |
| ANALYSIS | `sch101_precision_candidate` | `docs/AE-016A_AE016_Regression_Repair_Rev_A0.md` | 19 | `sch101_precision_candidate.py` for the next controlled migration. |
| DR039 | `DR-039` | `docs/AE-016B_Full_Regression_Staging_Repair_Rev_A0.md` | 4 | SCH101 model and DR-039 in the SCH103 physical builder. AE-016A repaired the |
| DR039 | `DR-039` | `docs/AE-016B_Full_Regression_Staging_Repair_Rev_A0.md` | 8 | DR-039 analytical model and selected decision. Both DR-038 and DR-039 will be |
| DR039 | `DR-039` | `docs/AE-016_DR038_DR039_Implementation_Baseline_Rev_A0.md` | 1 | # AE-016 — DR-038 / DR-039 Implementation Baseline |
| DR039 | `DR-039` | `docs/AE-016_DR038_DR039_Implementation_Baseline_Rev_A0.md` | 5 | This update converts DR-038 and DR-039 into the controlled electrical baseline. |
| DR039 | `DR-039` | `docs/AE-016_DR038_DR039_Implementation_Baseline_Rev_A0.md` | 10 | DR-039 inserts a 1 µF film / 330 kΩ common post-EQ DC block before the SCH107 |
| DR039 | `0.48 Hz` | `docs/AE-016_DR038_DR039_Implementation_Baseline_Rev_A0.md` | 11 | filter/bypass split. Its nominal corner is ~0.48 Hz and its calculated loss at |
| DR039 | `DR-039` | `docs/AE-017_Atomic_Migration_Dependency_Mapping_Gate_Rev_A0.md` | 10 | AE-016 demonstrated that DR-038 and DR-039 cannot safely be inserted by changing |
| SCH101_NUMERIC | `3.48` | `docs/AE-017_Atomic_Migration_Dependency_Mapping_Gate_Rev_A0.md` | 22 | 1. numerical — the active test suite explicitly requires a 3.48x differential |
| SCH101_CAD | `R112` | `docs/AE-017_Atomic_Migration_Dependency_Mapping_Gate_Rev_A0.md` | 24 | 2. rendered CAD — tests explicitly require `SW1011`, `R112`, `R113`, `R114` |
| SCH101_CAD | `R113` | `docs/AE-017_Atomic_Migration_Dependency_Mapping_Gate_Rev_A0.md` | 24 | 2. rendered CAD — tests explicitly require `SW1011`, `R112`, `R113`, `R114` |
| SCH101_CAD | `R114` | `docs/AE-017_Atomic_Migration_Dependency_Mapping_Gate_Rev_A0.md` | 24 | 2. rendered CAD — tests explicitly require `SW1011`, `R112`, `R113`, `R114` |
| SCH101_CAD | `SW1011` | `docs/AE-017_Atomic_Migration_Dependency_Mapping_Gate_Rev_A0.md` | 24 | 2. rendered CAD — tests explicitly require `SW1011`, `R112`, `R113`, `R114` |
| SCH101_NUMERIC | `21680` | `docs/AE-017_Atomic_Migration_Dependency_Mapping_Gate_Rev_A0.md` | 25 | and the current 4420 / 8280 / 21680 resistor segmentation. |
| SCH101_NUMERIC | `4420` | `docs/AE-017_Atomic_Migration_Dependency_Mapping_Gate_Rev_A0.md` | 25 | and the current 4420 / 8280 / 21680 resistor segmentation. |
| SCH101_NUMERIC | `8280` | `docs/AE-017_Atomic_Migration_Dependency_Mapping_Gate_Rev_A0.md` | 25 | and the current 4420 / 8280 / 21680 resistor segmentation. |
| DR039 | `DR-039` | `docs/AE-017_Atomic_Migration_Dependency_Mapping_Gate_Rev_A0.md` | 27 | SCH103 has a separately frozen replay-EQ transfer-function topology. DR-039 must |
| DR039 | `DR-039` | `docs/AE-017_Atomic_Migration_Dependency_Mapping_Gate_Rev_A0.md` | 49 | Do not implement DR-038/DR-039 until the generated map has been reviewed and |
| SCH103_OUTPUT | `POST_EQ` | `docs/SR-004_SCH107_Pin_Aware_Conversion_Rev_A.md` | 16 | - POST_EQ input net; |
| SCH101_CAD | `DIP_Switch_Block` | `docs/SR-006_SCH101_DIP_Switch_Closure_Rev_A.md` | 8 | was the missing embedded definition for `ProjectShellac:DIP_Switch_Block`. |
| SCH103_OUTPUT | `POST_EQ` | `docs/SR-021_SCH107_Human_Reviewable_Conversion_Rev_A.md` | 28 | POST_EQ -> input TP -> HP section A -> stage TP -> HP section B |
| SCH103_OUTPUT | `POST_EQ` | `docs/SR-024_SCH103_Human_Reviewable_Rev_A.md` | 5 | treble selector and 2.1x recovery stage to POST_EQ. |
| ANALYSIS | `AE-013` | `docs/decisions/DR-038_SCH101_Precision_Architecture_PROPOSED.md` | 5 | **Evidence:** AE-013, AE-014 |
| ANALYSIS | `AE-014` | `docs/decisions/DR-038_SCH101_Precision_Architecture_PROPOSED.md` | 5 | **Evidence:** AE-013, AE-014 |
| ANALYSIS | `AE-013` | `docs/decisions/DR-038_SCH101_Precision_Architecture_PROPOSED.md` | 25 | - removes the tolerance-limited CMRR weakness identified by AE-013; |
| ANALYSIS | `AE-012` | `docs/decisions/DR-038_SCH101_Precision_Architecture_PROPOSED.md` | 35 | - AE-012 headroom regression passes; |
| ANALYSIS | `AE-012` | `docs/decisions/DR-038_SCH101_Precision_Architecture_SELECTED.md` | 9 | Reason: the current generator, schematic builder, AE-010/AE-012 regressions and |
| SCH101_NUMERIC | `3.48` | `docs/decisions/DR-038_SCH101_Precision_Architecture_SELECTED.md` | 10 | precision/noise assurance suite are mutually coupled to the proven 3.48x |
| DR039 | `DR-039` | `docs/decisions/DR-039_Common_Post_EQ_DC_Block_PROPOSED.md` | 1 | # DR-039 — Proposed common post-EQ DC block |
| ANALYSIS | `AE-015` | `docs/decisions/DR-039_Common_Post_EQ_DC_Block_PROPOSED.md` | 5 | **Evidence:** AE-015 |
| DR039 | `1.0 µF` | `docs/decisions/DR-039_Common_Post_EQ_DC_Block_PROPOSED.md` | 13 | - C = 1.0 µF film |
| DR039 | `0.48 Hz` | `docs/decisions/DR-039_Common_Post_EQ_DC_Block_PROPOSED.md` | 15 | - fc ≈ 0.48 Hz |
| DR039 | `DR-039` | `docs/decisions/DR-039_Common_Post_EQ_DC_Block_SELECTED.md` | 1 | # DR-039 — Common post-EQ DC block |
| DR039 | `1.0 µF` | `docs/decisions/DR-039_Common_Post_EQ_DC_Block_SELECTED.md` | 7 | - 1.0 µF non-polar film series capacitor per channel; |
| DR039 | `0.48 Hz` | `docs/decisions/DR-039_Common_Post_EQ_DC_Block_SELECTED.md` | 10 | - nominal corner approximately 0.48 Hz. |
| DR039 | `DR-039` | `docs/decisions/DR-039_Common_Post_EQ_DC_Block_SELECTED.md` | 12 | DR-039 is not yet substituted into the active SCH103 generator. It shall be |
| ANALYSIS | `AE-012` | `docs/updates/AE012_UPDATE_MANIFEST.md` | 1 | # AE-012 update manifest |
| ANALYSIS | `signal_chain_analysis` | `docs/updates/AE012_UPDATE_MANIFEST.md` | 6 | - `generator/model/signal_chain_analysis.py` |
| ANALYSIS | `signal_chain_analysis` | `docs/updates/AE012_UPDATE_MANIFEST.md` | 7 | - `tests/test_signal_chain_analysis.py` |
| ANALYSIS | `AE-012` | `docs/updates/AE012_UPDATE_MANIFEST.md` | 10 | - `docs/AE-012_All_State_Gain_Headroom_Closure_Rev_A0.md` |
| ANALYSIS | `AE-013` | `docs/updates/AE013_UPDATE_MANIFEST.md` | 1 | # AE-013 update manifest |
| ANALYSIS | `sch101_precision_analysis` | `docs/updates/AE013_UPDATE_MANIFEST.md` | 6 | - `generator/model/sch101_precision_analysis.py` |
| ANALYSIS | `sch101_precision_analysis` | `docs/updates/AE013_UPDATE_MANIFEST.md` | 7 | - `tests/test_sch101_precision_analysis.py` |
| ANALYSIS | `AE-013` | `docs/updates/AE013_UPDATE_MANIFEST.md` | 8 | - `docs/AE-013_SCH101_Noise_CMRR_Review_Rev_A0.md` |
| ANALYSIS | `AE-014` | `docs/updates/AE014_UPDATE_MANIFEST.md` | 1 | # AE-014 update manifest |
| ANALYSIS | `sch101_precision_candidate` | `docs/updates/AE014_UPDATE_MANIFEST.md` | 6 | - generator/model/sch101_precision_candidate.py |
| ANALYSIS | `sch101_precision_candidate` | `docs/updates/AE014_UPDATE_MANIFEST.md` | 7 | - tests/test_sch101_precision_candidate.py |
| ANALYSIS | `AE-014` | `docs/updates/AE014_UPDATE_MANIFEST.md` | 8 | - docs/AE-014_SCH101_Precision_Architecture_Downselect_Rev_A0.md |
| ANALYSIS | `AE-015` | `docs/updates/AE015_UPDATE_MANIFEST.md` | 1 | # AE-015 update manifest |
| ANALYSIS | `signal_chain_noise_dc` | `docs/updates/AE015_UPDATE_MANIFEST.md` | 6 | - `generator/model/signal_chain_noise_dc.py` |
| ANALYSIS | `signal_chain_noise_dc` | `docs/updates/AE015_UPDATE_MANIFEST.md` | 7 | - `tests/test_signal_chain_noise_dc.py` |
| ANALYSIS | `AE-015` | `docs/updates/AE015_UPDATE_MANIFEST.md` | 8 | - `docs/AE-015_Full_Chain_Noise_DC_Review_Rev_A0.md` |
| DR039 | `DR-039` | `docs/updates/AE015_UPDATE_MANIFEST.md` | 9 | - `docs/decisions/DR-039_Common_Post_EQ_DC_Block_PROPOSED.md` |
| DR039 | `post_eq_dc_block` | `docs/updates/AE016A_UPDATE_MANIFEST.md` | 13 | - generator/model/post_eq_dc_block.py |
| DR039 | `DR-039` | `docs/updates/AE016A_UPDATE_MANIFEST.md` | 14 | - DR-039 SCH103 physical patch |
| ANALYSIS | `signal_chain_analysis` | `docs/updates/AE016A_UPDATE_MANIFEST.md` | 17 | - AE-016 `signal_chain_analysis.py` modification. |
| ANALYSIS | `signal_chain_analysis` | `docs/updates/AE016A_UPDATE_MANIFEST.md` | 19 | If AE-016 already modified `signal_chain_analysis.py`, run the repair script |
| SCH103_OUTPUT | `replay_eq.py` | `docs/updates/AE016B_UPDATE_MANIFEST.md` | 6 | - restore `generator/blocks/replay_eq.py` to its pre-DR039 physical baseline; |
| DR039 | `post_eq_dc_block` | `docs/updates/AE016B_UPDATE_MANIFEST.md` | 7 | - retain `generator/model/post_eq_dc_block.py`; |
| DR039 | `DR-039` | `docs/updates/AE016B_UPDATE_MANIFEST.md` | 8 | - restage DR-039 as SELECTED / CAD migration pending; |
| ANALYSIS | `AE-012` | `docs/updates/AE016B_UPDATE_MANIFEST.md` | 10 | - restore the AE-012 signal-chain calculation if it is still patched. |
| DR039 | `post_eq_dc_block` | `docs/updates/AE016_UPDATE_MANIFEST.md` | 9 | - generator/model/post_eq_dc_block.py |
| DR039 | `DR-039` | `docs/updates/AE016_UPDATE_MANIFEST.md` | 11 | - selected DR-038 / DR-039 decision records |
| SCH103_OUTPUT | `replay_eq.py` | `docs/updates/AE016_UPDATE_MANIFEST.md` | 15 | - generator/blocks/replay_eq.py |
| ANALYSIS | `signal_chain_analysis` | `docs/updates/AE016_UPDATE_MANIFEST.md` | 16 | - generator/model/signal_chain_analysis.py |
| DR039 | `DR-039` | `docs/updates/AE016_UPDATE_MANIFEST.md` | 24 | `git commit -m "feat(signal-chain): implement DR-038 precision gain and DR-039 DC block"` |
| DR039 | `DR-039` | `docs/updates/AE017_UPDATE_MANIFEST.md` | 22 | `git commit -m "analysis(migration): map DR-038 and DR-039 atomic dependencies"` |
| ANALYSIS | `signal_chain_analysis` | `docs/updates/DR037_UPDATE_MANIFEST.md` | 18 | - `generator/model/signal_chain_analysis.py` |
| ANALYSIS | `signal_chain_analysis` | `docs/updates/DR037_UPDATE_MANIFEST.md` | 24 | - `tests/test_signal_chain_analysis.py` |
| SCH101_NUMERIC | `DIFF_CONVERTER_GAIN` | `generator/blocks/balanced_input.py` | 23 | DIFF_CONVERTER_GAIN, |
| SCH101_NUMERIC | `GAIN_BASE_RF_OHM` | `generator/blocks/balanced_input.py` | 24 | GAIN_BASE_RF_OHM, |
| SCH101_NUMERIC | `GAIN_DEFAULT_ADD_OHM` | `generator/blocks/balanced_input.py` | 25 | GAIN_DEFAULT_ADD_OHM, |
| SCH101_NUMERIC | `GAIN_HIGH_ADD_OHM` | `generator/blocks/balanced_input.py` | 26 | GAIN_HIGH_ADD_OHM, |
| SCH101_NUMERIC | `GAIN_RG_OHM` | `generator/blocks/balanced_input.py` | 27 | GAIN_RG_OHM, |
| SCH101_CAD | `DIP_Switch_Block` | `generator/blocks/balanced_input.py` | 50 | lib_id="ProjectShellac:DIP_Switch_Block", |
| SCH101_CAD | `STEREO GAIN DIP` | `generator/blocks/balanced_input.py` | 51 | value="STEREO GAIN DIP", |
| SCH101_NUMERIC | `GAIN_RG_OHM` | `generator/blocks/balanced_input.py` | 159 | f"R{refbase}{suffix}1", f"{GAIN_RG_OHM:g}", Point(165, fb_pin.y), |
| SCH101_NUMERIC | `GAIN_HIGH_ADD_OHM` | `generator/blocks/balanced_input.py` | 163 | f"R{refbase}{suffix}4", f"{GAIN_HIGH_ADD_OHM:g}", Point(220, feedback_y), |
| SCH101_NUMERIC | `GAIN_DEFAULT_ADD_OHM` | `generator/blocks/balanced_input.py` | 167 | f"R{refbase}{suffix}3", f"{GAIN_DEFAULT_ADD_OHM:g}", Point(250, feedback_y), |
| SCH101_NUMERIC | `GAIN_BASE_RF_OHM` | `generator/blocks/balanced_input.py` | 171 | f"R{refbase}{suffix}2", f"{GAIN_BASE_RF_OHM:g}", Point(280, feedback_y), |
| SCH101_NUMERIC | `DIFF_CONVERTER_GAIN` | `generator/blocks/balanced_input.py` | 217 | f"{channel} DIFF {DIFF_CONVERTER_GAIN:.2f}x", |
| SCH101_CAD | `3.48x differential converter` | `generator/blocks/balanced_input.py` | 289 | sheet.add_note("Signal path: floating cartridge -> RF/load -> matched JFET leg gain -> 3.48x differential converter -> pre-EQ.") |
| SCH101_NUMERIC | `3.48` | `generator/blocks/balanced_input.py` | 289 | sheet.add_note("Signal path: floating cartridge -> RF/load -> matched JFET leg gain -> 3.48x differential converter -> pre-EQ.") |
| SCH101_CAD | `10k / 34.8k` | `generator/blocks/balanced_input.py` | 292 | sheet.add_note("Differential converter: 3.48x using 10k / 34.8k, 0.1% or matched network.") |
| SCH101_NUMERIC | `3.48` | `generator/blocks/balanced_input.py` | 292 | sheet.add_note("Differential converter: 3.48x using 10k / 34.8k, 0.1% or matched network.") |
| SCH101_CAD | `SW1011` | `generator/blocks/balanced_input.py` | 294 | switch = sheet.add_component(_gain_selector("SW1011", "STEREO", Point(125, 155))) |
| DR039 | `1u` | `generator/blocks/power_entry.py` | 179 | ("C902", "1u", 160, "+18VA bypass"), |
| DR039 | `1u` | `generator/blocks/power_entry.py` | 188 | "Capacitor_SMD:C_1206_3216Metric" if value == "1u" else |
| DR039 | `1u` | `generator/blocks/power_entry.py` | 198 | ("C905", "1u", 240, "-18VA bypass"), |
| DR039 | `1u` | `generator/blocks/power_entry.py` | 207 | "Capacitor_SMD:C_1206_3216Metric" if value == "1u" else |
| SCH103_OUTPUT | `POST_EQ` | `generator/blocks/replay_eq.py` | 110 | post = f"POST_EQ_{channel}" |
| SCH103_OUTPUT | `_EQ_OUT` | `generator/blocks/replay_eq.py` | 160 | f"TP{base}2", f"{channel}_LF_EQ_OUT", Point(118, y + 5.08) |
| SCH103_OUTPUT | `_EQ_OUT` | `generator/blocks/replay_eq.py` | 283 | f"TP{base}3", f"{channel}_HF_EQ_OUT", Point(300, y + 5.08) |
| SCH103_OUTPUT | `output_end = Point(420` | `generator/blocks/replay_eq.py` | 289 | output_end = Point(420, u2_out.y) |
| SCH103_OUTPUT | `TP{base}4` | `generator/blocks/replay_eq.py` | 291 | f"TP{base}4", f"{channel}_EQ_OUT", Point(395, u2_out.y + 5.08) |
| SCH103_OUTPUT | `_EQ_OUT` | `generator/blocks/replay_eq.py` | 291 | f"TP{base}4", f"{channel}_EQ_OUT", Point(395, u2_out.y + 5.08) |
| SCH103_OUTPUT | `TP{base}4` | `generator/blocks/rumble_filter.py` | 202 | f"TP{base}4", f"{channel}_RUMBLE_OUT", Point(output_tp_x, y - 5.08) |
| SCH103_OUTPUT | `POST_EQ` | `generator/blocks/rumble_filter.py` | 209 | sheet.add_label(f"POST_EQ_{channel}", input_end.x, input_end.y) |
| SCH103_OUTPUT | `POST_EQ` | `generator/commissioning/model.py` | 127 | _m("M-0501", "Replay curve tracking", "Log-spaced sweep for each bass/treble selection", "PRE_EQ and POST_EQ test points", "Matches generated replay-curve analy |
| SCH103_OUTPUT | `POST_EQ` | `generator/commissioning/model.py` | 128 | _m("M-0502", "True-RIAA setting", "20 Hz to 20 kHz sweep", "POST_EQ", "Matches dedicated 3180/318 us plus 2121 Hz model", "Initial target ±0.20 dB from calculat |
| SCH103_OUTPUT | `POST_EQ` | `generator/commissioning/model.py` | 129 | _m("M-0503", "Channel tracking", "Identical sweep both channels", "POST_EQ_L versus POST_EQ_R", "Curves overlay", "Target ≤0.10 dB through 20 Hz–20 kHz, subject |
| SCH103_OUTPUT | `POST_EQ` | `generator/commissioning/model.py` | 140 | _m("M-0603", "Rumble filter transfer", "Low-frequency sweep, bypass and active", "POST_EQ to FILTERED", "Matches frozen SCH107 model", "Initial target ±0.20 dB  |
| SCH101_NUMERIC | `3.48` | `generator/core/components.py` | 81 | "Gain": "3.48x / +10.8 dB", |
| SCH101_CAD | `10k / 34.8k` | `generator/core/components.py` | 82 | "Resistor Network": "10k / 34.8k, 0.1% or matched network"}) |
| SCH101_CAD | `DIP_Switch_Block` | `generator/core/pins.py` | 142 | SYMBOL_PIN_CONTRACTS["ProjectShellac:DIP_Switch_Block"] = { |
| SCH101_CAD | `R112` | `generator/layout/placement_clusters.py` | 116 | "SW1011 U101 U102 R111 R112 R113 R114 R121 R122 R123 R124 U103 R130 R131 R132 R133", "U101 U102 U103", |
| SCH101_CAD | `R113` | `generator/layout/placement_clusters.py` | 116 | "SW1011 U101 U102 R111 R112 R113 R114 R121 R122 R123 R124 U103 R130 R131 R132 R133", "U101 U102 U103", |
| SCH101_CAD | `R114` | `generator/layout/placement_clusters.py` | 116 | "SW1011 U101 U102 R111 R112 R113 R114 R121 R122 R123 R124 U103 R130 R131 R132 R133", "U101 U102 U103", |
| SCH101_CAD | `SW1011` | `generator/layout/placement_clusters.py` | 116 | "SW1011 U101 U102 R111 R112 R113 R114 R121 R122 R123 R124 U103 R130 R131 R132 R133", "U101 U102 U103", |
| SCH101_NUMERIC | `3.48` | `generator/model/balanced_input.py` | 5 | - fixed 3.48x precision differential converter per channel. |
| SCH101_NUMERIC | `3.48` | `generator/model/balanced_input.py` | 17 | DIFF_CONVERTER_GAIN = 3.48 |
| SCH101_NUMERIC | `DIFF_CONVERTER_GAIN` | `generator/model/balanced_input.py` | 17 | DIFF_CONVERTER_GAIN = 3.48 |
| SCH101_NUMERIC | `GAIN_RG_OHM` | `generator/model/balanced_input.py` | 18 | GAIN_RG_OHM = 10_000.0 |
| SCH101_NUMERIC | `GAIN_BASE_RF_OHM` | `generator/model/balanced_input.py` | 19 | GAIN_BASE_RF_OHM = 4_420.0 |
| SCH101_NUMERIC | `GAIN_DEFAULT_ADD_OHM` | `generator/model/balanced_input.py` | 20 | GAIN_DEFAULT_ADD_OHM = 8_280.0 |
| SCH101_NUMERIC | `GAIN_HIGH_ADD_OHM` | `generator/model/balanced_input.py` | 21 | GAIN_HIGH_ADD_OHM = 21_680.0 |
| SCH101_NUMERIC | `GAIN_RG_OHM` | `generator/model/balanced_input.py` | 42 | return 1.0 + self.rf_ohm / GAIN_RG_OHM |
| SCH101_NUMERIC | `DIFF_CONVERTER_GAIN` | `generator/model/balanced_input.py` | 46 | return self.per_leg_gain * DIFF_CONVERTER_GAIN |
| SCH101_NUMERIC | `GAIN_BASE_RF_OHM` | `generator/model/balanced_input.py` | 74 | assert GAIN_BASE_RF_OHM + GAIN_DEFAULT_ADD_OHM == GAIN_SETTINGS[1].rf_ohm |
| SCH101_NUMERIC | `GAIN_DEFAULT_ADD_OHM` | `generator/model/balanced_input.py` | 74 | assert GAIN_BASE_RF_OHM + GAIN_DEFAULT_ADD_OHM == GAIN_SETTINGS[1].rf_ohm |
| SCH101_NUMERIC | `GAIN_BASE_RF_OHM` | `generator/model/balanced_input.py` | 75 | assert GAIN_BASE_RF_OHM + GAIN_HIGH_ADD_OHM == GAIN_SETTINGS[2].rf_ohm |
| SCH101_NUMERIC | `GAIN_HIGH_ADD_OHM` | `generator/model/balanced_input.py` | 75 | assert GAIN_BASE_RF_OHM + GAIN_HIGH_ADD_OHM == GAIN_SETTINGS[2].rf_ohm |
| DR039 | `DR-039` | `generator/model/post_eq_dc_block.py` | 1 | """DR-039 common post-EQ DC block.""" |
| DR039 | `post_eq_dc_block` | `generator/model/post_eq_dc_block.py` | 20 | def validate_post_eq_dc_block(): |
| ANALYSIS | `AE-013` | `generator/model/sch101_precision_analysis.py` | 1 | """AE-013 SCH101 noise and resistor-tolerance CMRR review. |
| SCH101_NUMERIC | `GAIN_RG_OHM` | `generator/model/sch101_precision_analysis.py` | 32 | GAIN_RG_OHM = 10_000.0 |
| SCH101_NUMERIC | `GAIN_RG_OHM` | `generator/model/sch101_precision_analysis.py` | 88 | rg = GAIN_RG_OHM * impedance_scale |
| SCH101_NUMERIC | `GAIN_RG_OHM` | `generator/model/sch101_precision_analysis.py` | 153 | gp = 1.0 + setting.rf_ohm * (1.0 + srfp*t) / (GAIN_RG_OHM * (1.0 + srgp*t)) |
| SCH101_NUMERIC | `GAIN_RG_OHM` | `generator/model/sch101_precision_analysis.py` | 154 | gm = 1.0 + setting.rf_ohm * (1.0 + srfm*t) / (GAIN_RG_OHM * (1.0 + srgm*t)) |
| ANALYSIS | `AE-014` | `generator/model/sch101_precision_candidate.py` | 1 | """AE-014 SCH101 precision-architecture down-selection. |
| SCH101_NUMERIC | `3.48` | `generator/model/sch101_precision_candidate.py` | 3 | Compares the controlled 3.48x / high-impedance implementation with the |
| SCH103_OUTPUT | `POST_EQ` | `generator/model/shellac.py` | 64 | ("POST_EQ_L", SignalKind.ANALOG, "Left-channel replay-equalised signal."), |
| SCH103_OUTPUT | `POST_EQ` | `generator/model/shellac.py` | 65 | ("POST_EQ_R", SignalKind.ANALOG, "Right-channel replay-equalised signal."), |
| SCH103_OUTPUT | `POST_EQ` | `generator/model/shellac.py` | 121 | _interface("OUT_L", "POST_EQ_L", Direction.OUTPUT), |
| SCH103_OUTPUT | `POST_EQ` | `generator/model/shellac.py` | 122 | _interface("OUT_R", "POST_EQ_R", Direction.OUTPUT), |
| SCH103_OUTPUT | `POST_EQ` | `generator/model/shellac.py` | 185 | _interface("IN_L", "POST_EQ_L", Direction.INPUT), |
| SCH103_OUTPUT | `POST_EQ` | `generator/model/shellac.py` | 186 | _interface("IN_R", "POST_EQ_R", Direction.INPUT), |
| ANALYSIS | `AE-012` | `generator/model/signal_chain_analysis.py` | 1 | """AE-011/AE-012 complete signal-chain gain and headroom analysis. |
| ANALYSIS | `AE-015` | `generator/model/signal_chain_noise_dc.py` | 1 | """AE-015 full-chain noise and DC-offset review for Project Shellac. |
| ANALYSIS | `AE-014` | `generator/model/signal_chain_noise_dc.py` | 27 | # AE-014 first-order input-referred white-noise result, rounded conservatively. |
| DR039 | `DR-039` | `generator/model/signal_chain_noise_dc.py` | 49 | # Proposed DR-039 common post-EQ DC block. |
| DR039 | `330k` | `generator/model/signal_chain_noise_dc.py` | 92 | # Series capacitor into the defined 330k bias/load resistor. |
| SCH101_CAD | `DIP_Switch_Block` | `generator/writers/kicad9.py` | 45 | "ProjectShellac:DIP_Switch_Block": 16, |
| SCH101_CAD | `DIP_Switch_Block` | `generator/writers/kicad9.py` | 226 | "ProjectShellac:DIP_Switch_Block", |
| SCH101_CAD | `DIP_Switch_Block` | `generator/writers/kicad9.py` | 500 | (symbol "ProjectShellac:DIP_Switch_Block" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom yes) (on_board yes) |
| SCH101_CAD | `DIP_Switch_Block` | `generator/writers/kicad9.py` | 503 | (symbol "DIP_Switch_Block_0_1" |
| SCH103_OUTPUT | `replay_eq.py` | `manifest.json` | 14 | "path": "generator/blocks/replay_eq.py", |
| SCH103_OUTPUT | `POST_EQ` | `out/commissioning/commissioning_baseline.json` | 332 | "measurement_point": "PRE_EQ and POST_EQ test points", |
| SCH103_OUTPUT | `POST_EQ` | `out/commissioning/commissioning_baseline.json` | 343 | "measurement_point": "POST_EQ", |
| SCH103_OUTPUT | `POST_EQ` | `out/commissioning/commissioning_baseline.json` | 354 | "measurement_point": "POST_EQ_L versus POST_EQ_R", |
| SCH103_OUTPUT | `POST_EQ` | `out/commissioning/commissioning_baseline.json` | 412 | "measurement_point": "POST_EQ to FILTERED", |
| SCH103_OUTPUT | `POST_EQ` | `out/kicad/ProjectShellac.kicad_sch` | 82 | (pin "POST_EQ_L" output (at 187.96 33.02 0) |
| SCH103_OUTPUT | `POST_EQ` | `out/kicad/ProjectShellac.kicad_sch` | 86 | (pin "POST_EQ_R" output (at 187.96 38.10 0) |
| SCH103_OUTPUT | `POST_EQ` | `out/kicad/ProjectShellac.kicad_sch` | 109 | (pin "POST_EQ_L" input (at 213.36 33.02 180) |
| SCH103_OUTPUT | `POST_EQ` | `out/kicad/ProjectShellac.kicad_sch` | 113 | (pin "POST_EQ_R" input (at 213.36 38.10 180) |
| SCH103_OUTPUT | `POST_EQ` | `out/kicad/ProjectShellac.kicad_sch` | 546 | (global_label "ROOT__POST_EQ_L" (shape bidirectional) (at 198.12 33.02 0) |
| SCH103_OUTPUT | `POST_EQ` | `out/kicad/ProjectShellac.kicad_sch` | 555 | (global_label "ROOT__POST_EQ_L" (shape bidirectional) (at 203.20 33.02 0) |
| SCH103_OUTPUT | `POST_EQ` | `out/kicad/ProjectShellac.kicad_sch` | 564 | (global_label "ROOT__POST_EQ_R" (shape bidirectional) (at 198.12 38.10 0) |
| SCH103_OUTPUT | `POST_EQ` | `out/kicad/ProjectShellac.kicad_sch` | 573 | (global_label "ROOT__POST_EQ_R" (shape bidirectional) (at 203.20 38.10 0) |
| SCH101_CAD | `DIP_Switch_Block` | `out/kicad/ProjectShellac.kicad_sym` | 122 | (symbol "DIP_Switch_Block" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom yes) (on_board yes) |
| SCH101_CAD | `DIP_Switch_Block` | `out/kicad/ProjectShellac.kicad_sym` | 125 | (symbol "DIP_Switch_Block_0_1" |
| SCH101_CAD | `DIP_Switch_Block` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 204 | (symbol "ProjectShellac:DIP_Switch_Block" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom yes) (on_board yes) |
| SCH101_CAD | `DIP_Switch_Block` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 207 | (symbol "DIP_Switch_Block_0_1" |
| SCH101_CAD | `3.48x differential converter` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 294 | (text "Signal path: floating cartridge -> RF/load -> matched JFET leg gain -> 3.48x differential converter -> pre-EQ." (at 20.00 34.00 0) |
| SCH101_NUMERIC | `3.48` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 294 | (text "Signal path: floating cartridge -> RF/load -> matched JFET leg gain -> 3.48x differential converter -> pre-EQ." (at 20.00 34.00 0) |
| SCH101_CAD | `10k / 34.8k` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 306 | (text "Differential converter: 3.48x using 10k / 34.8k, 0.1% or matched network." (at 20.00 55.00 0) |
| SCH101_NUMERIC | `3.48` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 306 | (text "Differential converter: 3.48x using 10k / 34.8k, 0.1% or matched network." (at 20.00 55.00 0) |
| SCH101_CAD | `DIP_Switch_Block` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 826 | (symbol (lib_id "ProjectShellac:DIP_Switch_Block") (at 124.46 154.94 0) (unit 1) |
| SCH101_CAD | `SW1011` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 829 | (property "Reference" "SW1011" (id 0) (at 124.46 151.14 0) |
| SCH101_CAD | `STEREO GAIN DIP` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 832 | (property "Value" "STEREO GAIN DIP" (id 1) (at 124.46 158.74 0) |
| SCH101_CAD | `SW1011` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 869 | (reference "SW1011") |
| SCH101_CAD | `SW1011` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 873 | (reference "SW1011") |
| SCH101_CAD | `R114` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 1214 | (property "Reference" "R114" (id 0) (at 219.71 40.65 0) |
| SCH101_NUMERIC | `21680` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 1217 | (property "Value" "21680" (id 1) (at 219.71 48.25 0) |
| SCH101_CAD | `R114` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 1234 | (reference "R114") |
| SCH101_CAD | `R114` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 1238 | (reference "R114") |
| SCH101_CAD | `R113` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 1247 | (property "Reference" "R113" (id 0) (at 250.19 40.65 0) |
| SCH101_NUMERIC | `8280` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 1250 | (property "Value" "8280" (id 1) (at 250.19 48.25 0) |
| SCH101_CAD | `R113` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 1267 | (reference "R113") |
| SCH101_CAD | `R113` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 1271 | (reference "R113") |
| SCH101_CAD | `R112` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 1280 | (property "Reference" "R112" (id 0) (at 279.40 40.65 0) |
| SCH101_NUMERIC | `4420` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 1283 | (property "Value" "4420" (id 1) (at 279.40 48.25 0) |
| SCH101_CAD | `R112` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 1300 | (reference "R112") |
| SCH101_CAD | `R112` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 1304 | (reference "R112") |
| SCH101_NUMERIC | `21680` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 1391 | (property "Value" "21680" (id 1) (at 219.71 128.26 0) |
| SCH101_NUMERIC | `8280` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 1424 | (property "Value" "8280" (id 1) (at 250.19 128.26 0) |
| SCH101_NUMERIC | `4420` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 1457 | (property "Value" "4420" (id 1) (at 279.40 128.26 0) |
| SCH101_NUMERIC | `3.48` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 1490 | (property "Value" "L DIFF 3.48x" (id 1) (at 350.52 88.89 0) |
| SCH101_NUMERIC | `3.48` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 1505 | (property "Gain" "3.48x / +10.8 dB" (at 350.52 99.09 0) |
| SCH101_CAD | `10k / 34.8k` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 1508 | (property "Resistor Network" "10k / 34.8k, 0.1% or matched network" (at 350.52 101.09 0) |
| SCH101_NUMERIC | `21680` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 1999 | (property "Value" "21680" (id 1) (at 219.71 168.90 0) |
| SCH101_NUMERIC | `8280` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 2032 | (property "Value" "8280" (id 1) (at 250.19 168.90 0) |
| SCH101_NUMERIC | `4420` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 2065 | (property "Value" "4420" (id 1) (at 279.40 168.90 0) |
| SCH101_NUMERIC | `21680` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 2173 | (property "Value" "21680" (id 1) (at 219.71 248.91 0) |
| SCH101_NUMERIC | `8280` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 2206 | (property "Value" "8280" (id 1) (at 250.19 248.91 0) |
| SCH101_NUMERIC | `4420` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 2239 | (property "Value" "4420" (id 1) (at 279.40 248.91 0) |
| SCH101_NUMERIC | `3.48` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 2272 | (property "Value" "R DIFF 3.48x" (id 1) (at 350.52 208.27 0) |
| SCH101_NUMERIC | `3.48` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 2287 | (property "Gain" "3.48x / +10.8 dB" (at 350.52 218.47 0) |
| SCH101_CAD | `10k / 34.8k` | `out/kicad/ProjectShellac_SCH101.kicad_sch` | 2290 | (property "Resistor Network" "10k / 34.8k, 0.1% or matched network" (at 350.52 220.47 0) |
| SCH101_CAD | `DIP_Switch_Block` | `out/kicad/ProjectShellac_SCH103.kicad_sch` | 204 | (symbol "ProjectShellac:DIP_Switch_Block" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom yes) (on_board yes) |
| SCH101_CAD | `DIP_Switch_Block` | `out/kicad/ProjectShellac_SCH103.kicad_sch` | 207 | (symbol "DIP_Switch_Block_0_1" |
| SCH103_OUTPUT | `_EQ_OUT` | `out/kicad/ProjectShellac_SCH103.kicad_sch` | 1013 | (property "Value" "L_LF_EQ_OUT" (id 1) (at 118.11 93.97 0) |
| SCH103_OUTPUT | `_EQ_OUT` | `out/kicad/ProjectShellac_SCH103.kicad_sch` | 1664 | (property "Value" "L_HF_EQ_OUT" (id 1) (at 299.72 93.97 0) |
| SCH103_OUTPUT | `_EQ_OUT` | `out/kicad/ProjectShellac_SCH103.kicad_sch` | 1690 | (property "Value" "L_EQ_OUT" (id 1) (at 394.97 93.97 0) |
| SCH101_NUMERIC | `4420` | `out/kicad/ProjectShellac_SCH103.kicad_sch` | 1927 | (uuid "ca0bf19f-ca2b-5e6f-b030-4be3044201af") |
| SCH103_OUTPUT | `_EQ_OUT` | `out/kicad/ProjectShellac_SCH103.kicad_sch` | 1997 | (property "Value" "R_LF_EQ_OUT" (id 1) (at 118.11 204.46 0) |
| SCH103_OUTPUT | `_EQ_OUT` | `out/kicad/ProjectShellac_SCH103.kicad_sch` | 2648 | (property "Value" "R_HF_EQ_OUT" (id 1) (at 299.72 204.46 0) |
| SCH103_OUTPUT | `_EQ_OUT` | `out/kicad/ProjectShellac_SCH103.kicad_sch` | 2674 | (property "Value" "R_EQ_OUT" (id 1) (at 394.97 204.46 0) |
| SCH103_OUTPUT | `POST_EQ` | `out/kicad/ProjectShellac_SCH103.kicad_sch` | 3078 | (hierarchical_label "POST_EQ_L" (shape output) (at 420.37 85.09 0) |
| SCH103_OUTPUT | `POST_EQ` | `out/kicad/ProjectShellac_SCH103.kicad_sch` | 3082 | (hierarchical_label "POST_EQ_R" (shape output) (at 420.37 195.58 0) |
| SCH101_CAD | `DIP_Switch_Block` | `out/kicad/ProjectShellac_SCH104.kicad_sch` | 204 | (symbol "ProjectShellac:DIP_Switch_Block" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom yes) (on_board yes) |
| SCH101_CAD | `DIP_Switch_Block` | `out/kicad/ProjectShellac_SCH104.kicad_sch` | 207 | (symbol "DIP_Switch_Block_0_1" |
| SCH101_CAD | `DIP_Switch_Block` | `out/kicad/ProjectShellac_SCH105.kicad_sch` | 204 | (symbol "ProjectShellac:DIP_Switch_Block" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom yes) (on_board yes) |
| SCH101_CAD | `DIP_Switch_Block` | `out/kicad/ProjectShellac_SCH105.kicad_sch` | 207 | (symbol "DIP_Switch_Block_0_1" |
| SCH101_CAD | `DIP_Switch_Block` | `out/kicad/ProjectShellac_SCH106.kicad_sch` | 204 | (symbol "ProjectShellac:DIP_Switch_Block" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom yes) (on_board yes) |
| SCH101_CAD | `DIP_Switch_Block` | `out/kicad/ProjectShellac_SCH106.kicad_sch` | 207 | (symbol "DIP_Switch_Block_0_1" |
| DR039 | `1u` | `out/kicad/ProjectShellac_SCH106.kicad_sch` | 1029 | (property "Value" "1u" (id 1) (at 160.02 78.73 0) |
| DR039 | `1u` | `out/kicad/ProjectShellac_SCH106.kicad_sch` | 1167 | (property "Value" "1u" (id 1) (at 240.03 109.21 0) |
| SCH101_CAD | `DIP_Switch_Block` | `out/kicad/ProjectShellac_SCH107.kicad_sch` | 204 | (symbol "ProjectShellac:DIP_Switch_Block" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom yes) (on_board yes) |
| SCH101_CAD | `DIP_Switch_Block` | `out/kicad/ProjectShellac_SCH107.kicad_sch` | 207 | (symbol "DIP_Switch_Block_0_1" |
| SCH103_OUTPUT | `POST_EQ` | `out/kicad/ProjectShellac_SCH107.kicad_sch` | 2269 | (hierarchical_label "POST_EQ_L" (shape input) (at 25.40 77.47 0) |
| SCH103_OUTPUT | `POST_EQ` | `out/kicad/ProjectShellac_SCH107.kicad_sch` | 2273 | (hierarchical_label "POST_EQ_R" (shape input) (at 25.40 185.42 0) |
| SCH101_CAD | `DIP_Switch_Block` | `out/kicad/ProjectShellac_SCH108.kicad_sch` | 204 | (symbol "ProjectShellac:DIP_Switch_Block" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom yes) (on_board yes) |
| SCH101_CAD | `DIP_Switch_Block` | `out/kicad/ProjectShellac_SCH108.kicad_sch` | 207 | (symbol "DIP_Switch_Block_0_1" |
| SCH101_CAD | `DIP_Switch_Block` | `out/kicad/ProjectShellac_SCH109.kicad_sch` | 204 | (symbol "ProjectShellac:DIP_Switch_Block" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom yes) (on_board yes) |
| SCH101_CAD | `DIP_Switch_Block` | `out/kicad/ProjectShellac_SCH109.kicad_sch` | 207 | (symbol "DIP_Switch_Block_0_1" |
| SCH101_CAD | `SW1011` | `out/layout/cluster_placement_baseline.json` | 42 | "SW1011", |
| SCH101_CAD | `R112` | `out/layout/cluster_placement_baseline.json` | 46 | "R112", |
| SCH101_CAD | `R113` | `out/layout/cluster_placement_baseline.json` | 47 | "R113", |
| SCH101_CAD | `R114` | `out/layout/cluster_placement_baseline.json` | 48 | "R114", |
| SCH101_CAD | `SW1011` | `out/layout/detailed_placement_readiness.json` | 172 | "SW1011" |
| SCH101_CAD | `SW1011` | `out/layout/detailed_placement_readiness.json` | 184 | "SW1011" |
| SCH101_CAD | `SW1011` | `out/layout/detailed_placement_readiness.json` | 196 | "SW1011" |
| SCH101_CAD | `SW1011` | `out/layout/detailed_placement_readiness.json` | 255 | "SW1011", |
| SCH101_CAD | `R112` | `out/layout/detailed_placement_readiness.json` | 380 | "R112", |
| SCH101_CAD | `R113` | `out/layout/detailed_placement_readiness.json` | 381 | "R113", |
| SCH101_CAD | `R114` | `out/layout/detailed_placement_readiness.json` | 382 | "R114", |
| SCH101_CAD | `SW1011` | `out/layout/detailed_placement_readiness.json` | 391 | "SW1011", |
| SCH101_CAD | `R112` | `out/layout/footprint_contract.json` | 163 | "ref": "R112", |
| SCH101_NUMERIC | `4420` | `out/layout/footprint_contract.json` | 165 | "value": "4420", |
| SCH101_CAD | `R113` | `out/layout/footprint_contract.json` | 175 | "ref": "R113", |
| SCH101_NUMERIC | `8280` | `out/layout/footprint_contract.json` | 177 | "value": "8280", |
| SCH101_CAD | `R114` | `out/layout/footprint_contract.json` | 187 | "ref": "R114", |
| SCH101_NUMERIC | `21680` | `out/layout/footprint_contract.json` | 189 | "value": "21680", |
| SCH101_NUMERIC | `4420` | `out/layout/footprint_contract.json` | 213 | "value": "4420", |
| SCH101_NUMERIC | `8280` | `out/layout/footprint_contract.json` | 225 | "value": "8280", |
| SCH101_NUMERIC | `21680` | `out/layout/footprint_contract.json` | 237 | "value": "21680", |
| SCH101_NUMERIC | `4420` | `out/layout/footprint_contract.json` | 333 | "value": "4420", |
| SCH101_NUMERIC | `8280` | `out/layout/footprint_contract.json` | 345 | "value": "8280", |
| SCH101_NUMERIC | `21680` | `out/layout/footprint_contract.json` | 357 | "value": "21680", |
| SCH101_NUMERIC | `4420` | `out/layout/footprint_contract.json` | 381 | "value": "4420", |
| SCH101_NUMERIC | `8280` | `out/layout/footprint_contract.json` | 393 | "value": "8280", |
| SCH101_NUMERIC | `21680` | `out/layout/footprint_contract.json` | 405 | "value": "21680", |
| SCH101_CAD | `SW1011` | `out/layout/footprint_contract.json` | 463 | "ref": "SW1011", |
| SCH101_CAD | `STEREO GAIN DIP` | `out/layout/footprint_contract.json` | 465 | "value": "STEREO GAIN DIP", |
| SCH101_CAD | `DIP_Switch_Block` | `out/layout/footprint_contract.json` | 466 | "lib_id": "ProjectShellac:DIP_Switch_Block", |
| SCH101_NUMERIC | `3.48` | `out/layout/footprint_contract.json` | 501 | "value": "L DIFF 3.48x", |
| SCH101_NUMERIC | `3.48` | `out/layout/footprint_contract.json` | 537 | "value": "R DIFF 3.48x", |
| SCH103_OUTPUT | `_EQ_OUT` | `out/layout/footprint_contract.json` | 1113 | "value": "L_LF_EQ_OUT", |
| SCH103_OUTPUT | `_EQ_OUT` | `out/layout/footprint_contract.json` | 1125 | "value": "L_HF_EQ_OUT", |
| SCH103_OUTPUT | `_EQ_OUT` | `out/layout/footprint_contract.json` | 1137 | "value": "L_EQ_OUT", |
| SCH103_OUTPUT | `_EQ_OUT` | `out/layout/footprint_contract.json` | 1161 | "value": "R_LF_EQ_OUT", |
| SCH103_OUTPUT | `_EQ_OUT` | `out/layout/footprint_contract.json` | 1173 | "value": "R_HF_EQ_OUT", |
| SCH103_OUTPUT | `_EQ_OUT` | `out/layout/footprint_contract.json` | 1185 | "value": "R_EQ_OUT", |
| DR039 | `1u` | `out/layout/footprint_contract.json` | 1617 | "value": "1u", |
| DR039 | `1u` | `out/layout/footprint_contract.json` | 1653 | "value": "1u", |
| SCH101_CAD | `R112` | `out/layout/footprint_contract.json` | 2971 | "R112", |
| SCH101_CAD | `R113` | `out/layout/footprint_contract.json` | 2972 | "R113", |
| SCH101_CAD | `R114` | `out/layout/footprint_contract.json` | 2973 | "R114", |
| SCH101_CAD | `SW1011` | `out/layout/footprint_contract.json` | 2996 | "SW1011", |
| DR039 | `1u` | `out/layout/kicad_native_pipeline.json` | 866 | "value": "1u", |
| DR039 | `1u` | `out/layout/kicad_native_pipeline.json` | 902 | "value": "1u", |
| SCH101_CAD | `R112` | `out/layout/kicad_native_pipeline.json` | 1177 | "reference": "R112", |
| SCH101_NUMERIC | `4420` | `out/layout/kicad_native_pipeline.json` | 1178 | "value": "4420", |
| SCH101_CAD | `R113` | `out/layout/kicad_native_pipeline.json` | 1189 | "reference": "R113", |
| SCH101_NUMERIC | `8280` | `out/layout/kicad_native_pipeline.json` | 1190 | "value": "8280", |
| SCH101_CAD | `R114` | `out/layout/kicad_native_pipeline.json` | 1201 | "reference": "R114", |
| SCH101_NUMERIC | `21680` | `out/layout/kicad_native_pipeline.json` | 1202 | "value": "21680", |
| SCH101_NUMERIC | `4420` | `out/layout/kicad_native_pipeline.json` | 1226 | "value": "4420", |
| SCH101_NUMERIC | `8280` | `out/layout/kicad_native_pipeline.json` | 1238 | "value": "8280", |
| SCH101_NUMERIC | `21680` | `out/layout/kicad_native_pipeline.json` | 1250 | "value": "21680", |
| SCH101_NUMERIC | `4420` | `out/layout/kicad_native_pipeline.json` | 1346 | "value": "4420", |
| SCH101_NUMERIC | `8280` | `out/layout/kicad_native_pipeline.json` | 1358 | "value": "8280", |
| SCH101_NUMERIC | `21680` | `out/layout/kicad_native_pipeline.json` | 1370 | "value": "21680", |
| SCH101_NUMERIC | `4420` | `out/layout/kicad_native_pipeline.json` | 1394 | "value": "4420", |
| SCH101_NUMERIC | `8280` | `out/layout/kicad_native_pipeline.json` | 1406 | "value": "8280", |
| SCH101_NUMERIC | `21680` | `out/layout/kicad_native_pipeline.json` | 1418 | "value": "21680", |
| SCH101_CAD | `SW1011` | `out/layout/kicad_native_pipeline.json` | 1993 | "reference": "SW1011", |
| SCH101_CAD | `STEREO GAIN DIP` | `out/layout/kicad_native_pipeline.json` | 1994 | "value": "STEREO GAIN DIP", |
| SCH103_OUTPUT | `_EQ_OUT` | `out/layout/kicad_native_pipeline.json` | 2018 | "value": "L_LF_EQ_OUT", |
| SCH103_OUTPUT | `_EQ_OUT` | `out/layout/kicad_native_pipeline.json` | 2030 | "value": "L_HF_EQ_OUT", |
| SCH103_OUTPUT | `_EQ_OUT` | `out/layout/kicad_native_pipeline.json` | 2042 | "value": "L_EQ_OUT", |
| SCH103_OUTPUT | `_EQ_OUT` | `out/layout/kicad_native_pipeline.json` | 2066 | "value": "R_LF_EQ_OUT", |
| SCH103_OUTPUT | `_EQ_OUT` | `out/layout/kicad_native_pipeline.json` | 2078 | "value": "R_HF_EQ_OUT", |
| SCH103_OUTPUT | `_EQ_OUT` | `out/layout/kicad_native_pipeline.json` | 2090 | "value": "R_EQ_OUT", |
| SCH101_NUMERIC | `3.48` | `out/layout/kicad_native_pipeline.json` | 2498 | "value": "L DIFF 3.48x", |
| SCH101_NUMERIC | `3.48` | `out/layout/kicad_native_pipeline.json` | 2534 | "value": "R DIFF 3.48x", |
| SCH101_CAD | `R112` | `out/layout/preliminary_placement_baseline.json` | 1367 | "ref": "R112", |
| SCH101_CAD | `R113` | `out/layout/preliminary_placement_baseline.json` | 1381 | "ref": "R113", |
| SCH101_CAD | `R114` | `out/layout/preliminary_placement_baseline.json` | 1395 | "ref": "R114", |
| SCH101_CAD | `SW1011` | `out/layout/preliminary_placement_baseline.json` | 2319 | "ref": "SW1011", |
| DR039 | `1u` | `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | 840 | (property "Value" "1u" (at 0 3.100 0.0) (layer "F.Fab") hide (effects (font (size 1 1) (thickness 0.15)))) |
| DR039 | `1u` | `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | 873 | (property "Value" "1u" (at 0 3.100 0.0) (layer "F.Fab") hide (effects (font (size 1 1) (thickness 0.15)))) |
| SCH101_CAD | `R112` | `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | 1125 | (property "Reference" "R112" (at 0 -2.700 0.0) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15)))) |
| SCH101_NUMERIC | `4420` | `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | 1126 | (property "Value" "4420" (at 0 2.700 0.0) (layer "F.Fab") hide (effects (font (size 1 1) (thickness 0.15)))) |
| SCH101_CAD | `R113` | `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | 1136 | (property "Reference" "R113" (at 0 -2.700 0.0) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15)))) |
| SCH101_NUMERIC | `8280` | `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | 1137 | (property "Value" "8280" (at 0 2.700 0.0) (layer "F.Fab") hide (effects (font (size 1 1) (thickness 0.15)))) |
| SCH101_CAD | `R114` | `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | 1147 | (property "Reference" "R114" (at 0 -2.700 0.0) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15)))) |
| SCH101_NUMERIC | `21680` | `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | 1148 | (property "Value" "21680" (at 0 2.700 0.0) (layer "F.Fab") hide (effects (font (size 1 1) (thickness 0.15)))) |
| SCH101_NUMERIC | `4420` | `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | 1170 | (property "Value" "4420" (at 0 2.700 0.0) (layer "F.Fab") hide (effects (font (size 1 1) (thickness 0.15)))) |
| SCH101_NUMERIC | `8280` | `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | 1181 | (property "Value" "8280" (at 0 2.700 0.0) (layer "F.Fab") hide (effects (font (size 1 1) (thickness 0.15)))) |
| SCH101_NUMERIC | `21680` | `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | 1192 | (property "Value" "21680" (at 0 2.700 0.0) (layer "F.Fab") hide (effects (font (size 1 1) (thickness 0.15)))) |
| SCH101_NUMERIC | `4420` | `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | 1280 | (property "Value" "4420" (at 0 2.700 0.0) (layer "F.Fab") hide (effects (font (size 1 1) (thickness 0.15)))) |
| SCH101_NUMERIC | `8280` | `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | 1291 | (property "Value" "8280" (at 0 2.700 0.0) (layer "F.Fab") hide (effects (font (size 1 1) (thickness 0.15)))) |
| SCH101_NUMERIC | `21680` | `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | 1302 | (property "Value" "21680" (at 0 2.700 0.0) (layer "F.Fab") hide (effects (font (size 1 1) (thickness 0.15)))) |
| SCH101_NUMERIC | `4420` | `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | 1324 | (property "Value" "4420" (at 0 2.700 0.0) (layer "F.Fab") hide (effects (font (size 1 1) (thickness 0.15)))) |
| SCH101_NUMERIC | `8280` | `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | 1335 | (property "Value" "8280" (at 0 2.700 0.0) (layer "F.Fab") hide (effects (font (size 1 1) (thickness 0.15)))) |
| SCH101_NUMERIC | `21680` | `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | 1346 | (property "Value" "21680" (at 0 2.700 0.0) (layer "F.Fab") hide (effects (font (size 1 1) (thickness 0.15)))) |
| SCH101_CAD | `SW1011` | `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | 1873 | (property "Reference" "SW1011" (at 0 -6.500 0.0) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15)))) |
| SCH101_CAD | `STEREO GAIN DIP` | `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | 1874 | (property "Value" "STEREO GAIN DIP" (at 0 6.500 0.0) (layer "F.Fab") hide (effects (font (size 1 1) (thickness 0.15)))) |
| SCH103_OUTPUT | `_EQ_OUT` | `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | 1896 | (property "Value" "L_LF_EQ_OUT" (at 0 3.000 0.0) (layer "F.Fab") hide (effects (font (size 1 1) (thickness 0.15)))) |
| SCH103_OUTPUT | `_EQ_OUT` | `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | 1907 | (property "Value" "L_HF_EQ_OUT" (at 0 3.000 0.0) (layer "F.Fab") hide (effects (font (size 1 1) (thickness 0.15)))) |
| SCH103_OUTPUT | `_EQ_OUT` | `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | 1918 | (property "Value" "L_EQ_OUT" (at 0 3.000 0.0) (layer "F.Fab") hide (effects (font (size 1 1) (thickness 0.15)))) |
| SCH103_OUTPUT | `_EQ_OUT` | `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | 1940 | (property "Value" "R_LF_EQ_OUT" (at 0 3.000 0.0) (layer "F.Fab") hide (effects (font (size 1 1) (thickness 0.15)))) |
| SCH103_OUTPUT | `_EQ_OUT` | `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | 1951 | (property "Value" "R_HF_EQ_OUT" (at 0 3.000 0.0) (layer "F.Fab") hide (effects (font (size 1 1) (thickness 0.15)))) |
| SCH103_OUTPUT | `_EQ_OUT` | `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | 1962 | (property "Value" "R_EQ_OUT" (at 0 3.000 0.0) (layer "F.Fab") hide (effects (font (size 1 1) (thickness 0.15)))) |
| SCH101_NUMERIC | `3.48` | `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | 2336 | (property "Value" "L DIFF 3.48x" (at 0 5.000 0.0) (layer "F.Fab") hide (effects (font (size 1 1) (thickness 0.15)))) |
| SCH101_NUMERIC | `3.48` | `out/pcb/ProjectShellac_Gate3A_Review.kicad_pcb` | 2369 | (property "Value" "R DIFF 3.48x" (at 0 5.000 0.0) (layer "F.Fab") hide (effects (font (size 1 1) (thickness 0.15)))) |
| SCH101_NUMERIC | `DIFF_CONVERTER_GAIN` | `scripts/report_balanced_input_gain.py` | 9 | DIFF_CONVERTER_GAIN, |
| SCH101_NUMERIC | `GAIN_RG_OHM` | `scripts/report_balanced_input_gain.py` | 10 | GAIN_RG_OHM, |
| SCH101_NUMERIC | `DIFF_CONVERTER_GAIN` | `scripts/report_balanced_input_gain.py` | 20 | print(f"Fixed differential converter gain: {DIFF_CONVERTER_GAIN:.4f}x") |
| SCH101_NUMERIC | `GAIN_RG_OHM` | `scripts/report_balanced_input_gain.py` | 21 | print(f"Per-leg Rg: {GAIN_RG_OHM:g} ohm") |
| SCH101_NUMERIC | `3.48` | `tests/test_ae017_dependency_map.py` | 9 | "DIFF_CONVERTER_GAIN = 3.48\nGAIN_RG_OHM = 10000\n", |
| SCH101_NUMERIC | `DIFF_CONVERTER_GAIN` | `tests/test_ae017_dependency_map.py` | 9 | "DIFF_CONVERTER_GAIN = 3.48\nGAIN_RG_OHM = 10000\n", |
| SCH101_NUMERIC | `GAIN_RG_OHM` | `tests/test_ae017_dependency_map.py` | 9 | "DIFF_CONVERTER_GAIN = 3.48\nGAIN_RG_OHM = 10000\n", |
| SCH101_CAD | `R112` | `tests/test_ae017_dependency_map.py` | 13 | 'assert "SW1011"\nassert "R112"\n', |
| SCH101_CAD | `SW1011` | `tests/test_ae017_dependency_map.py` | 13 | 'assert "SW1011"\nassert "R112"\n', |
| SCH101_NUMERIC | `DIFF_CONVERTER_GAIN` | `tests/test_ae017_dependency_map.py` | 18 | assert "DIFF_CONVERTER_GAIN" in tokens |
| SCH101_NUMERIC | `3.48` | `tests/test_ae017_dependency_map.py` | 19 | assert "3.48" in tokens |
| SCH101_CAD | `SW1011` | `tests/test_ae017_dependency_map.py` | 20 | assert "SW1011" in tokens |
| SCH101_CAD | `R112` | `tests/test_ae017_dependency_map.py` | 21 | assert "R112" in tokens |
| DR039 | `DR-039` | `tests/test_ae017_dependency_map.py` | 30 | assert "DR-039 / SCH103" in text |
| SCH101_CAD | `SW1011` | `tests/test_balanced_input.py` | 37 | assert "SW1011" in by_ref |
| SCH101_CAD | `R112` | `tests/test_balanced_input.py` | 38 | assert by_ref["R112"].value == "4420" |
| SCH101_NUMERIC | `4420` | `tests/test_balanced_input.py` | 38 | assert by_ref["R112"].value == "4420" |
| SCH101_CAD | `R113` | `tests/test_balanced_input.py` | 39 | assert by_ref["R113"].value == "8280" |
| SCH101_NUMERIC | `8280` | `tests/test_balanced_input.py` | 39 | assert by_ref["R113"].value == "8280" |
| SCH101_CAD | `R114` | `tests/test_balanced_input.py` | 40 | assert by_ref["R114"].value == "21680" |
| SCH101_NUMERIC | `21680` | `tests/test_balanced_input.py` | 40 | assert by_ref["R114"].value == "21680" |
| SCH101_CAD | `R112` | `tests/test_balanced_input.py` | 47 | base = float(by_ref["R112"].value) |
| SCH101_CAD | `R113` | `tests/test_balanced_input.py` | 48 | assert base + float(by_ref["R113"].value) == 12700.0 |
| SCH101_NUMERIC | `12700` | `tests/test_balanced_input.py` | 48 | assert base + float(by_ref["R113"].value) == 12700.0 |
| SCH101_CAD | `R114` | `tests/test_balanced_input.py` | 49 | assert base + float(by_ref["R114"].value) == 26100.0 |
| SCH101_NUMERIC | `26100` | `tests/test_balanced_input.py` | 49 | assert base + float(by_ref["R114"].value) == 26100.0 |
| SCH101_NUMERIC | `DIFF_CONVERTER_GAIN` | `tests/test_balanced_input_gain.py` | 6 | DIFF_CONVERTER_GAIN, |
| SCH101_NUMERIC | `3.48` | `tests/test_balanced_input_gain.py` | 20 | assert DIFF_CONVERTER_GAIN == pytest.approx(3.48) |
| SCH101_NUMERIC | `DIFF_CONVERTER_GAIN` | `tests/test_balanced_input_gain.py` | 20 | assert DIFF_CONVERTER_GAIN == pytest.approx(3.48) |
| SCH101_NUMERIC | `DIFF_CONVERTER_GAIN` | `tests/test_dr038_dr039.py` | 1 | from generator.model.balanced_input import DIFF_CONVERTER_GAIN, validate_balanced_input |
| DR039 | `post_eq_dc_block` | `tests/test_dr038_dr039.py` | 2 | from generator.model.post_eq_dc_block import cutoff_hz, magnitude_db, validate_post_eq_dc_block |
| ANALYSIS | `sch101_precision_candidate` | `tests/test_dr038_dr039.py` | 3 | from generator.model.sch101_precision_candidate import validate_ae014 |
| SCH101_NUMERIC | `3.48` | `tests/test_dr038_dr039.py` | 8 | assert DIFF_CONVERTER_GAIN == 3.48 |
| SCH101_NUMERIC | `DIFF_CONVERTER_GAIN` | `tests/test_dr038_dr039.py` | 8 | assert DIFF_CONVERTER_GAIN == 3.48 |
| DR039 | `post_eq_dc_block` | `tests/test_dr038_dr039.py` | 16 | validate_post_eq_dc_block() |
| SCH101_CAD | `DIP_Switch_Block` | `tests/test_kicad_writer_instances.py` | 76 | assert "ProjectShellac:DIP_Switch_Block" in embedded_custom_symbol_ids() |
| SCH101_CAD | `DIP_Switch_Block` | `tests/test_kicad_writer_instances.py` | 77 | assert 'symbol "ProjectShellac:DIP_Switch_Block"' in local_symbol_library() |
| SCH103_OUTPUT | `POST_EQ` | `tests/test_pin_connectivity.py` | 89 | "POST_EQ_L", "POST_EQ_R", "FILTERED_L", "FILTERED_R", |
| SCH103_OUTPUT | `POST_EQ` | `tests/test_pin_connectivity.py` | 160 | "PRE_EQ_L", "PRE_EQ_R", "POST_EQ_L", "POST_EQ_R", |
| SCH101_CAD | `DIP_Switch_Block` | `tests/test_pin_connectivity.py` | 166 | dip = Component("SW1", "ProjectShellac:DIP_Switch_Block", "GAIN", Point(100.0, 100.0)) |
| SCH101_CAD | `DIP_Switch_Block` | `tests/test_root_hierarchy.py` | 115 | assert '(symbol "DIP_Switch_Block" ' in custom_library |
| ANALYSIS | `sch101_precision_analysis` | `tests/test_sch101_precision_analysis.py` | 1 | from generator.model.sch101_precision_analysis import ( |
| ANALYSIS | `sch101_precision_candidate` | `tests/test_sch101_precision_candidate.py` | 1 | from generator.model.sch101_precision_candidate import candidate_settings, validate_ae014 |
| SCH103_OUTPUT | `POST_EQ` | `tests/test_sch103_human_readable.py` | 25 | assert {"PRE_EQ_L", "PRE_EQ_R", "POST_EQ_L", "POST_EQ_R"}.issubset(labels) |
| SCH103_OUTPUT | `POST_EQ` | `tests/test_sch107_human_readable.py` | 30 | for name in ("POST_EQ_L", "POST_EQ_R", "FILTERED_L", "FILTERED_R"): |
| ANALYSIS | `signal_chain_analysis` | `tests/test_signal_chain_analysis.py` | 1 | from generator.model.signal_chain_analysis import ( |
| ANALYSIS | `signal_chain_noise_dc` | `tests/test_signal_chain_noise_dc.py` | 1 | from generator.model.signal_chain_noise_dc import ( |
| DR039 | `post_eq_dc_block` | `tests/test_signal_chain_noise_dc.py` | 24 | def test_post_eq_dc_block_collapses_worst_case_offset(): |
| DR039 | `DR-039` | `tools/ae017_dependency_map.py` | 1 | """AE-017 dependency mapper for the DR-038 / DR-039 atomic CAD migration. |
| SCH101_NUMERIC | `DIFF_CONVERTER_GAIN` | `tools/ae017_dependency_map.py` | 15 | "DIFF_CONVERTER_GAIN", |
| SCH101_NUMERIC | `GAIN_RG_OHM` | `tools/ae017_dependency_map.py` | 16 | "GAIN_RG_OHM", |
| SCH101_NUMERIC | `GAIN_BASE_RF_OHM` | `tools/ae017_dependency_map.py` | 17 | "GAIN_BASE_RF_OHM", |
| SCH101_NUMERIC | `GAIN_DEFAULT_ADD_OHM` | `tools/ae017_dependency_map.py` | 18 | "GAIN_DEFAULT_ADD_OHM", |
| SCH101_NUMERIC | `GAIN_HIGH_ADD_OHM` | `tools/ae017_dependency_map.py` | 19 | "GAIN_HIGH_ADD_OHM", |
| SCH101_NUMERIC | `3.48` | `tools/ae017_dependency_map.py` | 20 | "3.48", |
| SCH101_NUMERIC | `4420` | `tools/ae017_dependency_map.py` | 21 | "4420", |
| SCH101_NUMERIC | `8280` | `tools/ae017_dependency_map.py` | 22 | "8280", |
| SCH101_NUMERIC | `21680` | `tools/ae017_dependency_map.py` | 23 | "21680", |
| SCH101_NUMERIC | `12700` | `tools/ae017_dependency_map.py` | 24 | "12700", |
| SCH101_NUMERIC | `26100` | `tools/ae017_dependency_map.py` | 25 | "26100", |
| SCH101_CAD | `SW1011` | `tools/ae017_dependency_map.py` | 28 | "SW1011", |
| SCH101_CAD | `R112` | `tools/ae017_dependency_map.py` | 29 | "R112", |
| SCH101_CAD | `R113` | `tools/ae017_dependency_map.py` | 30 | "R113", |
| SCH101_CAD | `R114` | `tools/ae017_dependency_map.py` | 31 | "R114", |
| SCH101_CAD | `DIP_Switch_Block` | `tools/ae017_dependency_map.py` | 32 | "DIP_Switch_Block", |
| SCH101_CAD | `STEREO GAIN DIP` | `tools/ae017_dependency_map.py` | 33 | "STEREO GAIN DIP", |
| SCH101_CAD | `3.48x differential converter` | `tools/ae017_dependency_map.py` | 34 | "3.48x differential converter", |
| SCH101_NUMERIC | `3.48` | `tools/ae017_dependency_map.py` | 34 | "3.48x differential converter", |
| SCH101_CAD | `10k / 34.8k` | `tools/ae017_dependency_map.py` | 35 | "10k / 34.8k", |
| SCH103_OUTPUT | `TP{base}4` | `tools/ae017_dependency_map.py` | 38 | "TP{base}4", |
| SCH103_OUTPUT | `_EQ_OUT` | `tools/ae017_dependency_map.py` | 39 | "_EQ_OUT", |
| SCH103_OUTPUT | `output_end = Point(420` | `tools/ae017_dependency_map.py` | 40 | "output_end = Point(420", |
| SCH103_OUTPUT | `POST_EQ` | `tools/ae017_dependency_map.py` | 41 | "POST_EQ", |
| SCH103_OUTPUT | `replay_eq.py` | `tools/ae017_dependency_map.py` | 42 | "replay_eq.py", |
| DR039 | `post_eq_dc_block` | `tools/ae017_dependency_map.py` | 45 | "post_eq_dc_block", |
| DR039 | `DR-039` | `tools/ae017_dependency_map.py` | 46 | "DR-039", |
| DR039 | `1.0 µF` | `tools/ae017_dependency_map.py` | 47 | "1.0 µF", |
| DR039 | `1u` | `tools/ae017_dependency_map.py` | 48 | "1u", |
| DR039 | `330k` | `tools/ae017_dependency_map.py` | 49 | "330k", |
| DR039 | `0.48 Hz` | `tools/ae017_dependency_map.py` | 50 | "0.48 Hz", |
| ANALYSIS | `signal_chain_analysis` | `tools/ae017_dependency_map.py` | 53 | "signal_chain_analysis", |
| ANALYSIS | `sch101_precision_candidate` | `tools/ae017_dependency_map.py` | 54 | "sch101_precision_candidate", |
| ANALYSIS | `sch101_precision_analysis` | `tools/ae017_dependency_map.py` | 55 | "sch101_precision_analysis", |
| ANALYSIS | `signal_chain_noise_dc` | `tools/ae017_dependency_map.py` | 56 | "signal_chain_noise_dc", |
| ANALYSIS | `AE-012` | `tools/ae017_dependency_map.py` | 57 | "AE-012", |
| ANALYSIS | `AE-013` | `tools/ae017_dependency_map.py` | 58 | "AE-013", |
| ANALYSIS | `AE-014` | `tools/ae017_dependency_map.py` | 59 | "AE-014", |
| ANALYSIS | `AE-015` | `tools/ae017_dependency_map.py` | 60 | "AE-015", |
| DR039 | `DR-039` | `tools/ae017_dependency_map.py` | 129 | "# AE-017 Generated DR-038 / DR-039 Dependency Map", |
| ANALYSIS | `AE-012` | `tools/ae017_dependency_map.py` | 171 | "9. AE-012 headroom regression;", |
| ANALYSIS | `AE-013` | `tools/ae017_dependency_map.py` | 172 | "10. AE-013/014 noise/CMRR regression.", |
| DR039 | `DR-039` | `tools/ae017_dependency_map.py` | 174 | "### DR-039 / SCH103", |
| DR039 | `0.48 Hz` | `tools/ae017_dependency_map.py` | 183 | "6. replay-curve regression including the ~0.48 Hz pole;", |
| ANALYSIS | `AE-012` | `tools/ae017_dependency_map.py` | 184 | "7. AE-012 headroom update;", |
| ANALYSIS | `AE-015` | `tools/ae017_dependency_map.py` | 185 | "8. AE-015 DC/noise update;", |
