# SR-042 update manifest

Base: develop `47f7c01e639f85ebc28d77f7eb2d84718a8caf4b`.

Adds the native-KiCad hand-off after routing release:
- frozen-hole placement reference board;
- 250-reference placement manifest;
- mounting-hole manifest;
- native routing-bootstrap contract;
- regression tests.

No copper routing is generated in Python. KiCad remains authoritative for pads,
nets, zones, routing and edit history.
