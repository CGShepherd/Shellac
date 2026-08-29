# AE-015 update manifest

Base commit: `f51ef216c881773371359a5567a1a495f5815b9d`

Adds analysis only:
- `generator/model/signal_chain_noise_dc.py`
- `tests/test_signal_chain_noise_dc.py`
- `docs/AE-015_Full_Chain_Noise_DC_Review_Rev_A0.md`
- `docs/decisions/DR-039_Common_Post_EQ_DC_Block_PROPOSED.md`
- `docs/updates/AE015_UPDATE_MANIFEST.md`

No existing schematic or controlled circuit value is changed.

Key findings:
- full-RIAA electronics output noise ~109 µV RMS;
- electronics SNR ~75.5 dB at nominal default-gain output;
- rumble-filter noise penalty is small;
- conservative direct-coupled DC stack-up exceeds 3 V differential;
- proposed 1 µF film + 330 kΩ post-EQ block reduces upstream DC propagation
  while losing <0.01 dB at 20 Hz.

Validate:
`python -m pytest`

Suggested commit:
`git add -A`
`git commit -m "analysis(signal-chain): close noise review and identify DC-block requirement"`
`git push`
