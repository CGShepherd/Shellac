from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
CFG = ROOT / "simulation/config/integrated_baseline.yaml"

def main():
    data = yaml.safe_load(CFG.read_text(encoding="utf-8"))
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

    if errors:
        print("AE-060 integrated preflight: CONTRACT ERROR")
        for e in errors:
            print("ERROR:", e)
        return 1

    unresolved = [x["id"] for x in data["required_model_sources"] if x["status"] != "RESOLVED"]
    print("AE-060 integrated preflight: contract coherent.")
    if unresolved:
        print("Integrated RUN00 remains BLOCKED. Unresolved controlled model sources:")
        for item in unresolved:
            print("  -", item)
        print("This is expected at AE-060 and prevents false integrated-model authority.")
        return 2

    print("Model-source gate resolved; SHELLAC_TOP implementation may proceed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
