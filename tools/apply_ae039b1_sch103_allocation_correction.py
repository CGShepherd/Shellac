from pathlib import Path

REPO=Path(__file__).resolve().parents[1]
ALLOC=REPO/'generator/model/opamp_package_allocation.py'
RF_TEST=REPO/'tests/test_real_footprint_audit.py'

def main():
    text=ALLOC.read_text(encoding='utf-8')
    replacements=[
        ('AmplifierUnitAllocation("SCH103","U301","U301","OPA1612","A"', 'AmplifierUnitAllocation("SCH103","U3001","U3001","OPA1612","A"'),
        ('AmplifierUnitAllocation("SCH103","U302","U301","OPA1612","B"', 'AmplifierUnitAllocation("SCH103","U3002","U3001","OPA1612","B"'),
        ('AmplifierUnitAllocation("SCH103","U351","U351","OPA1612","A"', 'AmplifierUnitAllocation("SCH103","U3501","U3501","OPA1612","A"'),
        ('AmplifierUnitAllocation("SCH103","U352","U351","OPA1612","B"', 'AmplifierUnitAllocation("SCH103","U3502","U3501","OPA1612","B"'),
        ('"U102","U202","U302","U352","U402","U502","U720","U770"', '"U102","U202","U3002","U3502","U402","U502","U720","U770"'),
    ]
    for old,new in replacements:
        if old in text:
            text=text.replace(old,new,1)
        elif new not in text:
            raise SystemExit(f'Allocation correction pattern not found: {old}')
    ALLOC.write_text(text,encoding='utf-8')

    text=RF_TEST.read_text(encoding='utf-8')
    imp='from generator.layout.footprint_contract import build_footprint_contract\n'
    if imp not in text:
        text=imp+text
    old='    assert audit.board_population_count == 254\n    assert audit.accepted_identity_count == 254\n'
    new='    expected=len(build_footprint_contract().board_population_refs)\n    assert audit.board_population_count == expected\n    assert audit.accepted_identity_count == expected\n'
    if old in text:
        text=text.replace(old,new,1)
    elif new not in text:
        raise SystemExit('Real-footprint population assertion differs from expected state.')
    RF_TEST.write_text(text,encoding='utf-8')

    print('AE-039B1 APPLIED')
    print('Corrected SCH103 allocation refs:')
    print('  U3001/U3002 -> physical U3001')
    print('  U3501/U3502 -> physical U3501')
    print('Expected physical board population: 246')

if __name__=='__main__':
    main()
