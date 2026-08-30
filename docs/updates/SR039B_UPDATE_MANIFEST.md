# SR-039B — installer self-copy fix

Root cause:
`tools/apply_sr039_release_gate.py` attempted to copy files such as
`config/release/sr039_schematic_to_layout.yaml` onto the exact same path after
the SR-039 ZIP had already been extracted into the repository root.

Python correctly raised `shutil.SameFileError`, so the installer aborted before
updating DR-038, DR-039, DR-040, the decision index, or layout constraints.

SR-039B removes those self-copy operations, reruns the SR-039 installer, then
runs the full pytest suite.

No electrical or mechanical design changes are introduced by SR-039B.
