"""AE-076F1F informational mechanical evidence, not release authority."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_ae076f1f_continuity_tracks_real_pcb_not_phantom_switches():
    state = (ROOT / "PROJECT_SHELLAC_WORKING_STATE.md").read_text(encoding="utf-8")
    risk = (ROOT / "docs/knowledge/RISK_REGISTER.md").read_text(encoding="utf-8")
    evidence = (ROOT / "docs/design_pack/AE-076F1F_Native_Control_and_Mechanical_Evidence_Rev_A0.md").read_text(encoding="utf-8")
    assert "24899753d05597aedd7a2ced6a482e6e1001c705" in state
    assert "AE-076F1E" in state
    # F1F remains historical native-PCB evidence, not a perpetual current state.
    assert "AE-076F1F" in state
    current = [line for line in state.splitlines()
               if line.startswith("- Current transaction state: ")]
    assert len(current) == 1
    assert "AE076F1F_EVIDENCE_RECONCILED_PHYSICAL_QUALIFICATION_HELD" not in current[0]
    assert "- Historical transaction state: AE076E_B_PROMOTED_AE076F_QUALIFICATION_AND_MCAD_HELD" in state
    assert "Routing: HELD" in state
    assert "Manufacturing release: FALSE" in state
    for token in ("R-006", "R-012", "AE-076F1E"):
        assert token in risk
    for token in ("256 current native footprints", "No native switch footprints", "7.657547 mm",
                  "NOT", "MH1", "MH4", "+17.0 V / 0VA / -17.0 V", "routing HELD"):
        assert token in evidence
