from generator.model.production_integrity_audit import FINDINGS, routing_blockers, validate_findings

def test_ae036_findings_are_well_formed():
    validate_findings()

def test_three_items_block_further_routing():
    assert {x.identifier for x in routing_blockers()} == {
        "AE036-F01","AE036-F02","AE036-F03"
    }

def test_build_native_pcb_hazard_is_p0():
    f=next(x for x in FINDINGS if x.identifier=="AE036-F01")
    assert f.severity=="P0" and f.routing_blocker
