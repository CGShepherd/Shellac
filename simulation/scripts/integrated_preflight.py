from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parents[2]
CFG = ROOT / "simulation/config/integrated_baseline.yaml"
QUAL = ROOT / "simulation/config/model_qualification.yaml"

SOURCE_MAP = {
    "LT5400": ("LT5400", {"QUALIFIED_LOCAL_LIBRARY_SOURCE"}),
    "OPA1612": ("OPA1612", {"QUALIFIED_LOCAL_SOURCE"}),
    "OPA1656": ("OPA1656", {"QUALIFIED_LOCAL_SOURCE"}),
    "THAT1646": ("THAT1646", {"QUALIFIED_LOCAL_SOURCE"}),
    "DIODE_S1G": ("S1G", {"QUALIFIED_LOCAL_REFERENCE_SOURCE"}),
    "CARTRIDGE_GRADO_78C": ("GRADO_78C", {"QUALIFIED_BEHAVIOURAL_REFERENCE_MODEL"}),
    "CARTRIDGE_AT_VM95SP": ("AT_VM95SP", {"QUALIFIED_BEHAVIOURAL_REFERENCE_MODEL"}),
}

def main():
    data = yaml.safe_load(CFG.read_text(encoding="utf-8"))
    qual = yaml.safe_load(QUAL.read_text(encoding="utf-8"))
    errors = []

    if data["top_level"] != "SHELLAC_TOP":
        errors.append("top_level must be SHELLAC_TOP")
    if data["nominal_rails_v"] != {"plus": 18.0, "minus": -18.0}:
        errors.append("nominal rails must remain +/-18 V")
    sem = data["model_semantics"]
    if sem["integrated_spice"] != "SELECTED_NEXT_CANDIDATE_ANALYSIS":
        errors.append("integrated model semantics invalid")
    if sem["generator_migration_implied"] is not False:
        errors.append("integrated model must not imply generator migration")
    mute = data["selected_next_contract"]["mute"]
    if mute["type"] != "MECHANICAL_DPDT_INPUT_MUTE" or mute["automatic_sequencing"] is not False:
        errors.append("mute contract invalid")

    qualification_sources = qual.get("sources", {})
    unresolved = []
    for source in data["required_model_sources"]:
        source_id = source["id"]
        if source.get("status") != "RESOLVED":
            unresolved.append(f"{source_id}: integrated status={source.get('status')}")
            continue
        if source_id not in SOURCE_MAP:
            unresolved.append(f"{source_id}: no qualification mapping")
            continue
        qual_id, allowed = SOURCE_MAP[source_id]
        actual = qualification_sources.get(qual_id, {}).get("status")
        if actual not in allowed:
            unresolved.append(f"{source_id}: qualification status={actual!r}")

    run00 = data["integrated_run00"]
    run00_status = run00.get("status")
    if run00_status == "READY_FOR_SHELLAC_TOP_IMPLEMENTATION":
        if run00.get("shellac_top_implemented") is not False:
            errors.append("pre-AE065 state must not claim SHELLAC_TOP is implemented")
        if run00.get("shellac_top_run00_executed") is not False:
            errors.append("pre-AE065 state must not claim integrated RUN00 has executed")
    elif run00_status == "PASSED_NOMINAL_SANITY":
        if run00.get("authority") != "AE-065":
            errors.append("PASSED_NOMINAL_SANITY requires AE-065 authority")
        if run00.get("shellac_top_implemented") is not True:
            errors.append("AE-065 passed state requires SHELLAC_TOP implementation")
        if run00.get("shellac_top_run00_executed") is not True:
            errors.append("AE-065 passed state requires genuine integrated RUN00 execution")
        result_rel = run00.get("result_record")
        if not result_rel:
            errors.append("AE-065 passed state requires a RUN00 result record")
        else:
            result_path = ROOT / result_rel
            if not result_path.is_file():
                errors.append("AE-065 RUN00 result record is missing")
            else:
                try:
                    result = json.loads(result_path.read_text(encoding="utf-8"))
                except Exception as exc:
                    errors.append(f"AE-065 RUN00 result record is unreadable: {exc}")
                else:
                    if result.get("authority") != "AE-065":
                        errors.append("AE-065 RUN00 result authority mismatch")
                    if result.get("run_id") != "RUN00_INTEGRATED":
                        errors.append("AE-065 RUN00 result run_id mismatch")
                    if result.get("pass") is not True:
                        errors.append("AE-065 RUN00 result is not PASS")
    else:
        errors.append(f"integrated RUN00 has uncontrolled status {run00_status!r}")

    integrated_ac_campaign = data.get("integrated_ac_campaign")
    if integrated_ac_campaign is not None:
        if integrated_ac_campaign.get("authority") != "AE-066":
            errors.append("integrated AC campaign requires AE-066 authority")
        if integrated_ac_campaign.get("generator_migration_implied") is not False:
            errors.append("AE-066 integrated AC campaign must not imply generator migration")
        summary_rel = integrated_ac_campaign.get("result_summary")
        if not summary_rel:
            errors.append("AE-066 integrated AC campaign requires a result summary")
        else:
            summary_path = ROOT / summary_rel
            if not summary_path.is_file():
                errors.append("AE-066 result summary is missing")
            else:
                try:
                    ac_summary = json.loads(summary_path.read_text(encoding="utf-8"))
                except Exception as exc:
                    errors.append(f"AE-066 result summary is unreadable: {exc}")
                else:
                    if ac_summary.get("authority") != "AE-066":
                        errors.append("AE-066 result summary authority mismatch")
                    if ac_summary.get("hard_gate_pass") is not True:
                        errors.append("AE-066 hard gate is not PASS")
                    if ac_summary.get("generator_migration_implied") is not False:
                        errors.append("AE-066 result incorrectly implies generator migration")
                    expected = {
                        "run01_status": ac_summary.get("run01", {}).get("status"),
                        "run02_status": ac_summary.get("run02", {}).get("status"),
                        "run03_status": ac_summary.get("run03", {}).get("status"),
                    }
                    for key, value in expected.items():
                        if integrated_ac_campaign.get(key) != value:
                            errors.append(f"AE-066 {key} does not match result summary")

    run04_lf_trade = data.get("run04_lf_trade")
    if run04_lf_trade is not None:
        if run04_lf_trade.get("authority") != "AE-067":
            errors.append("RUN04 LF trade requires AE-067 authority")
        if run04_lf_trade.get("status") != "SELECTED_BRANCH_LOCAL_QUALIFICATION_OPEN":
            errors.append("RUN04 LF trade has uncontrolled status")
        if run04_lf_trade.get("selected_topology") != "BRANCH_LOCAL_DIRECT_BYPASS_BLOCK":
            errors.append("AE-067 selected topology mismatch")
        if run04_lf_trade.get("generator_migration_implied") is not False:
            errors.append("AE-067 must not imply generator migration")
        result_rel = run04_lf_trade.get("result_record")
        if not result_rel:
            errors.append("AE-067 requires a RUN04 result record")
        else:
            result_path = ROOT / result_rel
            if not result_path.is_file():
                errors.append("AE-067 RUN04 result record is missing")
            else:
                try:
                    run04 = json.loads(result_path.read_text(encoding="utf-8"))
                except Exception as exc:
                    errors.append(f"AE-067 RUN04 result unreadable: {exc}")
                else:
                    if run04.get("authority") != "AE-067" or run04.get("run_id") != "RUN04":
                        errors.append("AE-067 RUN04 authority/run_id mismatch")
                    if run04.get("generator_migration_implied") is not False:
                        errors.append("AE-067 result incorrectly implies generator migration")
                    cases = run04.get("candidates", {})
                    branch = cases.get("BRANCH_LOCAL_DIRECT_BYPASS_BLOCK", {})
                    post = cases.get("POST_SWITCH_COMMON", {})
                    current = cases.get("CURRENT_COMMON_PRE_SPLIT", {})
                    scale10 = cases.get("RUMBLE_SCALE10_COMMON_1P2UF", {})
                    if branch.get("ac", {}).get("lf_hard_pass") is not True:
                        errors.append("AE-067 branch-local LF gate is not PASS")
                    if branch.get("switch", {}).get("internal_selector_objective_pass") is not True:
                        errors.append("AE-067 branch-local switch discriminator is not PASS")
                    settle = branch.get("offset_step", {}).get("direct_settle_to_1pct_s_after_step")
                    if settle is None or not (1.55 <= settle <= 1.65):
                        errors.append("AE-067 branch-local settling evidence mismatch")
                    if post.get("switch", {}).get("internal_selector_objective_pass") is not False:
                        errors.append("AE-067 post-switch reject evidence missing")
                    if current.get("ac", {}).get("lf_hard_pass") is not False:
                        errors.append("AE-067 current-common reject evidence missing")
                    if scale10.get("ac", {}).get("lf_hard_pass") is not False:
                        errors.append("AE-067 x10 reject evidence missing")
        dr039 = data.get("selected_next_contract", {}).get("dr039_sch107", {})
        if dr039.get("authority") != "AE-067":
            errors.append("DR039 selected-next contract requires AE-067 authority")
        if dr039.get("selected_topology") != run04_lf_trade.get("selected_topology"):
            errors.append("DR039 contract and RUN04 selected topology disagree")
        if dr039.get("status") != "CURRENT_SELECTED_PENDING_IMPLEMENTATION":
            errors.append("DR039 contract status mismatch")
        if dr039.get("generator_migration_implied") is not False:
            errors.append("DR039 selected-next contract must not imply generator migration")

    run05_matrix = data.get("run05_matrix")
    if run05_matrix is not None:
        if run05_matrix.get("authority") != "AE-068":
            errors.append("RUN05 matrix requires AE-068 authority")
        if run05_matrix.get("status") != "QUALIFIED_STEADY_STATE_TRANSIENT_OPEN":
            errors.append("RUN05 matrix has uncontrolled status")
        if run05_matrix.get("architecture") != "AE041_A1_3P4T_PASSIVE_MATRIX":
            errors.append("AE-068 matrix architecture mismatch")
        if run05_matrix.get("generator_migration_implied") is not False:
            errors.append("AE-068 must not imply generator migration")
        if run05_matrix.get("input_return_ohm") != 2200000:
            errors.append("AE-068 input-return contract mismatch")
        if run05_matrix.get("mono_resistor_ohm") != 4700:
            errors.append("AE-068 mono-resistor contract mismatch")
        result_rel = run05_matrix.get("result_record")
        if not result_rel:
            errors.append("AE-068 requires a RUN05 result record")
        else:
            result_path = ROOT / result_rel
            if not result_path.is_file():
                errors.append("AE-068 RUN05 result record is missing")
            else:
                try:
                    run05 = json.loads(result_path.read_text(encoding="utf-8"))
                except Exception as exc:
                    errors.append(f"AE-068 RUN05 result unreadable: {exc}")
                else:
                    if run05.get("authority") != "AE-068" or run05.get("run_id") != "RUN05":
                        errors.append("AE-068 RUN05 authority/run_id mismatch")
                    if run05.get("generator_migration_implied") is not False:
                        errors.append("AE-068 result incorrectly implies generator migration")
                    direct = run05.get("direct_insertion", {})
                    mono = run05.get("mono_nominal", {})
                    xtalk = run05.get("stereo_crosstalk", {})
                    if direct.get("pass") is not True:
                        errors.append("AE-068 direct insertion is not PASS")
                    if mono.get("hard_pass") is not True or mono.get("preferred_pass") is not True:
                        errors.append("AE-068 mono steady-state gate is not PASS")
                    if xtalk.get("hard_pass") is not True:
                        errors.append("AE-068 crosstalk gate is not PASS")
                    ps = xtalk.get("parasitic_sweep_pf", {}).get("10.0", {})
                    l20 = ps.get("l_to_r_separation_db", {}).get("20000")
                    r20 = ps.get("r_to_l_separation_db", {}).get("20000")
                    if l20 is None or r20 is None or min(l20, r20) <= 60.0:
                        errors.append("AE-068 10 pF 20 kHz parasitic bracket evidence missing/failing")
                    mm = run05.get("mono_pair_mismatch_sweep", {})
                    if mm.get("0.25", {}).get("pass_max_0p25_percent") is not True:
                        errors.append("AE-068 0.25% mono-pair matching evidence missing")
                    if mm.get("0.5", {}).get("pass_max_0p25_percent") is not False:
                        errors.append("AE-068 0.5% mono-pair rejection evidence missing")


    run06_output = data.get("run06_output")
    if run06_output is not None:
        if run06_output.get("authority") != "AE-069":
            errors.append("RUN06 output requires AE-069 authority")
        if run06_output.get("status") != "SIMULATION_EVIDENCE_COMPLETE_BENCH_GATES_OPEN":
            errors.append("RUN06 output has uncontrolled status")
        if run06_output.get("generator_migration_implied") is not False:
            errors.append("AE-069 must not imply generator migration")
        if run06_output.get("ferrite_selected") is not False:
            errors.append("AE-069 must not freeze a ferrite")
        if run06_output.get("sense_capacitor_mechanical_freeze") is not False:
            errors.append("AE-069 must not freeze sense-cap mechanical implementation")
        if run06_output.get("transient_stability_reproducibly_qualified") is not False:
            errors.append("AE-069 must retain transient stability bench gate")
        if run06_output.get("bench_load_stability_required") is not True:
            errors.append("AE-069 load-stability bench obligation missing")
        if run06_output.get("dynamic_large_signal_thd_qualified") is not False:
            errors.append("AE-069 must not claim dynamic large-signal THD qualification")
        if run06_output.get("bench_dynamic_thd_required") is not True:
            errors.append("AE-069 dynamic-THD bench obligation missing")
        result_rel = run06_output.get("result_record")
        if not result_rel:
            errors.append("AE-069 requires a RUN06 result record")
        else:
            result_path = ROOT / result_rel
            if not result_path.is_file():
                errors.append("AE-069 RUN06 result record is missing")
            else:
                try:
                    run06 = json.loads(result_path.read_text(encoding="utf-8"))
                except Exception as exc:
                    errors.append(f"AE-069 RUN06 result unreadable: {exc}")
                else:
                    if run06.get("authority") != "AE-069" or run06.get("run_id") != "RUN06":
                        errors.append("AE-069 RUN06 authority/run_id mismatch")
                    if run06.get("status") != "SIMULATION_EVIDENCE_COMPLETE_BENCH_GATES_OPEN_REVIEW_REQUIRED":
                        errors.append("AE-069 RUN06 result status mismatch")
                    if run06.get("generator_migration_implied") is not False:
                        errors.append("AE-069 result incorrectly implies generator migration")
                    gates = run06.get("analysis", {}).get("gates", {})
                    if gates.get("simulation_evidence_complete") is not True:
                        errors.append("AE-069 reproducible simulation evidence is not complete")
                    if gates.get("run06_fully_qualified") is not False:
                        errors.append("AE-069 result incorrectly claims RUN06 full qualification")
                    if gates.get("transient_stability_reproducibly_qualified") is not False:
                        errors.append("AE-069 result incorrectly claims transient stability qualification")
                    if gates.get("bench_load_stability_required") is not True:
                        errors.append("AE-069 result missing bench load-stability gate")
                    if gates.get("transient_large_signal_thd_qualified") is not False:
                        errors.append("AE-069 result incorrectly claims dynamic THD qualification")
                    if gates.get("bench_dynamic_thd_required") is not True:
                        errors.append("AE-069 result missing bench dynamic-THD gate")
                    execution = run06.get("execution", {})
                    if execution.get("headroom_input_rms_v") != [0.321, 3.21, 5.0]:
                        errors.append("AE-069 validated quasi-static input envelope mismatch")


    run07_end_to_end = data.get("run07_end_to_end")
    if run07_end_to_end is not None:
        if run07_end_to_end.get("authority") != "AE-070":
            errors.append("RUN07 end-to-end requires AE-070 authority")
        if run07_end_to_end.get("status") != "QUALIFIED_NOMINAL_REPRESENTATIVE_STATES":
            errors.append("RUN07 end-to-end has uncontrolled status")
        if run07_end_to_end.get("generator_migration_implied") is not False:
            errors.append("AE-070 must not imply generator migration")
        if run07_end_to_end.get("ferrite_selected") is not False:
            errors.append("AE-070 must not select a ferrite")
        if run07_end_to_end.get("nominal_lr_tracking_semantics") != "NOMINAL_MODEL_SYMMETRY_ONLY":
            errors.append("AE-070 nominal L/R symmetry semantics mismatch")
        if run07_end_to_end.get("tolerance_tracking_deferred_to") != ["RUN10", "RUN11"]:
            errors.append("AE-070 tolerance tracking deferral mismatch")

        result_rel = run07_end_to_end.get("result_record")
        phase_rel = run07_end_to_end.get("phase_correlation_record")
        comp_rel = run07_end_to_end.get("model_composition_discriminator_record")
        for label, relpath in (("RUN07", result_rel), ("phase", phase_rel), ("composition", comp_rel)):
            if not relpath or not (ROOT / relpath).is_file():
                errors.append(f"AE-070 {label} evidence record is missing")

        if result_rel and (ROOT / result_rel).is_file():
            try:
                run07 = json.loads((ROOT / result_rel).read_text(encoding="utf-8"))
            except Exception as exc:
                errors.append(f"AE-070 RUN07 result unreadable: {exc}")
            else:
                if run07.get("authority") != "AE-070" or run07.get("run_id") != "RUN07":
                    errors.append("AE-070 RUN07 authority/run_id mismatch")
                if run07.get("status") != "QUALIFIED_NOMINAL_REPRESENTATIVE_STATES":
                    errors.append("AE-070 RUN07 status mismatch")
                if run07.get("generator_migration_implied") is not False:
                    errors.append("AE-070 RUN07 incorrectly implies generator migration")
                gates = run07.get("gates", {})
                if gates.get("run07_nominal_ac_pass") is not True:
                    errors.append("AE-070 RUN07 nominal AC gate is not PASS")
                if gates.get("overload_qualified") is not False:
                    errors.append("AE-070 must defer overload to RUN08")
                if gates.get("noise_qualified") is not False:
                    errors.append("AE-070 must defer noise to RUN09")
                if gates.get("ferrite_selected") is not False:
                    errors.append("AE-070 result must not select ferrite")
                if run07.get("model_composition_discriminator", {}).get("pattern_match") is not True:
                    errors.append("AE-070 composition discriminator is not PASS in RUN07 result")

        if phase_rel and (ROOT / phase_rel).is_file():
            phase = json.loads((ROOT / phase_rel).read_text(encoding="utf-8"))
            if phase.get("acceptance", {}).get("pass") is not True:
                errors.append("AE-070 output phase correlation is not PASS")

        if comp_rel and (ROOT / comp_rel).is_file():
            comp = json.loads((ROOT / comp_rel).read_text(encoding="utf-8"))
            if comp.get("status") != "MODEL_COMPOSITION_LIMIT_CONFIRMED" or comp.get("pattern_match") is not True:
                errors.append("AE-070 controlled composition discriminator is not PASS")

    if errors:
        print("Integrated preflight: CONTRACT ERROR")
        for e in errors:
            print("ERROR:", e)
        return 1

    print("Integrated preflight: contract coherent.")
    if unresolved:
        print("Integrated RUN00 remains BLOCKED. Unresolved controlled model sources:")
        for item in unresolved:
            print("  -", item)
        return 2

    print("Model-source gate RESOLVED by controlled qualification evidence.")
    if run00_status == "PASSED_NOMINAL_SANITY":
        print("SHELLAC_TOP implemented; genuine integrated RUN00 nominal sanity PASSED.")
        if integrated_ac_campaign is not None:
            print(
                "AE-066 RUN01-RUN03 campaign evidence present: "
                + str(integrated_ac_campaign.get("status"))
            )
            if run04_lf_trade is not None:
                print("AE-067 RUN04 selected topology: " + str(run04_lf_trade.get("selected_topology")))
                if run05_matrix is not None:
                    print("AE-068 RUN05 matrix steady-state qualification: " + str(run05_matrix.get("status")))
                    if run06_output is not None:
                        print("AE-069 RUN06 simulation evidence: " + str(run06_output.get("status")))
                        if run07_end_to_end is not None:
                            print("AE-070 RUN07 nominal end-to-end evidence: " + str(run07_end_to_end.get("status")))
                            print("RUN08-RUN14 remain; RUN06 load-stability/dynamic-THD bench gates remain under R-024.")
                        else:
                            print("RUN07-RUN14 remain; RUN06 load-stability/dynamic-THD bench gates remain under R-024.")
                    else:
                        print("RUN06-RUN14 and explicit open findings remain under R-024.")
                else:
                    print("RUN05-RUN14 and explicit open findings remain under R-024.")
            else:
                print("RUN04-RUN14 and explicit open findings remain under R-024.")
        else:
            print("Full RUN01-RUN14 qualification remains open.")
    else:
        print("SHELLAC_TOP implementation may proceed; integrated RUN00 has NOT yet executed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
