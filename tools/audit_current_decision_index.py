"""Guard the authoritative decision index against implementation-status drift."""
from pathlib import Path
import re
import sys

INDEX = Path("config/decisions/current_decision_index.yaml")

BAD_IMPLEMENTED_PHRASES = (
    "remains the pre-DR038 implementation",
    "until atomic CAD migration",
    "pending implementation",
    "not yet substituted",
)


def audit(text: str):
    errors = []
    # Narrow guard for the currently implemented DR-038/039 production baseline.
    for decision in ("DR-038", "DR-039"):
        match = re.search(
            rf"(?ms)^  {re.escape(decision)}:\n(.*?)(?=^  DR-\d+:|^historical_implementation_events:|\Z)",
            text,
        )
        if not match:
            errors.append(f"{decision}: missing from authoritative index")
            continue
        block = match.group(1)
        if "status: CURRENT_IMPLEMENTED" not in block:
            errors.append(f"{decision}: expected CURRENT_IMPLEMENTED")
        lower = block.lower()
        for phrase in BAD_IMPLEMENTED_PHRASES:
            if phrase.lower() in lower:
                errors.append(
                    f"{decision}: CURRENT_IMPLEMENTED conflicts with phrase {phrase!r}"
                )
    return errors


def main():
    text = INDEX.read_text(encoding="utf-8")
    errors = audit(text)
    if errors:
        print("\n".join(f"ERROR: {e}" for e in errors))
        return 1
    print("Decision-index implementation-status audit passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
