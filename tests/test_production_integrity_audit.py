from generator.model.production_integrity_audit import (
    FINDINGS, closed_findings, open_findings, routing_blockers, validate_findings
)

def test_ae036_findings_are_well_formed():
    validate_findings()

def test_original_routing_hold_and_control_authority_items_are_formally_closed():
    assert {x.identifier for x in closed_findings()} == {
        "AE036-F01","AE036-F02","AE036-F03","AE036-F04"
    }

def test_repository_wide_routing_hold_remains_lifted():
    assert routing_blockers() == ()

def test_build_native_pcb_hazard_remains_historical_p0_but_closed():
    f=next(x for x in FINDINGS if x.identifier=="AE036-F01")
    assert f.severity=="P0"
    assert f.state=="CLOSED"
    assert not f.routing_blocker

def test_control_authority_conflict_is_closed_by_ae040b():
    f=next(x for x in FINDINGS if x.identifier=="AE036-F04")
    assert f.severity=="P1"
    assert f.state=="CLOSED"
    assert "Lorlin PT" in f.resolution_evidence
    assert "Grayhill" in f.resolution_evidence

def test_remaining_findings_begin_at_f05():
    assert {x.identifier for x in open_findings()} == {
        "AE036-F05","AE036-F06","AE036-F07","AE036-F08",
        "AE036-F09","AE036-F10","AE036-F11","AE036-F12","AE036-F13"
    }
