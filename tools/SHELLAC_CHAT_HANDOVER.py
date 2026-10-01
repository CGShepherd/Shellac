#!/usr/bin/env python3
"""Project Shellac persistent chat/phase handover.

This file is a process-continuity aid only. It is NOT electrical, mechanical,
PCB, BOM, qualification, release, or manufacturing authority.

If this handover conflicts with controlled repository evidence, the controlled
repository wins. Read PROJECT_GUIDANCE.md and current configuration authority
before acting.

Maintenance policy:
- update at governed phase transitions;
- during a long phase, add only material decisions, newly discovered technical
  debt, and next-action changes;
- prune resolved working detail instead of accumulating an endless transcript;
- rely on Git history for prior handover states;
- never rewrite historical engineering evidence merely to simplify a handover.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]

MAINTAINED = {
    "project": "Shellac",
    "handover_schema": 1,
    "classification": "PROCESS_CONTINUITY_ONLY_NOT_ENGINEERING_AUTHORITY",
    "governed_increment_described": "AE-076B",
    "previous_governed_baseline": "817297ed7cccfdbaaa4c0ee3360d5c8ac3fdc35d",
    "next_phase": "AE-076B2_DIMENSIONALLY_CONTROLLED_MCAD_DIGITAL_MOCKUP",
    "working_method": {
        "default_execution": "normal ChatGPT plus connected tools; bounded fail-closed scripts for user to run locally",
        "do_not_auto_escalate_to_codex_or_work": True,
        "response_tail": ["Confidence: NN%", "Chat runway: High/Moderate/Short/Critical"],
        "review_style": "challenge assumptions; distinguish evidence, analysis, judgement and unresolved hypothesis",
        "language": "British English",
    },
    "read_first": [
        "PROJECT_GUIDANCE.md",
        "config/decisions/current_decision_index.yaml",
        "config/decisions/document_authority.yaml",
        "config/release/ae071_prerouting_hold.yaml",
        "docs/knowledge/DESIGN_PACK_INDEX.md",
        "docs/knowledge/RISK_REGISTER.md",
        "docs/knowledge/INDEPENDENT_REVIEW_AND_DESIGN_ASSURANCE_PLAN.md",
        "config/mechanical/ae076b_control_service_module.yaml",
        "docs/design_pack/AE-076B_Control_Service_Module_Architecture_Supersession_Rev_A0.md",
    ],
    "latest_validation": {
        "candidate_log": "logs/current/84_AE076B1_CONTROL_SERVICE_MODULE_ARCHITECTURE_FIX2.log",
        "promotion_log": "logs/current/85_AE076B1_CREATE_HANDOVER_AND_PROMOTE.log",
        "focused_tests_passed_before_promotion": 64,
        "full_tests_passed_before_promotion": 729,
        "configuration_audit": "PASS",
        "integrated_preflight": "PASS",
        "native_board_integrity": "PASS",
        "protected_physical_historical_artefacts": "9_BYTE_IDENTICAL",
        "git_diff_check": "PASS",
    },
    "absolute_do_not_regress": [
        "Current regulated rail authority is +17.0 V / 0VA / -17.0 V; historical +/-18 V evidence is provenance only.",
        "Routing authority remains FALSE until explicitly released.",
        "AE-075D/E/F and other historical records remain provenance and are not rewritten to match later architecture.",
        "Do not treat SR-040/AE-071B MH1-MH4 as the selected final support architecture after AE-076B; they are interim physical CAD pending AE-076B2.",
        "Do not invent a 14.5 mm or other common C&K/NKK PCB plane. NKK 12.3 mm is controlled; C&K installed-plane compatibility remains to be proven.",
        "Do not begin final/manual PCB placement acceptance or routing before the AE-076B2 dimensional mechanical gate closes.",
    ],
    "ae076b_selected_architecture": {
        "main_audio_pcb_count": 1,
        "all_seven_controls_direct_main_pcb": True,
        "service_module": "REMOVABLE_UPPER_COVER_PLUS_MAIN_PCB_PLUS_CONTROLS",
        "primary_supports_selected": 6,
        "support_relationship": "PCB_TO_REMOVABLE_UPPER_COVER",
        "support_xy_frozen": False,
        "support_z_tolerance_frozen": False,
        "aluminium_carrier_selected": False,
        "local_control_pcbs": "NONE",
        "control_interboard_harnesses": "NONE",
        "front_input_xlr_looms": "SHORT_DETACHABLE_RETAINED",
        "rear_output_xlr_looms": "SHORT_DETACHABLE_RETAINED",
        "rear_dc_loom": "SHORT_DETACHABLE_RETAINED",
        "nkk_installed_panel_to_pcb_mm": 12.3,
        "ck_installed_pcb_plane_verified": False,
        "native_pcb_physical_state": "INTERIM_SR040_AE071B_MH1_MH4",
    },
    "ae076b2_mcad_gate": {
        "preferred_toolchain": "FreeCAD plus KiCadStepUp; KiCad remains PCB authority and supplies PCB STEP geometry",
        "governance": "controlled datums/config drive the assembly; MCAD visualises/checks them rather than becoming electrical authority",
        "assembly_minimum": [
            "METCASE M5502119 enclosure body, removable top/base and front/rear panels",
            "current KiCad PCB STEP including significant component envelopes",
            "all seven NKK/C&K controls",
            "front input XLRs, rear output XLRs and rear DC connector",
            "six candidate PCB-to-upper-cover supports",
            "panel/connector intrusion volumes",
            "short-looms/service-removal envelopes",
        ],
        "required_reviews": [
            "top plan with cover removed",
            "upper-cover/underside view",
            "front elevation",
            "rear elevation",
            "longitudinal section through controls/PCB",
            "transverse section through the critical NKK/C&K stack",
            "exploded/service view",
            "clearance/interference and bottom-off commissioning access review",
        ],
        "must_close_before_native_migration": [
            "C&K A30403RNCB and 7201SYCBE fit at the rigid PCB plane constrained by NKK 12.3 mm evidence",
            "six-support XY/Z/hardware/tolerance stack",
            "exact control footprints, pin maps, courtyards and 3D/body envelopes",
            "control XY, panel apertures and keep-outs",
            "service/removal load path and accessibility",
        ],
    },
    "current_routing_blockers": {
        "AE071-B03": "AE-076B2 MCAD/control/support/footprint/physical migration and RUN10 switch-local parasitics",
        "AE071-B04": "LT5400B complete-stage RUN10 tolerance/CMRR and 20 kHz parasitic acceptance",
        "AE071-B08": "SCH101 service-shunt pairing/orientation and short symmetric load-header parasitic/layout verification",
    },
    "system_release_open": [
        "External PSU powered set-point/dropout/ripple/startup/fault/thermal qualification under RUN13/RUN14 and bench work",
        "RUN06 prototype load/cable stability and dynamic THD bench gates",
        "RUN08-RUN14 as applicable",
        "Grado extended-band open finding and final bench correlation",
        "PRE90 high-level clean hardware/operating correlation",
    ],
    "review_panel": [
        "Principal Analogue Designer",
        "Hostile Design Reviewer",
        "PCB / EMC Engineer",
        "Mechanical / Integration Engineer",
        "Component and Procurement Engineer",
        "Reliability / FMEA Engineer",
        "Verification and Test Engineer",
        "Manufacturing / DFM Engineer",
        "Service / Repair Engineer",
        "Configuration and Release Authority",
        "Design Assurance Challenger",
        "Independent Chief Engineer",
    ],
    "cross_cut_review_personas": [
        "QUAD-style Audio Technical Authority",
        "HP/Agilent/Keysight-style Instrument Technical Authority",
        "Airbus Civil-style Technical Design Authority",
    ],
    "next_actions": [
        "Confirm AE-076B promotion is a clean governed baseline.",
        "Create AE-076B2 mechanical datum/config schema and MCAD repository structure.",
        "Obtain/control manufacturer geometry for M5502119, NKK/C&K controls, XLRs and DC connector.",
        "Export/import the current KiCad PCB through STEP without treating MCAD as PCB electrical authority.",
        "Build the first dimensionally accurate assembly before accepting manual component placement.",
        "Run independent mechanical/PCB/DFM/service review on the same frozen digital mock-up.",
        "Only after dimensional closure migrate MH/support/control geometry into native KiCad.",
    ],
}


def _git(*args: str) -> tuple[int, str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return proc.returncode, proc.stdout.strip()


def live_state() -> dict:
    branch_rc, branch = _git("branch", "--show-current")
    head_rc, head = _git("rev-parse", "HEAD")
    origin_rc, origin = _git("rev-parse", "origin/develop")
    subject_rc, subject = _git("show", "-s", "--format=%s", "HEAD")
    status_rc, status = _git("status", "--porcelain=v1", "--untracked-files=all")
    tracked_rc, _ = _git("ls-files", "--error-unmatch", "tools/SHELLAC_CHAT_HANDOVER.py")

    clean = status_rc == 0 and status == ""
    synced = head_rc == 0 and origin_rc == 0 and head == origin
    tracked = tracked_rc == 0

    if tracked and clean and synced:
        state_class = "GOVERNED_TRACKED_CLEAN_AND_SYNCED"
    elif tracked:
        state_class = "TRACKED_BUT_WORKING_OR_REMOTE_STATE_REQUIRES_REVIEW"
    else:
        state_class = "UNTRACKED_CANDIDATE_OR_PRECOMMIT_STATE"

    return {
        "repository_root": str(ROOT),
        "state_class": state_class,
        "branch": branch if branch_rc == 0 else None,
        "head": head if head_rc == 0 else None,
        "head_subject": subject if subject_rc == 0 else None,
        "origin_develop": origin if origin_rc == 0 else None,
        "head_equals_origin_develop": synced,
        "handover_is_tracked": tracked,
        "worktree_clean": clean,
        "git_status_short": status.splitlines() if status else [],
    }


def render_text(payload: dict) -> str:
    m = payload["maintained"]
    live = payload["live"]
    lines = [
        "=== PROJECT SHELLAC CHAT / PHASE HANDOVER ===",
        "",
        "AUTHORITY WARNING",
        "This handover is process continuity only. Controlled repository authority wins on conflict.",
        "",
        "LIVE REPOSITORY",
        f"state: {live['state_class']}",
        f"branch: {live['branch']}",
        f"HEAD: {live['head']}",
        f"HEAD subject: {live['head_subject']}",
        f"origin/develop: {live['origin_develop']}",
        f"HEAD == origin/develop: {live['head_equals_origin_develop']}",
        f"worktree clean: {live['worktree_clean']}",
        "",
        "MAINTAINED PHASE",
        f"governed increment described: {m['governed_increment_described']}",
        f"next phase: {m['next_phase']}",
        "",
        "ABSOLUTE DO-NOT-REGRESS ITEMS",
    ]
    lines.extend(f"- {x}" for x in m["absolute_do_not_regress"])
    lines += ["", "SELECTED AE-076B ARCHITECTURE"]
    for k, v in m["ae076b_selected_architecture"].items():
        lines.append(f"- {k}: {v}")
    lines += ["", "CURRENT ROUTING BLOCKERS"]
    for k, v in m["current_routing_blockers"].items():
        lines.append(f"- {k}: {v}")
    lines += ["", "NEXT ACTIONS"]
    lines.extend(f"- {x}" for x in m["next_actions"])
    lines += [
        "",
        "RECOVERY PROCEDURE FOR A NEW CHAT",
        "1. Read this file and PROJECT_GUIDANCE.md.",
        "2. Read current_decision_index.yaml, ae071_prerouting_hold.yaml and the latest referenced logs.",
        "3. Treat Git/live controlled sources as authority if any maintained handover text is stale.",
        "4. Continue from the first unresolved next action; do not repeat closed historical work.",
        "5. End substantial Shellac responses with Confidence and Chat runway.",
    ]
    if live["git_status_short"]:
        lines += ["", "CURRENT GIT STATUS"]
        lines.extend(live["git_status_short"])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="emit machine-readable state")
    args = parser.parse_args()
    payload = {"maintained": MAINTAINED, "live": live_state()}
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(render_text(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
