#!/usr/bin/env python3
"""Create the browser-friendly data bundle from competitions.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from validate_data import DEFAULT_BUNDLE, DEFAULT_DATA, expected_bundle, validate


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path, default=DEFAULT_BUNDLE)
    parser.add_argument("--check", action="store_true", help="check synchronization without writing")
    args = parser.parse_args()

    data = json.loads(args.source.read_text(encoding="utf-8"))
    errors = validate(data)
    if errors:
        raise SystemExit("Source data is invalid:\n" + "\n".join(f"- {error}" for error in errors))

    expected = expected_bundle(data)
    if args.check:
        if not args.output.exists() or args.output.read_text(encoding="utf-8") != expected:
            raise SystemExit(f"Bundle is stale: {args.output}")
        print(f"OK: bundle matches {args.source}")
        return 0

    args.output.write_text(expected, encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
