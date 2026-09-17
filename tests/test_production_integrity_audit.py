from generator.model.production_integrity_audit import (
    FINDINGS, closed_findings, open_findings, routing_blockers, validate_findings
)

def test_findings_are_well_formed():
    validate_findings()

def test_closed_findings_include_ae071a_sch101_product_migration():
    assert {x.identifier for x in closed_findings()} == {
        "AE036-F01","AE036-F02","AE036-F03","AE036-F04","AE071-F01"
    }
    f=next(x for x in FINDINGS if x.identifier=="AE071-F01")
    assert "AE-071A" in f.resolution_evidence

def test_current_repository_routing_hold_remains_fail_closed():
    assert {x.identifier for x in routing_blockers()} == {
        "AE036-F05",
        "AE071-F02","AE071-F03","AE071-F04",
        "AE071-F05","AE071-F06","AE071-F08",
    }

def test_service_hardware_mapping_is_new_explicit_routing_blocker():
    f=next(x for x in FINDINGS if x.identifier=="AE071-F08")
    assert f.state=="OPEN"
    assert f.routing_blocker
    assert "pairing/orientation" in f.summary

def test_remaining_open_findings_are_explicit():
    assert {x.identifier for x in open_findings()} == {
        "AE036-F05","AE036-F06","AE036-F07","AE036-F08",
        "AE036-F09","AE036-F10","AE036-F11","AE036-F12","AE036-F13",
        "AE071-F02","AE071-F03","AE071-F04","AE071-F05",
        "AE071-F06","AE071-F07","AE071-F08",
    }
