from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from math import log10

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
