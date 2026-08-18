from generator.mechanical.psu_fit import ClosureState, build_psu_fit_closure, validate_psu_fit_closure


def test_g3021_psu_fit_is_internally_consistent():
    model = build_psu_fit_closure()
    assert validate_psu_fit_closure(model) == []


def test_m5501119_internal_envelope_is_drawing_based():
    model = build_psu_fit_closure()
    assert (model.floor.width_mm, model.floor.depth_mm, model.floor.usable_height_mm) == (181.0, 161.01, 61.2)
    assert "manufacturer drawing" in model.floor.source_reference.lower()


def test_known_transformer_and_regulator_fit_side_by_side():
    model = build_psu_fit_closure()
    fit = model.side_by_side_fit
    assert fit.fits
    assert fit.occupied_width_mm == 153.0
    assert fit.occupied_depth_mm == 85.0
    assert fit.residual_width_mm == 28.0
    assert round(fit.residual_depth_mm, 2) == 76.01


def test_known_component_heights_fit_internal_height():
    model = build_psu_fit_closure()
    assert model.transformer.height_mm == 36.0
    assert model.regulator.height_mm == 31.0
    assert max(model.transformer.height_mm, model.regulator.height_mm) < model.floor.usable_height_mm


def test_psu_is_not_frozen_without_exact_iec_and_thermal_evidence():
    model = build_psu_fit_closure()
    assert model.state is ClosureState.RELEASE_BLOCKED
    blockers = " ".join(model.release_blockers).lower()
    assert "iec" in blockers
    assert "thermal" in blockers
    assert len(model.release_blockers) == 2
