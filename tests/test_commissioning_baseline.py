from generator.commissioning import AcceptanceState, build_commissioning_baseline, validate_commissioning_baseline


def test_commissioning_baseline_validates_and_has_ten_ordered_stages():
    model = build_commissioning_baseline()
    validate_commissioning_baseline(model)
    assert [stage.identifier for stage in model.stages] == [f"COM-{index:02d}" for index in range(10)]


def test_no_stage_references_a_future_prerequisite():
    model = build_commissioning_baseline()
    seen = set()
    for stage in model.stages:
        assert set(stage.prerequisites) <= seen
        seen.add(stage.identifier)


def test_all_measurements_have_unique_identifiers_and_retained_evidence():
    model = build_commissioning_baseline()
    measurements = [m for stage in model.stages for m in stage.measurements]
    assert len({m.identifier for m in measurements}) == len(measurements)
    assert all(m.retain for m in measurements)


def test_calculated_gain_expectations_preserve_frozen_design():
    model = build_commissioning_baseline()
    expected = {m.parameter: m.expected for stage in model.stages for m in stage.measurements}
    assert "7.9960 V/V" in expected["SCH101 DEFAULT gain"]
    assert expected["SCH104 gain"] == "1.000 V/V"
    assert "2.000 V/V" in expected["Differential output gain"]


def test_objective_characterisation_precedes_listening_release():
    model = build_commissioning_baseline()
    release = next(stage for stage in model.stages if stage.identifier == "COM-09")
    assert release.prerequisites == ("COM-08",)
    assert any("Subjective" in rule for rule in model.global_rules)


def test_open_numeric_limits_are_explicit_not_silent():
    model = build_commissioning_baseline()
    assert model.open_values
    assert any(m.state is AcceptanceState.MEASUREMENT_REQUIRED for stage in model.stages for m in stage.measurements)
    assert any("open" in m.tolerance_or_limit.lower() or "freeze" in m.tolerance_or_limit.lower() for stage in model.stages for m in stage.measurements)


def test_mains_stage_contains_protective_earth_and_wrong_polarity_stop_conditions():
    model = build_commissioning_baseline()
    stage = next(stage for stage in model.stages if stage.identifier == "COM-02")
    text = " ".join(m.parameter for m in stage.measurements) + " " + " ".join(stage.stop_conditions)
    assert "Protective-earth" in text
    assert "polarity" in text
