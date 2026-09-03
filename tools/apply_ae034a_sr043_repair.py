from __future__ import annotations
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TARGET = REPO / "generator/layout/sr043_native_board_audit.py"

HEADER = '''\"\"\"SR-043 native-board audit.\"\"\"
from __future__ import annotations

from pathlib import Path
import sys

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import json
import re
from dataclasses import asdict, dataclass

'''

def main():
    text = TARGET.read_text(encoding="utf-8")
    marker = "from generator.layout.preliminary_placement import build_preliminary_placement_baseline"
    idx = text.find(marker)
    if idx < 0:
        raise SystemExit("Could not find SR-043 generator import marker; file layout differs from expected baseline.")

    body = text[idx:]
    body = body.replace("from __future__ import annotations\n", "")
    TARGET.write_text(HEADER + body, encoding="utf-8")

    print(f"Repaired {TARGET}")
    print("SR-043 now supports both direct-script and -m invocation.")

if __name__ == "__main__":
    main()
