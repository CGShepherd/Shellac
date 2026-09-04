
from pathlib import Path

REPO=Path(__file__).resolve().parents[1]
FPC=REPO/"generator/layout/footprint_contract.py"
CLUSTERS=REPO/"generator/layout/placement_clusters.py"
T_CLUSTER=REPO/"tests/test_cluster_placement_baseline.py"

def patch_footprint_contract():
    text=FPC.read_text(encoding="utf-8")
    imp="from generator.model.opamp_package_allocation import ALLOCATIONS\n"
    if imp not in text:
        anchor="from generator.model.shellac import build_shellac_model\n"
        if anchor not in text:
            raise SystemExit("footprint_contract import anchor not found")
        text=text.replace(anchor,anchor+imp,1)

    helper = '''
_OPAMP_ALLOCATION = {(a.sheet, a.logical_ref): a for a in ALLOCATIONS}

def _physical_component_identity(sheet_id: str, component):
    allocation=_OPAMP_ALLOCATION.get((sheet_id,component.ref))
    if allocation is None:
        return component.ref,component.value,component.footprint
    if allocation.logical_ref != allocation.physical_ref:
        return None
    return allocation.physical_ref,allocation.device,allocation.footprint

'''
    marker="# These connectors are electrically correct in the frozen schematic"
    if "_physical_component_identity(" not in text:
        if marker not in text:
            raise SystemExit("footprint_contract helper anchor not found")
        text=text.replace(marker,helper+marker,1)

    old = '''        for component in sheet.components:
            if component.ref in _MECHANICAL_ECO:
                status = PopulationStatus.MECHANICAL_ECO_REQUIRED
                rationale = _MECHANICAL_ECO[component.ref]
            elif not component.on_board:
                status = PopulationStatus.PANEL_EXCLUDED
                rationale = "Schematic explicitly declares panel/virtual ownership."
            else:
                status = PopulationStatus.APPROVED
                rationale = "PCB-owned component with an assigned schematic footprint."
            package = _package_family(component.footprint, component.lib_id)
            entries.append(FootprintEntry(
                ref=component.ref,
                sheet_id=block.identifier,
                value=component.value,
                lib_id=component.lib_id,
                footprint=component.footprint,
                schematic_on_board=component.on_board,
                population_status=status,
                package_family=package,
                placement_authority=_placement_authority(component.ref, package),
                rationale=rationale,
            ))
'''
    new = '''        for component in sheet.components:
            physical=_physical_component_identity(block.identifier,component)
            if physical is None:
                continue
            physical_ref,physical_value,physical_footprint=physical
            if component.ref in _MECHANICAL_ECO:
                status = PopulationStatus.MECHANICAL_ECO_REQUIRED
                rationale = _MECHANICAL_ECO[component.ref]
            elif not component.on_board:
                status = PopulationStatus.PANEL_EXCLUDED
                rationale = "Schematic explicitly declares panel/virtual ownership."
            else:
                status = PopulationStatus.APPROVED
                rationale = "PCB-owned physical package with an assigned footprint."
            package = _package_family(physical_footprint, component.lib_id)
            entries.append(FootprintEntry(
                ref=physical_ref,
                sheet_id=block.identifier,
                value=physical_value,
                lib_id=component.lib_id,
                footprint=physical_footprint,
                schematic_on_board=component.on_board,
                population_status=status,
                package_family=package,
                placement_authority=_placement_authority(physical_ref, package),
                rationale=rationale,
            ))
'''
    if new not in text:
        if old not in text:
            raise SystemExit("footprint_contract component loop differs from expected baseline")
        text=text.replace(old,new,1)
    FPC.write_text(text,encoding="utf-8")

def patch_clusters():
    text=CLUSTERS.read_text(encoding="utf-8")
    replacements={
        '"U101 U102 R111':'"U101 R111',
        '"U201 U202 R211':'"U201 R211',
        '"U101 U102 U103"':'"U101 U103"',
        '"U201 U202 U203"':'"U201 U203"',
        'C30026 U3002 R30040':'C30026 R30040',
        'C35026 U3502 R35040':'C35026 R35040',
        '"U3002"':'"U3001"',
        '"U3502"':'"U3501"',
        'R7001 R7002 U720 C7201':'R7001 R7002 C7201',
        'R7501 R7502 U770 C7701':'R7501 R7502 C7701',
        '"U700 U720"':'"U700"',
        '"U750 U770"':'"U750"',
        '"U401 U402 R4001':'"U401 R4001',
        '"U401 U402"':'"U401"',
        '"R501 R502 U501 U502 R510':'"R501 R502 U501 R510',
        '"U501 U502"':'"U501"',
    }
    for old,new in replacements.items():
        if old in text:
            text=text.replace(old,new,1)
        elif new not in text:
            raise SystemExit(f"placement cluster replacement not found: {old}")
    CLUSTERS.write_text(text,encoding="utf-8")

def patch_cluster_test():
    text=T_CLUSTER.read_text(encoding="utf-8")
    if "from generator.layout.footprint_contract import build_footprint_contract" not in text:
        text="from generator.layout.footprint_contract import build_footprint_contract\n"+text
    old = '''def _on_board_refs():
    registry = shellac_builder_registry()
    refs = set()
    for block_id in registry.registered_ids():
        registration = registry.resolve(block_id)
        sheet = Sheet(registration.title, f"{block_id}.kicad_sch")
        registration.builder(sheet)
        refs.update(component.ref for component in sheet.components if component.on_board)
    return refs
'''
    new = '''def _on_board_refs():
    return set(build_footprint_contract().board_population_refs)
'''
    if new not in text:
        if old not in text:
            raise SystemExit("cluster test helper differs from expected baseline")
        text=text.replace(old,new,1)
    T_CLUSTER.write_text(text,encoding="utf-8")

def main():
    patch_footprint_contract()
    patch_clusters()
    patch_cluster_test()
    print("AE-039B APPLIED")
    print("Expected physical board population: 246")

if __name__=="__main__":
    main()
