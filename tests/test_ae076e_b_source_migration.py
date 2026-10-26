from pathlib import Path
import hashlib
import yaml

from generator.blocks.balanced_input import add_sch101_rf_slice
from generator.core.sheet import Sheet
from generator.layout.footprint_contract import build_footprint_contract
from generator.layout.placement_clusters import build_cluster_placement_baseline

ROOT=Path(__file__).resolve().parents[1]
BOARD=ROOT/"out/kicad/ProjectShellac.kicad_pcb"

def _sheet():
    s=Sheet(title="SCH101",filename="ProjectShellac_SCH101.kicad_sch")
    add_sch101_rf_slice(s)
    return s

def test_source_population_delta_is_exact():
    refs={c.ref for c in _sheet().components}
    assert {"H120","H220"} <= refs
    assert not {"H121","H122","C103","C104","C203","C204"} & refs
    population=set(build_footprint_contract().board_population_refs)
    assert len(population)==252
    assert {"H120","H220"} <= population
    assert not {"H121","H122","C103","C104","C203","C204"} & population

def test_personality_placement_is_per_channel_local():
    owners={}
    model=build_cluster_placement_baseline()
    for cluster in model.clusters:
        for ref in cluster.member_refs:
            owners.setdefault(ref,[]).append(cluster.identifier)
    assert owners["H120"]==["CLU-101-A"]
    assert owners["H220"]==["CLU-101-C"]
    assert "CLU-101-F" not in {c.identifier for c in model.clusters}

def test_source_phase_holds_native_and_release():
    cfg=yaml.safe_load(
        (ROOT/"config/decisions/ae076c_cartridge_personality.yaml").read_text(
            encoding="utf-8"
        )
    )
    q=cfg["qualification"]
    assert q["live_sch101_generator_migration"]=="IMPLEMENTED_AE076E_B_SOURCE"
    assert q["native_pcb_migration"]=="IMPLEMENTED_AE076E_B_NATIVE_F8_VALIDATED"
    assert not q["routing_authority"]
    assert not q["layout_freeze"]
    assert not q["bom_freeze"]
    assert not q["manufacturing_release"]

def _native_footprint(text, ref):
    blocks = text.replace("\r\n", "\n").split('\n\t(footprint "')
    matches = [block for block in blocks if f'(property "Reference" "{ref}"' in block]
    assert len(matches) == 1, (ref, len(matches))
    return matches[0]


def test_native_pcb_exact_ae076eb_migration_and_model_bindings():
    import re
    digest = hashlib.sha256(BOARD.read_bytes()).hexdigest()
    assert digest == "6824b2c311173046e0fd8ec782d8a61ba017ca2cc359cc7a17179252b28f81a2"
    text = BOARD.read_text(encoding="utf-8")
    assert text.count('(footprint "') == 256
    assert text.count('(segment ') == 0 and text.count('(via ') == 0
    for ref in ("H121", "H122", "C103", "C104", "C203", "C204"):
        assert f'(property "Reference" "{ref}"' not in text
    for ref, channel in (("H120", "L"), ("H220", "R")):
        block = _native_footprint(text, ref)
        assert block.startswith('ProjectShellac:Samtec_SLW-102-01-G-D_2x02_P2.54mm_Vertical"')
        assert '(model ' not in block
        pads = {int(pin): net for pin, net in re.findall(
            r'\(pad "([1-4])"[\s\S]*?\(net \d+ "([^"]+)"\)', block
        )}
        assert set(pads) == {1, 2, 3, 4}
        assert pads[1].endswith(f"SCH101_{channel}_LOAD_POS")
        assert pads[4].endswith(f"SCH101_{channel}_LOAD_POS")
        assert pads[2].endswith(f"SCH101_{channel}_LOAD_NEG")
        assert pads[3].endswith(f"SCH101_{channel}_LOAD_NEG")
    models = {
        "H901": "Molex_0039299063_5566-06A2.stp",
        "C30060": "C_Rect_L7.2mm_W5.0mm_P5.00mm.step",
        "C35060": "C_Rect_L7.2mm_W5.0mm_P5.00mm.step",
    }
    for ref, basename in models.items():
        assert f'${{KIPRJMOD}}/../../mechanical/mcad/models/{basename}' in _native_footprint(text, ref)
    for ref in ("D901", "D902", "C909"):
        assert '(attr smd dnp)' in _native_footprint(text, ref)
    for ref in ("MH1", "MH2", "MH3", "MH4"):
        _native_footprint(text, ref)


def test_ae076eb_controlled_model_assets_have_expected_hashes():
    model_dir = ROOT / "mechanical/mcad/models"
    expected = {
        "Molex_0039299063_5566-06A2.stp": "40cd349dcd35a3aa04844d09e13f92a40d90f1a664e1ad8baec2cd010259e87a",
        "C_Rect_L7.2mm_W5.0mm_P5.00mm.step": "35659ae3b9a50ddeb0aa5add4edfaea1770d99f3a8c2db7320eb8fb13be8ee1b",
    }
    for name, sha in expected.items():
        assert hashlib.sha256((model_dir / name).read_bytes()).hexdigest() == sha


def test_ae076eb_export_evidence_is_registered_without_releasing_routing():
    cfg = yaml.safe_load((ROOT / "config/decisions/ae076c_cartridge_personality.yaml").read_text(encoding="utf-8"))
    hold = yaml.safe_load((ROOT / "config/release/ae071_prerouting_hold.yaml").read_text(encoding="utf-8"))
    assert cfg["status"] == "CURRENT_SELECTED_SOURCE_AND_NATIVE_IMPLEMENTED_QUALIFICATION_OPEN"
    assert cfg["qualification"]["native_pcb_migration"] == "IMPLEMENTED_AE076E_B_NATIVE_F8_VALIDATED"
    assert hold["routing_blockers"][-1]["source_migration_status"] == "AE076E_B_H120_H220_SOURCE_AND_NATIVE_IMPLEMENTED"
    assert all(not hold["permissions"][k] for k in ("final_routing", "layout_freeze", "bom_freeze", "manufacturing_release"))
