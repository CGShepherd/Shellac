from pathlib import Path
import csv,json
from generator.layout.sr041_routing_release import build_sr041_routing_release
from generator.layout.preliminary_placement import build_preliminary_placement_baseline
from generator.mechanical.sr040_audio_freeze import frozen_audio_board_outline

out=Path("out/sr041")
out.mkdir(parents=True,exist_ok=True)
gate=build_sr041_routing_release()
outline=frozen_audio_board_outline()
placement=build_preliminary_placement_baseline(
    width_mm=outline.outline.width_mm,
    depth_mm=outline.outline.depth_mm,
)

(out/"routing_release.json").write_text(json.dumps(gate.to_dict(),indent=2),encoding="utf-8")

with (out/"accepted_placement.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.writer(f)
    w.writerow(["ref","sheet","cluster","x_mm","y_mm","rotation_deg","footprint","routing_baseline"])
    for p in placement.proposals:
        w.writerow([p.ref,p.sheet_id,p.cluster_id,p.x_mm,p.y_mm,p.rotation_deg,p.footprint,"YES"])

with (out/"mounting_holes.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.writer(f)
    w.writerow(["id","x_mm","y_mm","finished_diameter_mm","copper_keepout_diameter_mm"])
    for h in outline.mounting_holes:
        w.writerow([h.identifier,h.centre.x_mm,h.centre.y_mm,h.finished_diameter_mm,h.copper_keepout_diameter_mm])

print(json.dumps(gate.to_dict(),indent=2))
print("SR-041 reports written to",out)
