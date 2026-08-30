from __future__ import annotations
from pathlib import Path
import re
import uuid

from generator.layout.preliminary_placement import build_preliminary_placement_baseline
from generator.mechanical.sr040_audio_freeze import frozen_audio_board_outline

BOARD=Path("out/kicad/ProjectShellac.kicad_pcb")
ORIGIN_X=20.0
ORIGIN_Y=20.0

def _matching_paren(text: str, start: int) -> int:
    depth=0
    quoted=False
    escaped=False
    for i in range(start,len(text)):
        c=text[i]
        if quoted:
            if escaped:
                escaped=False
            elif c=="\\":
                escaped=True
            elif c=='"':
                quoted=False
            continue
        if c=='"':
            quoted=True
        elif c=='(':
            depth+=1
        elif c==')':
            depth-=1
            if depth==0:
                return i+1
    raise ValueError("unbalanced KiCad S-expression")

def _top_blocks(text: str, token: str):
    needle=f"\n\t({token}"
    pos=0
    while True:
        start=text.find(needle,pos)
        if start<0:
            break
        start+=1
        end=_matching_paren(text,start)
        yield start,end,text[start:end]
        pos=end

def _reference(block: str):
    m=re.search(r'\(property\s+"Reference"\s+"([^"]+)"',block)
    return m.group(1) if m else None

def _replace_footprint_at(block: str, x: float, y: float, rotation: float) -> str:
    prop=block.find("(property")
    head=block if prop<0 else block[:prop]
    m=re.search(r'\(at\s+[-+0-9.eE]+\s+[-+0-9.eE]+(?:\s+[-+0-9.eE]+)?\)',head)
    if not m:
        raise ValueError("footprint has no top-level at position")
    repl=f"(at {x:.3f} {y:.3f} {rotation:.1f})"
    return block[:m.start()]+repl+block[m.end():]

def _det_uuid(name: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL,"ProjectShellac/SR043/"+name))

def _hole_block(ref: str, x: float, y: float, drill: float, keepout: float) -> str:
    return (
        '\t(footprint "MountingHole:MountingHole_3.2mm_M3"\n'
        '\t\t(layer "F.Cu")\n'
        f'\t\t(uuid "{_det_uuid(ref)}")\n'
        f'\t\t(at {x:.3f} {y:.3f})\n'
        f'\t\t(property "Reference" "{ref}" (at 0 -4 0) (layer "F.SilkS")\n'
        '\t\t\t(effects (font (size 1 1) (thickness 0.15)))\n'
        '\t\t)\n'
        '\t\t(property "Value" "MountingHole_3.2mm_M3" (at 0 4 0) (layer "F.Fab") hide\n'
        '\t\t\t(effects (font (size 1 1) (thickness 0.15)))\n'
        '\t\t)\n'
        '\t\t(attr exclude_from_pos_files exclude_from_bom)\n'
        f'\t\t(fp_circle (center 0 0) (end {keepout/2:.3f} 0)\n'
        f'\t\t\t(stroke (width 0.2) (type default)) (fill none) (layer "Dwgs.User") (uuid "{_det_uuid(ref+"/keepout")}")\n'
        '\t\t)\n'
        f'\t\t(pad "" np_thru_hole circle (at 0 0) (size {drill:.3f} {drill:.3f})\n'
        f'\t\t\t(drill {drill:.3f}) (layers "*.Cu" "*.Mask") (uuid "{_det_uuid(ref+"/pad")}")\n'
        '\t\t)\n'
        '\t)\n'
    )

def _outline_text() -> str:
    x0,y0=ORIGIN_X,ORIGIN_Y
    x1,y1=x0+220.0,y0+140.0
    pts=[(x0,y0,x1,y0),(x1,y0,x1,y1),(x1,y1,x0,y1),(x0,y1,x0,y0)]
    return "".join(
        f'\t(gr_line (start {xa:.3f} {ya:.3f}) (end {xb:.3f} {yb:.3f}) '
        f'(stroke (width 0.1) (type default)) (layer "Edge.Cuts") '
        f'(uuid "{_det_uuid("outline/"+str(i))}"))\n'
        for i,(xa,ya,xb,yb) in enumerate(pts,1)
    )

def apply() -> None:
    text=BOARD.read_text(encoding="utf-8")
    outline=frozen_audio_board_outline()
    placement=build_preliminary_placement_baseline(
        width_mm=outline.outline.width_mm,depth_mm=outline.outline.depth_mm)
    wanted={p.ref:p for p in placement.proposals}

    blocks=list(_top_blocks(text,"footprint"))
    refs={_reference(b):(s,e,b) for s,e,b in blocks if _reference(b)}
    missing=sorted(set(wanted)-set(refs))
    if missing:
        raise SystemExit(f"Native board missing {len(missing)} schematic footprints: {missing[:20]}")

    replacements=[]
    for ref,p in wanted.items():
        s,e,b=refs[ref]
        replacements.append((s,e,_replace_footprint_at(
            b,ORIGIN_X+p.x_mm,ORIGIN_Y+p.y_mm,p.rotation_deg)))
    for s,e,nb in sorted(replacements,reverse=True):
        text=text[:s]+nb+text[e:]

    if _det_uuid("outline/1") not in text:
        first=min(s for s,_,_ in _top_blocks(text,"footprint"))
        text=text[:first]+_outline_text()+text[first:]

    existing_refs={_reference(b) for _,_,b in _top_blocks(text,"footprint")}
    holes=""
    for h in outline.mounting_holes:
        if h.identifier not in existing_refs:
            holes+=_hole_block(
                h.identifier,ORIGIN_X+h.centre.x_mm,ORIGIN_Y+h.centre.y_mm,
                h.finished_diameter_mm,h.copper_keepout_diameter_mm)
    if holes:
        first=min(s for s,_,_ in _top_blocks(text,"footprint"))
        text=text[:first]+holes+text[first:]

    BOARD.write_text(text,encoding="utf-8")
    print(f"SR-043 applied {len(wanted)} native footprint placements.")
    print("Applied 220 x 140 mm Edge.Cuts and four frozen NPTH mounting holes.")

if __name__=="__main__":
    apply()
