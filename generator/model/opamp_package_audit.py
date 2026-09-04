from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class PackagePlan:
    sheet: str
    family: str
    functional_channels: int
    current_pseudo_packages: int
    physical_packages: int
    allocation: str

PLANS=(
    PackagePlan("SCH101","OPA165x",6,6,4,"2x OPA1656 dual gain pairs + 2x OPA1655 single differential converters"),
    PackagePlan("SCH103","OPA1612",4,4,2,"one OPA1612 dual per channel"),
    PackagePlan("SCH104","OPA1656",2,2,1,"one stereo dual package"),
    PackagePlan("SCH105","OPA1656",2,2,1,"one stereo dual package"),
    PackagePlan("SCH107","OPA1656",4,4,2,"one dual package per channel"),
)

FINAL_DEVICE_COUNTS={"OPA1656":6,"OPA1655":2,"OPA1612":2}

def functional_channel_count():
    return sum(x.functional_channels for x in PLANS)

def current_pseudo_package_count():
    return sum(x.current_pseudo_packages for x in PLANS)

def physical_package_count():
    return sum(x.physical_packages for x in PLANS)

def validate_package_plan():
    assert functional_channel_count()==18
    assert current_pseudo_package_count()==18
    assert physical_package_count()==10
    assert sum(FINAL_DEVICE_COUNTS.values())==10
    assert FINAL_DEVICE_COUNTS["OPA1656"]*2 + FINAL_DEVICE_COUNTS["OPA1655"] + FINAL_DEVICE_COUNTS["OPA1612"]*2 == 18
