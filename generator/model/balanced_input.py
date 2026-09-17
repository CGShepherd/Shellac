from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from math import log10, pi

DIFF_CONVERTER_GAIN=4.0
DIFF_RIN_OHM=1250.0
DIFF_RFB_OHM=5000.0
LT5400_FOOTPRINT="Package_SO:MSOP-8-1EP_3x3mm_P0.65mm_EP1.68x1.88mm"

# AE-042 / AE-066 product-migrated fail-safe gain programming.
GAIN_RG_OHM=1000.0
GAIN_FIXED_RF_OHM=999.0
GAIN_LOW_PARALLEL_RF_OHM=332.0
GAIN_HIGH_PARALLEL_RG_OHM=866.0
DEFAULT_GAIN_DB=18.0
SELECTOR=(
    "Internal removable gold ganged service shunt; normal DEFAULT has no active "
    "LOW/HIGH programming branch and the shunt is parked"
)

# AE-037 fixed cartridge interface retained.
INPUT_SERIES_OHM=100.0
INPUT_LOAD_LEG_OHM=23700.0
INPUT_DIFFERENTIAL_LOAD_OHM=2.0*INPUT_LOAD_LEG_OHM
INPUT_CM_SHUNT_PF=47.0
INPUT_FIXED_BOARD_DIFF_EQUIV_PF=INPUT_CM_SHUNT_PF/2.0

# AE-042 service-capacitance states, exercised by AE-066 RUN01.
SERVICE_CAPACITANCE_PF={
    "BASE":0.0,
    "PLUS_47":47.0,
    "PLUS_100":100.0,
}
DEFAULT_SERVICE_CAP_STATE="BASE"

CABLE_CAP_MIN_PF=50.0
CABLE_CAP_MAX_PF=300.0
MAX_BOARD_ADDED_RESPONSE_DB_20K=0.20

@dataclass(frozen=True,slots=True)
class CartridgeModel:
    name:str
    resistance_ohm:float
    inductance_h:float
    recommended_load_ohm:float

GRADO_78C=CartridgeModel("Grado Prestige 78C",475.0,45e-3,47000.0)
AT_VM95SP=CartridgeModel("Audio-Technica AT-VM95SP",485.0,550e-3,47000.0)
GRADO_GOLD=CartridgeModel("Grado Gold / 8MZ proxy",660.0,50e-3,47000.0)
SUPPORTED_CARTRIDGES=(GRADO_78C,AT_VM95SP,GRADO_GOLD)

# The legacy AE-037 <0.2 dB fixed-board-capacitance sanity check was not
# specified for the later high-inductance AT model. AE-066 RUN01 is current
# authority for the AT loading envelope.
AE037_FIXED_RF_SANITY_CARTRIDGES=(GRADO_78C,GRADO_GOLD)

def _loaded_transfer(cartridge:CartridgeModel,frequency_hz:float,total_cap_pf:float)->complex:
    w=2.0*pi*frequency_hz
    z_source=cartridge.resistance_ohm+2.0*INPUT_SERIES_OHM+1j*w*cartridge.inductance_h
    c=total_cap_pf*1e-12
    y_load=1.0/INPUT_DIFFERENTIAL_LOAD_OHM + (1j*w*c if c else 0j)
    z_load=1.0/y_load
    return z_load/(z_source+z_load)

def service_capacitance_pf(state:str)->float:
    try:
        return SERVICE_CAPACITANCE_PF[state]
    except KeyError as exc:
        raise ValueError(f"unknown SCH101 service-capacitance state {state!r}") from exc

def bookkeeping_total_cap_pf(cable_cap_pf:float,state:str=DEFAULT_SERVICE_CAP_STATE)->float:
    return (
        float(cable_cap_pf)
        + INPUT_FIXED_BOARD_DIFF_EQUIV_PF
        + service_capacitance_pf(state)
    )

