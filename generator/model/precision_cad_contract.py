"""AE-018/AE-071A physical/electrical contracts for DR-038 precision CAD.

AE-071A migrates the AE-042 fail-safe removable-shunt topology into the live
product generator. LT5400-7 B grade is the procurement-feasible family;
numeric tolerance/CMRR acceptance remains explicitly owned by RUN10.
"""
from __future__ import annotations
from dataclasses import dataclass

LT5400_FAMILY="LT5400"
LT5400_OPTION="LT5400-7"
LT5400_GRADE="B_CANDIDATE"
LT5400_MANUFACTURER="Analog Devices"
LT5400_DATASHEET="LT5400 Rev C"

LT5400_R1_OHM=5_000.0
LT5400_R2_OHM=1_250.0
LT5400_R3_OHM=1_250.0
LT5400_R4_OHM=5_000.0
LT5400_RATIO=4.0

LT5400_RESISTOR_PINS={
    "R1":("1","8"),
    "R2":("2","7"),
    "R3":("3","6"),
    "R4":("4","5"),
}
LT5400_EXPOSED_PAD_PIN="9"
LT5400_EXPOSED_PAD_ELECTRICAL="FLOATING"
LT5400_TOLERANCE_CMRR_AUTHORITY="RUN10_OPEN"
LT5400_MATCHING_DRIFT_TYP_PPM_C=0.2
LT5400_MATCHING_DRIFT_MAX_PPM_C=1.0

LT5400_PACKAGE="MS8E: 8-lead plastic MSOP with exposed pad"
LT5400_CAD_FOOTPRINT_STATUS="FOOTPRINT_BOUND_EP_DISPOSITION_OPEN"
LT5400_CAD_RULE=(
    "One physical MS8E component per channel; pad 9 exists physically and is "
    "currently electrically floating pending RUN10/AE-072 disposition."
)

GAIN_SERVICE_SHUNT_CANDIDATE="Samtec MNT-104-BK-G"
GAIN_SERVICE_HEADER_CANDIDATE="Samtec TSW-104-07-G-D"
GAIN_SERVICE_HEADER_REFS={"LOW":"H110","HIGH":"H111","DEFAULT_PARK":"H112"}
GAIN_SERVICE_PAIRING_STATUS="PRODUCTION_PAIRING_ORIENTATION_VERIFICATION_OPEN"
GAIN_SERVICE_RULE=(
    "One removable four-gang gold shunt configures all L+/L-/R+/R- legs. "
    "DEFAULT is complete with no LOW/HIGH branch bridged; normal shunt location "
    "is electrically inert PARK. Ordinary DIP switching is prohibited."
)

LOAD_SERVICE_SHUNT_CANDIDATE="Samtec MNT-102-BK-G"
LOAD_SERVICE_HEADER_CANDIDATE="Samtec TSW-102-07-G-D"
LOAD_SERVICE_HEADER_REFS={"PLUS_47":"H120","BASE_PARK":"H121","PLUS_100":"H122"}
LOAD_SERVICE_PAIRING_STATUS="PRODUCTION_PAIRING_ORIENTATION_VERIFICATION_OPEN"

@dataclass(frozen=True,slots=True)
class PrecisionCadGate:
    name:str
    status:str
    acceptance:tuple[str,...]

GATES=(
    PrecisionCadGate(
        "LT5400 exposed pad / RUN10 tolerance",
        "OPEN",
        (
            "B-grade complete tolerance/CMRR stack accepted by RUN10",
            "final temperature-grade MPN selected",
            "pad 9 disposition confirmed before layout/BOM freeze",
        ),
    ),
    PrecisionCadGate(
        "AE-042 gain service hardware",
        "OPEN",
        (
            "production MNT-104 internal pairing/orientation verified",
            "LOW/HIGH/PARK silkscreen and continuity mapping verified",
            "single supplied shunt returns missing/open state to DEFAULT",
            "all four gain legs configured identically",
        ),
    ),
    PrecisionCadGate(
        "AE-042 load service hardware",
        "OPEN",
        (
            "production MNT-102 internal pairing/orientation verified",
            "BASE/+47/+100 continuity mapping verified",
            "service-header parasitic/layout effect accepted before final routing",
        ),
    ),
)

def validate_precision_cad_contract()->None:
    assert LT5400_R1_OHM/LT5400_R2_OHM==LT5400_RATIO
    assert LT5400_R4_OHM/LT5400_R3_OHM==LT5400_RATIO
    assert set(LT5400_RESISTOR_PINS)=={"R1","R2","R3","R4"}
    all_pins=[p for pair in LT5400_RESISTOR_PINS.values() for p in pair]
    assert sorted(all_pins,key=int)==[str(i) for i in range(1,9)]
    assert LT5400_EXPOSED_PAD_PIN not in all_pins
    assert LT5400_GRADE=="B_CANDIDATE"
    assert LT5400_TOLERANCE_CMRR_AUTHORITY=="RUN10_OPEN"
    assert GAIN_SERVICE_HEADER_REFS["DEFAULT_PARK"]=="H112"
    assert LOAD_SERVICE_HEADER_REFS["BASE_PARK"]=="H121"
