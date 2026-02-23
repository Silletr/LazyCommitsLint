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


def analyze_staged() -> Dict[str, List[str]]:
    result = subprocess.run(
        ["git", "diff", "--staged", "--name-status"], text=True, capture_output=True
    )
    changes = defaultdict(list)
    for line in result.stdout.strip().splitlines():
        if line:
            # Handles "R100 file1 file2"
            status, *files = line.split(maxsplit=2)
            cat = CATEGORY_MAP.get(status[0], "CHANGED")
            file_list = files if len(files) > 1 else [files[0]]
            changes[cat].extend(file_list)
    print(f"CHANGES LIST:\n{dict(changes)}")
    return changes  # {'NEW': ['src/foo.py'], 'CHANGED': ['README.md']}


if __name__ == "__main__":
    analyze_staged()
