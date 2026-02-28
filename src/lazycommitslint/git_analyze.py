import subprocess
from collections import defaultdict
from typing import Dict, List

STAGED_MAP = {
    "A": "NEW",
    "D": "DELETED",
    "M": "CHANGED",
    "R": "RENAMED",
    "C": "COPIED",
}

UNSTAGED_MAP = {
    "M": "MODIFIED",
    "D": "DELETED",
}


def run_git(*args) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            text=True,
            capture_output=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return ""


def analyze_all_changes() -> Dict[str, Dict[str, List[str]]]:
    """
    Returns:
    {
        "staged":   {"NEW": [...], "CHANGED": [...], ...},
        "unstaged": {"MODIFIED": [...], "DELETED": [...]},
        "untracked": {"UNTRACKED": [...]},
    }
    """
    raw = run_git("status", "--porcelain", "-z")
    if not raw.strip():
        return {"staged": {}, "unstaged": {}, "untracked": {}}

    staged: Dict[str, List[str]] = defaultdict(list)
    unstaged: Dict[str, List[str]] = defaultdict(list)
    untracked: List[str] = []

    parts = raw.rstrip("\x00").split("\x00")
    i = 0
    while i < len(parts):
        entry = parts[i]
        if len(entry) < 3:
            i += 1
            continue

        x = entry[0]  # staged status
        y = entry[1]  # unstaged status
        path = entry[3:]  # skip "XY "

        # handle renames — next null-delimited entry is the old path, skip it
        if x in ("R", "C"):
            i += 2  # current + old path
        else:
            i += 1

        if x == "?" and y == "?":
            untracked.append(path)
            continue

        if x != " " and x in STAGED_MAP:
            staged[STAGED_MAP[x]].append(path)

        if y != " " and y in UNSTAGED_MAP:
            unstaged[UNSTAGED_MAP[y]].append(path)

    return {
        "staged": dict(staged),
        "unstaged": dict(unstaged),
        "untracked": {"UNTRACKED": untracked} if untracked else {},
    }
