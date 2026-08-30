from generator.blocks.balanced_input import add_sch101_rf_slice
from generator.core.sheet import Sheet

def test_rf_slice_components():
    sheet = Sheet(title="test", filename="test.kicad_sch")
    add_sch101_rf_slice(sheet)
    refs = {c.ref for c in sheet.components}
    assert "J101" in refs
    assert "J201" in refs
    assert "R102" in refs
    assert "R103" in refs
    assert "C101" in refs
    assert "C103" in refs
    assert "R202" in refs
    assert "C203" in refs

def test_rf_slice_uses_only_true_signal_interfaces_as_audio_labels():
    sheet = Sheet(title="test", filename="test.kicad_sch")
    add_sch101_rf_slice(sheet)
    labels = [label.name for label in sheet.labels]
    for name in (
        "INPUT_L_POS", "INPUT_L_NEG",
        "INPUT_R_POS", "INPUT_R_NEG",
    ):
        assert labels.count(name) == 1

    # DR-038 uses PRE_EQ_L/R as the local feedback/output net name and the
    # exported sheet interface, so each must appear exactly twice.
    assert labels.count("PRE_EQ_L") == 2
    assert labels.count("PRE_EQ_R") == 2
    # These former local stub nets are now continuous visible conductors.
    assert "L_IN_FILT_PLUS" not in labels
    assert "L_IN_FILT_MINUS" not in labels
    assert "R_IN_FILT_PLUS" not in labels
    assert "R_IN_FILT_MINUS" not in labels


def test_gain_selector_and_values_are_rendered():
    sheet = Sheet(title="test", filename="test.kicad_sch")
    add_sch101_rf_slice(sheet)
    by_ref = {component.ref: component for component in sheet.components}
    assert "SW1011" not in by_ref
    assert "RN130" in by_ref and "RN230" in by_ref
    assert by_ref["R112"].value == "249"
    assert by_ref["R113"].value == "750"
    assert by_ref["R114"].value == "1910"


def test_gain_selector_segments_realise_validated_feedback_values():
    sheet = Sheet(title="test", filename="test.kicad_sch")
    add_sch101_rf_slice(sheet)
    by_ref = {component.ref: component for component in sheet.components}
    base = float(by_ref["R112"].value)
    assert base + float(by_ref["R113"].value) == 999.0
    assert base + float(by_ref["R114"].value) == 2159.0
    assert len(sheet.wires) > 100
