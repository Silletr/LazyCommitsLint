import subprocess
from collections import defaultdict
from typing import Dict, List

CATEGORY_MAP = {
    "A": "NEW",
    "D": "DELETED",
    "M": "CHANGED",
    "R": "RENAMED",
    "C": "RENAMED",
}


CATEGORY_MAP = {
    "A": "NEW",
    "D": "DELETED",
    "M": "CHANGED",
    "R": "RENAMED",
    "C": "RENAMED",
}


def analyze_all_changes() -> Dict[str, List[str]]:
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain", "-z"],
            text=True,
            capture_output=True,
            check=True,
        )
    except Exception:
        return {}

    if not result.stdout.strip():
        return {}

    changes = defaultdict(list)
    parts = result.stdout.rstrip("\x00").split("\x00")  # Remove trailing nulls
    i = 0
    while i < len(parts) - 1:
        status_line = parts[i]
        if len(status_line) < 2:
            i += 1
            continue

        status = status_line[:2]  # "MM", "M ", "A ", "??"
        # Everything after first 2 chars
        path = status_line[2:].lstrip()  # strip leading space after status

        if path:
            if status[0] == "?" and status[1] == "?":
                cat = "UNTRACKED"
            elif status[0] == " ":  # Unstaged tracked " M", "MM"
                cat = "UNSTAGED"
            elif status[0] in CATEGORY_MAP:
                cat = CATEGORY_MAP[status[0]]
            else:
                cat = "UNKNOWN"
            changes[cat].append(path)

        i += 1  # Single entries per null

    print(f"ALL CHANGES LIST:\n{dict(changes)}\n")
    return dict(changes)


if __name__ == "__main__":
    analyze_all_changes()
