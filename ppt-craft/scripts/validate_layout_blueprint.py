#!/usr/bin/env python3
"""Validate a PPT Craft layout-blueprint.json file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


BOX_KEYS = ("claim", "support", "visual", "evidence", "loop", "mask")
OVERLAP_KEYS = ("claim", "support", "visual", "evidence", "loop")


def load(path: Path) -> tuple[dict | None, list[str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, [f"file not found: {path}"]
    except json.JSONDecodeError as exc:
        return None, [f"invalid JSON: {exc}"]
    if not isinstance(data, dict):
        return None, ["blueprint root must be an object"]
    return data, []


def validate_box(label: str, box: object, width: float, height: float) -> list[str]:
    errors: list[str] = []
    if not isinstance(box, dict):
        return [f"{label} must be an object"]
    for key in ("x", "y", "w", "h"):
        if not isinstance(box.get(key), (int, float)):
            errors.append(f"{label}.{key} must be numeric")
    if errors:
        return errors
    if box["w"] <= 0 or box["h"] <= 0:
        errors.append(f"{label} has non-positive size")
    if box["x"] < 0 or box["y"] < 0 or box["x"] + box["w"] > width or box["y"] + box["h"] > height:
        errors.append(f"{label} is outside the {width:g}x{height:g} stage")
    return errors


def overlap_area(a: dict, b: dict) -> float:
    left = max(a["x"], b["x"])
    top = max(a["y"], b["y"])
    right = min(a["x"] + a["w"], b["x"] + b["w"])
    bottom = min(a["y"] + a["h"], b["y"] + b["h"])
    if right <= left or bottom <= top:
        return 0
    return (right - left) * (bottom - top)


def validate_overlaps(label: str, slide: dict) -> list[str]:
    errors: list[str] = []
    boxes = {
        key: slide[key]
        for key in OVERLAP_KEYS
        if isinstance(slide.get(key), dict) and all(isinstance(slide[key].get(part), (int, float)) for part in ("x", "y", "w", "h"))
    }
    keys = list(boxes)
    for index, first in enumerate(keys):
        for second in keys[index + 1:]:
            if {first, second} == {"visual", "loop"}:
                continue
            area = overlap_area(boxes[first], boxes[second])
            if area > 1:
                errors.append(f"{label}.{first} overlaps {second} by {area:g}px^2")
    return errors


def load_archetype_ids(path: Path | None) -> set[str]:
    if not path:
        return set()
    data, errors = load(path)
    if errors or not isinstance(data, dict):
        return set()
    items = data.get("archetypes", [])
    if not isinstance(items, list):
        return set()
    return {str(item.get("id")) for item in items if isinstance(item, dict) and item.get("id")}


def validate(data: dict, archetype_ids: set[str] | None = None) -> list[str]:
    errors: list[str] = []
    stage = data.get("stage")
    slides = data.get("slides")
    if not isinstance(stage, dict):
        return ["missing stage object"]
    if not isinstance(slides, list) or not slides:
        return ["missing non-empty slides array"]

    width = stage.get("width")
    height = stage.get("height")
    if not isinstance(width, (int, float)) or width <= 0:
        errors.append("stage.width must be positive")
    if not isinstance(height, (int, float)) or height <= 0:
        errors.append("stage.height must be positive")
    if errors:
        return errors

    if "safe" not in stage:
        errors.append("stage.safe is required")
    else:
        errors += validate_box("stage.safe", stage["safe"], width, height)

    seen: set[str] = set()
    for index, slide in enumerate(slides, start=1):
        if not isinstance(slide, dict):
            errors.append(f"slides[{index}] must be an object")
            continue
        slide_id = str(slide.get("id") or "").strip()
        label = slide_id or f"slides[{index}]"
        if not slide_id:
            errors.append(f"{label}.id is required")
        elif slide_id in seen:
            errors.append(f"duplicate slide id: {slide_id}")
        seen.add(slide_id)
        if not str(slide.get("job") or "").strip():
            errors.append(f"{label}.job is required")
        archetype = str(slide.get("archetype") or "").strip()
        if archetype_ids is not None and archetype and archetype not in archetype_ids:
            errors.append(f"{label}.archetype is not in the archetype library: {archetype}")
        if not any(key in slide for key in ("claim", "visual", "evidence", "loop")):
            errors.append(f"{label} needs at least one of claim, visual, evidence, or loop")
        for key in BOX_KEYS:
            if key in slide:
                errors += validate_box(f"{label}.{key}", slide[key], width, height)
        errors += validate_overlaps(label, slide)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("blueprint", type=Path)
    parser.add_argument("--archetypes", type=Path, default=None)
    args = parser.parse_args()

    data, errors = load(args.blueprint)
    if data is not None:
        archetype_ids = load_archetype_ids(args.archetypes) if args.archetypes else None
        errors += validate(data, archetype_ids)

    if errors:
        print("layout-blueprint-validation-failed")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"layout-blueprint-validation-ok path={args.blueprint.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
