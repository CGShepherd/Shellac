from pathlib import Path
import re

REPO=Path(__file__).resolve().parents[1]
TEST=REPO/"tests/test_ae039c_real_kicad_opamp_units.py"

def main():
    text=TEST.read_text(encoding="utf-8")

    pattern=re.compile(
        r'assert\s+text\.count\(\s*[\'"]\(reference\s+\\"U401\\"\)[\'"]\s*\)\s*==\s*4'
    )
    text,new_count=pattern.subn(
        'assert text.count(\'(reference "U401")\')==2',
        text,
        count=1,
    )

    # Accept already-corrected state as idempotent.
    if new_count == 0 and 'assert text.count(\'(reference "U401")\')==2' not in text:
        # Fallback for the exact quoting style generated in AE-039C.
        old='assert text.count(\'(reference "U401")\')==4'
        if old in text:
            text=text.replace(old,'assert text.count(\'(reference "U401")\')==2',1)
            new_count=1

    if new_count == 0 and 'assert text.count(\'(reference "U401")\')==2' not in text:
        raise SystemExit(
            "Could not find the U401 reference-count assertion. "
            "No file was changed."
        )

    # The existing AE-039C regression already checks both unit numbers.
    if "assert '(unit 1)' in text" not in text:
        raise SystemExit("Expected unit-1 assertion is missing.")
    if "assert '(unit 2)' in text" not in text:
        raise SystemExit("Expected unit-2 assertion is missing.")
    if 'assert \'(reference "U402")\' not in text' not in text:
        raise SystemExit("Expected U402-absence assertion is missing.")

    TEST.write_text(text,encoding="utf-8")

    final=TEST.read_text(encoding="utf-8")
    assert 'assert text.count(\'(reference "U401")\')==2' in final
    assert '==4' not in "\n".join(
        line for line in final.splitlines() if 'reference "U401"' in line
    )

    print("AE-039C2A APPLIED")
    print("U401 reference-count regression corrected: 4 -> 2.")
    print("Existing unit-1, unit-2 and U402-absence checks verified.")

if __name__=="__main__":
    main()
