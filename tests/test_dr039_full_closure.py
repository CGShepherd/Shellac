from pathlib import Path
from generator.model.post_eq_dc_block import cutoff_hz, magnitude_db

def test_dr039_source_and_response():
    text = Path("generator/blocks/replay_eq.py").read_text(encoding="utf-8")
    assert 'C{base}60' in text
    assert 'R{base}60' in text
    assert 'C_Rect_L7.2mm_W5.0mm_P5.00mm' in text
    assert 0.4 < cutoff_hz() < 0.6
    assert magnitude_db(20.0) > -0.01

def test_dr039_authoritative_status():
    text = Path("config/decisions/current_decision_index.yaml").read_text(encoding="utf-8")
    block = text.split("  DR-039:", 1)[1].split("  DR-040:", 1)[0]
    assert "status: CURRENT_IMPLEMENTED" in block
