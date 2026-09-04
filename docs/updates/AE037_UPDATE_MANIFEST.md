# AE-037 update manifest

Complete replacement files; no manual patching.

Replaces:
- generator/model/balanced_input.py
- generator/blocks/balanced_input.py
- tests/test_balanced_input.py
- tests/test_balanced_input_gain.py

Adds:
- docs/design_pack/AE-037_SCH101_Cartridge_Interface_Closure_Rev_A0.md
- docs/updates/AE037_UPDATE_MANIFEST.md

Run:
1. `python -m pytest tests/test_balanced_input.py tests/test_balanced_input_gain.py -v`
2. `build_shellac.bat`
3. `python -m pytest`

Because AE-036B is installed, the native PCB must survive the clean build.
