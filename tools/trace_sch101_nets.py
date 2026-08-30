from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))

from collections import defaultdict, deque
from generator.blocks.balanced_input import add_sch101_diff_converter_slice
from generator.core.geometry import Point
from generator.core.sheet import Sheet
from generator.core.pins import SYMBOL_PIN_CONTRACTS, pin_position
from generator.electrical_audit import _point_on_segment

def key(p):
    return (round(float(p.x),8),round(float(p.y),8))

def graph_for(sheet):
    nodes=set()
    for w in sheet.wires:
        nodes.add((round(w.x1,8),round(w.y1,8)))
        nodes.add((round(w.x2,8),round(w.y2,8)))
    for lab in sheet.labels:
        nodes.add((round(lab.x,8),round(lab.y,8)))
    for c in sheet.components:
        for pin in SYMBOL_PIN_CONTRACTS.get(c.lib_id,{}):
            nodes.add(key(pin_position(c,pin)))
    graph=defaultdict(set)
    pts=[Point(*n) for n in nodes]
    for w in sheet.wires:
        on=[p for p in pts if _point_on_segment(p,w)]
        on.sort(key=lambda p:(p.x,p.y) if abs(w.x2-w.x1)>=abs(w.y2-w.y1) else (p.y,p.x))
        for a,b in zip(on,on[1:]):
            ka,kb=key(a),key(b)
            graph[ka].add(kb); graph[kb].add(ka)
    return graph

def connected(graph,source):
    seen={source}; q=deque([source])
    while q:
        n=q.popleft()
        for m in graph[n]:
            if m not in seen:
                seen.add(m); q.append(m)
    return seen

def main():
    sheet=Sheet("SCH101","SCH101.kicad_sch")
    add_sch101_diff_converter_slice(sheet)
    graph=graph_for(sheet)
    label_points=defaultdict(list)
    for lab in sheet.labels:
        label_points[lab.name].append((round(lab.x,8),round(lab.y,8)))
    targets=["0VA","PRE_EQ_L","PRE_EQ_R"]
    for target in targets:
        if target not in label_points:
            continue
        seen=connected(graph,label_points[target][0])
        labels=sorted({lab.name for lab in sheet.labels if (round(lab.x,8),round(lab.y,8)) in seen})
        pins=[]
        for c in sheet.components:
            for pin in SYMBOL_PIN_CONTRACTS.get(c.lib_id,{}):
                if key(pin_position(c,pin)) in seen:
                    pins.append(f"{c.ref}.{pin}")
        print("\n===",target,"===")
        print("labels:",", ".join(labels))
        print("pins:",", ".join(sorted(pins)))

if __name__=="__main__":
    main()
