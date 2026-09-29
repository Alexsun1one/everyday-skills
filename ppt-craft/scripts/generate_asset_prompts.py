#!/usr/bin/env python3
"""Generate blueprint-aware image prompts for a PPT Craft deck."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_ARCHETYPES = SKILL_DIR / "assets" / "layout-archetypes.json"
DEFAULT_DESIGN_SYSTEM = SKILL_DIR / "assets" / "slide-design-system.json"

TEXT_BOXES = ("claim", "support", "evidence", "loop")


def read_json(path: Path, fallback: Any = None) -> Any:
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def archetype_map(path: Path) -> dict[str, dict[str, Any]]:
    data = read_json(path, {"archetypes": []})
    items = data.get("archetypes", []) if isinstance(data, dict) else []
    return {str(item.get("id")): item for item in items if isinstance(item, dict) and item.get("id")}


def merged_slide(slide: dict[str, Any], archetypes: dict[str, dict[str, Any]]) -> dict[str, Any]:
    archetype = archetypes.get(str(slide.get("archetype", "")))
    merged: dict[str, Any] = {}
    if archetype:
        merged.update(archetype.get("coordinates", {}))
        merged["_archetype_name"] = archetype.get("name", archetype.get("id"))
        merged["_archetype_guardrails"] = archetype.get("guardrails", [])
    merged.update(slide)
    return merged


def fmt_box(box: dict[str, Any]) -> str:
    return f"x={box['x']}, y={box['y']}, w={box['w']}, h={box['h']}"


def has_box(slide: dict[str, Any], key: str) -> bool:
    box = slide.get(key)
    return isinstance(box, dict) and all(part in box for part in ("x", "y", "w", "h"))


def foreground_for(kind: str, box: dict[str, Any]) -> dict[str, Any]:
    family_by_kind = {
        "claim": "paper-card/dark-strip behind title",
        "support": "paper-card or caption-band behind support copy",
        "evidence": "evidence plate / table plate / chart plate",
        "loop": "route chips, number badges, loop connectors",
    }
    return {
        "object_family": family_by_kind.get(kind, "paper-card"),
        "role": f"external editable {kind}",
        "region": box,
    }


def text_safe_zone(kind: str, box: dict[str, Any]) -> dict[str, Any]:
    instruction_by_kind = {
        "claim": "Keep quiet enough for large editable title lines and a strong backplate; no focal object here.",
        "support": "Keep low-detail and uncluttered for editable body copy on a paper card.",
        "evidence": "Reserve for editable table/chart/caption plate; no dense props underneath.",
        "loop": "Reserve for editable route chips, labels, and connector lines.",
    }
    return {
        "name": kind,
        "box": box,
        "instruction": instruction_by_kind.get(kind, "Keep visually quiet for editable foreground type."),
    }


def make_prompt(
    *,
    deck_brief: dict[str, Any],
    design: dict[str, Any],
    stage: dict[str, Any],
    slide: dict[str, Any],
) -> dict[str, Any]:
    slide_id = str(slide.get("id") or "slide")
    job = str(slide.get("job") or "")
    archetype = str(slide.get("archetype") or "custom")
    route = str(deck_brief.get("route") or "hybrid")
    style_direction = str(deck_brief.get("style_direction") or "")
    visual = slide.get("visual") if has_box(slide, "visual") else {
        "x": 0,
        "y": 0,
        "w": stage.get("width", 1280),
        "h": stage.get("height", 720),
    }

    text_zones = [text_safe_zone(kind, slide[kind]) for kind in TEXT_BOXES if has_box(slide, kind)]
    no_go_zones = [
        {
            "name": zone["name"],
            "box": zone["box"],
            "reason": "The image focal subject, busy texture, and fake labels must not occupy this text-safe region.",
        }
        for zone in text_zones
    ]
    overlays = [foreground_for(kind, slide[kind]) for kind in TEXT_BOXES if has_box(slide, kind)]
    if has_box(slide, "visual"):
        overlays.append({
            "object_family": "optional blank plaques attached to visual props",
            "role": "alignment anchors for later editable labels",
            "region": slide["visual"],
        })

    no_text_policy = design.get("image_prompt_contract", {}).get("no_text_policy", "")
    negative_prompt = design.get("image_prompt_contract", {}).get("negative_prompt", "")
    camera = design.get("image_prompt_contract", {}).get("camera", "16:9 slide visual")

    zone_lines = "; ".join(f"{item['name']} zone ({fmt_box(item['box'])})" for item in text_zones) or "none"
    overlay_lines = "; ".join(f"{item['object_family']} in {fmt_box(item['region'])}" for item in overlays)
    prompt = (
        f"Create a {camera} for slide '{slide_id}'. "
        f"Slide job: {job}. "
        f"Style direction: {style_direction}. "
        f"Primary visual subject must live inside visual region ({fmt_box(visual)}). "
        f"Reserve these text-safe zones as quiet, low-detail surfaces: {zone_lines}. "
        f"Foreground editable overlay objects will be added later: {overlay_lines}. "
        f"For route '{route}', follow this text policy: {no_text_policy}. "
        "Use strong spatial hierarchy, clear subject placement, enough negative space, and tactile material depth. "
        "If using paper-operators, the paper operator must physically perform the slide's core action inside the visual region, "
        "while the reserved zones remain calm enough for external type plates."
    )

    qa = [
        "text-safe zones are quiet and usable for editable type/backplates",
        "visual subject stays inside the visual region",
        "no fake text or accidental labels in hybrid/editable route",
        "blank plaques/tags only appear where external editable labels will sit",
        "image supports the slide job and does not force raw text on top of texture",
    ]
    guardrails = slide.get("_archetype_guardrails")
    if isinstance(guardrails, list):
        qa.extend(str(item) for item in guardrails[:3])

    return {
        "id": slide_id,
        "job": job,
        "archetype": archetype,
        "visual_region": visual,
        "text_safe_zones": text_zones,
        "no_go_zones": no_go_zones,
        "foreground_overlay": overlays,
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "qa": qa,
    }


def markdown_for_slide(slide: dict[str, Any]) -> str:
    text_zones = "\n".join(
        f"- {item['name']}: `{fmt_box(item['box'])}` — {item['instruction']}"
        for item in slide["text_safe_zones"]
    ) or "- none"
    overlays = "\n".join(
        f"- {item['object_family']}: {item['role']} in `{fmt_box(item['region'])}`"
        for item in slide["foreground_overlay"]
    ) or "- none"
    qa = "\n".join(f"- {item}" for item in slide["qa"])
    return f"""# {slide['id']} Asset Prompt

