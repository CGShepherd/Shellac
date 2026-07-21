from generator.layout.footprint_contract import (
    PopulationStatus,
    build_footprint_contract,
    validate_footprint_contract,
)


def test_footprint_contract_is_internally_valid():
    contract = build_footprint_contract()
    assert validate_footprint_contract(contract) == []


def test_every_approved_board_component_has_a_footprint():
    contract = build_footprint_contract()
    approved = [e for e in contract.entries if e.population_status is PopulationStatus.APPROVED]
    assert approved
    assert all(e.schematic_on_board and e.footprint for e in approved)


def test_panel_hardware_is_not_in_preliminary_board_population():
    contract = build_footprint_contract()
    assert set(contract.panel_interface_refs).isdisjoint(contract.board_population_refs)


def test_panel_connector_eco_is_closed_and_board_headers_are_populated():
    contract = build_footprint_contract()
    assert contract.status == "PRELIMINARY_READY"
    assert contract.mechanical_eco_refs == []
    assert {"J101", "J201", "J901"}.issubset(contract.panel_interface_refs)
    assert {"H101", "H201", "H901"}.issubset(contract.board_population_refs)


def test_contract_covers_all_generated_component_references_once():
    contract = build_footprint_contract()
    refs = [e.ref for e in contract.entries]
    assert len(refs) == len(set(refs))
    classified = set(contract.board_population_refs) | set(contract.panel_interface_refs) | set(contract.mechanical_eco_refs)
    assert classified == set(refs)
