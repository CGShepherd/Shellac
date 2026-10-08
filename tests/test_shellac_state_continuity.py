from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
GUIDANCE=ROOT/"PROJECT_GUIDANCE.md"
STATE=ROOT/"PROJECT_SHELLAC_WORKING_STATE.md"
STANDARD=ROOT/"docs/knowledge/ONE_OFF_BUILD_RECOVERABILITY_STANDARD.md"
AUTH=ROOT/"config/decisions/document_authority.yaml"
HOLD=ROOT/"config/release/ae071_prerouting_hold.yaml"
RISK=ROOT/"docs/knowledge/RISK_REGISTER.md"

def test_persistent_state_is_mandatory_but_not_design_authority():
    g=GUIDANCE.read_text(encoding="utf-8")
    s=STATE.read_text(encoding="utf-8")
    a=yaml.safe_load(AUTH.read_text(encoding="utf-8"))
    assert "PROJECT_SHELLAC_WORKING_STATE.md" in g
    assert "NON-AUTHORITATIVE SUMMARY" in s
    assert "PROJECT_SHELLAC_WORKING_STATE.md" not in a["current_authority"]

def test_one_off_recoverability_standard_is_current_authority():
    a=yaml.safe_load(AUTH.read_text(encoding="utf-8"))
    assert "docs/knowledge/ONE_OFF_BUILD_RECOVERABILITY_STANDARD.md" in a["current_authority"]
    text=STANDARD.read_text(encoding="utf-8")
    for token in ("CLOSE_BEFORE_FAB","ESCAPE_ROUTE_REQUIRED","BENCH_ONLY_ACCEPTABLE","PASS_WITH_CONTROLLED_RECOVERY"):
        assert token in text

def test_state_repeats_critical_fail_closed_invariants():
    s=STATE.read_text(encoding="utf-8")
    assert "258751f56f536cc28e836c2d013dbde46aaf4cb6" in s
    assert "+17.0 V / 0VA / -17.0 V" in s
    assert "AE-076E-A" in s
    assert "AE-076E-B" in s
    assert "NATIVE_MIGRATED_SOLID_MODEL_EXPORT_VALIDATED_GOVERNANCE_PENDING" in s
    assert "Routing: HELD" in s
    assert "Manufacturing release: FALSE" in s

def test_current_hold_remains_fail_closed():
    h=yaml.safe_load(HOLD.read_text(encoding="utf-8"))
    assert not h["permissions"]["final_routing"]
    assert not h["permissions"]["layout_freeze"]
    assert not h["permissions"]["bom_freeze"]
    assert not h["permissions"]["manufacturing_release"]

def test_recoverability_risk_is_registered():
    text=RISK.read_text(encoding="utf-8")
    assert "| R-038 |" in text
    assert "one-off" in text.lower()
    assert "escape route" in text.lower()
