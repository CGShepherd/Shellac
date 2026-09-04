from generator.model.opamp_package_audit import (
    FINAL_DEVICE_COUNTS,functional_channel_count,current_pseudo_package_count,
    physical_package_count,validate_package_plan,
)

def test_ae038_package_plan_balances():
    validate_package_plan()

def test_functional_channels_are_preserved():
    assert functional_channel_count()==18

def test_physical_package_overcount_is_eight():
    assert current_pseudo_package_count()-physical_package_count()==8

def test_no_unused_halves_in_recommended_plan():
    used=FINAL_DEVICE_COUNTS["OPA1656"]*2+FINAL_DEVICE_COUNTS["OPA1655"]+FINAL_DEVICE_COUNTS["OPA1612"]*2
    assert used==18
