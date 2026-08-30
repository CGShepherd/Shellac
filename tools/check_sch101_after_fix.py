from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))

from generator.blocks.balanced_input import add_sch101_diff_converter_slice
from generator.core.sheet import Sheet
from generator.electrical_audit import audit_sheet_electrical

sheet=Sheet("SCH101","SCH101.kicad_sch")
add_sch101_diff_converter_slice(sheet)
audit=audit_sheet_electrical(sheet)
print("SCH101 audit passed:",audit.passed)
print("off-grid:",audit.off_grid_items)
print("unterminated:",audit.unterminated_pins)
print("net conflicts:",audit.net_name_conflicts)
print("zero-length wires:",audit.zero_length_wires)
