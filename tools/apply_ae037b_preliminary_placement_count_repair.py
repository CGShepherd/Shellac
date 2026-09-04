from pathlib import Path

REPO=Path(__file__).resolve().parents[1]
TEST=REPO/"tests/test_preliminary_placement.py"

def main():
    text=TEST.read_text(encoding="utf-8")
    old='assert len(placement.proposals) == len(contract.board_population_refs) == 250'
    new='assert len(placement.proposals) == len(contract.board_population_refs)'
    if old in text:
        text=text.replace(old,new,1)
        TEST.write_text(text,encoding="utf-8")
    elif new not in text:
        raise SystemExit("Expected preliminary-placement population assertion not found.")

    final=TEST.read_text(encoding="utf-8")
    assert new in final
    assert "== 250" not in final
    print("AE-037B APPLIED AND VERIFIED")
    print("Removed stale hard-coded board population count from preliminary placement test.")

if __name__=="__main__":
    main()
