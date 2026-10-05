"""Current DR-038 precision-CAD contract after AE-076C.

Gain programming remains live. AE-075B selected LT5400BIMS8E-7#PBF and EP9 to
quiet 0VA. AE-076C selects two local per-channel passive cartridge-personality
cards; that load architecture remains selected-next until controlled live/native
migration.
"""
from __future__ import annotations
from dataclasses import dataclass

LT5400_FAMILY="LT5400"
LT5400_OPTION="LT5400-7"
LT5400_MPN="LT5400BIMS8E-7#PBF"
LT5400_GRADE="B_SELECTED"
LT5400_MANUFACTURER="Analog Devices"
LT5400_DATASHEET="LT5400 Rev C"
LT5400_R1_OHM=5_000.0
LT5400_R2_OHM=1_250.0
LT5400_R3_OHM=1_250.0
LT5400_R4_OHM=5_000.0
LT5400_RATIO=4.0
LT5400_RESISTOR_PINS={"R1":("1","8"),"R2":("2","7"),"R3":("3","6"),"R4":("4","5")}
LT5400_EXPOSED_PAD_PIN="9"
LT5400_EXPOSED_PAD_ELECTRICAL="QUIET_0VA"
LT5400_TOLERANCE_CMRR_AUTHORITY="RUN10_OPEN"
LT5400_MATCHING_DRIFT_TYP_PPM_C=0.2
LT5400_MATCHING_DRIFT_MAX_PPM_C=1.0
LT5400_PACKAGE="MS8E: 8-lead plastic MSOP with exposed pad"
LT5400_CAD_FOOTPRINT_STATUS="EXACT_MPN_SELECTED_EP9_IMPLEMENTED"
LT5400_CAD_RULE=("Exact LT5400BIMS8E-7#PBF; EP9 bonds to quiet 0VA; RUN10 complete-stage tolerance/CMRR and 20 kHz parasitics remain open.")

GAIN_SERVICE_SHUNT_MPN="Samtec MNT-104-BK-G"
GAIN_SERVICE_HEADER_MPN="Samtec TSW-104-07-G-D"
GAIN_SERVICE_HEADER_REFS={"LOW":"H110","HIGH":"H111","DEFAULT_PARK":"H112"}
GAIN_SERVICE_PAIRING_STATUS="PRODUCTION_PAIRING_ORIENTATION_VERIFICATION_OPEN"
GAIN_SERVICE_RULE=("Four-gang gold shunt programs all gain legs; no LOW/HIGH bridge is the complete default; PARK is inert.")

LOAD_PERSONALITY_ARCHITECTURE="TWO_IDENTICAL_PER_CHANNEL_PASSIVE_CARDS"
LOAD_PERSONALITY_IMPLEMENTATION_STATUS="SELECTED_NEXT_PENDING_LIVE_MIGRATION"
LOAD_PERSONALITY_MAIN_SOCKET_MPN="Samtec SLW-102-01-G-D"
LOAD_PERSONALITY_CARD_HEADER_MPN="Samtec TSW-102-07-G-D"
LOAD_PERSONALITY_SELECTED_REFS={"L":"H120","R":"H220"}
LOAD_PERSONALITY_PIN_NODES={1:"POS",2:"NEG",3:"NEG",4:"POS"}
LOAD_PERSONALITY_STATES=("BASE_NO_CARD","PLUS_47_PF_PAIR","PLUS_100_PF_PAIR")
LOAD_PERSONALITY_PARASITIC_AUTHORITY="RUN10_OPEN"
LOAD_PERSONALITY_RULE=("One local 2x2 interface per channel, differential shunt only; audio path does not traverse the card; diagonal duplicate-node mapping makes 180-degree insertion electrically benign; no card is BASE; +47/+100 pF are matched L/R service pairs selected using cartridge plus measured cable capacitance.")

@dataclass(frozen=True,slots=True)
class PrecisionCadGate:
    name:str
    status:str
    acceptance:tuple[str,...]

GATES=(
    PrecisionCadGate("LT5400 complete-stage tolerance / CMRR","OPEN",("RUN10 complete-stage tolerance/CMRR","RUN10 20 kHz parasitics","retain exact MPN and EP9-to-quiet-0VA")),
    PrecisionCadGate("Gain service hardware","OPEN",("MNT-104 pairing/orientation","LOW/HIGH/PARK mapping","all four gain legs identical")),
    PrecisionCadGate("Cartridge personality interface","OPEN",("exact SLW/TSW footprint/MCAD","live SCH101/native migration","diagonal pin-map verification","RUN10 capacitance and L/R matching")),
)

def validate_precision_cad_contract()->None:
    assert LT5400_R1_OHM/LT5400_R2_OHM==LT5400_RATIO
    assert LT5400_R4_OHM/LT5400_R3_OHM==LT5400_RATIO
    all_pins=[p for pair in LT5400_RESISTOR_PINS.values() for p in pair]
    assert sorted(all_pins,key=int)==[str(i) for i in range(1,9)]
    assert LT5400_MPN=="LT5400BIMS8E-7#PBF"
    assert LT5400_GRADE=="B_SELECTED"
    assert LT5400_EXPOSED_PAD_ELECTRICAL=="QUIET_0VA"
    assert LOAD_PERSONALITY_SELECTED_REFS=={"L":"H120","R":"H220"}
    assert LOAD_PERSONALITY_PIN_NODES[1]==LOAD_PERSONALITY_PIN_NODES[4]=="POS"
    assert LOAD_PERSONALITY_PIN_NODES[2]==LOAD_PERSONALITY_PIN_NODES[3]=="NEG"
    assert LOAD_PERSONALITY_IMPLEMENTATION_STATUS.startswith("SELECTED_NEXT")
