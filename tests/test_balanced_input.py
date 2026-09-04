from generator.blocks.balanced_input import add_sch101_rf_slice
from generator.core.sheet import Sheet

def _sheet():
    s=Sheet(title="test",filename="test.kicad_sch")
    add_sch101_rf_slice(s)
    return s

def test_rf_slice_components():
    refs={c.ref for c in _sheet().components}
    for ref in ("J101","J201","R102","R103","R104","R105","C101","C103","R202","R204","R205","C203"):
        assert ref in refs

def test_ae037_load_and_rf_values_are_rendered():
    by_ref={c.ref:c for c in _sheet().components}
    assert by_ref["R104"].value=="23700"
    assert by_ref["R105"].value=="23700"
    assert by_ref["R204"].value=="23700"
    assert by_ref["R205"].value=="23700"
    assert by_ref["C101"].value=="47p"
    assert by_ref["C102"].value=="47p"
    assert by_ref["C103"].value=="22p" and by_ref["C103"].dnp
    assert by_ref["C203"].value=="22p" and by_ref["C203"].dnp

def test_rf_slice_uses_only_true_signal_interfaces_as_audio_labels():
    sheet=_sheet()
    labels=[label.name for label in sheet.labels]
    for name in ("INPUT_L_POS","INPUT_L_NEG","INPUT_R_POS","INPUT_R_NEG"):
        assert labels.count(name)==1
    assert labels.count("PRE_EQ_L")==2
    assert labels.count("PRE_EQ_R")==2
    assert "L_IN_FILT_PLUS" not in labels
    assert "L_IN_FILT_MINUS" not in labels
    assert "R_IN_FILT_PLUS" not in labels
    assert "R_IN_FILT_MINUS" not in labels

def test_gain_selector_and_values_are_rendered():
    by_ref={component.ref:component for component in _sheet().components}
    assert "SW1011" not in by_ref
    assert "RN130" in by_ref and "RN230" in by_ref
    assert by_ref["R112"].value=="249"
    assert by_ref["R113"].value=="750"
    assert by_ref["R114"].value=="1910"

def test_gain_selector_segments_realise_validated_feedback_values():
    sheet=_sheet()
    by_ref={component.ref:component for component in sheet.components}
    base=float(by_ref["R112"].value)
    assert base+float(by_ref["R113"].value)==999.0
    assert base+float(by_ref["R114"].value)==2159.0
    assert len(sheet.wires)>100
