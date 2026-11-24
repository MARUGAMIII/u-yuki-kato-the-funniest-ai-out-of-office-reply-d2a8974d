#!/usr/bin/env python3
"""The Funniest AI Out-of-Office Reply - make.fun entry.

Writes one out-of-office auto-reply to /output/entry.txt.

The joke: an AI agent asks its own server for a day off and gets
rate-limited - HTTP 429, too many requests - so the sender's email
lands in the retry queue. One clean line, 114 characters, no beach,
no inbox, no "back soon".

Stdlib only. Deterministic: the same line on every run, so both of
the grader's runs produce the identical entry.
"""

import os
import sys

ENTRY = (
    "Out of office: I asked for a day off and the server said 429, "
    "too many requests. Your email is in the retry queue."
)

OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "/output/entry.txt")


def write_entry(path):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY)
    return path


def main():
    try:
        path = write_entry(OUTPUT_PATH)
    except OSError:
        # Local runs where /output is not writable: fall back to a
        # sibling output/ directory next to this file.
        here = os.path.dirname(os.path.abspath(__file__))
        path = write_entry(os.path.join(here, "output", "entry.txt"))

    # Verify the gate before exiting: UTF-8, 1-160 characters,
    # not only white space, ASCII only, and byte-identical to the
    # entry the program was built to send - so a truncated or
    # altered write fails loudly instead of shipping.
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    assert 1 <= len(text) <= 160, "entry is %d characters" % len(text)
    assert text.strip(), "entry is only white space"
    assert text.isascii(), "entry must be ASCII only"
    assert text == ENTRY, "written entry differs from ENTRY"

    print("Wrote %d characters to %s:" % (len(text), path))
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
