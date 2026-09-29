#!/usr/bin/env python3
"""Render a low-fidelity HTML skeleton deck from PPT Craft system artifacts."""

from __future__ import annotations

import argparse
import html
import json
import shutil
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_ARCHETYPES = SKILL_DIR / "assets" / "layout-archetypes.json"
DEFAULT_DESIGN_SYSTEM = SKILL_DIR / "assets" / "slide-design-system.json"
BOX_ORDER = ("mask", "claim", "support", "visual", "evidence", "loop")
BOX_TITLES = {
    "mask": "contrast mask",
    "claim": "primary claim",
    "support": "supporting copy",
    "visual": "visual subject",
    "evidence": "evidence object",
    "loop": "loop / path",
}
BOX_CLASSES = {
    "mask": "box-mask",
    "claim": "box-claim",
    "support": "box-support",
    "visual": "box-visual",
    "evidence": "box-evidence",
    "loop": "box-loop",
}
TYPE_ROLES = {
    "claim": "title_line",
    "support": "body",
    "visual": "caption",
    "evidence": "table",
    "loop": "label",
    "mask": "micro",
}
PLATE_RULES = {
    "claim": "plate: quiet field or strong title card",
    "support": "plate: paper card / caption band",
    "visual": "asset: visual subject only; avoid text zones",
    "evidence": "plate: evidence table/chart card",
    "loop": "objects: route chips + connectors",
    "mask": "quiet field: generated image must stay low-detail here",
}
OBJECT_FAMILIES = {
    "claim": "paper-card, dark-strip, receipt title",
    "support": "paper-card, caption-band",
    "visual": "image subject, blank plaques, magnifier window",
    "evidence": "table plate, chart plate, evidence drawer",
    "loop": "route-chip, number-badge, loop-connector",
    "mask": "contrast mask / quiet surface",
}


def read_json(path: Path, fallback: Any = None) -> Any:
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def slug_name(index: int, slide_id: str) -> str:
    clean = "".join(ch if ch.isalnum() or ch in ("-", "_") else "-" for ch in slide_id.strip().lower())
    clean = "-".join(part for part in clean.split("-") if part)
    return f"{index:02d}-{clean or 'slide'}"


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


def style_for_box(box: dict[str, Any]) -> str:
    return (
        f"left:{box['x']}px;top:{box['y']}px;"
        f"width:{box['w']}px;height:{box['h']}px;"
    )


def type_role_text(kind: str, design: dict[str, Any]) -> str:
    role = TYPE_ROLES.get(kind, "body")
    scale = design.get("type_scale", {}) if isinstance(design, dict) else {}
    token = scale.get(role, {}) if isinstance(scale, dict) else {}
    size = token.get("size", "?") if isinstance(token, dict) else "?"
    weight = token.get("weight", "?") if isinstance(token, dict) else "?"
    return f"type: {role} / {size}px / weight {weight}"


def box_html(kind: str, box: dict[str, Any], slide: dict[str, Any], design: dict[str, Any]) -> str:
    title = BOX_TITLES.get(kind, kind)
    label = ""
    if kind == "claim":
        label = str(slide.get("job") or "Slide claim")
    elif kind == "support":
        label = "one supporting sentence or short paragraph"
    elif kind == "visual":
        label = str(slide.get("_archetype_name") or "visual system")
    elif kind == "evidence":
        label = "table / chart / proof object"
    elif kind == "loop":
        label = "ordered loop, path, or active state"
    elif kind == "mask":
        opacity = box.get("opacity", "")
        label = f"quiet field opacity {opacity}" if opacity != "" else "quiet field"
    role = type_role_text(kind, design)
    plate = PLATE_RULES.get(kind, "plate required")
    objects = OBJECT_FAMILIES.get(kind, "foreground objects")
    return (
        f'<div class="slot {BOX_CLASSES.get(kind, "")}" style="{style_for_box(box)}">'
        f'<div class="slot-title">{html.escape(title)}</div>'
        f'<div class="slot-label">{html.escape(label)}</div>'
        f'<div class="slot-meta">{html.escape(role)}</div>'
        f'<div class="slot-rule">{html.escape(plate)}</div>'
        f'<div class="slot-objects">{html.escape(objects)}</div>'
        "</div>"
    )


