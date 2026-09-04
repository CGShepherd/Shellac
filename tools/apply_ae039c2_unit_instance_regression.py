from pathlib import Path

REPO=Path(__file__).resolve().parents[1]
TEST=REPO/'tests/test_ae039c_real_kicad_opamp_units.py'

def main():
    text=TEST.read_text(encoding='utf-8')

    old='''    assert '(reference "U402")' not in text
    assert text.count('(reference "U401")')==4
    assert '(unit 1)' in text
    assert '(unit 2)' in text
'''
    new='''    assert '(reference "U402")' not in text
    assert text.count('(reference "U401")')==2

    # The two visible amplifier functions must be the A and B units of one
    # physical U401 package, not duplicate unit-1 instances.
    u401_blocks=[]
    cursor=0
    marker='(reference "U401")'
    while True:
        idx=text.find(marker,cursor)
        if idx<0:
            break
        block_start=text.rfind('(path "',0,idx)
        block_end=text.find(')',idx)
        u401_blocks.append(text[block_start:block_end+1])
        cursor=idx+len(marker)

    assert len(u401_blocks)==2
    assert any('(unit 1)' in block for block in u401_blocks)
    assert any('(unit 2)' in block for block in u401_blocks)
'''
    if old in text:
        text=text.replace(old,new,1)
    elif new not in text:
        raise SystemExit('Expected AE-039C SCH104 writer assertion not found.')

    TEST.write_text(text,encoding='utf-8')
    print('AE-039C2 APPLIED')
    print('Corrected SCH104 shared-reference expectation: 2 x U401 instances.')
    print('Regression now requires one unit 1 and one unit 2 instance.')

if __name__=='__main__':
    main()
