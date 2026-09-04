from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FILES=(
    ROOT/'generator/blocks/final_gain.py',
    ROOT/'generator/blocks/mode_matrix.py',
    ROOT/'generator/blocks/rumble_filter.py',
)

def test_no_synthetic_opamp_0va_builder_connections_remain():
    offenders=[]
    for path in FILES:
        text=path.read_text(encoding='utf-8')
        for line in text.splitlines():
            compact=line.replace(' ','').replace('\t','')
            if (
                'connect_pin_to_net(' in compact
                and ',"0VA","0VA"' in compact
                and ('opamp,' in compact or 'buf,' in compact)
            ):
                offenders.append((path.name,line.strip()))
    assert offenders==[]

def test_all_buffer_builders_explicitly_reference_inverting_input():
    expectations={
        'final_gain.py':'pin_position(opamp, "IN-")',
        'mode_matrix.py':'pin_position(buf, "IN-")',
        'rumble_filter.py':'pin_position(opamp, "IN-")',
    }
    for path in FILES:
        text=path.read_text(encoding='utf-8')
        assert expectations[path.name] in text

def test_real_buffer_pin_contract_has_no_0va():
    from generator.core.pins import SYMBOL_PIN_CONTRACTS
    pins=SYMBOL_PIN_CONTRACTS['ProjectShellac:OpAmp_Buffer_Block']
    assert '0VA' not in pins
    assert 'IN-' in pins
