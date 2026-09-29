#!/usr/bin/env python3
"""Validate PPT Craft style anchor starter specs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_ANCHORS = SKILL_DIR / "assets" / "style-anchor-library.json"
DEFAULT_STARTERS = SKILL_DIR / "assets" / "style-anchor-starters.json"
DEFAULT_ARCHETYPES = SKILL_DIR / "assets" / "layout-archetypes.json"
REQUIRED_ROLES = {"cover", "proof", "system", "closing"}
REQUIRED_FIELDS = {
    "role",
    "archetype",
    "headline",
    "support",
    "visual",
    "object_families",
    "asset_direction",
    "qa",
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def ids_from_library(path: Path) -> set[str]:
    data = read_json(path)
    anchors = data.get("anchors", []) if isinstance(data, dict) else []
    return {str(anchor.get("id")) for anchor in anchors if isinstance(anchor, dict) and anchor.get("id")}


def archetype_ids(path: Path) -> set[str]:
    data = read_json(path)
    items = data.get("archetypes", []) if isinstance(data, dict) else []
    return {str(item.get("id")) for item in items if isinstance(item, dict) and item.get("id")}


def validate(args: argparse.Namespace) -> list[str]:
    errors: list[str] = []
    anchor_ids = ids_from_library(args.anchors)
    local_archetypes = archetype_ids(args.archetypes)
    data = read_json(args.starters)

    if not isinstance(data, dict):
        return ["style-anchor-starters.json must be an object"]
    if data.get("stage", {}).get("width") != 1280 or data.get("stage", {}).get("height") != 720:
        errors.append("stage must be 1280x720")
    declared_roles = set(data.get("required_roles", []))
    if declared_roles != REQUIRED_ROLES:
        errors.append(f"required_roles must be exactly {sorted(REQUIRED_ROLES)}")

    starter_items = data.get("anchors")
    if not isinstance(starter_items, list) or not starter_items:
        return ["anchors must be a non-empty array"]

    starter_ids: set[str] = set()
    for item in starter_items:
        if not isinstance(item, dict):
            errors.append("each starter anchor must be an object")
            continue
        anchor_id = str(item.get("anchor_id") or "")
        if not anchor_id:
            errors.append("starter anchor missing anchor_id")
            continue
        starter_ids.add(anchor_id)
        if anchor_id not in anchor_ids:
            errors.append(f"unknown anchor_id: {anchor_id}")
        starters = item.get("starters")
        if not isinstance(starters, list):
            errors.append(f"{anchor_id}.starters must be an array")
            continue
        roles = [starter.get("role") for starter in starters if isinstance(starter, dict)]
        if set(roles) != REQUIRED_ROLES or len(roles) != len(REQUIRED_ROLES):
            errors.append(f"{anchor_id}.starters must contain exactly cover/proof/system/closing")
        for starter in starters:
            if not isinstance(starter, dict):
                errors.append(f"{anchor_id}.starter must be an object")
                continue
            role = str(starter.get("role") or "?")
            missing = REQUIRED_FIELDS - set(starter)
            for field in sorted(missing):
                errors.append(f"{anchor_id}.{role} missing field: {field}")
            archetype = str(starter.get("archetype") or "")
            if archetype not in local_archetypes:
                errors.append(f"{anchor_id}.{role} uses unknown local archetype: {archetype}")
            for field in ("headline", "support", "visual", "asset_direction"):
                if not str(starter.get(field) or "").strip():
                    errors.append(f"{anchor_id}.{role}.{field} is empty")
            for field in ("object_families", "qa"):
                value = starter.get(field)
                if not isinstance(value, list) or not value or not all(str(part).strip() for part in value):
                    errors.append(f"{anchor_id}.{role}.{field} must be a non-empty string array")

    missing_anchors = anchor_ids - starter_ids
    extra_anchors = starter_ids - anchor_ids
    for anchor_id in sorted(missing_anchors):
        errors.append(f"missing starter set for anchor: {anchor_id}")
    for anchor_id in sorted(extra_anchors):
        errors.append(f"starter set has no matching anchor: {anchor_id}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--anchors", type=Path, default=DEFAULT_ANCHORS)
    parser.add_argument("--starters", type=Path, default=DEFAULT_STARTERS)
    parser.add_argument("--archetypes", type=Path, default=DEFAULT_ARCHETYPES)
    args = parser.parse_args()

    errors = validate(args)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"style-anchor-starters-ok path={args.starters}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
