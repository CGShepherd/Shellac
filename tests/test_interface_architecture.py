from generator.mechanical.interface_architecture import (
    EnclosureFace,
    MountingMode,
    build_interface_architecture,
    validate_interface_architecture,
)


def test_shellac_interface_architecture_is_internally_consistent():
    model = build_interface_architecture()
    assert validate_interface_architecture(model) == []
    assert model.enclosure_family.manufacturer == "METCASE"
    assert model.enclosure_family.family == "UNICASE"
    assert model.enclosure_family.colour_standard == "RAL 9005"


def test_audio_signal_flow_and_panel_ownership_are_frozen_front_to_rear():
    model = build_interface_architecture()
    by_id = {item.identifier: item for item in model.interfaces}
    assert by_id["IF-A-IN"].face is EnclosureFace.FRONT
    assert by_id["IF-A-OUT"].face is EnclosureFace.REAR
    assert by_id["IF-A-DC"].face is EnclosureFace.REAR
    assert "front-to-rear" in model.signal_flow_rule


def test_controls_are_pcb_mounted_and_upper_cover_supported_without_flying_leads():
    model = build_interface_architecture()
    controls = next(item for item in model.interfaces if item.identifier == "IF-A-CTRL")
    assert controls.face is EnclosureFace.UPPER_COVER
    assert controls.mounting is MountingMode.PCB_BUSHING
    assert "no flying" in controls.wiring_rule.lower()
    assert "never pull a misaligned pcb" in controls.structural_rule.lower()


def test_psu_flow_is_rear_mains_to_front_dc_and_clamshells_are_preserved():
    model = build_interface_architecture()
    by_id = {item.identifier: item for item in model.interfaces}
    assert by_id["IF-P-MAINS"].face is EnclosureFace.REAR
    assert by_id["IF-P-DC"].face is EnclosureFace.FRONT
    assert any("unmachined" in rule for rule in model.invariants)


def test_drilling_template_is_true_scale_and_datum_based():
    template = build_interface_architecture().drilling_template
    assert template is not None
    assert template.scale == "1:1"
    assert template.primary_format == "PDF"
    assert template.machine_format == "DXF"
    assert "never chained" in template.coordinate_origin
    assert any("100 x 100" in feature for feature in template.required_features)
    assert "do not release" in template.release_gate.lower()
