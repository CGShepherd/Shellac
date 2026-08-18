from generator.mechanical.psu_release import ReleaseDecision, build_psu_release_decision, validate_psu_release_decision


def test_g3022_release_decision_is_consistent():
    model = build_psu_release_decision()
    assert validate_psu_release_decision(model) == []


def test_exact_integrated_mains_entry_is_frozen():
    model = build_psu_release_decision()
    assert model.mains_entry.manufacturer == "SCHURTER"
    assert model.mains_entry.order_code == "KMF1.1121.11"
    assert model.mains_entry.switch.startswith("2-pole")
    assert model.mains_entry.fuseholder.startswith("2-pole")


def test_kmf_geometry_is_compatible_with_two_mm_panel():
    model = build_psu_release_decision()
    assert model.mains_geometry_fits
    assert 2.0 in model.mains_entry.accepted_panel_thickness_mm
    assert model.mains_entry.behind_panel_depth_mm == 40.4
    assert round(model.residual_depth_after_mains_mm, 2) == 35.61


def test_thermal_evidence_is_not_invented():
    model = build_psu_release_decision()
    assert not model.thermal_evidence_complete
    text = " ".join(model.findings).lower()
    assert "rail current" in text
    assert "thermal resistance" in text


def test_binary_gate_rejects_m5501119():
    model = build_psu_release_decision()
    assert model.decision is ReleaseDecision.REJECTED
    assert "next larger" in model.next_action.lower()
