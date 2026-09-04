from generator.layout.footprint_contract import PopulationStatus,build_footprint_contract
from generator.layout.placement_clusters import build_cluster_placement_baseline
from generator.layout.preliminary_placement import build_preliminary_placement_baseline

NEW_LOAD_REFS={"R104","R105","R204","R205"}

def test_ae037_load_resistors_have_exact_cluster_owners():
    model=build_cluster_placement_baseline()
    owners={}
    for cluster in model.clusters:
        for ref in cluster.member_refs:
            owners.setdefault(ref,[]).append(cluster.identifier)
    assert owners["R104"]==["CLU-101-A"]
    assert owners["R105"]==["CLU-101-A"]
    assert owners["R204"]==["CLU-101-C"]
    assert owners["R205"]==["CLU-101-C"]

def test_ae037_load_resistors_are_approved_board_population():
    contract=build_footprint_contract()
    approved={
        entry.ref for entry in contract.entries
        if entry.population_status is PopulationStatus.APPROVED
    }
    assert NEW_LOAD_REFS <= approved

def test_ae037_load_resistors_receive_placement_proposals():
    placement=build_preliminary_placement_baseline()
    by_ref={item.ref:item for item in placement.proposals}
    assert NEW_LOAD_REFS <= set(by_ref)
    assert by_ref["R104"].cluster_id=="CLU-101-A"
    assert by_ref["R105"].cluster_id=="CLU-101-A"
    assert by_ref["R204"].cluster_id=="CLU-101-C"
    assert by_ref["R205"].cluster_id=="CLU-101-C"
