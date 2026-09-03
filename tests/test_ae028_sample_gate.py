from pathlib import Path

def test_ae028_does_not_modify_production_bom():
    text = Path("docs/design_pack/AE-028_PT_Mechanical_Sample_Validation_Gate_Rev_A0.md").read_text(encoding="utf-8")
    assert "mechanical proxies only" in text.lower()
    assert "do not" in text.lower()

def test_ae028_requires_two_wafer_validation():
    text = Path("docs/design_pack/AE-028_PT_Mechanical_Sample_Validation_Gate_Rev_A0.md").read_text(encoding="utf-8")
    assert "Two-wafer simulation" in text
