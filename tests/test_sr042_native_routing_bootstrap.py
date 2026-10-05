from pathlib import Path
import pytest, yaml
from generator.layout.sr042_native_routing_bootstrap import build_native_routing_bootstrap,write_native_routing_bootstrap
from generator.mechanical.released_placement_board import render_released_placement_reference_board,validate_released_placement_reference_board
from generator.layout.footprint_contract import build_footprint_contract

def test_sr042_executable_is_historical_only_and_fail_closed():
    g=build_native_routing_bootstrap()
    assert g.status=='HISTORICAL_SNAPSHOT_ONLY_DO_NOT_USE_FOR_CURRENT_RELEASE'
    assert g.historical_status=='READY_FOR_NATIVE_KICAD_BOARD_CREATION'
    assert g.base_commit=='47f7c01e639f85ebc28d77f7eb2d84718a8caf4b'
    assert not g.current_authority and not g.current_routing_authorized
    assert not g.observed_current_hold_final_routing
    assert g.current_hold_authority=='AE-076D'
    assert (g.placement_count,g.mounting_hole_count,g.critical_manual_net_count)==(250,4,10)

def test_sr042_historical_yaml_remains_immutable_provenance():
    c=yaml.safe_load(Path('config/release/sr042_native_kicad_bootstrap.yaml').read_text(encoding='utf-8'))
    assert c['status']=='READY_FOR_NATIVE_KICAD_BOARD_CREATION'
    assert c['base_commit']=='47f7c01e639f85ebc28d77f7eb2d84718a8caf4b'
    assert c['placement_count']==250 and c['mounting_hole_count']==4 and c['manual_critical_net_count']==10

def test_sr042_historical_regeneration_is_disabled():
    with pytest.raises(RuntimeError,match='historical bootstrap evidence'):
        write_native_routing_bootstrap(Path('out/sr042_should_not_be_written'))

def test_sr042_reference_board_geometry_utility_remains_nonrouting_evidence():
    text=render_released_placement_reference_board()
    assert validate_released_placement_reference_board(text)==[]
    assert text.count('(footprint "ProjectShellac:MountingHole"')==4
    assert text.count('(footprint "ProjectShellac:PlacementReference"')==len(build_footprint_contract().board_population_refs)
    assert '(segment ' not in text
