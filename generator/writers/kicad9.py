import json
import shutil
import time
from math import gcd
from pathlib import Path

from generator.core.geometry import Point
from generator.hierarchy import (
    GLOBAL_POWER_DOMAINS,
    HierarchicalPort,
    deterministic_uuid,
    pin_shape,
    root_instance_path,
    root_schematic_uuid,
    sheet_instance_path,
    sheet_instance_uuid,
)

PROPERTY_IDS = {
    "Reference": 0,
    "Value": 1,
    "Footprint": 2,
    "Datasheet": 3,
    "Description": 4,
}

PIN_COUNTS = {
    "Device:R": 2,
    "Device:C": 2,
    "Device:D": 2,
    "Device:Ferrite_Bead": 2,
    "Connector_Generic:Conn_01x03": 3,
    "Connector_Generic:Conn_01x05": 5,
    "Connector_Generic:Conn_01x06": 6,
    "ProjectShellac:OpAmp_NonInv_Block": 5,
    "ProjectShellac:DiffAmp_Block": 5,
    "ProjectShellac:LT5400_Network": 9,
    "ProjectShellac:TestPoint": 1,
    "ProjectShellac:Replay_EQ_Core_Block": 5,
    "ProjectShellac:Rotary_Switch_Block": 2,
    "ProjectShellac:OpAmp_Buffer_Block": 5,
    "ProjectShellac:Mode_Switch_Block": 7,
    "ProjectShellac:Switch_Bypass_Block": 6,
    "ProjectShellac:Balanced_Line_Driver_Block": 8,
    "ProjectShellac:Switch_Mute_Block": 6,
    "ProjectShellac:DIP_Switch_Block": 16,
    "ProjectShellac:Panel_Control_Block": 1,
    "ProjectShellac:Hierarchy_Port_Anchor": 1,
    "ProjectShellac:Power_Rail_Source": 1,
    "ProjectShellac:Panel_LED_Block": 2,
    "ProjectShellac:Bass_Select_Block": 6,
    "ProjectShellac:Treble_Select_Block": 5,
}

PROJECT_NAME = "ProjectShellac"
CONNECTION_GRID_MM = 1.27


def snap_coordinate(value, grid=CONNECTION_GRID_MM):
    """Snap an electrical coordinate to KiCad's 50 mil connection grid."""

    return round(float(value) / grid) * grid


_uuid_context = "unscoped"
_uuid_index = 0


def reset_uuid_stream(context):
    """Start a deterministic per-artifact UUID sequence."""
    global _uuid_context, _uuid_index
    _uuid_context = str(context)
    _uuid_index = 0


def u():
    global _uuid_index
    _uuid_index += 1
    return deterministic_uuid("generated-item", _uuid_context, _uuid_index)


def esc(value):
    return str(value).replace('"', '\\"')


def eff(size=1.27, hide=False, justify=None):
    hidden = " hide" if hide else ""
    justification = f' (justify {justify})' if justify else ""
    return f'(effects (font (size {size} {size})){justification}{hidden})'


def prop(name, value, x, y, size=1.0, hide=False):
    prop_id = PROPERTY_IDS.get(name)
    id_txt = f' (id {prop_id})' if prop_id is not None else ""
    return (
        f'(property "{esc(name)}" "{esc(value)}"{id_txt} '
        f'(at {x:.2f} {y:.2f} 0)\n'
        f'      {eff(size, hide)}\n'
        f'    )'
    )


def text(t, x, y, size=1.27):
    return (
        f'  (text "{esc(t)}" (at {x:.2f} {y:.2f} 0)\n'
        f'    {eff(size, justify="left")}\n'
        f'    (uuid "{u()}")\n'
        f'  )\n'
    )


def label(name, x, y, size=0.9, justify=None):
    x, y = snap_coordinate(x), snap_coordinate(y)
    return (
        f'  (label "{esc(name)}" (at {x:.2f} {y:.2f} 0)\n'
        f'    {eff(size, justify=justify)}\n'
        f'    (uuid "{u()}")\n'
        f'  )\n'
    )


def global_net_label(name, x, y, size=0.9, justify=None):
    x, y = snap_coordinate(x), snap_coordinate(y)
    return (
        f'  (global_label "{esc(name)}" (shape bidirectional) (at {x:.2f} {y:.2f} 0)\n'
        f'    {eff(size, justify=justify)}\n'
        f'    (uuid "{u()}")\n'
        f'    (property "Intersheetrefs" "${{INTERSHEET_REFS}}" '
        f'(at {x:.2f} {y + 1.27:.2f} 0) '
        f'(effects (font (size 1.27 1.27)) hide))\n'
        f'  )\n'
    )


def wire_line(w):
    x1, y1 = snap_coordinate(w.x1), snap_coordinate(w.y1)
    x2, y2 = snap_coordinate(w.x2), snap_coordinate(w.y2)
    return (
        f'  (wire (pts (xy {x1:.2f} {y1:.2f}) '
        f'(xy {x2:.2f} {y2:.2f}))\n'
        f'    (stroke (width 0.1524) (type solid))\n'
        f'    (uuid "{u()}")\n'
        f'  )\n'
    )


def _grid_point(x, y):
    """Represent a rendered electrical point as integer 50-mil grid units."""
    return (
        round(float(x) / CONNECTION_GRID_MM),
        round(float(y) / CONNECTION_GRID_MM),
    )


