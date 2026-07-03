import datetime
import json
import uuid

def u():
    return str(uuid.uuid4())

def eff(size=1.27):
    return f'(effects (font (size {size} {size})))'

def prop(name, value, x, y, size=1.27):
    value = str(value).replace('"', '\\"')
    return f'(property "{name}" "{value}" (at {x:.2f} {y:.2f} 0) {eff(size)})'

def text(t, x, y, size=1.5):
    t = t.replace('"', '\\"')
    return f'  (text "{t}" (at {x:.2f} {y:.2f} 0)\n    {eff(size)}\n  )\n'

def local_symbol_library():
    return f'''  (lib_symbols
    (symbol "ProjectShellac:R" (pin_numbers hide) (pin_names hide) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "R" (at 0 -2.54 0) {eff()})
      (property "Value" "R" (at 0 2.54 0) {eff()})
      (symbol "R_0_1"
        (rectangle (start -1.778 -0.762) (end 1.778 0.762) (stroke (width 0.1524) (type solid)) (fill (type none)))
        (pin passive line (at -3.81 0 0) (length 2.032) (name "1" {eff(1.0)}) (number "1" {eff(1.0)}))
        (pin passive line (at 3.81 0 180) (length 2.032) (name "2" {eff(1.0)}) (number "2" {eff(1.0)}))
      )
    )
    (symbol "ProjectShellac:C" (pin_numbers hide) (pin_names hide) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "C" (at 0 -2.54 0) {eff()})
      (property "Value" "C" (at 0 2.54 0) {eff()})
      (symbol "C_0_1"
        (polyline (pts (xy -0.762 1.27) (xy -0.762 -1.27)) (stroke (width 0.1524) (type solid)) (fill (type none)))
        (polyline (pts (xy 0.762 1.27) (xy 0.762 -1.27)) (stroke (width 0.1524) (type solid)) (fill (type none)))
        (pin passive line (at -3.81 0 0) (length 3.048) (name "1" {eff(1.0)}) (number "1" {eff(1.0)}))
        (pin passive line (at 3.81 0 180) (length 3.048) (name "2" {eff(1.0)}) (number "2" {eff(1.0)}))
      )
    )
    (symbol "ProjectShellac:TestPoint" (pin_names hide) (exclude_from_sim no) (in_bom no) (on_board yes)
      (property "Reference" "TP" (at 0 -2.54 0) {eff()})
      (property "Value" "TestPoint" (at 0 2.54 0) {eff()})
      (symbol "TestPoint_0_1"
        (circle (center 0 0) (radius 1.27) (stroke (width 0.1524) (type solid)) (fill (type none)))
        (pin passive line (at -3.81 0 0) (length 2.54) (name "1" {eff(1.0)}) (number "1" {eff(1.0)}))
      )
    )
  )
'''

def symbol_instance(c):
    x, y = c.at.x, c.at.y
    dnp = "yes" if c.dnp else "no"
    in_bom = "yes" if c.in_bom else "no"
    on_board = "yes" if c.on_board else "no"

    s = f'''  (symbol (lib_id "{c.lib_id}") (at {x:.2f} {y:.2f} 0) (unit 1)
    (exclude_from_sim no) (in_bom {in_bom}) (on_board {on_board}) (dnp {dnp})
    (uuid "{u()}")
    {prop("Reference", c.ref, x, y - 4)}
    {prop("Value", c.value, x, y + 4)}
'''
    if c.footprint:
        s += f'    {prop("Footprint", c.footprint, x, y + 6, 1.0)}\n'
    yy = y + 8
    for k, v in c.fields.items():
        s += f'    {prop(k, v, x, yy, 1.0)}\n'
        yy += 2
    pin_count = {"ProjectShellac:R": 2, "ProjectShellac:C": 2, "ProjectShellac:TestPoint": 1}.get(c.lib_id, 2)
    for pin in range(1, pin_count + 1):
        s += f'    (pin "{pin}" (uuid "{u()}"))\n'
    return s + "  )\n"

def write_schematic(sheet, out_path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    s = f'''(kicad_sch (version 20250114) (generator "project_shellac_generator") (generator_version "0.1.0")
  (uuid "{u()}")
  (paper "A3")
  (title_block
    (title "{sheet.title}")
    (date "{datetime.date.today().isoformat()}")
    (rev "0.1")
    (company "Project Shellac")
    (comment 1 "Generated output: edit generator source, not schematic output")
  )
'''
    s += local_symbol_library()
    y = 20
    for note in sheet.notes:
        s += text(note, 20, y)
        y += 7
    for c in sheet.components:
        s += symbol_instance(c)
    s += ")\n"
    out_path.write_text(s, encoding="utf-8")

def write_project(project_name, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    pro = {
        "meta": {"filename": f"{project_name}.kicad_pro", "version": 1},
        "schematic": {"meta": {"version": 1}},
        "sheets": [["00000000-0000-0000-0000-000000000000", ""]],
        "text_variables": {}
    }
    (out_dir / f"{project_name}.kicad_pro").write_text(json.dumps(pro, indent=2), encoding="utf-8")
