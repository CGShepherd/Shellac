from pathlib import Path
import csv, json

from generator.layout.preliminary_placement import build_preliminary_placement_baseline
from generator.layout.sr040_routing_readiness import build_sr040_routing_readiness
from generator.mechanical.sr040_audio_freeze import frozen_audio_board_outline
from generator.procurement.full_bom_census import build_full_bom_census

out=Path("out/sr040")
out.mkdir(parents=True,exist_ok=True)

outline=frozen_audio_board_outline()
placement=build_preliminary_placement_baseline(
    width_mm=outline.outline.width_mm,
    depth_mm=outline.outline.depth_mm,
)
census=build_full_bom_census()
gate=build_sr040_routing_readiness()

(out/"routing_readiness.json").write_text(json.dumps(gate.to_dict(),indent=2),encoding="utf-8")
(out/"mechanical_outline.json").write_text(json.dumps(outline.to_dict(),indent=2),encoding="utf-8")
(out/"bom_census.json").write_text(json.dumps(census.to_dict(),indent=2),encoding="utf-8")

with (out/"critical_placement.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.writer(f)
    w.writerow(["ref","sheet","cluster","x_mm","y_mm","rotation_deg","footprint","manual_review"])
    manual=set(placement.manual_review_clusters)
    for p in placement.proposals:
        if p.cluster_id in manual:
            w.writerow([p.ref,p.sheet_id,p.cluster_id,p.x_mm,p.y_mm,p.rotation_deg,p.footprint,"YES"])

print(json.dumps(gate.to_dict(),indent=2))
print("SR-040 reports written to",out)
