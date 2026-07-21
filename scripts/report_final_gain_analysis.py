from pathlib import Path
import sys
REPO_ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(REPO_ROOT))
from generator.model.final_gain import *

def main()->int:
    validate_final_gain_stage()
    print("SCH104 final-gain electrical closure")
    print(f"Device: {OPAMP}")
    print(f"Rails: +/-{SUPPLY_RAIL_V:g} V")
    print(f"Gain={GAIN_LINEAR:.4f}x ({GAIN_DB:.3f} dB)")
    print(f"Output isolation={OUTPUT_ISOLATION_OHM:g} ohm")
    print(f"Conservative design ceiling={DESIGN_OUTPUT_RMS_V:g} V RMS")
    for label,value in (("Nominal",NOMINAL_INPUT_RMS_V),("Severe",SEVERE_INPUT_RMS_V)):
        b=gain_budget(value)
        print(f"{label}: input={b.input_rms_v:.3f} V RMS, output={b.output_rms_v:.3f} V RMS, peak={b.output_peak_v:.3f} V, margin={b.margin_to_design_ceiling_db:.2f} dB")
    return 0
if __name__=='__main__': raise SystemExit(main())
