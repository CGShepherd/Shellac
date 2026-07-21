from generator.core.connectivity import Wire
from generator.core.sheet import Sheet
from generator.writers.kicad9 import junction_points, write_schematic


GRID = 1.27


def _coordinates(wires):
    return tuple((point.x, point.y) for point in junction_points(wires))


def test_t_branch_gets_one_junction_dot():
    wires = [
        Wire(0, GRID, GRID, GRID),
        Wire(GRID, GRID, 2 * GRID, GRID),
        Wire(GRID, GRID, GRID, 2 * GRID),
    ]

    assert _coordinates(wires) == ((GRID, GRID),)


def test_endpoint_on_unsplit_wire_is_not_silently_joined():
    wires = [
        Wire(0, GRID, 2 * GRID, GRID),
        Wire(GRID, GRID, GRID, 2 * GRID),
    ]

    assert _coordinates(wires) == ()


def test_simple_bend_does_not_get_junction_dot():
    wires = [
        Wire(0, GRID, GRID, GRID),
        Wire(GRID, GRID, GRID, 2 * GRID),
    ]

    assert _coordinates(wires) == ()


def test_unconnected_crossing_does_not_get_junction_dot():
    wires = [
        Wire(0, GRID, 2 * GRID, GRID),
        Wire(GRID, 0, GRID, 2 * GRID),
    ]

    assert _coordinates(wires) == ()


def test_four_way_branch_gets_one_junction_dot():
    wires = [
        Wire(0, GRID, GRID, GRID),
        Wire(GRID, GRID, 2 * GRID, GRID),
        Wire(GRID, 0, GRID, GRID),
        Wire(GRID, GRID, GRID, 2 * GRID),
    ]

    assert _coordinates(wires) == ((GRID, GRID),)


def test_writer_emits_deterministic_junction(tmp_path):
    sheet = Sheet(title="Junction proof", filename="SCH_TEST")
    sheet.wires.extend([
        Wire(0, GRID, GRID, GRID),
        Wire(GRID, GRID, 2 * GRID, GRID),
        Wire(GRID, GRID, GRID, 2 * GRID),
    ])
    first = tmp_path / "first.kicad_sch"
    second = tmp_path / "second.kicad_sch"

    write_schematic(sheet, first)
    write_schematic(sheet, second)

    first_text = first.read_text(encoding="utf-8")
    assert first_text == second.read_text(encoding="utf-8")
    assert first_text.count("(junction ") == 1
    assert "(junction (at 1.27 1.27)" in first_text
