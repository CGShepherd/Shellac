"""AE-041 / AE-009 SCH109 controls and user-interface engineering model."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
class ControlsStatus(str, Enum):
    DEFINED="defined"; ELECTRICALLY_CLOSED="electrically_closed"; ARCHITECTURE_SELECTED_PROCUREMENT_PARTIAL="architecture_selected_procurement_partial"; PHYSICAL_HARDWARE_SELECTED="physical_hardware_selected"
DESIGN_STATUS=ControlsStatus.ARCHITECTURE_SELECTED_PROCUREMENT_PARTIAL
LED_SERIES_RESISTANCE_OHM=8200.0; NOMINAL_RAIL_VOLTAGE_V=18.0; ASSUMED_LED_FORWARD_V=2.4
LED_CURRENT_A=(NOMINAL_RAIL_VOLTAGE_V-ASSUMED_LED_FORWARD_V)/LED_SERIES_RESISTANCE_OHM
EQ_ROTARY_MANUFACTURER="NKK"; EQ_ROTARY_FAMILY="NR01"; EQ_ROTARY_MPN="OPEN — exact NR01 production order code pending mechanical/wafer confirmation"
MATRIX_MANUFACTURER="C&K"; MATRIX_MPN="A30403RNCB"; MATRIX_FALLBACK_MPN="TE/Alcoswitch MRJE3404"
TOGGLE_MANUFACTURER="C&K"; TOGGLE_MPN="7201SYCBE"; LED_MANUFACTURER="Vishay"; LED_MPN="TLLG4401"; LED_BEZEL_MANUFACTURER="Arcolectric / Bulgin"; LED_BEZEL_MPN="A104700BLACK"
@dataclass(frozen=True, slots=True)
class ControlDefinition:
    identifier:str; name:str; control_type:str; positions:tuple[str,...]; electrical_function:str; manufacturer:str; mpn:str; channel:str|None=None
    mounting:str="PCB through-hole with threaded bushing through top cover; PCB/standoffs define geometry and bushing is a secondary structural connection"
    switching:str="Break-before-make"
@dataclass(frozen=True, slots=True)
class IndicatorDefinition:
    identifier:str; name:str; rail:str; resistor_ohm:float; nominal_current_a:float; manufacturer:str=LED_MANUFACTURER; mpn:str=LED_MPN; bezel_manufacturer:str=LED_BEZEL_MANUFACTURER; bezel_mpn:str=LED_BEZEL_MPN
    mounting:str="Audio-chassis top cover, central longitudinal spine, panel-mounted black brass bezel, short flying leads"
BASS_POSITIONS=("FLAT","200 Hz","400 Hz","500 Hz 78","TRUE RIAA"); TREBLE_POSITIONS=("FLAT","1600 Hz","2121 Hz RIAA","3400 Hz","5800 Hz")
CONTROLS=(
 ControlDefinition("SW901L","Bass characteristic L","5-position rotary",BASS_POSITIONS,"Independent left-channel selection of the complete SCH103 bass RS+C branches.",EQ_ROTARY_MANUFACTURER,EQ_ROTARY_MPN,"L"),
 ControlDefinition("SW901R","Bass characteristic R","5-position rotary",BASS_POSITIONS,"Independent right-channel selection of the complete SCH103 bass RS+C branches.",EQ_ROTARY_MANUFACTURER,EQ_ROTARY_MPN,"R"),
 ControlDefinition("SW902L","Treble characteristic L","5-position rotary",TREBLE_POSITIONS,"Independent left-channel selection of the SCH103 passive treble networks.",EQ_ROTARY_MANUFACTURER,EQ_ROTARY_MPN,"L"),
 ControlDefinition("SW902R","Treble characteristic R","5-position rotary",TREBLE_POSITIONS,"Independent right-channel selection of the SCH103 passive treble networks.",EQ_ROTARY_MANUFACTURER,EQ_ROTARY_MPN,"R"),
 ControlDefinition("SW903","Channel mode","3P4T rotary",("DUAL LEFT","STEREO","L+R MONO","DUAL RIGHT"),"Two poles select L/R/MONO_AVG outputs; third pole connects the R 4.7k averaging leg only in L+R, eliminating intentional L-R coupling in other modes.",MATRIX_MANUFACTURER,MATRIX_MPN),
 ControlDefinition("SW904","Rumble filter","DPDT toggle",("BYPASS","IN"),"Selects direct or SCH107-filtered path for both channels.",TOGGLE_MANUFACTURER,TOGGLE_MPN),
 ControlDefinition("SW905","Output mute","DPDT toggle",("RUN","MUTE"),"Manual output-mute command; exact downstream contact implementation remains subject to mute fail-safe review.",TOGGLE_MANUFACTURER,TOGGLE_MPN))
INDICATORS=(IndicatorDefinition("LED901","+18 V","+18V",LED_SERIES_RESISTANCE_OHM,LED_CURRENT_A),IndicatorDefinition("LED902","-18 V","-18V",LED_SERIES_RESISTANCE_OHM,LED_CURRENT_A))
def validate_controls()->None:
    assert DESIGN_STATUS is ControlsStatus.ARCHITECTURE_SELECTED_PROCUREMENT_PARTIAL
    assert len(CONTROLS)==7 and [len(x.positions) for x in CONTROLS]==[5,5,5,5,4,2,2]
    assert CONTROLS[4].mpn==MATRIX_MPN and CONTROLS[4].control_type=="3P4T rotary"
    assert CONTROLS[5].mpn==CONTROLS[6].mpn==TOGGLE_MPN
    assert 0.0018<LED_CURRENT_A<0.0020
