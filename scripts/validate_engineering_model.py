from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from generator.model.shellac import build_shellac_model
from generator.model.validation import validate_project


def main() -> int:
    project = build_shellac_model()
    issues = validate_project(project, raise_on_error=False)

    print(f"{project.name} — {project.revision}")
    print(f"Functional blocks: {len(list(project.all_blocks()))}")
    print(f"Signals: {len(project.signals)}")

    if issues:
        print(f"Validation FAILED: {len(issues)} issue(s)")
        for issue in issues:
            print(f"  {issue.code} {issue.location}: {issue.message}")
        return 1

    print("Validation PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
