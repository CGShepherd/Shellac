from generator.layout.performance import (
    Criticality,
    EvidenceStatus,
    build_performance_baseline,
)


def test_three_input_gain_settings_are_monotonic():
    rows = build_performance_baseline().gain_settings
    assert [r.name for r in rows] == ["LOW", "DEFAULT", "HIGH"]
    assert [r.input_stage_gain_linear for r in rows] == sorted(r.input_stage_gain_linear for r in rows)


def test_nominal_input_gain_outputs_are_consistent():
    baseline = build_performance_baseline()
    for row in baseline.gain_settings:
        assert abs(row.nominal_5mv_output_rms_v - baseline.nominal_cartridge_rms_v * row.input_stage_gain_linear) < 1e-12


def test_all_margin_records_have_positive_headroom():
    for margin in build_performance_baseline().margins:
        assert margin.design_value > margin.requirement
        assert margin.margin_ratio > 1.0


def test_validated_worst_case_cartridge_margin_exceeds_17_db():
    margin = next(m for m in build_performance_baseline().margins if m.identifier == "MAR-001")
    assert margin.status is EvidenceStatus.VALIDATED
    assert margin.margin_db is not None and margin.margin_db > 17.0


def test_performance_defining_parts_cannot_be_freely_substituted():
    for record in build_performance_baseline().criticality:
        if record.classification is Criticality.PERFORMANCE_DEFINING:
            assert "without" in record.substitution_policy.lower() or "only" in record.substitution_policy.lower()
            assert record.verification.strip()


def test_every_critical_loop_has_verification_and_no_more_than_zero_vias():
    for constraint in build_performance_baseline().placement_constraints:
        assert constraint.maximum_signal_vias == 0
        assert constraint.verification.strip()


def test_unclosed_quantities_are_explicitly_listed():
    baseline = build_performance_baseline()
    joined = " ".join(baseline.open_measurements).lower()
    assert "noise" in joined
    assert "thd" in joined
    assert "psu" in joined