## Job

{slide['job']}

## Visual Region

`{fmt_box(slide['visual_region'])}`

## Text-Safe Zones

{text_zones}

## Foreground Editable Overlay

{overlays}

## Prompt

{slide['prompt']}

## Negative Prompt

{slide['negative_prompt']}

## QA

{qa}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck_dir", type=Path)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--archetypes", type=Path, default=DEFAULT_ARCHETYPES)
    parser.add_argument("--design-system", type=Path, default=DEFAULT_DESIGN_SYSTEM)
    args = parser.parse_args()

    deck_dir = args.deck_dir.resolve()
    out_dir = (args.out or deck_dir / "asset-prompts").resolve()
    blueprint = read_json(deck_dir / "layout-blueprint.json")
    deck_brief = read_json(deck_dir / "deck-brief.json", {})
    design = read_json(args.design_system.resolve(), {})
    if not isinstance(blueprint, dict):
        raise SystemExit(f"missing or invalid layout blueprint: {deck_dir / 'layout-blueprint.json'}")
    if not isinstance(deck_brief, dict):
        deck_brief = {}
    if not isinstance(design, dict):
        design = {}

    stage = blueprint.get("stage", {})
    if not isinstance(stage, dict) or "width" not in stage or "height" not in stage:
        stage = design.get("stage", {"width": 1280, "height": 720})

    archetypes = archetype_map(args.archetypes.resolve())
    slides = blueprint.get("slides", [])
    if not isinstance(slides, list) or not slides:
        raise SystemExit("layout blueprint has no slides")

    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    plan = {
        "version": 1,
        "deck_dir": str(deck_dir),
        "style_direction": str(deck_brief.get("style_direction") or ""),
        "stage": stage,
        "slides": [],
    }
    for index, raw in enumerate(slides, start=1):
        if not isinstance(raw, dict):
            continue
        slide = make_prompt(
            deck_brief=deck_brief,
            design=design,
            stage=stage,
            slide=merged_slide(raw, archetypes),
        )
        plan["slides"].append(slide)
        file_name = f"{index:02d}-{slide['id']}.md"
        (out_dir / file_name).write_text(markdown_for_slide(slide), encoding="utf-8")

    (out_dir / "asset-prompts.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"asset-prompts-written {out_dir}")
    print(f"asset-prompts-slides {len(plan['slides'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
