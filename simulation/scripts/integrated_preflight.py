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
