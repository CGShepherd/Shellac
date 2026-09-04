
from generator.layout.footprint_contract import build_footprint_contract
from generator.layout.placement_clusters import build_cluster_placement_baseline
from generator.layout.preliminary_placement import build_preliminary_placement_baseline
from generator.model.opamp_package_allocation import absorbed_logical_refs,package_counts

ABSORBED=set(absorbed_logical_refs())

def test_absorbed_logical_units_have_no_physical_footprints():
    contract=build_footprint_contract()
    assert ABSORBED.isdisjoint(contract.board_population_refs)

def test_physical_opamp_package_census_is_ten():
    contract=build_footprint_contract()
    opamps=[
        e for e in contract.entries
        if e.value in {"OPA1656","OPA1655","OPA1612"}
        and e.ref in contract.board_population_refs
    ]
    assert len(opamps)==10
    by_value={}
    for e in opamps:
        by_value[e.value]=by_value.get(e.value,0)+1
    assert by_value==package_counts()=={"OPA1656":6,"OPA1655":2,"OPA1612":2}

def test_board_population_reduces_by_eight_packages():
    contract=build_footprint_contract()
    assert len(contract.board_population_refs)==246

def test_absorbed_refs_are_removed_from_cluster_authority():
    model=build_cluster_placement_baseline()
    owned={r for c in model.clusters for r in c.member_refs}
    assert ABSORBED.isdisjoint(owned)

def test_every_physical_package_receives_one_placement():
    contract=build_footprint_contract()
    placement=build_preliminary_placement_baseline()
    assert {p.ref for p in placement.proposals}==set(contract.board_population_refs)
    assert len(placement.proposals)==246
