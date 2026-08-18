from generator.mechanical.unicase_fit import FitStatus, build_unicase_fit_decision, validate_unicase_fit_decision

def test_g3020_unicase_fit_is_internally_consistent():
    model = build_unicase_fit_decision()
    assert validate_unicase_fit_decision(model) == []

def test_audio_unicase2_is_exactly_frozen_and_fits_carrier():
    model = build_unicase_fit_decision()
    assert model.audio.order_code == "M5502119"
    assert model.audio_status is FitStatus.FROZEN
    assert model.audio.base_pcb_width_mm >= 230.0
    assert model.audio.base_pcb_depth_mm >= 150.0
    assert model.audio.usable_inside_height_mm >= 60.0

def test_psu_unicase1_is_not_prematurely_frozen():
    model = build_unicase_fit_decision()
    assert model.psu.order_code == "M5501119"
    assert model.psu_status is FitStatus.REJECTED
    assert any("thermal" in item.lower() for item in model.open_items)
    assert any("next larger" in item.lower() for item in model.open_items)

def test_transformer_envelope_includes_datasheet_allowance():
    t = build_unicase_fit_decision().transformer
    assert (t.width_mm, t.depth_mm, t.height_mm) == (78.0, 78.0, 36.0)

def test_control_stack_prohibits_nut_forced_alignment_and_stays_part_gated():
    stack = build_unicase_fit_decision().control_stack
    assert "never pull" in stack.alignment_rule.lower()
    assert stack.panel_thickness_mm is None
    assert len(stack.release_inputs) >= 5
