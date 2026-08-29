# AE-012 update manifest

Base commit: `da19a2721c8adfa4d6fedcc0a4f419fa32c4b796`

Replaces:
- `generator/model/signal_chain_analysis.py`
- `tests/test_signal_chain_analysis.py`

Adds:
- `docs/AE-012_All_State_Gain_Headroom_Closure_Rev_A0.md`
- `docs/updates/AE012_UPDATE_MANIFEST.md`

Dense sweep result at 5 mV RMS:
- LOW worst wanted-band margin: ~8.58 dB
- DEFAULT: ~4.64 dB
- HIGH: ~0.61 dB
- limiting case: complete RIAA, rumble bypass, ~20 Hz

Apply by extracting at repository root, then:

`python -m pytest`

If clean:

`git status`
`git add -A`
`git commit -m "analysis(signal-chain): close all-state gain and headroom envelope"`
`git push`
