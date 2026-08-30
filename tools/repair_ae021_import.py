from pathlib import Path

p = Path("generator/model/signal_chain_analysis.py")
text = p.read_text(encoding="utf-8")

bad = (
    "from .output_driver import DIFFERENTIAL_GAIN_LINEAR, DESIGN_OUTPUT_RMS_V"
    "\\nfrom .post_eq_dc_block import magnitude as post_eq_dc_magnitude"
)
good = (
    "from .output_driver import DIFFERENTIAL_GAIN_LINEAR, DESIGN_OUTPUT_RMS_V\n"
    "from .post_eq_dc_block import magnitude as post_eq_dc_magnitude"
)

if bad in text:
    text = text.replace(bad, good, 1)
    p.write_text(text, encoding="utf-8")
    print("Repaired literal \\\\n in signal_chain_analysis.py import.")
elif good in text:
    print("signal_chain_analysis.py import already repaired.")
else:
    raise SystemExit("Expected broken or repaired import pattern not found.")
