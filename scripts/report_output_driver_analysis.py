from pathlib import Path
import sys
REPO_ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(REPO_ROOT))

from generator.model.final_gain import gain_budget
from generator.model.output_driver import (
    COMMON_MODE_CAPACITANCE_UF, DATASHEET_MAX_OUTPUT_RMS_V, DESIGN_OUTPUT_RMS_V,
    DIFFERENTIAL_GAIN_DB, DIFFERENTIAL_GAIN_LINEAR, DRIVER, MUTE_SWITCH,
    NOMINAL_INPUT_RMS_V, SEVERE_INPUT_RMS_V, output_budget, validate_output_driver,
)

def main()->int:
    validate_output_driver()
    print("SCH108 balanced-output analysis")
    print(f"Driver: {DRIVER}")
    print(f"Differential gain: {DIFFERENTIAL_GAIN_LINEAR:.3f}x ({DIFFERENTIAL_GAIN_DB:.3f} dB)")
    print(f"Mute: {MUTE_SWITCH}, switching both driver inputs between signal and 0VA")
    print(f"Common-mode offset reduction: two {COMMON_MODE_CAPACITANCE_UF:g} uF non-polar sense capacitors per channel")
    print(f"Conservative differential-output ceiling: {DESIGN_OUTPUT_RMS_V:.2f} V RMS")
    print(f"Datasheet high-output capability: {DATASHEET_MAX_OUTPUT_RMS_V:.2f} V RMS")
    print()
    print(f"{'Case':<10} {'SCH104 out/V':>14} {'Balanced out/V':>16} {'Peak/V':>10} {'Margin/dB':>12}")
    print("-"*68)
    for name,value in (("Nominal",NOMINAL_INPUT_RMS_V),("Severe",SEVERE_INPUT_RMS_V)):
        budget=output_budget(value)
        print(f"{name:<10} {value:>14.3f} {budget.differential_output_rms_v:>16.3f} {budget.differential_output_peak_v:>10.3f} {budget.margin_to_design_ceiling_db:>12.3f}")
    print()
    print("System gain correction: SCH104=0 dB, THAT1646=+6.021 dB; net unchanged from pre-AE008 architecture.")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
