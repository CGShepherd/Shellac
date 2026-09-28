from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
DECISIONS = ROOT / "config/decisions/current_decision_index.yaml"
AUTHORITY = ROOT / "config/decisions/document_authority.yaml"
RECORD = ROOT / "docs/design_pack/AE-075D_B03_Control_Z_Stack_and_EQ_Mezzanine_Discriminator_Rev_A0.md"


def _record() -> str:
    return RECORD.read_text(encoding="utf-8")


def test_ae075d_record_preserves_nkk_stack_discriminator():
    text = _record()
    assert "switch/catalogue depth behind panel: **10.5 mm**" in text
    assert "panel to PCB: **12.3 mm**" in text
    assert "Panasonic `ECEA1VN100U` sense capacitor is 11.0 mm high" in text
    assert "**1.3 mm nominal cover clearance**" in text


def test_ae075d_record_preserves_unicase_carrier_discriminator():
    text = _record()
    assert "**1.6 mm PCB thickness**" in text
    assert "**2.0 mm aluminium carrier plate**" in text
    assert "carrier is therefore not qualified for use as a slide-in guide-rail PCB" in text


def test_ae075d_record_preserves_channel_local_architecture_decision():
    text = _record()
    assert "single remote top-cover control strip with long analogue runs is therefore rejected" in text
    assert "two channel-local EQ mezzanine PCBs" in text
    assert "REG-08 remains the AE-041 top-cover mechanical-registration authority" in text
    assert "it is not the physical identity of either PCB" in text


def test_ae075d_record_keeps_interconnect_and_physical_detail_open():
    text = _record()
    assert "interconnect topology is not frozen" in text
    assert "short rigid board-to-board" in text
    assert "short low-parasitic flex/harness" in text
    assert "long remote analogue runs are prohibited" in text
    assert "interconnect family/stack height, mechanical support" in text
    assert "No native PCB geometry" in text


def test_ae075d_historical_record_remains_cross_registered():
    decisions = yaml.safe_load(DECISIONS.read_text(encoding="utf-8"))
    authority = yaml.safe_load(AUTHORITY.read_text(encoding="utf-8"))
    rel = "docs/design_pack/AE-075D_B03_Control_Z_Stack_and_EQ_Mezzanine_Discriminator_Rev_A0.md"
    assert decisions["pre_spice_assurance"]["AE-075D"] == rel
    assert rel in authority["pre_spice_assurance_evidence"]
    assert RECORD.exists()
