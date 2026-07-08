#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


ALLOWED_TYPES = {
    "chore",
    "docs",
    "feat",
    "fix",
    "refactor",
    "release",
    "revert",
    "test",
}

MAX_SUBJECT_LENGTH = 120
PATTERN = re.compile(r"^(?P<type>[a-z]+)(?:\([a-z0-9._/-]+\))?: (?P<subject>.+)$")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_commit_msg.py <commit-msg-file>", file=sys.stderr)
        return 2

    message_path = Path(sys.argv[1])
    lines = message_path.read_text().splitlines()
    first_line = next((line.strip() for line in lines if line.strip() and not line.startswith("#")), "")

    if not first_line:
        print("Commit message must not be empty.", file=sys.stderr)
        return 1

    if first_line.startswith(("Merge ", "Revert ")):
        return 0

    match = PATTERN.fullmatch(first_line)
    if match is None:
        print(
            "Invalid commit message.\n"
            "\n"
            "Use: <type>: <message>\n"
            "Example: fix: handle empty project library\n",
            file=sys.stderr,
        )
        return 1

    commit_type = match.group("type")
    subject = match.group("subject")

    if commit_type not in ALLOWED_TYPES:
        allowed = ", ".join(sorted(ALLOWED_TYPES))
        print(f"Invalid commit type '{commit_type}'. Allowed types: {allowed}", file=sys.stderr)
        return 1

    if len(subject) > MAX_SUBJECT_LENGTH:
        print(
            f"Commit message subject is {len(subject)} characters; "
            f"maximum is {MAX_SUBJECT_LENGTH}.",
            file=sys.stderr,
        )
        return 1

    if subject[0].isspace() or subject[-1].isspace():
        print("Commit message subject must not start or end with whitespace.", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
