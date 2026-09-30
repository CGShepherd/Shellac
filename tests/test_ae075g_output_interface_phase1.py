from pathlib import Path

from generator.blocks.balanced_output import add_balanced_output
from generator.core.components import Component
from generator.core.geometry import Point
from generator.core.pins import pin_position
from generator.core.sheet import Sheet
from generator.layout.footprint_contract import (
    PopulationStatus,
    build_footprint_contract,
)
from generator.model.output_driver import (
    OUTPUT_IMPEDANCE_DIFFERENTIAL_OHM,
    OUTPUT_IMPEDANCE_PER_LEG_OHM,
)
from generator.writers.kicad9 import PIN_COUNTS, local_symbol_library

FP = (
    "ProjectShellac:"
    "Molex_MicroLockPlus_5055780221_1x02_P2.00mm_Horizontal"
)


def _sheet():
    s = Sheet("SCH108", "ProjectShellac_SCH108.kicad_sch")
    add_balanced_output(s)
    return s


def _wire_component(sheet, start):
    adjacency = {}
    for wire in sheet.wires:
        a = (wire.x1, wire.y1)
        b = (wire.x2, wire.y2)
        adjacency.setdefault(a, set()).add(b)
        adjacency.setdefault(b, set()).add(a)

    seen = {start}
    pending = [start]
    while pending:
        point = pending.pop()
        for neighbour in adjacency.get(point, ()):
            if neighbour not in seen:
                seen.add(neighbour)
                pending.append(neighbour)
    return seen


def test_two_pin_connector_generator_primitive():
    c = Component(
        "H1",
        "Connector_Generic:Conn_01x02",
        "TEST",
        Point(100.0, 100.0),
    )
    p1 = pin_position(c, "1")
    p2 = pin_position(c, "2")
    assert p1.x == p2.x
    assert abs(abs(p1.y - p2.y) - 2.54) < 1e-9
    assert PIN_COUNTS["Connector_Generic:Conn_01x02"] == 2
    assert (
        '(symbol "Connector_Generic:Conn_01x02"'
        in local_symbol_library()
    )


def test_that1646_output_impedance_semantics():
    assert OUTPUT_IMPEDANCE_PER_LEG_OHM == 25.0
    assert OUTPUT_IMPEDANCE_DIFFERENTIAL_OHM == 50.0


def test_output_headers_are_real_pcb_components():
    s = _sheet()
    p = {c.ref: c for c in s.components}

    for h, j in (
        ("H801", "J8001"),
        ("H802", "J9001"),
    ):
        assert p[h].on_board is True
        assert p[h].footprint == FP
        assert p[h].fields["PCB header"] == "5055780221"
        assert p[h].fields["Harness housing"] == "5055700201"
        assert p[h].fields["Harness terminal"] == "5055721200"
        assert p[h].fields["Pin 1"] == "HOT/+"
        assert p[h].fields["Pin 2"] == "COLD/-"

        assert p[j].on_board is False
        assert p[j].fields["Local 0VA"] == "NONE"


def test_headers_continue_to_matching_xlr_pins():
    s = _sheet()
    p = {c.ref: c for c in s.components}

    for h, j in (
        ("H801", "J8001"),
        ("H802", "J9001"),
    ):
        hp = pin_position(p[h], "1")
        hn = pin_position(p[h], "2")

        pos = _wire_component(s, (hp.x, hp.y))
        neg = _wire_component(s, (hn.x, hn.y))

        xp = pin_position(p[j], "2")
        xn = pin_position(p[j], "3")

        assert (xp.x, xp.y) in pos
        assert (xn.x, xn.y) in neg


def test_footprint_contract_owns_output_headers():
    c = build_footprint_contract()
    entries = {e.ref: e for e in c.entries}

    for ref in ("H801", "H802"):
        assert (
            entries[ref].population_status
            is PopulationStatus.APPROVED
        )
        assert entries[ref].footprint == FP


def test_exact_two_way_footprint_geometry():
    path = Path(
        "generator/footprints/ProjectShellac.pretty/"
        "Molex_MicroLockPlus_5055780221_"
        "1x02_P2.00mm_Horizontal.kicad_mod"
    )
    text = path.read_text(encoding="utf-8")

    assert '(pad "1" smd rect (at -1.000001 -4.3791)' in text
    assert '(pad "2" smd rect (at 1.000001 -4.3791)' in text
    assert '(pad "3" smd rect (at -3.399999 -0.2291)' in text
    assert '(pad "4" smd rect (at 3.399999 -0.2291)' in text
    assert text.count("(zone (net 0)") == 3


def test_phase1_output_harness_hardware_identity_persists():
    text = Path(
        "config/bom/shellac_bom.yaml"
    ).read_text(encoding="utf-8")

    for mpn in ("5055780221", "5055700201", "5055721200"):
        assert mpn in text

    # Mutable current implementation status is deliberately not asserted in
    # this historical-invariant test. Current state belongs in
    # tests/test_current_decision_index.py.
