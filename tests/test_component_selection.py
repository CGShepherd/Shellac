import pytest

from generator.component_selection import (
    TIMING_CAPACITOR_0805,
    TIMING_CAPACITOR_1206,
    CapacitorDielectric,
    ComponentFunction,
    ComponentRequirements,
    timing_capacitor_footprint,
    timing_capacitor_requirements,
)


def test_timing_capacitor_policy_encodes_engineering_requirements():
    requirements = timing_capacitor_requirements(22.0)

    assert requirements.function is ComponentFunction.TIMING
    assert requirements.dielectric is CapacitorDielectric.C0G_NP0
    assert requirements.tolerance_percent == 1.0
    assert requirements.minimum_voltage_v == 50.0
    assert requirements.signal_path is True
    assert requirements.preferred_footprints == (TIMING_CAPACITOR_0805,)
    assert requirements.selected_footprint == TIMING_CAPACITOR_0805


def test_large_timing_capacitor_policy_retains_1206_threshold():
    requirements = timing_capacitor_requirements(27.0)

    assert requirements.preferred_footprints == (TIMING_CAPACITOR_1206,)
    assert timing_capacitor_footprint(27.0) == TIMING_CAPACITOR_1206


@pytest.mark.parametrize("value_nf", (0.0, -1.0))
def test_timing_capacitor_policy_rejects_non_positive_values(value_nf):
    with pytest.raises(ValueError, match="must be positive"):
        timing_capacitor_requirements(value_nf)


@pytest.mark.parametrize(
    ("field", "replacement", "message"),
    (
        ("tolerance_percent", 0.0, "tolerance must be positive"),
        ("minimum_voltage_v", 0.0, "voltage rating must be positive"),
        ("preferred_footprints", (), "at least one preferred footprint"),
        ("preferred_footprints", ("",), "must be non-empty"),
    ),
)
def test_component_requirements_reject_invalid_physical_constraints(
    field, replacement, message
):
    values = {
        "function": ComponentFunction.TIMING,
        "dielectric": CapacitorDielectric.C0G_NP0,
        "tolerance_percent": 1.0,
        "minimum_voltage_v": 50.0,
        "preferred_footprints": (TIMING_CAPACITOR_0805,),
        "signal_path": True,
    }
    values[field] = replacement

    with pytest.raises(ValueError, match=message):
        ComponentRequirements(**values)


def test_component_function_vocabulary_covers_planned_policy_classes():
    assert {function.value for function in ComponentFunction} == {
        "timing",
        "coupling",
        "decoupling",
        "feedback",
        "compensation",
    }


def test_bulk_decoupling_policy_closes_generic_0805_placeholder():
    from generator.component_selection import (
        BULK_DECOUPLING_10UF_SMD,
        CapacitorDielectric,
        ComponentFunction,
        bulk_decoupling_capacitor_requirements,
    )

    req = bulk_decoupling_capacitor_requirements()
    assert req.function is ComponentFunction.DECOUPLING
    assert req.dielectric is CapacitorDielectric.ELECTROLYTIC
    assert req.minimum_voltage_v == 35.0
    assert req.signal_path is False
    assert req.selected_footprint == BULK_DECOUPLING_10UF_SMD
    assert "0805" not in req.selected_footprint


def test_common_mode_sense_policy_is_nonpolar_and_signal_path():
    from generator.component_selection import (
        NONPOLAR_FEEDBACK_10UF_THT,
        CapacitorDielectric,
        ComponentFunction,
        common_mode_sense_capacitor_requirements,
    )

    req = common_mode_sense_capacitor_requirements()
    assert req.function is ComponentFunction.FEEDBACK
    assert req.dielectric is CapacitorDielectric.NONPOLAR_ELECTROLYTIC
    assert req.minimum_voltage_v == 35.0
    assert req.signal_path is True
    assert req.selected_footprint == NONPOLAR_FEEDBACK_10UF_THT
    assert "0805" not in req.selected_footprint
