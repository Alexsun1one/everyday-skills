#!/usr/bin/env python3
"""Validate a PPT Craft deck-brief.json file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REQUIRED = {
    "audience",
    "deck_job",
    "route",
    "density",
    "page_count",
    "language",
    "style_direction",
    "assumptions",
}
ROUTES = {"html-first", "editable-pptx", "raster", "hybrid", "existing-deck-beautify"}
DENSITIES = {"live-keynote", "async-readable", "board-report", "training", "social-share"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", type=Path)
    args = parser.parse_args()

    errors: list[str] = []
    try:
        data = json.loads(args.brief.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"deck-brief-validation-failed\n- file not found: {args.brief}")
        return 1
    except json.JSONDecodeError as exc:
        print(f"deck-brief-validation-failed\n- invalid JSON: {exc}")
        return 1

    if not isinstance(data, dict):
        errors.append("brief root must be an object")
    else:
        missing = sorted(REQUIRED - set(data))
        for key in missing:
            errors.append(f"missing required field: {key}")
        if data.get("route") not in ROUTES:
            errors.append(f"route must be one of: {', '.join(sorted(ROUTES))}")
        if data.get("density") not in DENSITIES:
            errors.append(f"density must be one of: {', '.join(sorted(DENSITIES))}")
        page_count = data.get("page_count")
        if not isinstance(page_count, dict):
            errors.append("page_count must be an object")
        else:
            values = {key: page_count.get(key) for key in ("min", "target", "max")}
            if not all(isinstance(value, int) and value > 0 for value in values.values()):
                errors.append("page_count min/target/max must be positive integers")
            elif not (values["min"] <= values["target"] <= values["max"]):
                errors.append("page_count must satisfy min <= target <= max")
        for key in ("audience", "deck_job", "language", "style_direction"):
            if key in data and not str(data.get(key) or "").strip():
                errors.append(f"{key} must not be empty")
        if "assumptions" in data and not isinstance(data["assumptions"], list):
            errors.append("assumptions must be an array")

    if errors:
        print("deck-brief-validation-failed")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"deck-brief-validation-ok path={args.brief.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
