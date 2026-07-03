from generator.core.components import resistor
from generator.core.geometry import Point

def test_resistor_metadata():
    r = resistor("R101", "100R", Point(1, 2), tolerance="1%", function="RF isolation")
    assert r.ref == "R101"
    assert r.value == "100R"
    assert r.fields["Tolerance"] == "1%"
    assert r.fields["Function"] == "RF isolation"
