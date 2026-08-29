# AE-013 update manifest

Base commit: `b7f3385bf85335c30c839989b72a72c03f20957e`

Adds:
- `generator/model/sch101_precision_analysis.py`
- `tests/test_sch101_precision_analysis.py`
- `docs/AE-013_SCH101_Noise_CMRR_Review_Rev_A0.md`
- `docs/updates/AE013_UPDATE_MANIFEST.md`

No existing circuit file is changed.

Key result:
- current 0.1% independent resistor policy gives worst-case CMRR of roughly
  53.5 / 50.1 / 48.4 dB for LOW / DEFAULT / HIGH;
- 0.01% ratio tracking raises deterministic worst-case CMRR to about 68 dB or
  better across all gain settings;
- current DEFAULT SCH101 white-noise estimate is about 18 nV/sqrt(Hz)
  input-referred;
- scaling the gain and differential resistor impedances by 0.1 gives about
  9 nV/sqrt(Hz), roughly a 6 dB improvement.

This package records a design-assurance finding, not an unapproved schematic change.

Validate:

`python -m pytest`

Then:

`git status`
`git add -A`
`git commit -m "analysis(sch101): review noise and tolerance-limited CMRR"`
`git push`
