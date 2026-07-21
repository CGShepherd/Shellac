from pathlib import Path
import re


def parse_erc_summary(text: str) -> tuple[int, int]:
    match = re.search(r"ERC messages:\s+\d+\s+Errors\s+(\d+)\s+Warnings\s+(\d+)", text)
    if not match:
        raise ValueError("ERC summary not found")
    return int(match.group(1)), int(match.group(2))


def test_parser_recognises_nonzero_native_erc_baseline():
    sample = " ** ERC messages: 53  Errors 27  Warnings 26"
    assert parse_erc_summary(sample) == (27, 26)
