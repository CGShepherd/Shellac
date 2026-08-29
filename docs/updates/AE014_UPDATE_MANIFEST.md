# AE-014 update manifest

Base commit: `27f0a0eb641347925cb5e99e2c4f821553961bac`

Adds analysis only:
- generator/model/sch101_precision_candidate.py
- tests/test_sch101_precision_candidate.py
- docs/AE-014_SCH101_Precision_Architecture_Downselect_Rev_A0.md
- docs/decisions/DR-038_SCH101_Precision_Architecture_PROPOSED.md
- docs/updates/AE014_UPDATE_MANIFEST.md

No controlled schematic/component value is changed.

Validate:
`python -m pytest`

Suggested commit after review:
`git add -A`
`git commit -m "analysis(sch101): down-select precision front-end architecture"`
`git push`
