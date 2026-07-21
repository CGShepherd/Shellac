from generator.layout.footprint_contract import build_footprint_contract
from generator.layout.preliminary_placement import build_preliminary_placement_baseline


def _overlap(a, b):
    return (
        abs(a.x_mm - b.x_mm) < (a.width_mm + b.width_mm) / 2.0
        and abs(a.y_mm - b.y_mm) < (a.depth_mm + b.depth_mm) / 2.0
    )


def test_power_entry_bulk_capacitors_use_physical_radial_footprints():
    entries = {entry.ref: entry for entry in build_footprint_contract().entries}
    for ref in ("C901", "C904"):
        assert entries[ref].value == "470u"
        assert entries[ref].footprint == "Capacitor_THT:CP_Radial_D10.0mm_P5.00mm"
    for ref in ("C902", "C905"):
        assert entries[ref].footprint == "Capacitor_SMD:C_1206_3216Metric"


def test_power_entry_gate3a_envelopes_do_not_overlap():
    placements = [
        proposal
        for proposal in build_preliminary_placement_baseline().proposals
        if proposal.cluster_id == "CLU-106"
    ]
    overlaps = [
        (a.ref, b.ref)
        for index, a in enumerate(placements)
        for b in placements[index + 1 :]
        if _overlap(a, b)
    ]
    assert overlaps == []
