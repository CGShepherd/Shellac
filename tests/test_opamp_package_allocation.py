from generator.model.opamp_package_allocation import (
    ALLOCATIONS,DUAL_PIN_MAP,OPA1655_NC_PINS,OPA1655_PIN_MAP,
    absorbed_logical_refs,package_counts,physical_packages,validate_allocations,
)

def test_ae039a_allocation_is_closed():
    validate_allocations()

def test_eighteen_functions_map_to_ten_packages():
    assert len(ALLOCATIONS)==18
    assert len(physical_packages())==10

def test_eight_pseudo_package_refs_are_absorbed():
    assert len(absorbed_logical_refs())==8

def test_physical_device_census():
    assert package_counts()=={"OPA1656":6,"OPA1655":2,"OPA1612":2}

def test_dual_soic8_pin_authority():
    assert DUAL_PIN_MAP["A"]=={"OUT":"1","IN-":"2","IN+":"3"}
    assert DUAL_PIN_MAP["B"]=={"IN+":"5","IN-":"6","OUT":"7"}
    assert DUAL_PIN_MAP["SUPPLY"]=={"V-":"4","V+":"8"}

def test_opa1655_single_pin_authority():
    assert OPA1655_PIN_MAP=={"IN-":"2","IN+":"3","V-":"4","OUT":"6","V+":"7"}
    assert OPA1655_NC_PINS==("1","5","8")

def test_no_cross_channel_sch101_dual_converter_pairing():
    left=next(a for a in ALLOCATIONS if a.logical_ref=="U103")
    right=next(a for a in ALLOCATIONS if a.logical_ref=="U203")
    assert left.device==right.device=="OPA1655"
    assert left.physical_ref!=right.physical_ref