def _direction(start, end):
    dx, dy = end[0] - start[0], end[1] - start[1]
    divisor = gcd(abs(dx), abs(dy))
    if divisor == 0:
        return None
    return (dx // divisor, dy // divisor)


def junction_points(wires):
    """Find intentional branch nodes without joining simple wire crossings.

    A connection is intentional only when generated wire endpoints meet.  It
    becomes a visible junction when three or more conductor directions meet at
    that endpoint.  Consequently, ordinary bends and two-wire joins receive no
    dot, while a wire that merely crosses or terminates on the middle of an
    unrelated wire cannot be silently converted into an electrical connection.
    """
    segments = []
    candidates = set()
    for wire in wires:
        start = _grid_point(wire.x1, wire.y1)
        end = _grid_point(wire.x2, wire.y2)
        if start == end:
            continue
        segments.append((start, end))
        candidates.update((start, end))

    junctions = []
    for point in candidates:
        directions = set()
        for start, end in segments:
            if point == start:
                direction = _direction(point, end)
                if direction:
                    directions.add(direction)
            elif point == end:
                direction = _direction(point, start)
                if direction:
                    directions.add(direction)
        if len(directions) >= 3:
            junctions.append(Point(
                point[0] * CONNECTION_GRID_MM,
                point[1] * CONNECTION_GRID_MM,
            ))

    return tuple(sorted(junctions, key=lambda item: (item.y, item.x)))


def junction(point, identity):
    x = snap_coordinate(point.x)
    y = snap_coordinate(point.y)
    return (
        f'  (junction (at {x:.2f} {y:.2f}) (diameter 0) '
        f'(color 0 0 0 0)\n'
        f'    (uuid "{deterministic_uuid("junction", identity, x, y)}")\n'
        f'  )\n'
    )


def embedded_custom_symbol_ids():
    """Return the deterministic set of custom symbols embedded by the writer."""
    return frozenset({
        "ProjectShellac:OpAmp_NonInv_Block",
        "ProjectShellac:Replay_EQ_Core_Block",
        "ProjectShellac:Rotary_Switch_Block",
        "ProjectShellac:DiffAmp_Block",
        "ProjectShellac:LT5400_Network",
        "ProjectShellac:OpAmp_Buffer_Block",
        "ProjectShellac:TestPoint",
        "ProjectShellac:Mode_Switch_Block",
        "ProjectShellac:Switch_Bypass_Block",
        "ProjectShellac:Balanced_Line_Driver_Block",
        "ProjectShellac:Switch_Mute_Block",
        "ProjectShellac:DIP_Switch_Block",
        "ProjectShellac:Panel_Control_Block",
        "ProjectShellac:Hierarchy_Port_Anchor",
        "ProjectShellac:Power_Rail_Source",
        "ProjectShellac:Panel_LED_Block",
        "ProjectShellac:Bass_Select_Block",
        "ProjectShellac:Treble_Select_Block",
    })


def embedded_standard_symbol_ids():
    return frozenset({
        "Device:R",
        "Device:C",
        "Device:D",
        "Device:Ferrite_Bead",
        "Connector_Generic:Conn_01x03",
        "Connector_Generic:Conn_01x05",
        "Connector_Generic:Conn_01x06",
    })


def embedded_symbol_ids():
    return embedded_custom_symbol_ids() | embedded_standard_symbol_ids()


def _symbol_blocks(library_name):
    """Extract top-level embedded symbols for one project-local library."""
    lines = local_symbol_library().splitlines()
    blocks = []
    current = []
    depth = 0
    for line in lines:
        prefix = f'    (symbol "{library_name}:'
        if not current and line.startswith(prefix):
            current = [line.replace(f'"{library_name}:', '"', 1)]
            depth = line.count("(") - line.count(")")
            continue
        if current:
            current.append(line)
            depth += line.count("(") - line.count(")")
            if depth == 0:
                blocks.append("\n".join(current))
                current = []
    return tuple(blocks)


def write_project_library_tables(out_dir):
    """Write self-contained project tables independent of a user's KiCad profile."""
    out_dir.mkdir(parents=True, exist_ok=True)
    for library_name in ("Device", "Connector_Generic", "ProjectShellac"):
        symbols = "\n".join(_symbol_blocks(library_name))
        (out_dir / f"{library_name}.kicad_sym").write_text(
            '(kicad_symbol_lib (version 20231120) (generator "project_shellac_generator")\n'
            f'{symbols}\n)\n',
            encoding="utf-8",
        )
    (out_dir / "sym-lib-table").write_text(
        '(sym_lib_table\n'
        '  (version 7)\n'
        '  (lib (name "Device")(type "KiCad")(uri "${KIPRJMOD}/Device.kicad_sym")(options "")(descr "Generated passive symbols"))\n'
        '  (lib (name "Connector_Generic")(type "KiCad")(uri "${KIPRJMOD}/Connector_Generic.kicad_sym")(options "")(descr "Generated connector symbols"))\n'
        '  (lib (name "ProjectShellac")(type "KiCad")(uri "${KIPRJMOD}/ProjectShellac.kicad_sym")(options "")(descr "Project Shellac generated symbols"))\n'
        ')\n',
        encoding="utf-8",
    )
    footprint_libraries = (
        "Button_Switch_THT", "Capacitor_SMD", "Connector_Audio", "Diode_SMD",
        "Inductor_SMD", "Package_SO", "Resistor_SMD", "TestPoint",
    )
    rows = "\n".join(
        f'  (lib (name "{name}")(type "KiCad")(uri "${{KICAD9_FOOTPRINT_DIR}}/{name}.pretty")(options "")(descr ""))'
        for name in footprint_libraries
    )
    (out_dir / "fp-lib-table").write_text(
        f'(fp_lib_table\n  (version 7)\n{rows}\n)\n',
        encoding="utf-8",
    )


def local_symbol_library():
    return f'''  (lib_symbols
    (symbol "Device:R" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "R" (id 0) (at 0 -2.54 0) {eff()})
      (property "Value" "R" (id 1) (at 0 2.54 0) {eff()})
      (symbol "R_0_1"
        (rectangle (start -1.27 -2.03) (end 1.27 2.03) (stroke (width 0.254) (type solid)) (fill (type none)))
        (pin passive line (at -2.54 0 0) (length 1.27) (name "1" {eff(1.0)}) (number "1" {eff(1.0)}))
        (pin passive line (at 2.54 0 180) (length 1.27) (name "2" {eff(1.0)}) (number "2" {eff(1.0)}))
      )
    )
    (symbol "Device:C" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "C" (id 0) (at 2.54 0 90) {eff()})
      (property "Value" "C" (id 1) (at -2.54 0 90) {eff()})
      (symbol "C_0_1"
        (polyline (pts (xy -1.78 -0.51) (xy 1.78 -0.51)) (stroke (width 0.254) (type solid)) (fill (type none)))
        (polyline (pts (xy -1.78 0.51) (xy 1.78 0.51)) (stroke (width 0.254) (type solid)) (fill (type none)))
        (pin passive line (at 0 -2.54 90) (length 2.03) (name "1" {eff(1.0)}) (number "1" {eff(1.0)}))
        (pin passive line (at 0 2.54 270) (length 2.03) (name "2" {eff(1.0)}) (number "2" {eff(1.0)}))
      )
    )
    (symbol "Device:D" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "D" (id 0) (at 0 -2.54 0) {eff()})
      (property "Value" "D" (id 1) (at 0 2.54 0) {eff()})
      (symbol "D_0_1"
        (rectangle (start -1.27 -1.27) (end 1.27 1.27) (stroke (width 0.254) (type solid)) (fill (type none)))
        (pin passive line (at -2.54 0 0) (length 1.27) (name "K" {eff(1.0)}) (number "1" {eff(1.0)}))
        (pin passive line (at 2.54 0 180) (length 1.27) (name "A" {eff(1.0)}) (number "2" {eff(1.0)}))
      )
    )
    (symbol "Device:Ferrite_Bead" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "FB" (id 0) (at 0 -2.54 0) {eff()})
      (property "Value" "Ferrite_Bead" (id 1) (at 0 2.54 0) {eff()})
      (symbol "Ferrite_Bead_0_1"
        (rectangle (start -1.27 -1.27) (end 1.27 1.27) (stroke (width 0.254) (type solid)) (fill (type none)))
        (pin passive line (at -2.54 0 0) (length 1.27) (name "1" {eff(1.0)}) (number "1" {eff(1.0)}))
        (pin passive line (at 2.54 0 180) (length 1.27) (name "2" {eff(1.0)}) (number "2" {eff(1.0)}))
      )
    )
    (symbol "Connector_Generic:Conn_01x03" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "J" (id 0) (at 2.54 -5.08 0) {eff()})
      (property "Value" "Conn_01x03" (id 1) (at 2.54 5.08 0) {eff()})
      (symbol "Conn_01x03_0_1"
        (rectangle (start -2.54 -3.81) (end 2.54 3.81) (stroke (width 0.254) (type solid)) (fill (type none)))
        (pin passive line (at -5.08 -2.54 0) (length 2.54) (name "1" {eff(1.0)}) (number "1" {eff(1.0)}))
        (pin passive line (at -5.08 0 0) (length 2.54) (name "2" {eff(1.0)}) (number "2" {eff(1.0)}))
        (pin passive line (at -5.08 2.54 0) (length 2.54) (name "3" {eff(1.0)}) (number "3" {eff(1.0)}))
      )
    )
    (symbol "Connector_Generic:Conn_01x05" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "J" (id 0) (at 2.54 -7.62 0) {eff()})
      (property "Value" "Conn_01x05" (id 1) (at 2.54 7.62 0) {eff()})
      (symbol "Conn_01x05_0_1"
        (rectangle (start -2.54 -6.35) (end 2.54 6.35) (stroke (width 0.254) (type solid)) (fill (type none)))
        (pin passive line (at -5.08 -5.08 0) (length 2.54) (name "1" {eff(1.0)}) (number "1" {eff(1.0)}))
        (pin passive line (at -5.08 -2.54 0) (length 2.54) (name "2" {eff(1.0)}) (number "2" {eff(1.0)}))
        (pin passive line (at -5.08 0 0) (length 2.54) (name "3" {eff(1.0)}) (number "3" {eff(1.0)}))
        (pin passive line (at -5.08 2.54 0) (length 2.54) (name "4" {eff(1.0)}) (number "4" {eff(1.0)}))
        (pin passive line (at -5.08 5.08 0) (length 2.54) (name "5" {eff(1.0)}) (number "5" {eff(1.0)}))
      )
    )
    (symbol "Connector_Generic:Conn_01x06" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "J" (id 0) (at 2.54 -8.89 0) {eff()})
      (property "Value" "Conn_01x06" (id 1) (at 2.54 8.89 0) {eff()})
      (symbol "Conn_01x06_0_1"
        (rectangle (start -2.54 -7.62) (end 2.54 7.62) (stroke (width 0.254) (type solid)) (fill (type none)))
        (pin passive line (at -5.08 -6.35 0) (length 2.54) (name "1" {eff(1.0)}) (number "1" {eff(1.0)}))
        (pin passive line (at -5.08 -3.81 0) (length 2.54) (name "2" {eff(1.0)}) (number "2" {eff(1.0)}))
        (pin passive line (at -5.08 -1.27 0) (length 2.54) (name "3" {eff(1.0)}) (number "3" {eff(1.0)}))
        (pin passive line (at -5.08 1.27 0) (length 2.54) (name "4" {eff(1.0)}) (number "4" {eff(1.0)}))
        (pin passive line (at -5.08 3.81 0) (length 2.54) (name "5" {eff(1.0)}) (number "5" {eff(1.0)}))
        (pin passive line (at -5.08 6.35 0) (length 2.54) (name "6" {eff(1.0)}) (number "6" {eff(1.0)}))
      )
    )
    (symbol "ProjectShellac:OpAmp_NonInv_Block" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "U" (id 0) (at 0 -9.0 0) {eff()})
      (property "Value" "OPA1656_GAIN" (id 1) (at 0 9.0 0) {eff()})
      (symbol "OpAmp_NonInv_Block_0_1"
        (rectangle (start -7.62 -6.35) (end 7.62 6.35) (stroke (width 0.1524) (type solid)) (fill (type none)))
        (pin input line (at -11.43 0 0) (length 3.81) (name "IN+" {eff(1.0)}) (number "1" {eff(1.0)}))
        (pin input line (at -2.54 -10.16 90) (length 3.81) (name "FB-" {eff(1.0)}) (number "2" {eff(1.0)}))
        (pin output line (at 11.43 0 180) (length 3.81) (name "OUT" {eff(1.0)}) (number "3" {eff(1.0)}))
        (pin power_in line (at 2.54 10.16 270) (length 3.81) (name "+V" {eff(1.0)}) (number "4" {eff(1.0)}))
        (pin power_in line (at 2.54 -10.16 90) (length 3.81) (name "-V" {eff(1.0)}) (number "5" {eff(1.0)}))
      )
    )
    (symbol "ProjectShellac:Replay_EQ_Core_Block" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "U" (id 0) (at 0 -9.0 0) {eff()})
      (property "Value" "P06_LM4562_EQ" (id 1) (at 0 9.0 0) {eff()})
      (symbol "Replay_EQ_Core_Block_0_1"
        (rectangle (start -10.16 -7.62) (end 10.16 7.62) (stroke (width 0.1524) (type solid)) (fill (type none)))
        (pin input line (at -15.24 0 0) (length 5.08) (name "IN" {eff(1.0)}) (number "1" {eff(1.0)}))
        (pin output line (at 15.24 0 180) (length 5.08) (name "OUT" {eff(1.0)}) (number "2" {eff(1.0)}))
        (pin power_in line (at 2.54 -12.70 90) (length 5.08) (name "+V" {eff(1.0)}) (number "3" {eff(1.0)}))
        (pin power_in line (at 2.54 12.70 270) (length 5.08) (name "-V" {eff(1.0)}) (number "4" {eff(1.0)}))
        (pin power_in line (at -2.54 12.70 270) (length 5.08) (name "0VA" {eff(1.0)}) (number "5" {eff(1.0)}))
      )
    )
    (symbol "ProjectShellac:Rotary_Switch_Block" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom no) (on_board no)
      (property "Reference" "SW" (id 0) (at 0 -7.0 0) {eff()})
      (property "Value" "ROTARY_SELECT" (id 1) (at 0 7.0 0) {eff()})
      (symbol "Rotary_Switch_Block_0_1"
        (rectangle (start -7.62 -5.08) (end 7.62 5.08) (stroke (width 0.1524) (type solid)) (fill (type none)))
        (pin passive line (at -12.70 0 0) (length 5.08) (name "COMMON" {eff(1.0)}) (number "1" {eff(1.0)}))
        (pin passive line (at 12.70 0 180) (length 5.08) (name "SELECTED" {eff(1.0)}) (number "2" {eff(1.0)}))
      )
    )
    (symbol "ProjectShellac:DiffAmp_Block" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "U" (id 0) (at 0 -9.0 0) {eff()})
      (property "Value" "OPA1656_DIFF" (id 1) (at 0 9.0 0) {eff()})
      (symbol "DiffAmp_Block_0_1"
        (rectangle (start -7.62 -6.35) (end 7.62 6.35) (stroke (width 0.1524) (type solid)) (fill (type none)))
        (pin input line (at -11.43 2.54 0) (length 3.81) (name "IN+" {eff(1.0)}) (number "1" {eff(1.0)}))
        (pin input line (at -11.43 -2.54 0) (length 3.81) (name "IN-" {eff(1.0)}) (number "2" {eff(1.0)}))
        (pin output line (at 11.43 0 180) (length 3.81) (name "OUT" {eff(1.0)}) (number "3" {eff(1.0)}))
        (pin power_in line (at 2.54 10.16 270) (length 3.81) (name "+V" {eff(1.0)}) (number "4" {eff(1.0)}))
        (pin power_in line (at 2.54 -10.16 90) (length 3.81) (name "-V" {eff(1.0)}) (number "5" {eff(1.0)}))
      )
    )
    (symbol "ProjectShellac:OpAmp_Buffer_Block" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "U" (id 0) (at 0 -9.0 0) {eff()})
      (property "Value" "OPA1656_BUFFER" (id 1) (at 0 9.0 0) {eff()})
      (symbol "OpAmp_Buffer_Block_0_1"
        (rectangle (start -7.62 -6.35) (end 7.62 6.35) (stroke (width 0.1524) (type solid)) (fill (type none)))
        (pin input line (at -11.43 0 0) (length 3.81) (name "IN" {eff(1.0)}) (number "1" {eff(1.0)}))
        (pin output line (at 11.43 0 180) (length 3.81) (name "OUT" {eff(1.0)}) (number "2" {eff(1.0)}))
        (pin power_in line (at 2.54 -10.16 90) (length 3.81) (name "+V" {eff(1.0)}) (number "3" {eff(1.0)}))
        (pin power_in line (at 2.54 10.16 270) (length 3.81) (name "-V" {eff(1.0)}) (number "4" {eff(1.0)}))
        (pin passive line (at -2.54 10.16 270) (length 3.81) (name "0VA" {eff(1.0)}) (number "5" {eff(1.0)}))
      )
    )
    (symbol "ProjectShellac:TestPoint" (pin_names (offset 0.8)) (exclude_from_sim yes) (in_bom no) (on_board yes)
      (property "Reference" "TP" (id 0) (at 0 -4.0 0) {eff()})
      (property "Value" "TESTPOINT" (id 1) (at 0 4.0 0) {eff()})
      (symbol "TestPoint_0_1"
        (circle (center 0 0) (radius 1.27) (stroke (width 0.254) (type solid)) (fill (type none)))
        (pin passive line (at 0 -5.08 90) (length 3.81) (name "TP" {eff(1.0)}) (number "1" {eff(1.0)}))
      )
    )
    (symbol "ProjectShellac:Mode_Switch_Block" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom no) (on_board no)
      (property "Reference" "SW" (id 0) (at 0 -17.0 0) {eff()})
      (property "Value" "MODE_4P4T" (id 1) (at 0 17.0 0) {eff()})
      (symbol "Mode_Switch_Block_0_1"
        (rectangle (start -10.16 -10.16) (end 10.16 10.16) (stroke (width 0.1524) (type solid)) (fill (type none)))
        (pin passive line (at -15.24 -7.62 0) (length 5.08) (name "L_IN" {eff(1.0)}) (number "1" {eff(1.0)}))
        (pin passive line (at -15.24 7.62 0) (length 5.08) (name "R_IN" {eff(1.0)}) (number "2" {eff(1.0)}))
        (pin passive line (at -5.08 -12.70 90) (length 2.54) (name "SUM_L" {eff(1.0)}) (number "3" {eff(1.0)}))
        (pin passive line (at 5.08 -12.70 90) (length 2.54) (name "SUM_R" {eff(1.0)}) (number "4" {eff(1.0)}))
        (pin passive line (at 0 12.70 270) (length 2.54) (name "MONO" {eff(1.0)}) (number "5" {eff(1.0)}))
        (pin passive line (at 15.24 -5.08 180) (length 5.08) (name "L_OUT" {eff(1.0)}) (number "6" {eff(1.0)}))
        (pin passive line (at 15.24 5.08 180) (length 5.08) (name "R_OUT" {eff(1.0)}) (number "7" {eff(1.0)}))
      )
    )
    (symbol "ProjectShellac:Switch_Bypass_Block" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom no) (on_board no)
      (property "Reference" "SW" (id 0) (at 0 -17.0 0) {eff()})
      (property "Value" "RUMBLE_BYPASS_2P2T" (id 1) (at 0 17.0 0) {eff()})
      (symbol "Switch_Bypass_Block_0_1"
        (rectangle (start -10.16 -10.16) (end 10.16 10.16) (stroke (width 0.1524) (type solid)) (fill (type none)))
        (pin passive line (at -15.24 -7.62 0) (length 5.08) (name "L_DIRECT" {eff(1.0)}) (number "1" {eff(1.0)}))
        (pin passive line (at -15.24 -2.54 0) (length 5.08) (name "L_FILTER" {eff(1.0)}) (number "2" {eff(1.0)}))
        (pin passive line (at -15.24 2.54 0) (length 5.08) (name "R_DIRECT" {eff(1.0)}) (number "3" {eff(1.0)}))
        (pin passive line (at -15.24 7.62 0) (length 5.08) (name "R_FILTER" {eff(1.0)}) (number "4" {eff(1.0)}))
        (pin passive line (at 15.24 -3.81 180) (length 5.08) (name "L_OUT" {eff(1.0)}) (number "5" {eff(1.0)}))
        (pin passive line (at 15.24 3.81 180) (length 5.08) (name "R_OUT" {eff(1.0)}) (number "6" {eff(1.0)}))
      )
    )
    (symbol "ProjectShellac:Balanced_Line_Driver_Block" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "U" (id 0) (at 0 -17.0 0) {eff()})
      (property "Value" "THAT1646" (id 1) (at 0 17.0 0) {eff()})
      (symbol "Balanced_Line_Driver_Block_0_1"
        (rectangle (start -10.16 -10.16) (end 10.16 10.16) (stroke (width 0.1524) (type solid)) (fill (type none)))
        (pin output line (at 15.24 5.08 180) (length 5.08) (name "OUT-" {eff(1.0)}) (number "1" {eff(1.0)}))
        (pin input line (at 0 12.70 270) (length 2.54) (name "SNS-" {eff(1.0)}) (number "2" {eff(1.0)}))
        (pin passive line (at -5.08 12.70 270) (length 2.54) (name "GND" {eff(1.0)}) (number "3" {eff(1.0)}))
        (pin input line (at -15.24 0 0) (length 5.08) (name "IN" {eff(1.0)}) (number "4" {eff(1.0)}))
        (pin power_in line (at -5.08 -12.70 90) (length 2.54) (name "-V" {eff(1.0)}) (number "5" {eff(1.0)}))
        (pin power_in line (at 5.08 -12.70 90) (length 2.54) (name "+V" {eff(1.0)}) (number "6" {eff(1.0)}))
        (pin input line (at 5.08 12.70 270) (length 2.54) (name "SNS+" {eff(1.0)}) (number "7" {eff(1.0)}))
        (pin output line (at 15.24 -5.08 180) (length 5.08) (name "OUT+" {eff(1.0)}) (number "8" {eff(1.0)}))
      )
    )
    (symbol "ProjectShellac:Switch_Mute_Block" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom no) (on_board no)
      (property "Reference" "SW" (id 0) (at 0 -17.0 0) {eff()})
      (property "Value" "OUTPUT_MUTE_2P2T" (id 1) (at 0 17.0 0) {eff()})
      (symbol "Switch_Mute_Block_0_1"
        (rectangle (start -10.16 -10.16) (end 10.16 10.16) (stroke (width 0.1524) (type solid)) (fill (type none)))
        (pin passive line (at -15.24 -7.62 0) (length 5.08) (name "L_SIGNAL" {eff(1.0)}) (number "1" {eff(1.0)}))
        (pin passive line (at -15.24 -2.54 0) (length 5.08) (name "L_MUTE" {eff(1.0)}) (number "2" {eff(1.0)}))
        (pin passive line (at -15.24 2.54 0) (length 5.08) (name "R_SIGNAL" {eff(1.0)}) (number "3" {eff(1.0)}))
        (pin passive line (at -15.24 7.62 0) (length 5.08) (name "R_MUTE" {eff(1.0)}) (number "4" {eff(1.0)}))
        (pin passive line (at 15.24 -3.81 180) (length 5.08) (name "L_OUT" {eff(1.0)}) (number "5" {eff(1.0)}))
        (pin passive line (at 15.24 3.81 180) (length 5.08) (name "R_OUT" {eff(1.0)}) (number "6" {eff(1.0)}))
      )
    )
    (symbol "ProjectShellac:LT5400_Network" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "RN" (id 0) (at 0 -10 0) {eff()})
      (property "Value" "LT5400-7" (id 1) (at 0 10 0) {eff()})
      (symbol "LT5400_Network_0_1"
        (rectangle (start -5.08 -6.35) (end 5.08 6.35) (stroke (width 0.1524) (type solid)) (fill (type none)))
        (pin passive line (at -12.70 -7.62 0) (length 2.54) (name "1" {eff(1.0)}) (number "1" {eff(1.0)}))
        (pin passive line (at -12.70 -2.54 0) (length 2.54) (name "2" {eff(1.0)}) (number "2" {eff(1.0)}))
        (pin passive line (at -12.70 2.54 0) (length 2.54) (name "3" {eff(1.0)}) (number "3" {eff(1.0)}))
        (pin passive line (at -12.70 7.62 0) (length 2.54) (name "4" {eff(1.0)}) (number "4" {eff(1.0)}))
        (pin passive line (at 12.70 7.62 180) (length 2.54) (name "5" {eff(1.0)}) (number "5" {eff(1.0)}))
        (pin passive line (at 12.70 2.54 180) (length 2.54) (name "6" {eff(1.0)}) (number "6" {eff(1.0)}))
        (pin passive line (at 12.70 -2.54 180) (length 2.54) (name "7" {eff(1.0)}) (number "7" {eff(1.0)}))
        (pin passive line (at 12.70 -7.62 180) (length 2.54) (name "8" {eff(1.0)}) (number "8" {eff(1.0)}))
        (pin passive line (at 0 12.70 270) (length 1.27) (name "EP" {eff(1.0)}) (number "9" {eff(1.0)}))
      )
    )
    (symbol "ProjectShellac:DIP_Switch_Block" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "SW" (id 0) (at 0 -16.0 0) {eff()})
      (property "Value" "DIP_SPSTx08" (id 1) (at 0 16.0 0) {eff()})
      (symbol "DIP_Switch_Block_0_1"
        (rectangle (start -12.70 -12.70) (end 12.70 12.70) (stroke (width 0.1524) (type solid)) (fill (type none)))
        (pin passive line (at -17.78 -8.89 0) (length 5.08) (name "1A" {eff(1.0)}) (number "1" {eff(1.0)}))
        (pin passive line (at 17.78 -8.89 180) (length 5.08) (name "1B" {eff(1.0)}) (number "16" {eff(1.0)}))
        (pin passive line (at -17.78 -6.35 0) (length 5.08) (name "2A" {eff(1.0)}) (number "2" {eff(1.0)}))
        (pin passive line (at 17.78 -6.35 180) (length 5.08) (name "2B" {eff(1.0)}) (number "15" {eff(1.0)}))
        (pin passive line (at -17.78 -3.81 0) (length 5.08) (name "3A" {eff(1.0)}) (number "3" {eff(1.0)}))
        (pin passive line (at 17.78 -3.81 180) (length 5.08) (name "3B" {eff(1.0)}) (number "14" {eff(1.0)}))
        (pin passive line (at -17.78 -1.27 0) (length 5.08) (name "4A" {eff(1.0)}) (number "4" {eff(1.0)}))
        (pin passive line (at 17.78 -1.27 180) (length 5.08) (name "4B" {eff(1.0)}) (number "13" {eff(1.0)}))
        (pin passive line (at -17.78 1.27 0) (length 5.08) (name "5A" {eff(1.0)}) (number "5" {eff(1.0)}))
        (pin passive line (at 17.78 1.27 180) (length 5.08) (name "5B" {eff(1.0)}) (number "12" {eff(1.0)}))
        (pin passive line (at -17.78 3.81 0) (length 5.08) (name "6A" {eff(1.0)}) (number "6" {eff(1.0)}))
        (pin passive line (at 17.78 3.81 180) (length 5.08) (name "6B" {eff(1.0)}) (number "11" {eff(1.0)}))
        (pin passive line (at -17.78 6.35 0) (length 5.08) (name "7A" {eff(1.0)}) (number "7" {eff(1.0)}))
        (pin passive line (at 17.78 6.35 180) (length 5.08) (name "7B" {eff(1.0)}) (number "10" {eff(1.0)}))
        (pin passive line (at -17.78 8.89 0) (length 5.08) (name "8A" {eff(1.0)}) (number "8" {eff(1.0)}))
        (pin passive line (at 17.78 8.89 180) (length 5.08) (name "8B" {eff(1.0)}) (number "9" {eff(1.0)}))
      )
    )
    (symbol "ProjectShellac:Panel_Control_Block" (pin_names (offset 0.8)) (exclude_from_sim yes) (in_bom no) (on_board no)
      (property "Reference" "SW" (id 0) (at 0 -8.0 0) {eff()})
      (property "Value" "PANEL_CONTROL" (id 1) (at 0 8.0 0) {eff()})
      (symbol "Panel_Control_Block_0_1"
        (rectangle (start -10.16 -5.08) (end 10.16 5.08) (stroke (width 0.1524) (type solid)) (fill (type none)))
        (pin passive line (at 0 10.16 270) (length 5.08) (name "CONTROL" {eff(1.0)}) (number "1" {eff(1.0)}))
      )
    )
    (symbol "ProjectShellac:Hierarchy_Port_Anchor" (pin_names (offset 0.8)) (exclude_from_sim yes) (in_bom no) (on_board no)
      (property "Reference" "H" (id 0) (at 0 -3.0 0) {eff(hide=True)})
      (property "Value" "HIERARCHY_ANCHOR" (id 1) (at 0 3.0 0) {eff(hide=True)})
      (symbol "Hierarchy_Port_Anchor_0_1"
        (circle (center 0 0) (radius 1.27) (stroke (width 0.1524) (type solid)) (fill (type none)))
        (pin passive line (at -5.08 0 0) (length 3.81) (name "PORT" {eff(1.0)}) (number "1" {eff(1.0)}))
      )
    )
    (symbol "ProjectShellac:Power_Rail_Source" (pin_names (offset 0.8)) (exclude_from_sim yes) (in_bom no) (on_board no)
      (property "Reference" "PWR" (id 0) (at 0 -3.0 0) {eff()})
      (property "Value" "POWER_RAIL_SOURCE" (id 1) (at 0 3.0 0) {eff()})
      (symbol "Power_Rail_Source_0_1"
        (circle (center 0 0) (radius 1.27) (stroke (width 0.1524) (type solid)) (fill (type none)))
        (pin power_out line (at -5.08 0 0) (length 3.81) (name "POWER_OUT" {eff(1.0)}) (number "1" {eff(1.0)}))
      )
    )
    (symbol "ProjectShellac:Panel_LED_Block" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom yes) (on_board no)
      (property "Reference" "LED" (id 0) (at -5.0 0 90) {eff()})
      (property "Value" "PANEL_LED" (id 1) (at 5.0 0 90) {eff()})
      (symbol "Panel_LED_Block_0_1"
        (rectangle (start -3.81 -3.81) (end 3.81 3.81) (stroke (width 0.1524) (type solid)) (fill (type none)))
        (pin passive line (at 0 -8.89 90) (length 5.08) (name "A" {eff(1.0)}) (number "1" {eff(1.0)}))
        (pin passive line (at 0 8.89 270) (length 5.08) (name "K" {eff(1.0)}) (number "2" {eff(1.0)}))
      )
    )
    (symbol "ProjectShellac:Bass_Select_Block" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom no) (on_board no)
      (property "Reference" "SW" (id 0) (at 0 -15.0 0) {eff()})
      (property "Value" "BASS_1P5" (id 1) (at 0 15.0 0) {eff()})
      (symbol "Bass_Select_Block_0_1"
        (rectangle (start -10.16 -12.70) (end 10.16 12.70) (stroke (width 0.1524) (type solid)) (fill (type none)))
        (pin passive line (at 15.24 0 180) (length 5.08) (name "COMMON" {eff(1.0)}) (number "1" {eff(1.0)}))
        (pin passive line (at -15.24 -10.16 0) (length 5.08) (name "OUT" {eff(1.0)}) (number "2" {eff(1.0)}))
        (pin passive line (at -15.24 -5.08 0) (length 5.08) (name "B200" {eff(1.0)}) (number "3" {eff(1.0)}))
        (pin passive line (at -15.24 0 0) (length 5.08) (name "B400" {eff(1.0)}) (number "4" {eff(1.0)}))
        (pin passive line (at -15.24 5.08 0) (length 5.08) (name "B500" {eff(1.0)}) (number "5" {eff(1.0)}))
        (pin passive line (at -15.24 10.16 0) (length 5.08) (name "RIAA" {eff(1.0)}) (number "6" {eff(1.0)}))
      )
    )
    (symbol "ProjectShellac:Treble_Select_Block" (pin_names (offset 0.8)) (exclude_from_sim no) (in_bom no) (on_board no)
      (property "Reference" "SW" (id 0) (at 0 -12.0 0) {eff()})
      (property "Value" "TREBLE_1P5" (id 1) (at 0 12.0 0) {eff()})
      (symbol "Treble_Select_Block_0_1"
        (rectangle (start -10.16 -10.16) (end 10.16 10.16) (stroke (width 0.1524) (type solid)) (fill (type none)))
        (pin passive line (at -15.24 0 0) (length 5.08) (name "COMMON" {eff(1.0)}) (number "1" {eff(1.0)}))
        (pin passive line (at 15.24 -7.62 180) (length 5.08) (name "T1600" {eff(1.0)}) (number "2" {eff(1.0)}))
        (pin passive line (at 15.24 -2.54 180) (length 5.08) (name "T2121" {eff(1.0)}) (number "3" {eff(1.0)}))
        (pin passive line (at 15.24 2.54 180) (length 5.08) (name "T3400" {eff(1.0)}) (number "4" {eff(1.0)}))
        (pin passive line (at 15.24 7.62 180) (length 5.08) (name "T5800" {eff(1.0)}) (number "5" {eff(1.0)}))
      )
    )
  )
'''


def symbol_instances(ref, instance_path, unit=1, standalone_path=None):
    paths = [instance_path]
    if standalone_path and standalone_path != instance_path:
        paths.append(standalone_path)
    body = (
        '    (instances\n'
        f'      (project "{PROJECT_NAME}"\n'
    )
    for path in paths:
        body += (
        f'        (path "{path}"\n'
        f'          (reference "{esc(ref)}")\n'
        f'          (unit {unit})\n'
        '        )\n'
        )
    return body + (
        '      )\n'
        '    )\n'
    )


def symbol_instance(c, instance_path, standalone_path=None):
    x = snap_coordinate(c.at.x)
    y = snap_coordinate(c.at.y)
    s = (
        f'  (symbol (lib_id "{c.lib_id}") '
        f'(at {x:.2f} {y:.2f} {c.rotation:.0f}) (unit 1)\n'
        f'    (exclude_from_sim no) '
        f'(in_bom {"yes" if c.in_bom else "no"}) '
        f'(on_board {"yes" if c.on_board else "no"}) '
        f'(dnp {"yes" if c.dnp else "no"})\n'
        f'    (uuid "{u()}")\n'
        f'    {prop("Reference", c.ref, x, y - 3.8)}\n'
        f'    {prop("Value", c.value, x, y + 3.8)}\n'
    )

    if c.footprint:
        s += f'    {prop("Footprint", c.footprint, x, y + 6.0, 1.0, hide=True)}\n'

    yy = y + 8.0
    for key, value in c.fields.items():
        s += f'    {prop(key, value, x, yy, 1.0, hide=True)}\n'
        yy += 2.0

    for pin in range(1, PIN_COUNTS.get(c.lib_id, 2) + 1):
        s += f'    (pin "{pin}" (uuid "{u()}"))\n'

    s += symbol_instances(
        c.ref, instance_path, unit=1, standalone_path=standalone_path
    )
    return s + '  )\n'


def hierarchical_label(port: HierarchicalPort, identity: str, justify=None):
    x = snap_coordinate(port.x)
    y = snap_coordinate(port.y)
    return (
        f'  (hierarchical_label "{esc(port.name)}" (shape {port.shape}) '
        f'(at {x:.2f} {y:.2f} 0)\n'
        f'    {eff(0.9, hide=not port.visible, justify=justify)}\n'
        f'    (uuid "{deterministic_uuid("hierarchical-label", identity, port.name)}")\n'
        f'  )\n'
    )


def outward_label_justify(x, y, wires):
    """Keep net-label text outside the wire stub instead of over symbols."""
    x, y = snap_coordinate(x), snap_coordinate(y)
    for wire in wires:
        a = (snap_coordinate(wire.x1), snap_coordinate(wire.y1))
        b = (snap_coordinate(wire.x2), snap_coordinate(wire.y2))
        if (x, y) == a:
            other = b
        elif (x, y) == b:
            other = a
        else:
            continue
        if other[0] > x:
            return "right"
        if other[0] < x:
            return "left"
        return "right"
    return None


def clean_output(
    out_dir,
    *,
    attempts=6,
    initial_delay_s=0.20,
    preserve_patterns=("*.kicad_pcb", "*.kicad_dru"),
):
    """Remove generator-owned output while preserving native PCB authority."""
    out_dir = Path(out_dir)
    if not out_dir.exists():
        return

    preserved = {}
    for pattern in preserve_patterns:
        for path in out_dir.glob(pattern):
            if path.is_file():
                preserved[path.name] = path.read_bytes()

    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            shutil.rmtree(out_dir)
            if preserved:
                out_dir.mkdir(parents=True, exist_ok=True)
                for name, payload in preserved.items():
                    (out_dir / name).write_bytes(payload)
            return
        except PermissionError as error:
            last_error = error
            if attempt == attempts:
                break
            time.sleep(initial_delay_s * attempt)

    raise PermissionError(
        f"Could not clean generated output {out_dir!s} after {attempts} attempts. "
        "Close KiCad or Explorer windows using the folder, allow Dropbox to finish "
        "syncing, then rerun the build."
    ) from last_error


def write_schematic(
    sheet,
    out_path,
    *,
    hierarchical_ports=(),
    instance_path=None,
):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    reset_uuid_stream(sheet.filename)
    schematic_uuid = deterministic_uuid("schematic-file", sheet.filename)
    if instance_path is None:
        instance_path = f"/{schematic_uuid}"

    s = (
        f'(kicad_sch (version 20250114) '
        f'(generator "project_shellac_generator") '
        f'(generator_version "0.6.1")\n'
        f'  (uuid "{schematic_uuid}")\n'
        f'  (paper "A3")\n'
        f'  (title_block\n'
        f'    (title "{esc(sheet.title)}")\n'
        f'    (date "2026-07-15")\n'
        f'    (rev "0.6.1")\n'
        f'    (company "Project Shellac")\n'
        f'    (comment 1 "Generated output: edit generator source, not schematic output")\n'
        f'  )\n'
    )

    s += local_symbol_library()

    y = 20
    for note in sheet.notes:
        s += text(note, 20, y)
        y += 7

    for wire in sheet.wires:
        s += wire_line(wire)

    for point in junction_points(sheet.wires):
        s += junction(point, sheet.filename)

    for index, point in enumerate(sheet.no_connects):
        x, y = snap_coordinate(point.x), snap_coordinate(point.y)
        s += (
            f'  (no_connect (at {x:.2f} {y:.2f})\n'
            f'    (uuid "{deterministic_uuid("no-connect", sheet.filename, index, x, y)}")\n'
            f'  )\n'
        )

    standalone_path = f"/{schematic_uuid}"
    for component in sheet.components:
        s += symbol_instance(
            component, instance_path, standalone_path=standalone_path
        )

    # A hierarchical label is itself the authoritative local net label.  Do
    # not emit a second ordinary label at the identical endpoint: KiCad treats
    # the coincident pair as two dangling labels even though the wire is real.
    hierarchy_endpoints = {
        (port.name, snap_coordinate(port.x), snap_coordinate(port.y))
        for port in hierarchical_ports
    }
    hierarchy_names = {port.name for port in hierarchical_ports}
    wire_endpoints = {
        (snap_coordinate(wire.x1), snap_coordinate(wire.y1))
        for wire in sheet.wires
    } | {
        (snap_coordinate(wire.x2), snap_coordinate(wire.y2))
        for wire in sheet.wires
    }
    for lab in sheet.labels:
        endpoint = (lab.name, snap_coordinate(lab.x), snap_coordinate(lab.y))
        position = endpoint[1:]
        if lab.name in hierarchy_names and position not in wire_endpoints:
            continue
        if endpoint not in hierarchy_endpoints:
            render_label = (
                global_net_label if lab.name in GLOBAL_POWER_DOMAINS else label
            )
            s += render_label(
                lab.name, lab.x, lab.y,
                justify=outward_label_justify(lab.x, lab.y, sheet.wires),
            )

    for port in hierarchical_ports:
        s += hierarchical_label(
            port,
            sheet.filename,
            justify=outward_label_justify(port.x, port.y, sheet.wires),
        )

    s += ')\n'
    out_path.write_text(s, encoding='utf-8')


def _sheet_property(name, value, x, y, prop_id, justify):
    return (
        f'    (property "{name}" "{esc(value)}" (id {prop_id}) '
        f'(at {x:.2f} {y:.2f} 0)\n'
        f'      (effects (font (size 1.27 1.27)) (justify {justify}))\n'
        f'    )\n'
    )


def _root_sheet(block, filename, project_name, x, y, width, height, page):
    sheet_uuid = sheet_instance_uuid(project_name, block.identifier)
    root_interfaces = [
        item for item in block.interfaces
        if item.signal not in GLOBAL_POWER_DOMAINS
    ]
    inputs = [item for item in root_interfaces if item.direction.value != "output"]
    outputs = [item for item in root_interfaces if item.direction.value == "output"]
    body = (
        f'  (sheet (at {x:.2f} {y:.2f}) (size {width:.2f} {height:.2f})\n'
        f'    (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)\n'
        f'    (stroke (width 0.1524) (type solid))\n'
        f'    (fill (color 0 0 0 0.0000))\n'
        f'    (uuid "{sheet_uuid}")\n'
    )
    body += _sheet_property("Sheetname", f"{block.identifier} {block.name}", x, y - 0.762, 0, "left bottom")
    body += _sheet_property("Sheetfile", filename, x, y + height + 0.762, 1, "left top")

    pin_positions = []
    for index, interface in enumerate(inputs):
        py = y + 7.62 + index * 5.08
        body += (
            f'    (pin "{esc(interface.signal)}" {pin_shape(interface.direction)} '
            f'(at {x:.2f} {py:.2f} 180)\n'
            f'      (effects (font (size 1.27 1.27)) (justify left))\n'
            f'      (uuid "{deterministic_uuid("root-sheet-pin", project_name, block.identifier, interface.signal)}")\n'
            f'    )\n'
        )
        pin_positions.append((interface.signal, x, py, -10.16))
    for index, interface in enumerate(outputs):
        py = y + 7.62 + index * 5.08
        px = x + width
        body += (
            f'    (pin "{esc(interface.signal)}" {pin_shape(interface.direction)} '
            f'(at {px:.2f} {py:.2f} 0)\n'
            f'      (effects (font (size 1.27 1.27)) (justify right))\n'
            f'      (uuid "{deterministic_uuid("root-sheet-pin", project_name, block.identifier, interface.signal)}")\n'
            f'    )\n'
        )
        pin_positions.append((interface.signal, px, py, 10.16))
    body += (
        f'    (instances\n'
        f'      (project "{esc(project_name)}"\n'
        f'        (path "{root_instance_path(project_name)}"\n'
        f'          (page "{page}")\n'
        f'        )\n'
        f'      )\n'
        f'    )\n'
        f'  )\n'
    )
    return body, pin_positions


def write_root_schematic(project, block_files, out_path, project_name):
    """Write the deterministic root sheet linking every functional block."""

    out_path.parent.mkdir(parents=True, exist_ok=True)
    root_uuid = root_schematic_uuid(project_name)
    content = (
        f'(kicad_sch (version 20250114) '
        f'(generator "project_shellac_generator") '
        f'(generator_version "0.9.0")\n'
        f'  (uuid "{root_uuid}")\n'
        f'  (paper "A3")\n'
        f'  (title_block\n'
        f'    (title "{esc(project.name)} - Root Hierarchy")\n'
        f'    (date "2026-07-15")\n'
        f'    (rev "SR-009 Rev A")\n'
        f'    (company "Project Shellac")\n'
        f'    (comment 1 "Generated from the Engineering Model")\n'
        f'  )\n'
        f'  (lib_symbols)\n'
    )

    # Keep every root endpoint on KiCad's 2.54 mm schematic grid.
    positions = [
        (20.32, 25.40), (116.84, 25.40), (213.36, 25.40), (309.88, 25.40),
        (20.32, 154.94), (116.84, 154.94), (213.36, 154.94), (309.88, 154.94),
    ]
    root_connections = []
    for page, (block, position) in enumerate(zip(project.blocks, positions), start=2):
        filename = block_files[block.identifier]
        sheet_text, pin_positions = _root_sheet(
            block, filename, project_name, position[0], position[1], 71.12, 81.28, page
        )
        content += sheet_text
        root_connections.extend((block.identifier, *item) for item in pin_positions)

    # Join repeated hierarchy signals with global labels on short isolated
    # stubs.  Local labels are intended to name one physical conductor and
    # KiCad warns when the same local label resolves onto several disjoint
    # wires.  Direct inter-sheet wires were also rejected because long
    # diagonal segments could cross unrelated terminal stubs.  Global labels
    # are the native KiCad construct for joining separated root conductors.
    by_signal = {}
    for block_id, signal, x, y, dx in root_connections:
        by_signal.setdefault(signal, []).append((block_id, x, y, dx))

    for signal in sorted(by_signal):
        endpoints = sorted(
            by_signal[signal],
            key=lambda item: (item[2], item[1], item[0]),
        )
        repeated = len(endpoints) > 1
        for block_id, x, y, dx in endpoints:
            stub_x = x + dx
            justify = "right" if dx < 0 else "left"
            content += (
                f'  (wire (pts (xy {x:.2f} {y:.2f}) '
                f'(xy {stub_x:.2f} {y:.2f}))\n'
                f'    (stroke (width 0) (type default))\n'
                f'    (uuid "{deterministic_uuid("root-wire", project_name, block_id, signal)}")\n'
                f'  )\n'
            )
            if repeated:
                # Root-only global net names deliberately differ from the
                # engineering signal names used by child-sheet local labels.
                # This preserves hierarchical-pin connectivity while avoiding
                # KiCad's same_local_global_label warning.
                root_net_name = f"ROOT__{signal}"
                content += (
                    f'  (global_label "{esc(root_net_name)}" (shape bidirectional) '
                    f'(at {stub_x:.2f} {y:.2f} 0)\n'
                    f'    (effects (font (size 0.9 0.9)) '
                    f'(justify {justify}) hide)\n'
                    f'    (uuid "{deterministic_uuid("root-global-label", project_name, block_id, signal)}")\n'
                    f'    (property "Intersheetrefs" "${{INTERSHEET_REFS}}" '
                    f'(at {stub_x:.2f} {y + 1.27:.2f} 0) '
                    f'(effects (font (size 1.27 1.27)) hide))\n'
                    f'  )\n'
                )
            else:
                content += (
                    f'  (label "{esc(signal)}" (at {stub_x:.2f} {y:.2f} 0)\n'
                    f'    {eff(0.9, hide=True, justify=justify)}\n'
                    f'    (uuid "{deterministic_uuid("root-label", project_name, block_id, signal)}")\n'
                    f'  )\n'
                )

    content += '  (sheet_instances\n'
    content += '    (path "/" (page "1"))\n'
    content += '  )\n)\n'
    out_path.write_text(content, encoding="utf-8")
    return root_uuid


def write_project(project_name, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    write_project_library_tables(out_dir)
    pro = {
        "board": {},
        "boards": [],
        "cvpcb": {},
        "erc": {},
        "legacy": {},
        "libraries": {},
        "meta": {"filename": f"{project_name}.kicad_pro", "version": 1},
        "net_settings": {},
        "pcbnew": {},
        "schematic": {"meta": {"version": 1}},
        "sheets": [["00000000-0000-0000-0000-000000000000", ""]],
        "text_variables": {},
    }
    (out_dir / f"{project_name}.kicad_pro").write_text(
        json.dumps(pro, indent=2),
        encoding="utf-8",
    )
