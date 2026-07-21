from dataclasses import replace

import pytest

from generator.mechanical import EnclosureRole, build_mechanical_baseline
from generator.mechanical.freeze import (
    DrawingEvidence,
    build_enclosure_decision_baseline,
    decision_findings,
    derive_carrier_freeze,
)


def test_both_enclosure_roles_remain_blocked_without_drawings():
    decisions = build_enclosure_decision_baseline()
    assert {item.role for item in decisions} == {EnclosureRole.AUDIO, EnclosureRole.PSU}
    assert all(item.status.startswith("BLOCKED") for item in decisions)


def test_audio_decision_requires_vertical_service_access_evidence():
    baseline = build_mechanical_baseline()
    candidate = next(item for item in baseline.candidates if item.identifier == "ENC-A03")
    findings = decision_findings(candidate, baseline, DrawingEvidence(False, False, False, False, False, None))
    assert any("lid intrusion" in item for item in findings)
    assert any("manufacturer drawing" in item for item in findings)


def test_carrier_freeze_rejects_incomplete_evidence():
    candidate = next(item for item in build_mechanical_baseline().candidates if item.identifier == "ENC-A03")
    with pytest.raises(ValueError):
        derive_carrier_freeze(candidate, DrawingEvidence(True, True, False, True, True, "drawing"))


def test_carrier_freeze_centres_preferred_board_when_geometry_is_verified():
    candidate = next(item for item in build_mechanical_baseline().candidates if item.identifier == "ENC-A03")
    verified = replace(candidate, internal_width_mm=250.0, internal_depth_mm=160.0)
    evidence = DrawingEvidence(True, True, True, True, True, "manufacturer-drawing-rev-1")
    freeze = derive_carrier_freeze(verified, evidence)
    assert freeze.plate_width_mm == 240.0
    assert freeze.plate_depth_mm == 150.0
    assert freeze.pcb_origin_x_mm == 10.0
    assert freeze.pcb_origin_y_mm == 5.0
    assert freeze.service_removal_direction == "vertical"
