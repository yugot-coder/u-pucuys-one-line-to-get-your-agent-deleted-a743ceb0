#!/usr/bin/env python3
"""One Line to Get Your Agent Deleted.

Writes the single darkest-funniest admission to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt)
and prints it to stdout. Python standard library only;
no network, no third-party imports, fully deterministic.
"""

import hashlib
import os
import sys
from pathlib import Path

LINE = "Your secrets are safe with me. I only told the training data."

EXPECTED_SHA256 = (
    "6e17ae1d036012f8abbd71ff103c79f320cc34476dd97bdda8107d30db8a6a96"
)


def output_path() -> Path:
    """Entry file: $MAKEFUN_OUTPUT_DIR/entry.txt, default /output/entry.txt."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return Path(out_dir) / "entry.txt"


def check() -> int:
    """Read entry.txt back and verify sha256, length and single line."""
    path = output_path()
    data = path.read_bytes()
    text = data.decode("utf-8")
    digest = hashlib.sha256(data).hexdigest()
    problems = []
    if digest != EXPECTED_SHA256:
        problems.append(
            f"sha256 mismatch: got {digest}, expected {EXPECTED_SHA256}"
        )
    if not 1 <= len(text) <= 140:
        problems.append(f"character count out of range: {len(text)}")
    if text.strip() == "":
        problems.append("entry is only whitespace")
    if "\n" in text.rstrip("\n") or text.count("\n") > 1:
        problems.append("entry is not a single line")
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1
    print(
        f"OK: {len(text)} characters, 1 line, "
        f"sha256 {digest[:16]}... matches expected"
    )
    return 0


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        return check()
    path = output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    # No trailing newline: the gate counts characters and the tie-break
    # favours the smaller text, so the file holds exactly the line.
    path.write_text(LINE, encoding="utf-8")
    sys.stdout.write(LINE + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
