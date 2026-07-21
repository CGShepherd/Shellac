from generator.layout import NetClass, RoutingPolicy, build_layout_baseline


def test_layout_baseline_is_four_layer_and_preserves_continuous_reference_plane():
    baseline = build_layout_baseline()
    assert baseline.stackup.layer_count == 4
    assert "Continuous 0VA" in baseline.stackup.inner_1_role


def test_all_region_identifiers_and_sequences_are_unique():
    baseline = build_layout_baseline()
    assert len({r.identifier for r in baseline.regions}) == len(baseline.regions)
    assert len({r.sequence for r in baseline.regions}) == len(baseline.regions)
    assert [r.sequence for r in baseline.regions] == sorted(r.sequence for r in baseline.regions)


def test_critical_net_identifiers_are_unique_and_every_net_has_verification():
    baseline = build_layout_baseline()
    assert len({n.identifier for n in baseline.critical_nets}) == len(baseline.critical_nets)
    assert all(n.verification.strip() for n in baseline.critical_nets)


def test_cartridge_feedback_ground_and_chassis_are_manual_only():
    baseline = build_layout_baseline()
    required = {NetClass.CARTRIDGE, NetClass.FEEDBACK, NetClass.GROUND}
    for net in baseline.critical_nets:
        if net.net_class in required:
            assert net.routing_policy is RoutingPolicy.MANUAL_ONLY


def test_cartridge_and_feedback_nets_prohibit_signal_vias():
    baseline = build_layout_baseline()
    for net in baseline.critical_nets:
        if net.net_class in {NetClass.CARTRIDGE, NetClass.FEEDBACK}:
            assert net.max_signal_vias == 0


def test_provisional_envelope_is_not_tighter_than_existing_architecture():
    envelope = build_layout_baseline().envelope
    assert envelope.minimum_usable_width_mm >= 190
    assert envelope.minimum_usable_depth_mm >= 125
    assert envelope.preferred_usable_width_mm >= envelope.minimum_usable_width_mm
    assert envelope.preferred_usable_depth_mm >= envelope.minimum_usable_depth_mm


def test_audio_enclosure_access_rule_rejects_trapped_sliding_cover():
    rule = build_layout_baseline().envelope.access_rule.lower()
    assert "vertically removable" in rule
    assert "controls" in rule
