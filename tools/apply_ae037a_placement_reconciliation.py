from pathlib import Path

REPO=Path(__file__).resolve().parents[1]
PLACEMENT=REPO/"generator/layout/placement_clusters.py"
FPA_TEST=REPO/"tests/test_real_footprint_audit.py"

REPLACEMENTS=(
    (
        '"H101 R102 R103 C101 C102 C103"',
        '"H101 R102 R103 R104 R105 C101 C102 C103"',
    ),
    (
        '"H201 R202 R203 C201 C202 C203"',
        '"H201 R202 R203 R204 R205 C201 C202 C203"',
    ),
)

def replace_once(text, old, new, path):
    if new in text:
        return text
    count=text.count(old)
    if count != 1:
        raise SystemExit(f"Expected exactly one occurrence of {old!r} in {path}; found {count}.")
    return text.replace(old,new,1)

def main():
    text=PLACEMENT.read_text(encoding="utf-8")
    for old,new in REPLACEMENTS:
        text=replace_once(text,old,new,PLACEMENT)
    PLACEMENT.write_text(text,encoding="utf-8")

    tests=FPA_TEST.read_text(encoding="utf-8")
    if "assert audit.board_population_count == 254" not in tests:
        tests=replace_once(
            tests,
            "assert audit.board_population_count == 250",
            "assert audit.board_population_count == 254",
            FPA_TEST,
        )
        tests=replace_once(
            tests,
            "assert audit.accepted_identity_count == 250",
            "assert audit.accepted_identity_count == 254",
            FPA_TEST,
        )
    FPA_TEST.write_text(tests,encoding="utf-8")

    final=PLACEMENT.read_text(encoding="utf-8")
    assert '"H101 R102 R103 R104 R105 C101 C102 C103"' in final
    assert '"H201 R202 R203 R204 R205 C201 C202 C203"' in final
    print("AE-037A APPLIED AND VERIFIED")
    print("R104/R105 -> CLU-101-A")
    print("R204/R205 -> CLU-101-C")
    print("Expected board population -> 254")

if __name__=="__main__":
    main()
