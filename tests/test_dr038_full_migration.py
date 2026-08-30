from generator.model.balanced_input import DIFF_CONVERTER_GAIN,LT5400_FOOTPRINT,validate_balanced_input
from generator.writers.kicad9 import PIN_COUNTS,embedded_custom_symbol_ids

def test_dr038_active_contract():
    validate_balanced_input()
    assert DIFF_CONVERTER_GAIN==4.0
    assert LT5400_FOOTPRINT.endswith("EP1.68x1.88mm")
    assert PIN_COUNTS["ProjectShellac:LT5400_Network"]==9
    assert "ProjectShellac:LT5400_Network" in embedded_custom_symbol_ids()
