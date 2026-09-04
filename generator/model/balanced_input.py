from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from math import log10, pi
import cmath

DIFF_CONVERTER_GAIN=4.0
DIFF_RIN_OHM=1250.0
DIFF_RFB_OHM=5000.0
LT5400_FOOTPRINT="Package_SO:MSOP-8-1EP_3x3mm_P0.65mm_EP1.68x1.88mm"
GAIN_RG_OHM=1000.0
GAIN_BASE_RF_OHM=249.0
GAIN_DEFAULT_ADD_OHM=750.0
GAIN_HIGH_ADD_OHM=1910.0
DEFAULT_GAIN_DB=18.0
SELECTOR="Internal solder-link service configuration; default assembled state = DEFAULT"

# AE-037 cartridge-interface closure.
INPUT_SERIES_OHM=100.0
INPUT_LOAD_LEG_OHM=23700.0
INPUT_DIFFERENTIAL_LOAD_OHM=2.0*INPUT_LOAD_LEG_OHM
INPUT_CM_SHUNT_PF=47.0
INPUT_DIFF_SHUNT_PF=22.0
INPUT_DIFF_SHUNT_FITTED=False
INPUT_DEFAULT_BOARD_DIFF_CAP_PF=INPUT_CM_SHUNT_PF/2.0
CABLE_CAP_MIN_PF=50.0
CABLE_CAP_MAX_PF=300.0
MAX_BOARD_ADDED_RESPONSE_DB_20K=0.20

@dataclass(frozen=True,slots=True)
class CartridgeModel:
    name:str
    resistance_ohm:float
    inductance_h:float
    recommended_load_ohm:float

GRADO_78C=CartridgeModel("Grado 78C",475.0,45e-3,47000.0)
GRADO_GOLD=CartridgeModel("Grado Gold / 8MZ proxy",660.0,50e-3,47000.0)
SUPPORTED_CARTRIDGES=(GRADO_78C,GRADO_GOLD)

def _loaded_transfer(cartridge:CartridgeModel,frequency_hz:float,total_cap_pf:float)->complex:
    w=2.0*pi*frequency_hz
    z_source=cartridge.resistance_ohm+2.0*INPUT_SERIES_OHM+1j*w*cartridge.inductance_h
    c=total_cap_pf*1e-12
    y_load=1.0/INPUT_DIFFERENTIAL_LOAD_OHM + (1j*w*c if c else 0j)
    z_load=1.0/y_load
    return z_load/(z_source+z_load)

def board_added_response_db(cartridge:CartridgeModel,frequency_hz:float,cable_cap_pf:float)->float:
    base=_loaded_transfer(cartridge,frequency_hz,cable_cap_pf)
    with_board=_loaded_transfer(
        cartridge,frequency_hz,cable_cap_pf+INPUT_DEFAULT_BOARD_DIFF_CAP_PF
    )
    return 20.0*log10(abs(with_board/base))

class BalancedInputStatus(str,Enum):
    ELECTRICALLY_CLOSED="electrically_closed"
DESIGN_STATUS=BalancedInputStatus.ELECTRICALLY_CLOSED

@dataclass(frozen=True,slots=True)
class GainSetting:
    name:str
    target_total_db:float
    rf_ohm:float
    service_pattern:str
    @property
    def per_leg_gain(self): return 1.0+self.rf_ohm/GAIN_RG_OHM
    @property
    def total_gain(self): return self.per_leg_gain*DIFF_CONVERTER_GAIN
    @property
    def realised_total_db(self): return 20.0*log10(self.total_gain)
    @property
    def error_db(self): return self.realised_total_db-self.target_total_db

GAIN_SETTINGS=(
    GainSetting("LOW",14.0,249.0,"HI_BYPASS=FITTED; DEF_BYPASS=FITTED"),
    GainSetting("DEFAULT",18.0,999.0,"HI_BYPASS=FITTED; DEF_BYPASS=OPEN"),
    GainSetting("HIGH",22.0,2159.0,"HI_BYPASS=OPEN; DEF_BYPASS=FITTED"),
)
def default_setting(): return next(x for x in GAIN_SETTINGS if x.name=="DEFAULT")
def validate_balanced_input():
    assert DESIGN_STATUS is BalancedInputStatus.ELECTRICALLY_CLOSED
    assert DIFF_RFB_OHM/DIFF_RIN_OHM==DIFF_CONVERTER_GAIN
    assert abs(default_setting().realised_total_db-DEFAULT_GAIN_DB)<0.07
    assert all(abs(x.error_db)<0.08 for x in GAIN_SETTINGS)
    assert abs(INPUT_DIFFERENTIAL_LOAD_OHM-47400.0)<1.0
    assert INPUT_DIFF_SHUNT_FITTED is False
    assert INPUT_DEFAULT_BOARD_DIFF_CAP_PF==23.5
    for cartridge in SUPPORTED_CARTRIDGES:
        for cable_pf in (CABLE_CAP_MIN_PF,100.0,150.0,200.0,CABLE_CAP_MAX_PF):
            assert abs(board_added_response_db(cartridge,20000.0,cable_pf)) < MAX_BOARD_ADDED_RESPONSE_DB_20K