def board_added_response_db(
    cartridge:CartridgeModel,
    frequency_hz:float,
    cable_cap_pf:float,
    service_state:str=DEFAULT_SERVICE_CAP_STATE,
)->float:
    base=_loaded_transfer(cartridge,frequency_hz,cable_cap_pf)
    with_board=_loaded_transfer(
        cartridge,
        frequency_hz,
        bookkeeping_total_cap_pf(cable_cap_pf,service_state),
    )
    return 20.0*log10(abs(with_board/base))

class BalancedInputStatus(str,Enum):
    ELECTRICALLY_CLOSED="electrically_closed"
    LIVE_IMPLEMENTATION_REQUALIFICATION_OPEN="live_implementation_requalification_open"
    AE042_IMPLEMENTED_QUALIFICATION_OPEN="ae042_implemented_qualification_open"

DESIGN_STATUS=BalancedInputStatus.AE042_IMPLEMENTED_QUALIFICATION_OPEN

def _parallel(a:float,b:float|None)->float:
    if b is None:
        return a
    return 1.0/(1.0/a+1.0/b)

@dataclass(frozen=True,slots=True)
class GainSetting:
    name:str
    target_total_db:float
    rf_program_ohm:float|None
    rg_program_ohm:float|None
    service_pattern:str

    @property
    def effective_rf_ohm(self)->float:
        return _parallel(GAIN_FIXED_RF_OHM,self.rf_program_ohm)

    @property
    def effective_rg_ohm(self)->float:
        return _parallel(GAIN_RG_OHM,self.rg_program_ohm)

    @property
    def rf_ohm(self)->float:
        return self.effective_rf_ohm

    @property
    def per_leg_gain(self)->float:
        return 1.0+self.effective_rf_ohm/self.effective_rg_ohm

    @property
    def total_gain(self)->float:
        return self.per_leg_gain*DIFF_CONVERTER_GAIN

    @property
    def realised_total_db(self)->float:
        return 20.0*log10(self.total_gain)

    @property
    def error_db(self)->float:
        return self.realised_total_db-self.target_total_db

GAIN_SETTINGS=(
    GainSetting("LOW",14.0,GAIN_LOW_PARALLEL_RF_OHM,None,"GAIN_SHUNT=LOW"),
    GainSetting("DEFAULT",18.0,None,None,"GAIN_SHUNT=PARK/DEFAULT"),
    GainSetting("HIGH",22.0,None,GAIN_HIGH_PARALLEL_RG_OHM,"GAIN_SHUNT=HIGH"),
)

def default_setting():
    return next(x for x in GAIN_SETTINGS if x.name=="DEFAULT")

def simultaneous_low_high_gain_db()->float:
    rf=_parallel(GAIN_FIXED_RF_OHM,GAIN_LOW_PARALLEL_RF_OHM)
    rg=_parallel(GAIN_RG_OHM,GAIN_HIGH_PARALLEL_RG_OHM)
    return 20.0*log10(DIFF_CONVERTER_GAIN*(1.0+rf/rg))

def validate_balanced_input():
    assert DESIGN_STATUS is BalancedInputStatus.AE042_IMPLEMENTED_QUALIFICATION_OPEN
    assert DIFF_RFB_OHM/DIFF_RIN_OHM==DIFF_CONVERTER_GAIN
    assert abs(default_setting().realised_total_db-DEFAULT_GAIN_DB)<0.07
    assert all(abs(x.error_db)<0.08 for x in GAIN_SETTINGS)
    assert default_setting().rf_program_ohm is None
    assert default_setting().rg_program_ohm is None
    assert abs(INPUT_DIFFERENTIAL_LOAD_OHM-47400.0)<1.0
    assert INPUT_FIXED_BOARD_DIFF_EQUIV_PF==23.5
    assert SERVICE_CAPACITANCE_PF=={"BASE":0.0,"PLUS_47":47.0,"PLUS_100":100.0}
    assert 10.0 < simultaneous_low_high_gain_db() < 22.0
    for cartridge in AE037_FIXED_RF_SANITY_CARTRIDGES:
        for cable_pf in (CABLE_CAP_MIN_PF,100.0,150.0,200.0,CABLE_CAP_MAX_PF):
            assert abs(board_added_response_db(cartridge,20000.0,cable_pf)) < MAX_BOARD_ADDED_RESPONSE_DB_20K
