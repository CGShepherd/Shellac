from generator.core.sheet import Sheet
from generator.dispatch import shellac_builder_registry
from generator.model.opamp_package_allocation import ALLOCATIONS, absorbed_logical_refs

OPAMP_LIBS={
    'ProjectShellac:OpAmp_NonInv_Block',
    'ProjectShellac:OpAmp_Buffer_Block',
    'ProjectShellac:DiffAmp_Block',
}
AUDITED_SHEETS={'SCH101','SCH103','SCH104','SCH105','SCH107'}

def _generated_opamp_refs():
    registry=shellac_builder_registry()
    found=set()
    for sheet_id in AUDITED_SHEETS:
        registration=registry.resolve(sheet_id)
        assert registration is not None
        sheet=Sheet(registration.title,f'{sheet_id}.kicad_sch')
        registration.builder(sheet)
        for c in sheet.components:
            if c.lib_id in OPAMP_LIBS:
                found.add((sheet_id,c.ref))
    return found

def test_allocation_authority_matches_real_generated_opamp_refs_exactly():
    allocated={(a.sheet,a.logical_ref) for a in ALLOCATIONS}
    assert allocated==_generated_opamp_refs()

def test_sch103_uses_actual_four_digit_generated_references():
    sch103={a.logical_ref for a in ALLOCATIONS if a.sheet=='SCH103'}
    assert sch103=={'U3001','U3002','U3501','U3502'}

def test_absorbed_refs_are_actual_generated_b_units():
    assert set(absorbed_logical_refs())=={
        'U102','U202','U3002','U3502','U402','U502','U720','U770'
    }
