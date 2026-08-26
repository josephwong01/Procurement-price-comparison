#!/usr/bin/env python3
"""Validate Product Candidate documents with JSON Schema Draft 2020-12."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import jsonschema


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", required=True, type=Path)
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()

    with args.schema.open("r", encoding="utf-8") as handle:
        schema = json.load(handle)
    validator_class = jsonschema.Draft202012Validator
    validator_class.check_schema(schema)
    validator = validator_class(schema)

    errors: list[dict[str, str]] = []
    for path in args.paths:
        with path.open("r", encoding="utf-8") as handle:
            document = json.load(handle)
        for error in validator.iter_errors(document):
            errors.append(
                {
                    "file": str(path),
                    "json_path": str(error.json_path),
                    "message": error.message,
                }
            )

    result = {
        "status": "FAILED" if errors else "PASSED",
        "draft": "2020-12",
        "schema": str(args.schema),
        "files": len(args.paths),
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
