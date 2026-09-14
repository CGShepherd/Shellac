from pathlib import Path
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
    if run00.get("shellac_top_implemented") is not False:
        errors.append("AE-064 must not claim SHELLAC_TOP is implemented")
    if run00.get("shellac_top_run00_executed") is not False:
        errors.append("AE-064 must not claim integrated RUN00 has executed")

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
    print("SHELLAC_TOP implementation may proceed; integrated RUN00 has NOT yet executed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
