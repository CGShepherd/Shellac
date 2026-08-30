# SR-043 update manifest

Base: develop commit `6952a3f3895c26835ad4810d00cf7be8ce3eab66`.

Automatic:
- 250 real-footprint placements;
- frozen Edge.Cuts;
- four NPTH mounting holes;
- native-board audit and DRC gate.

No copper is added.

After APPLY_SR043.bat configure four copper layers in KiCad and save, then run
VALIDATE_SR043.bat.
