from __future__ import annotations
from pathlib import Path
import re

REPO=Path(__file__).resolve().parents[1]
FILES=(
    REPO/'generator/blocks/final_gain.py',
    REPO/'generator/blocks/mode_matrix.py',
    REPO/'generator/blocks/rumble_filter.py',
)

PATTERN=re.compile(
    r'^[ \t]*sheet\.connect_pin_to_net\(\s*'
    r'(?:opamp|buf)\s*,\s*["\']0VA["\']\s*,\s*["\']0VA["\']'
    r'.*?\)\s*$',
    re.MULTILINE,
)

def clean_file(path: Path) -> int:
    text=path.read_text(encoding='utf-8')
    new,count=PATTERN.subn('',text)
    new=re.sub(r'\n{3,}','\n\n',new)
    path.write_text(new,encoding='utf-8')
    return count

def require_feedback(path: Path, component_name: str) -> None:
    text=path.read_text(encoding='utf-8')
    if f'pin_position({component_name}, "IN-")' not in text:
        raise SystemExit(
            f'{path}: expected AE-039C OUT-to-IN- feedback wiring is missing. '
            'Reapply AE-039C before C1.'
        )

def main() -> int:
    removed={}
    for path in FILES:
        removed[path.name]=clean_file(path)

    require_feedback(REPO/'generator/blocks/final_gain.py','opamp')
    require_feedback(REPO/'generator/blocks/mode_matrix.py','buf')
    require_feedback(REPO/'generator/blocks/rumble_filter.py','opamp')

    residual=[]
    for path in FILES:
        if PATTERN.search(path.read_text(encoding='utf-8')):
            residual.append(str(path))
    if residual:
        raise SystemExit('Residual synthetic op-amp 0VA calls remain: '+', '.join(residual))

    print('AE-039C1 APPLIED')
    for name,count in removed.items():
        print(f'  {name}: removed {count} residual synthetic 0VA call(s)')
    print('Explicit follower IN- feedback confirmed in SCH104/SCH105/SCH107.')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