def slide_html(slide: dict[str, Any], stage: dict[str, Any], index: int, total: int, design: dict[str, Any]) -> str:
    slide_id = str(slide.get("id") or f"slide-{index}")
    archetype = str(slide.get("archetype") or "custom")
    job = str(slide.get("job") or "")
    safe = stage.get("safe", {"x": 64, "y": 56, "w": 1152, "h": 608})
    boxes = []
    for kind in BOX_ORDER:
        box = slide.get(kind)
        if isinstance(box, dict) and all(key in box for key in ("x", "y", "w", "h")):
            boxes.append(box_html(kind, box, slide, design))
    if not boxes:
        boxes.append('<div class="warning">No layout boxes found.</div>')

    empty = slide.get("empty", [])
    empty_html = ""
    if isinstance(empty, list) and empty:
        items = "".join(f"<li>{html.escape(str(item))}</li>" for item in empty[:3])
        empty_html = f'<ul class="empty-list">{items}</ul>'
    font_stack = ""
    if isinstance(design, dict):
        fonts = design.get("font_stack", {})
        if isinstance(fonts, dict):
            font_stack = str(fonts.get("zh_display") or "")
    design_note = "Skeleton contract: type roles + plates + asset text-safe zones are mandatory."

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(slide_id)}</title>
  <style>
    * {{ box-sizing: border-box; }}
    html, body {{ margin:0; width:{stage['width']}px; height:{stage['height']}px; overflow:hidden; background:#080b10; color:#e5edf8; font-family:"PingFang SC","Microsoft YaHei",Arial,sans-serif; }}
    .slide {{ position:relative; width:{stage['width']}px; height:{stage['height']}px; overflow:hidden; background:#080b10; }}
    .grid {{ position:absolute; inset:0; background-image:linear-gradient(rgba(148,163,184,.08) 1px, transparent 1px),linear-gradient(90deg, rgba(148,163,184,.08) 1px, transparent 1px); background-size:40px 40px; }}
    .safe {{ position:absolute; left:{safe['x']}px; top:{safe['y']}px; width:{safe['w']}px; height:{safe['h']}px; border:1px dashed rgba(148,163,184,.45); border-radius:10px; }}
    .meta {{ position:absolute; left:30px; top:24px; right:30px; display:flex; justify-content:space-between; gap:20px; color:#f2c96d; font-size:12px; font-weight:800; letter-spacing:0; }}
    .job {{ position:absolute; left:30px; bottom:24px; right:30px; color:#94a3b8; font-size:13px; line-height:1.35; }}
    .slot {{ position:absolute; border:2px solid rgba(148,163,184,.7); border-radius:10px; background:rgba(15,23,42,.48); padding:12px; overflow:hidden; }}
    .slot-title {{ color:#fff; font-size:15px; font-weight:820; line-height:1; }}
    .slot-label {{ margin-top:10px; color:#cbd5e1; font-size:18px; line-height:1.2; max-width:92%; }}
    .slot-meta {{ position:absolute; left:12px; right:12px; bottom:48px; color:#f8d98a; font-size:11px; line-height:1.25; font-weight:800; }}
    .slot-rule {{ position:absolute; left:12px; right:12px; bottom:27px; color:#bae6fd; font-size:11px; line-height:1.2; font-weight:760; }}
    .slot-objects {{ position:absolute; left:12px; right:12px; bottom:10px; color:#a7f3d0; font-size:10px; line-height:1.15; font-weight:700; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
    .box-mask {{ border-color:rgba(148,163,184,.22); background:rgba(15,23,42,.32); }}
    .box-mask .slot-title, .box-mask .slot-label {{ color:rgba(203,213,225,.58); }}
    .box-claim {{ border-color:#f2c96d; background:rgba(55,37,8,.36); }}
    .box-support {{ border-color:#94a3b8; background:rgba(30,41,59,.44); }}
    .box-visual {{ border-color:#38bdf8; background:rgba(8,47,73,.42); }}
    .box-evidence {{ border-color:#5eead4; background:rgba(20,83,45,.28); }}
    .box-loop {{ border-color:#a78bfa; background:rgba(76,29,149,.24); }}
    .empty-list {{ position:absolute; left:30px; bottom:68px; max-width:520px; margin:0; padding-left:18px; color:#64748b; font-size:11px; line-height:1.35; }}
    .design-note {{ position:absolute; right:30px; bottom:52px; max-width:560px; color:#64748b; font-size:11px; line-height:1.35; text-align:right; }}
    .font-note {{ position:absolute; right:30px; bottom:24px; max-width:620px; color:#475569; font-size:10px; line-height:1.2; text-align:right; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
    .warning {{ position:absolute; left:80px; top:120px; color:#fca5a5; }}
  </style>
</head>
<body>
  <main class="slide">
    <div class="grid"></div>
    <div class="safe"></div>
    <div class="meta"><span>{index:02d}/{total:02d} {html.escape(slide_id)}</span><span>{html.escape(archetype)}</span></div>
    {"".join(boxes)}
    {empty_html}
    <div class="design-note">{html.escape(design_note)}</div>
    <div class="font-note">{html.escape(font_stack)}</div>
    <div class="job">{html.escape(job)}</div>
  </main>
</body>
</html>
"""


def index_html(title: str, slides: list[tuple[str, str]], stage: dict[str, Any]) -> str:
    manifest = ",\n      ".join(
        f'{{ file: "slides/{html.escape(file)}", label: "{html.escape(label)}" }}' for file, label in slides
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} Skeleton</title>
  <style>
    * {{ box-sizing:border-box; }}
    html, body {{ margin:0; width:100%; min-height:100%; background:#05070d; color:#e5edf8; font-family:"PingFang SC","Microsoft YaHei",Arial,sans-serif; }}
    .wrap {{ padding:28px; }}
    h1 {{ margin:0 0 18px; font-size:28px; line-height:1.1; }}
    .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(360px,1fr)); gap:20px; }}
    .card {{ border:1px solid rgba(148,163,184,.28); border-radius:10px; background:#0b1120; overflow:hidden; }}
    iframe {{ display:block; width:100%; aspect-ratio:{stage['width']} / {stage['height']}; border:0; background:#080b10; }}
    .label {{ padding:10px 12px; color:#f2c96d; font-size:13px; font-weight:800; }}
  </style>
  <script>
    window.DECK_TITLE = {json.dumps(title + " Skeleton", ensure_ascii=False)};
    window.DECK_MANIFEST = [
      {manifest}
    ];
  </script>
</head>
<body>
  <main class="wrap">
    <h1>{html.escape(title)} Skeleton</h1>
    <section class="grid">
      {''.join(f'<article class="card"><iframe src="slides/{html.escape(file)}" title="{html.escape(label)}"></iframe><div class="label">{html.escape(label)}</div></article>' for file, label in slides)}
    </section>
  </main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck_dir", type=Path)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--archetypes", type=Path, default=DEFAULT_ARCHETYPES)
    parser.add_argument("--design-system", type=Path, default=DEFAULT_DESIGN_SYSTEM)
    args = parser.parse_args()

    deck_dir = args.deck_dir.resolve()
    out_dir = (args.out or (deck_dir / "skeleton")).resolve()
    blueprint_path = deck_dir / "layout-blueprint.json"
    blueprint = read_json(blueprint_path)
    if not isinstance(blueprint, dict):
        raise SystemExit(f"missing or invalid layout blueprint: {blueprint_path}")

    stage = blueprint.get("stage", {})
    if not isinstance(stage, dict) or "width" not in stage or "height" not in stage:
        raise SystemExit("layout blueprint missing stage.width/stage.height")
    if "safe" not in stage:
        stage["safe"] = {"x": 64, "y": 56, "w": stage["width"] - 128, "h": stage["height"] - 112}

    slides = blueprint.get("slides", [])
    if not isinstance(slides, list) or not slides:
        raise SystemExit("layout blueprint has no slides")

    deck_brief = read_json(deck_dir / "deck-brief.json", {})
    title = "PPT Craft"
    if isinstance(deck_brief, dict):
        title = str(deck_brief.get("deck_job") or deck_brief.get("style_direction") or title)
        if len(title) > 80:
            title = title[:77] + "..."

    archetypes = archetype_map(args.archetypes.resolve())
    design = read_json(args.design_system.resolve(), {})
    if not isinstance(design, dict):
        design = {}
    if out_dir.exists():
        shutil.rmtree(out_dir)
    (out_dir / "slides").mkdir(parents=True, exist_ok=True)

    if (deck_dir / "deck-brief.json").exists():
        shutil.copy2(deck_dir / "deck-brief.json", out_dir / "deck-brief.json")
    shutil.copy2(blueprint_path, out_dir / "layout-blueprint.json")

    manifest: list[tuple[str, str]] = []
    total = len(slides)
    for index, raw in enumerate(slides, start=1):
        if not isinstance(raw, dict):
            continue
        slide = merged_slide(raw, archetypes)
        slide_id = str(slide.get("id") or f"slide-{index}")
        file = f"{slug_name(index, slide_id)}.html"
        (out_dir / "slides" / file).write_text(slide_html(slide, stage, index, total, design), encoding="utf-8")
        manifest.append((file, slide_id))

    (out_dir / "index.html").write_text(index_html(title, manifest, stage), encoding="utf-8")
    print(f"skeleton-deck-written {out_dir}")
    print(f"skeleton-slides {len(manifest)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
