from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class AmplifierUnitAllocation:
    sheet: str
    logical_ref: str
    physical_ref: str
    device: str
    unit: str
    footprint: str
    role: str

SOIC8="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm"

ALLOCATIONS=(
    # SCH101: each cartridge channel keeps a local dual gain pair plus a
    # local single differential converter beside its LT5400.
    AmplifierUnitAllocation("SCH101","U101","U101","OPA1656","A",SOIC8,"L positive-leg gain"),
    AmplifierUnitAllocation("SCH101","U102","U101","OPA1656","B",SOIC8,"L negative-leg gain"),
    AmplifierUnitAllocation("SCH101","U103","U103","OPA1655","S",SOIC8,"L LT5400 differential converter"),
    AmplifierUnitAllocation("SCH101","U201","U201","OPA1656","A",SOIC8,"R positive-leg gain"),
    AmplifierUnitAllocation("SCH101","U202","U201","OPA1656","B",SOIC8,"R negative-leg gain"),
    AmplifierUnitAllocation("SCH101","U203","U203","OPA1655","S",SOIC8,"R LT5400 differential converter"),

    # SCH103: one dual OPA1612 per channel.
    AmplifierUnitAllocation("SCH103","U3001","U3001","OPA1612","A",SOIC8,"L active LF EQ"),
    AmplifierUnitAllocation("SCH103","U3002","U3001","OPA1612","B",SOIC8,"L recovery"),
    AmplifierUnitAllocation("SCH103","U3501","U3501","OPA1612","A",SOIC8,"R active LF EQ"),
    AmplifierUnitAllocation("SCH103","U3502","U3501","OPA1612","B",SOIC8,"R recovery"),

    # SCH104: one stereo dual.
    AmplifierUnitAllocation("SCH104","U401","U401","OPA1656","A",SOIC8,"L isolation buffer"),
    AmplifierUnitAllocation("SCH104","U402","U401","OPA1656","B",SOIC8,"R isolation buffer"),

    # SCH105: one stereo dual.
    AmplifierUnitAllocation("SCH105","U501","U501","OPA1656","A",SOIC8,"L mode buffer"),
    AmplifierUnitAllocation("SCH105","U502","U501","OPA1656","B",SOIC8,"R mode buffer"),

    # SCH107: one dual per channel.
    AmplifierUnitAllocation("SCH107","U700","U700","OPA1656","A",SOIC8,"L HP section A"),
    AmplifierUnitAllocation("SCH107","U720","U700","OPA1656","B",SOIC8,"L HP section B"),
    AmplifierUnitAllocation("SCH107","U750","U750","OPA1656","A",SOIC8,"R HP section A"),
    AmplifierUnitAllocation("SCH107","U770","U750","OPA1656","B",SOIC8,"R HP section B"),
)

DUAL_PIN_MAP={
    "A":{"OUT":"1","IN-":"2","IN+":"3"},
    "SUPPLY":{"V-":"4","V+":"8"},
    "B":{"IN+":"5","IN-":"6","OUT":"7"},
}
OPA1655_PIN_MAP={
    "IN-":"2","IN+":"3","V-":"4","OUT":"6","V+":"7",
}
OPA1655_NC_PINS=("1","5","8")

def physical_packages():
    by_key={}
    for a in ALLOCATIONS:
        key=(a.sheet,a.physical_ref)
        by_key.setdefault(key,[]).append(a)
    return by_key

def absorbed_logical_refs():
    return tuple(
        a.logical_ref for a in ALLOCATIONS
        if a.logical_ref != a.physical_ref
    )

def package_counts():
    counts={}
    for units in physical_packages().values():
        device=units[0].device
        counts[device]=counts.get(device,0)+1
    return counts

def validate_allocations():
    logical=[(a.sheet,a.logical_ref) for a in ALLOCATIONS]
    assert len(logical)==len(set(logical))==18

    packages=physical_packages()
    assert len(packages)==10

    for (_,physical_ref), units in packages.items():
        devices={x.device for x in units}
        footprints={x.footprint for x in units}
        assert len(devices)==1
        assert len(footprints)==1
        if units[0].device in {"OPA1656","OPA1612"}:
            assert {x.unit for x in units}=={"A","B"}
        elif units[0].device=="OPA1655":
            assert len(units)==1 and units[0].unit=="S"
        else:
            raise AssertionError(units[0].device)

    assert package_counts()=={"OPA1656":6,"OPA1655":2,"OPA1612":2}
    assert len(absorbed_logical_refs())==8
    assert set(absorbed_logical_refs())=={
        "U102","U202","U3002","U3502","U402","U502","U720","U770"
    }

    # All 18 intended amplifier channels are occupied; no unused dual half.
    used=sum(2 if d in {"OPA1656","OPA1612"} else 1 for d in
             [units[0].device for units in packages.values()])
    assert used==18
