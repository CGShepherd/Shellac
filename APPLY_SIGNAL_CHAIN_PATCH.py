from pathlib import Path
p=Path("generator/model/signal_chain_analysis.py")
t=p.read_text(encoding="utf-8")
if "post_eq_dc_block" not in t:
    t=t.replace(
        "from .output_driver import DIFFERENTIAL_GAIN_LINEAR, DESIGN_OUTPUT_RMS_V",
        "from .output_driver import DIFFERENTIAL_GAIN_LINEAR, DESIGN_OUTPUT_RMS_V\nfrom .post_eq_dc_block import magnitude as post_eq_dc_magnitude"
    )
    t=t.replace(
        "xlr = sch103 * rumble * DIFFERENTIAL_GAIN_LINEAR",
        "xlr = sch103 * post_eq_dc_magnitude(frequency_hz) * rumble * DIFFERENTIAL_GAIN_LINEAR"
    )
p.write_text(t,encoding="utf-8")
print("Patched signal_chain_analysis.py for DR-039")
