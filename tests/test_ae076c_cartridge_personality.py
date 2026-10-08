from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
CFG=ROOT/"config/decisions/ae076c_cartridge_personality.yaml"
def cfg(): return yaml.safe_load(CFG.read_text(encoding="utf-8"))
def test_selected_next_fail_safe():
    c=cfg(); a=c["architecture"]
    assert c["status"]=="CURRENT_SELECTED_SOURCE_AND_NATIVE_IMPLEMENTED_QUALIFICATION_OPEN"
    assert a["card_count_installed_when_nonbase"]==2 and a["cards_identical_per_channel"]
    assert not a["audio_path_passes_through_card"] and a["no_card_state"]=="BASE" and a["fail_safe_no_card"]
def test_rotation_benign_interface():
    i=cfg()["interface"]
    assert i["main_pcb_socket"]["mpn"]=="SLW-102-01-G-D"
    assert i["personality_card_header"]["mpn"]=="TSW-102-07-G-D"
    assert i["selected_refs"]=={"left":"H120","right":"H220"}
    m=i["diagonal_duplicate_node_map"]
    assert m[1]==m[4]=="POS" and m[2]==m[3]=="NEG"
def test_gain_separate_and_release_held():
    c=cfg(); g=c["gain_programming"]; q=c["qualification"]
    assert g["separate_from_personality_cards"] and g["header"]=="TSW-104-07-G-D" and g["shunt"]=="MNT-104-BK-G"
    assert q["live_sch101_generator_migration"]=="IMPLEMENTED_AE076E_B_SOURCE"
    assert q["native_pcb_migration"]=="IMPLEMENTED_AE076E_B_NATIVE_F8_VALIDATED"
    assert not q["routing_authority"] and not q["layout_freeze"] and not q["bom_freeze"] and not q["manufacturing_release"]
