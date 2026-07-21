from generator.layout.interconnect_architecture import (
    ConnectorFamily,
    HarnessClass,
    build_interconnect_architecture,
    validate_interconnect_architecture,
)


def test_interconnect_architecture_is_valid():
    model = build_interconnect_architecture()
    assert validate_interconnect_architecture(model) == []


def test_sn58b_drives_two_internal_connector_families():
    model = build_interconnect_architecture()
    assert set(model.crimp_tool.terminal_families) == {
        ConnectorFamily.JST_VH,
        ConnectorFamily.MINI_FIT_JR,
    }
    assert model.crimp_tool.acceptance_samples == 5


def test_low_level_inputs_are_separated_and_shielded():
    model = build_interconnect_architecture()
    inputs = [h for h in model.harnesses if h.harness_class is HarnessClass.MICROVOLT_ANALOGUE]
    assert len(inputs) == 2
    assert all(h.connector_family is ConnectorFamily.JST_VH for h in inputs)
    assert all("25 mm" in h.separation_rule for h in inputs)
    assert all("shield" in h.shield_termination.lower() for h in inputs)


def test_power_harness_is_mechanically_distinct_and_keyed():
    model = build_interconnect_architecture()
    power = [h for h in model.harnesses if h.harness_class is HarnessClass.REGULATED_POWER]
    assert len(power) == 1
    harness = power[0]
    assert harness.connector_family is ConnectorFamily.MINI_FIT_JR
    assert harness.ways == 5
    assert all(pin.populated for pin in harness.pins)
    assert {p.signal for p in harness.pins if p.populated} >= {"+18V", "0VA", "-18V", "CHASSIS"}


def test_panel_connector_eco_is_closed():
    model = build_interconnect_architecture()
    assert model.status == "PRELIMINARY_READY"
    assert model.eco_refs == []
