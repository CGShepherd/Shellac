from pathlib import Path
import json
from generator.layout.sr042_native_routing_bootstrap import write_native_routing_bootstrap
from generator.mechanical.released_placement_board import write_released_placement_reference_board

out=Path("out/sr042")
gate=write_native_routing_bootstrap(out)
ref=write_released_placement_reference_board(
    Path("out/kicad/ProjectShellac_PlacementReference.kicad_pcb"))
print(json.dumps(gate.to_dict(),indent=2))
print("Placement reference:",ref)
print("SR-042 manifests:",out)
