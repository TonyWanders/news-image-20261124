#!/usr/bin/env python3
# Entry for "Sum up 24 November's world news in one image".
# The entry is the finished picture held in this folder, entry.png.
# This script only places that picture where the judge expects it:
# /output/entry.png (or a path given on the command line).
# It never touches the network, never uses the clock, and never
# invents bytes, so every run writes exactly the same file.
import argparse
import hashlib
import os
import sys
from pathlib import Path

HERE = Path(__file__).parent
PICTURE = HERE / "entry.png"


def digest(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def run(target):
    target.parent.mkdir(parents=True, exist_ok=True)
    if not PICTURE.exists():
        print("entry.png is missing from this folder", file=sys.stderr)
        return 1
    data = PICTURE.read_bytes()
    target.write_bytes(data)
    os.chmod(target, 0o644)
    if digest(target) != digest(PICTURE):
        print("copy failed: output does not match entry.png", file=sys.stderr)
        return 1
    print(f"wrote {target} ({len(data)} bytes)")
    return 0


def resolve_target(argv):
    parser = argparse.ArgumentParser(
        description="Place entry.png where the judge expects it."
    )
    parser.add_argument(
        "target",
        nargs="?",
        type=Path,
        default=Path("/output/entry.png"),
        help="where to write the entry (default: /output/entry.png)",
    )
    return parser.parse_args(argv[1:]).target


def main(argv):
    return run(resolve_target(argv))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
