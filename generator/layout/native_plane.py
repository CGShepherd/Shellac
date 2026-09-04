from __future__ import annotations
from dataclasses import dataclass
import re, uuid

@dataclass(frozen=True, slots=True)
class PowerNetDiscovery:
    zero_va: tuple[int,str] | None
    positive_rail: tuple[int,str] | None
    negative_rail: tuple[int,str] | None

def net_table(text:str)->dict[int,str]:
    return {int(n):name for n,name in re.findall(r'\(net\s+(\d+)\s+"([^"]*)"\)', text)}

def discover_power_nets(text:str)->PowerNetDiscovery:
    nets=net_table(text)
    def find(names):
        hits=[(n,name) for n,name in nets.items() if name.upper() in {x.upper() for x in names}]
        return hits[0] if len(hits)==1 else None
    return PowerNetDiscovery(find({"0VA"}), find({"+17V","+17 V","17V","+V17","V+17"}), find({"-17V","-17 V","V-17","-V17"}))

def deterministic_uuid(name:str)->str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "ProjectShellac/AE035/"+name))

def in1_zone_block(net_id:int, net_name:str, x0=20.5, y0=20.5, x1=239.5, y1=159.5)->str:
    u=deterministic_uuid("In1_0VA_zone")
    lines=[
        "\t(zone",
        f"\t\t(net {net_id})",
        f'\t\t(net_name "{net_name}")',
        '\t\t(layer "In1.Cu")',
        f'\t\t(uuid "{u}")',
        "\t\t(hatch edge 0.5)",
        "\t\t(connect_pads",
        "\t\t\t(clearance 0.25)",
        "\t\t)",
        "\t\t(min_thickness 0.25)",
        "\t\t(fill yes",
        "\t\t\t(thermal_gap 0.3)",
        "\t\t\t(thermal_bridge_width 0.3)",
        "\t\t)",
        "\t\t(polygon",
        "\t\t\t(pts",
        f"\t\t\t\t(xy {x0:.3f} {y0:.3f})",
        f"\t\t\t\t(xy {x1:.3f} {y0:.3f})",
        f"\t\t\t\t(xy {x1:.3f} {y1:.3f})",
        f"\t\t\t\t(xy {x0:.3f} {y1:.3f})",
        "\t\t\t)",
        "\t\t)",
        "\t)",
    ]
    return "\n".join(lines)+"\n"

def add_in1_zone(text:str)->str:
    p=discover_power_nets(text)
    if p.zero_va is None: raise ValueError("0VA net is not uniquely discoverable")
    marker=deterministic_uuid("In1_0VA_zone")
    if marker in text: return text
    insert=text.rfind("\n)")
    if insert<0: raise ValueError("cannot locate root KiCad PCB closing parenthesis")
    return text[:insert]+"\n"+in1_zone_block(*p.zero_va)+text[insert:]

def audit_in1_zone(text:str)->list[str]:
    issues=[]; p=discover_power_nets(text)
    if p.zero_va is None: issues.append("0VA net unavailable")
    if deterministic_uuid("In1_0VA_zone") not in text: issues.append("AE-035 In1 0VA zone absent")
    return issues
