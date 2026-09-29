#!/usr/bin/env python3
"""Validate a PPT Craft deck folder."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


BAD_TEXT = ("TODO", "Lorem ipsum", "placeholder", "占位", "待补")
HTML_SIZE_RE = re.compile(r"(1920\s*px.*1080\s*px|1080\s*px.*1920\s*px|1280\s*px.*720\s*px|720\s*px.*1280\s*px)", re.I | re.S)
EDITABLE_SIZE_RE = re.compile(r"(960\s*pt.*540\s*pt|1280\s*px.*720\s*px|13\.333\s*in.*7\.5\s*in)", re.I | re.S)
BARE_DIV_TEXT_RE = re.compile(r"<div\b(?P<attrs>[^>]*)>\s*[^<\s][^<]*\s*</div>", re.I)
HERO_BR_RE = re.compile(r"<h[1-2]\b[^>]*>.*?<br\s*/?>.*?</h[1-2]>", re.I | re.S)
BRIEF_ROUTES = {"html-first", "editable-pptx", "raster", "hybrid", "existing-deck-beautify"}
BRIEF_DENSITIES = {"live-keynote", "async-readable", "board-report", "training", "social-share"}
BLUEPRINT_BOXES = ("claim", "support", "visual", "evidence", "loop", "mask")
BLUEPRINT_OVERLAP_BOXES = ("claim", "support", "visual", "evidence", "loop")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel(root: Path, path: Path) -> str:
    return str(path.relative_to(root))


def check_common(root: Path) -> list[str]:
    errors: list[str] = []
    if not root.exists():
        return [f"deck folder does not exist: {root}"]

    html_files = sorted(root.glob("**/*.html"))
    if not html_files:
        errors.append("no .html files found")

    for path in html_files:
        text = read(path)
        for token in BAD_TEXT:
            if token in text:
                errors.append(f"{rel(root, path)} contains unresolved marker: {token}")
        if "<html" not in text.lower() or "<body" not in text.lower():
            errors.append(f"{rel(root, path)} is not a complete HTML document")
    return errors


def check_layout_blueprint(root: Path, require: bool) -> list[str]:
    errors: list[str] = []
    path = root / "layout-blueprint.json"
    if not path.exists():
        if require:
            errors.append("layout-blueprint.json is required for this validation")
        return errors

    try:
        data = json.loads(read(path))
    except json.JSONDecodeError as exc:
        return [f"layout-blueprint.json is invalid JSON: {exc}"]

    if not isinstance(data, dict):
        return ["layout-blueprint.json must be an object"]

    stage = data.get("stage")
    slides = data.get("slides")
    if not isinstance(stage, dict):
        errors.append("layout-blueprint.json missing object: stage")
        return errors
    if not isinstance(slides, list) or not slides:
        errors.append("layout-blueprint.json missing non-empty array: slides")
        return errors

    width = stage.get("width")
    height = stage.get("height")
    if not isinstance(width, (int, float)) or width <= 0:
        errors.append("layout-blueprint.json stage.width must be positive")
    if not isinstance(height, (int, float)) or height <= 0:
        errors.append("layout-blueprint.json stage.height must be positive")

    def check_box(slide_id: str, name: str, box: object) -> None:
        if not isinstance(box, dict):
            errors.append(f"layout-blueprint.json {slide_id}.{name} must be a box object")
            return
        for key in ("x", "y", "w", "h"):
            if not isinstance(box.get(key), (int, float)):
                errors.append(f"layout-blueprint.json {slide_id}.{name}.{key} must be numeric")
                return
        if box["w"] <= 0 or box["h"] <= 0:
            errors.append(f"layout-blueprint.json {slide_id}.{name} has non-positive size")
        if isinstance(width, (int, float)) and isinstance(height, (int, float)):
            if box["x"] < 0 or box["y"] < 0 or box["x"] + box["w"] > width or box["y"] + box["h"] > height:
                errors.append(f"layout-blueprint.json {slide_id}.{name} is outside the stage")

    def overlap_area(a: dict, b: dict) -> float:
        left = max(a["x"], b["x"])
        top = max(a["y"], b["y"])
        right = min(a["x"] + a["w"], b["x"] + b["w"])
        bottom = min(a["y"] + a["h"], b["y"] + b["h"])
        if right <= left or bottom <= top:
            return 0
        return (right - left) * (bottom - top)

    safe = stage.get("safe")
    if safe is not None:
        check_box("stage", "safe", safe)

    seen: set[str] = set()
    for index, slide in enumerate(slides, start=1):
        if not isinstance(slide, dict):
            errors.append(f"layout-blueprint.json slides[{index}] must be an object")
            continue
        slide_id = str(slide.get("id") or "").strip()
        if not slide_id:
            errors.append(f"layout-blueprint.json slides[{index}] missing id")
            continue
        if slide_id in seen:
            errors.append(f"layout-blueprint.json duplicate slide id: {slide_id}")
        seen.add(slide_id)
        if not str(slide.get("job") or "").strip():
            errors.append(f"layout-blueprint.json {slide_id}.job is required")
        if not any(key in slide for key in ("claim", "visual", "evidence", "loop")):
            errors.append(f"layout-blueprint.json {slide_id} needs at least one claim, visual, evidence, or loop box")
        for key in BLUEPRINT_BOXES:
            if key in slide:
                check_box(slide_id, key, slide[key])
        overlap_boxes = {
            key: slide[key]
            for key in BLUEPRINT_OVERLAP_BOXES
            if isinstance(slide.get(key), dict) and all(isinstance(slide[key].get(part), (int, float)) for part in ("x", "y", "w", "h"))
        }
        overlap_keys = list(overlap_boxes)
        for i, first in enumerate(overlap_keys):
            for second in overlap_keys[i + 1:]:
                if {first, second} == {"visual", "loop"}:
                    continue
                area = overlap_area(overlap_boxes[first], overlap_boxes[second])
                if area > 1:
                    errors.append(f"layout-blueprint.json {slide_id}.{first} overlaps {second} by {area:g}px^2")

    return errors


def check_deck_brief(root: Path, require: bool) -> list[str]:
    errors: list[str] = []
    path = root / "deck-brief.json"
    if not path.exists():
        if require:
            errors.append("deck-brief.json is required for this validation")
        return errors

    try:
        data = json.loads(read(path))
    except json.JSONDecodeError as exc:
        return [f"deck-brief.json is invalid JSON: {exc}"]

    if not isinstance(data, dict):
        return ["deck-brief.json must be an object"]
    required = {"audience", "deck_job", "route", "density", "page_count", "language", "style_direction", "assumptions"}
    for key in sorted(required - set(data)):
        errors.append(f"deck-brief.json missing required field: {key}")
    if data.get("route") not in BRIEF_ROUTES:
        errors.append(f"deck-brief.json route must be one of: {', '.join(sorted(BRIEF_ROUTES))}")
    if data.get("density") not in BRIEF_DENSITIES:
        errors.append(f"deck-brief.json density must be one of: {', '.join(sorted(BRIEF_DENSITIES))}")
    page_count = data.get("page_count")
    if not isinstance(page_count, dict):
        errors.append("deck-brief.json page_count must be an object")
    else:
        values = {key: page_count.get(key) for key in ("min", "target", "max")}
        if not all(isinstance(value, int) and value > 0 for value in values.values()):
            errors.append("deck-brief.json page_count min/target/max must be positive integers")
        elif not (values["min"] <= values["target"] <= values["max"]):
            errors.append("deck-brief.json page_count must satisfy min <= target <= max")
    if "assumptions" in data and not isinstance(data["assumptions"], list):
        errors.append("deck-brief.json assumptions must be an array")
    return errors


def check_asset_prompts(root: Path, require: bool) -> list[str]:
    errors: list[str] = []
    path = root / "asset-prompts" / "asset-prompts.json"
    if not path.exists():
        if require:
            errors.append("asset-prompts/asset-prompts.json is required for this validation")
        return errors

    try:
        data = json.loads(read(path))
    except json.JSONDecodeError as exc:
        return [f"asset-prompts/asset-prompts.json is invalid JSON: {exc}"]
    if not isinstance(data, dict):
        return ["asset-prompts/asset-prompts.json must be an object"]
    slides = data.get("slides")
    if not isinstance(slides, list) or not slides:
        errors.append("asset-prompts/asset-prompts.json missing non-empty slides array")
        return errors
    for index, slide in enumerate(slides, start=1):
        if not isinstance(slide, dict):
            errors.append(f"asset prompt slide {index} must be an object")
            continue
        slide_id = str(slide.get("id") or f"#{index}")
        for key in ("job", "visual_region", "text_safe_zones", "foreground_overlay", "prompt", "negative_prompt", "qa"):
            if key not in slide:
                errors.append(f"asset prompt {slide_id} missing required field: {key}")
        if not isinstance(slide.get("visual_region"), dict):
            errors.append(f"asset prompt {slide_id}.visual_region must be an object")
        if not isinstance(slide.get("text_safe_zones"), list) or not slide.get("text_safe_zones"):
            errors.append(f"asset prompt {slide_id}.text_safe_zones must be a non-empty array")
        if not isinstance(slide.get("foreground_overlay"), list) or not slide.get("foreground_overlay"):
            errors.append(f"asset prompt {slide_id}.foreground_overlay must be a non-empty array")
        if not str(slide.get("prompt") or "").strip():
            errors.append(f"asset prompt {slide_id}.prompt is empty")
        if not str(slide.get("negative_prompt") or "").strip():
            errors.append(f"asset prompt {slide_id}.negative_prompt is empty")
    return errors


def check_html_route(root: Path, require_blueprint: bool, require_brief: bool, require_asset_prompts: bool) -> list[str]:
    errors = check_common(root)
    errors += check_deck_brief(root, require_brief)
    errors += check_layout_blueprint(root, require_blueprint)
    errors += check_asset_prompts(root, require_asset_prompts)
    index = root / "index.html"
    slides = sorted((root / "slides").glob("*.html")) if (root / "slides").exists() else []

    if not index.exists():
        errors.append("html route requires index.html")
    elif "DECK_MANIFEST" not in read(index):
        errors.append("index.html must define window.DECK_MANIFEST")

    if not slides:
        errors.append("html route requires slides/*.html")

    for slide in slides:
        text = read(slide)
        if not HTML_SIZE_RE.search(text):
            errors.append(f"{rel(root, slide)} does not appear to lock a 1920x1080 canvas")
        if re.search(r"(overflow\s*:\s*auto|overflow-y\s*:\s*scroll)", text, re.I):
            errors.append(f"{rel(root, slide)} uses scrolling inside a slide")
    return errors


def check_editable_route(root: Path, require_blueprint: bool, require_brief: bool, require_asset_prompts: bool) -> list[str]:
    errors = check_common(root)
    errors += check_deck_brief(root, require_brief)
    errors += check_layout_blueprint(root, require_blueprint)
    errors += check_asset_prompts(root, require_asset_prompts)
    slides = sorted((root / "slides").glob("*.html")) if (root / "slides").exists() else sorted(root.glob("*.html"))

    for slide in slides:
        text = read(slide)
        if not EDITABLE_SIZE_RE.search(text):
            errors.append(f"{rel(root, slide)} does not appear to use an editable-PPTX canvas size")
        if "linear-gradient" in text or "radial-gradient" in text:
            errors.append(f"{rel(root, slide)} uses CSS gradient; editable PPTX route needs solid fills")
        if "background-image" in text:
            errors.append(f"{rel(root, slide)} uses background-image; use <img> for PPTX")
        if HERO_BR_RE.search(text):
            errors.append(f"{rel(root, slide)} uses <br> inside h1/h2; split hero lines into separate positioned text boxes for PPTX")
        for match in BARE_DIV_TEXT_RE.finditer(text):
            attrs = match.group("attrs").lower()
            if "data-pptx-text" in attrs:
                continue
            errors.append(f"{rel(root, slide)} may contain bare text directly in a div")
            break
    return errors


def check_raster_route(root: Path) -> list[str]:
    errors: list[str] = []
    if not (root / "outline.md").exists():
        errors.append("raster route requires outline.md")
    prompts = sorted((root / "prompts").glob("*.md")) if (root / "prompts").exists() else []
    if not prompts:
        errors.append("raster route requires prompts/*.md")
    images = sorted(p for ext in ("*.png", "*.jpg", "*.jpeg", "*.webp") for p in root.glob(ext))
    if not images:
        errors.append("raster route requires slide image files in the deck root")
    if prompts and images and len(prompts) != len(images):
        errors.append(f"prompt/image count differs: prompts={len(prompts)} images={len(images)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck_dir", type=Path)
    parser.add_argument("--mode", choices=("html", "editable", "raster"), default="html")
    parser.add_argument("--require-blueprint", action="store_true", help="Require and validate layout-blueprint.json")
    parser.add_argument("--require-brief", action="store_true", help="Require and validate deck-brief.json")
    parser.add_argument("--require-asset-prompts", action="store_true", help="Require and validate asset-prompts/asset-prompts.json")
    args = parser.parse_args()

    root = args.deck_dir.resolve()
    if args.mode == "html":
        errors = check_html_route(root, args.require_blueprint, args.require_brief, args.require_asset_prompts)
    elif args.mode == "editable":
        errors = check_editable_route(root, args.require_blueprint, args.require_brief, args.require_asset_prompts)
    else:
        errors = check_raster_route(root)

    if errors:
        print("deck-validation-failed")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"deck-validation-ok mode={args.mode} path={root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
