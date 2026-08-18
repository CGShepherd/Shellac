from generator.mechanical.psu_enclosure_freeze import (
    build_psu_enclosure_freeze,
    validate_psu_enclosure_freeze,
)
from generator.mechanical.psu_release import ReleaseDecision


def test_g3023_freeze_is_internally_consistent():
    model = build_psu_enclosure_freeze()
    assert validate_psu_enclosure_freeze(model) == []
    assert model.decision is ReleaseDecision.FROZEN


def test_replacement_psu_is_exact_black_unicase2():
    enclosure = build_psu_enclosure_freeze().enclosure
    assert enclosure.order_code == "M5502119"
    assert enclosure.family == "UNICASE 2"
    assert enclosure.colour == "Black RAL 9005"
    assert (enclosure.usable_inside_width_mm, enclosure.usable_inside_depth_mm, enclosure.usable_inside_height_mm) == (256.0, 236.0, 86.2)


def test_known_psu_stack_has_large_residual_geometry():
    reserve = build_psu_enclosure_freeze().passive_thermal_reserve
    assert round(reserve.residual_width_after_known_components_mm, 1) == 103.0
    assert round(reserve.residual_depth_after_known_components_and_mains_mm, 1) == 110.6
    assert reserve.transformer_headroom_mm >= 50.0
    assert reserve.regulator_headroom_mm >= 55.0


def test_passive_thermal_margin_is_explicit_without_fake_temperature_model():
    reserve = build_psu_enclosure_freeze().passive_thermal_reserve
    assert reserve.internal_volume_ratio_vs_rejected > 2.9
    assert reserve.external_surface_area_ratio_vs_rejected > 1.9
    assert not reserve.temperature_prediction_available
    assert "prototype" in reserve.verification_rule.lower()


def test_frozen_mains_entry_carries_forward():
    model = build_psu_enclosure_freeze()
    assert model.mains_entry_order_code == "KMF1.1121.11"
