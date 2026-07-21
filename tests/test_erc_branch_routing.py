from generator.blocks.balanced_input import add_sch101_diff_converter_slice
from generator.blocks.mode_matrix import add_mode_matrix
from generator.core.pins import pin_position
from generator.core.sheet import Sheet

def _edges(sheet):
    return {frozenset(((w.x1,w.y1),(w.x2,w.y2))) for w in sheet.wires}

def test_sch101_diff_input_resistors_align_with_destination_pins():
    sheet=Sheet("SCH101","SCH101.kicad_sch"); add_sch101_diff_converter_slice(sheet)
    c={x.ref:x for x in sheet.components}; edges=_edges(sheet)
    for d,rp,rm in (("U103","R130","R131"),("U203","R230","R231")):
        plus=pin_position(c[d],"IN+"); minus=pin_position(c[d],"IN-")
        p2=pin_position(c[rp],"2"); m2=pin_position(c[rm],"2")
        assert plus.y < minus.y
        assert p2.y == plus.y and m2.y == minus.y
        assert frozenset(((p2.x,p2.y),(plus.x,plus.y))) in edges
        assert frozenset(((m2.x,m2.y),(minus.x,minus.y))) in edges

def test_sch101_no_vertical_conductor_runs_between_both_diff_inputs():
    sheet=Sheet("SCH101","SCH101.kicad_sch"); add_sch101_diff_converter_slice(sheet)
    c={x.ref:x for x in sheet.components}
    for d in ("U103","U203"):
        plus=pin_position(c[d],"IN+"); minus=pin_position(c[d],"IN-"); lo,hi=sorted((plus.y,minus.y))
        for w in sheet.wires:
            if w.x1==w.x2==plus.x:
                slo,shi=sorted((w.y1,w.y2)); assert not (slo < hi and shi > lo)

def test_sch105_bias_resistors_approach_buffer_inputs_vertically():
    sheet=Sheet("SCH105","SCH105.kicad_sch"); add_mode_matrix(sheet)
    c={x.ref:x for x in sheet.components}; edges=_edges(sheet)
    for br,ur in (("R510","U501"),("R520","U502")):
        b=pin_position(c[br],"1"); i=pin_position(c[ur],"IN"); corner=(i.x,b.y)
        assert frozenset(((b.x,b.y),corner)) in edges
        assert frozenset((corner,(i.x,i.y))) in edges


def test_sch101_reference_0va_stubs_do_not_touch_signal_outputs():
    sheet = Sheet("SCH101", "SCH101.kicad_sch")
    add_sch101_diff_converter_slice(sheet)
    components = {component.ref: component for component in sheet.components}

    labels = {(label.name, label.x, label.y) for label in sheet.labels}
    for opamp_ref, ref_resistor_ref in (("U102", "R133"), ("U202", "R233")):
        output_pin = pin_position(components[opamp_ref], "OUT")
        reference_pin = pin_position(components[ref_resistor_ref], "1")
        assert ("0VA", output_pin.x, output_pin.y) not in labels
        assert any(
            name == "0VA" and x == reference_pin.x and y > reference_pin.y
            for name, x, y in labels
        )


def test_sch101_converter_feedback_and_reference_are_direct_pin_connections():
    sheet = Sheet("SCH101", "SCH101.kicad_sch")
    add_sch101_diff_converter_slice(sheet)
    components = {component.ref: component for component in sheet.components}
    edges = _edges(sheet)

    for diff_ref, feedback_ref, reference_ref in (
        ("U103", "R132", "R133"),
        ("U203", "R232", "R233"),
    ):
        diff = components[diff_ref]
        feedback = components[feedback_ref]
        reference = components[reference_ref]

        expected = (
            (pin_position(feedback, "2"), pin_position(diff, "OUT")),
            (pin_position(feedback, "1"), pin_position(diff, "IN-")),
            (pin_position(reference, "2"), pin_position(diff, "IN+")),
        )
        for start, end in expected:
            assert frozenset(((start.x, start.y), (end.x, end.y))) in edges
