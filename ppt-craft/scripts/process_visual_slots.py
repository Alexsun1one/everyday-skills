#!/usr/bin/env python3
"""Prepare planned visual slot assets from a relationship-graph.json contract."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover - dependency check is runtime-facing.
    raise SystemExit("Pillow is required for visual slot processing. Install pillow in the active Python environment.") from exc


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"expected JSON object: {path}")
    return data


def resolve_path(base: Path, value: str | None) -> Path | None:
    if not value:
        return None
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = base / path
    return path


def truthy(value: Any) -> bool:
    return value is True or str(value).lower() == "true"


def as_box(value: Any) -> dict[str, float] | None:
    if not isinstance(value, dict):
        return None
    if not all(isinstance(value.get(key), (int, float)) for key in ("x", "y", "w", "h")):
        return None
    if float(value["w"]) <= 0 or float(value["h"]) <= 0:
        return None
    return {key: float(value[key]) for key in ("x", "y", "w", "h")}


def pixel_crop_box(crop: dict[str, float] | None, image_size: tuple[int, int]) -> tuple[int, int, int, int]:
    w, h = image_size
    if not crop:
        return (0, 0, w, h)
    x = crop["x"] * w if 0 <= crop["x"] <= 1 else crop["x"]
    y = crop["y"] * h if 0 <= crop["y"] <= 1 else crop["y"]
    cw = crop["w"] * w if 0 < crop["w"] <= 1 else crop["w"]
    ch = crop["h"] * h if 0 < crop["h"] <= 1 else crop["h"]
    left = max(0, min(w - 1, int(round(x))))
    top = max(0, min(h - 1, int(round(y))))
    right = max(left + 1, min(w, int(round(x + cw))))
    bottom = max(top + 1, min(h, int(round(y + ch))))
    return (left, top, right, bottom)


def infer_output_size(slot: dict[str, Any], slot_box: dict[str, float] | None, source_size: tuple[int, int]) -> tuple[int, int]:
    configured = slot.get("output_size") or slot.get("asset_size")
    if isinstance(configured, dict) and isinstance(configured.get("w"), (int, float)) and isinstance(configured.get("h"), (int, float)):
        return max(1, int(configured["w"])), max(1, int(configured["h"]))
    if isinstance(configured, list) and len(configured) >= 2:
        try:
            return max(1, int(configured[0])), max(1, int(configured[1]))
        except (TypeError, ValueError):
            pass
    if slot_box:
        ratio = slot_box["h"] / slot_box["w"] if slot_box["w"] else 9 / 16
        width = int(slot.get("output_width") or 640)
        height = int(round(width * ratio))
        return width, max(120, min(720, height))
    return source_size


def fit_image(image: Image.Image, size: tuple[int, int], fit: str, background: tuple[int, int, int, int]) -> Image.Image:
    target_w, target_h = size
    image = image.convert("RGBA")
    if fit == "fill":
        return image.resize(size, Image.Resampling.LANCZOS)

    src_w, src_h = image.size
    if src_w <= 0 or src_h <= 0:
        return Image.new("RGBA", size, background)

    if fit == "cover":
        scale = max(target_w / src_w, target_h / src_h)
        resized = image.resize((max(1, int(math.ceil(src_w * scale))), max(1, int(math.ceil(src_h * scale)))), Image.Resampling.LANCZOS)
        left = max(0, (resized.width - target_w) // 2)
        top = max(0, (resized.height - target_h) // 2)
        return resized.crop((left, top, left + target_w, top + target_h))

    if fit == "scale-down" and src_w <= target_w and src_h <= target_h:
        resized = image
    else:
        scale = min(target_w / src_w, target_h / src_h)
        resized = image.resize((max(1, int(src_w * scale)), max(1, int(src_h * scale))), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", size, background)
    canvas.alpha_composite(resized, ((target_w - resized.width) // 2, (target_h - resized.height) // 2))
    return canvas


def apply_transparency(image: Image.Image, slot: dict[str, Any]) -> Image.Image:
    image = image.convert("RGBA")
    threshold = float(slot.get("transparent_threshold") or 42)
    chroma_threshold = float(slot.get("transparent_chroma") or 42)
    softness = float(slot.get("transparent_softness") or 22)
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
            chroma = max(r, g, b) - min(r, g, b)
            if luminance <= threshold and chroma <= chroma_threshold:
                pixels[x, y] = (r, g, b, 0)
            elif luminance <= threshold + softness and chroma <= chroma_threshold + softness:
                fade = (luminance - threshold) / max(1.0, softness)
                pixels[x, y] = (r, g, b, int(a * max(0.18, min(1.0, fade))))
    return image


def iter_visual_slots(graph: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    slots: list[tuple[str, dict[str, Any]]] = []
    views = graph.get("views")
    if isinstance(views, list):
        for view in views:
            if not isinstance(view, dict):
                continue
            view_id = str(view.get("id") or "view")
            for slot in view.get("visual_slots", []) or []:
                if isinstance(slot, dict):
                    slots.append((view_id, slot))
    for slot in graph.get("visual_slots", []) or []:
        if isinstance(slot, dict):
            slots.append(("graph", slot))
    return slots


def process(deck_dir: Path, graph_path: Path, report_path: Path) -> dict[str, Any]:
    graph = read_json(graph_path)
    deck_dir = deck_dir.resolve()
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    prepared = 0
    pending = 0

    for view_id, slot in iter_visual_slots(graph):
        slot_id = str(slot.get("id") or f"{view_id}-slot")
        slot_box = as_box(slot.get("box"))
        source = resolve_path(deck_dir, str(slot.get("source") or slot.get("source_image") or "").strip() or None)
        src = resolve_path(deck_dir, str(slot.get("src") or "").strip() or None)
        out = resolve_path(deck_dir, str(slot.get("out") or slot.get("asset_out") or "").strip() or None) or src
        if source and not source.exists():
            errors.append(f"{view_id}:{slot_id}: source not found: {source}")
            records.append({"view": view_id, "slot": slot_id, "status": "error", "error": "source not found", "source": str(source)})
            continue
        if not source:
            exists = bool(src and src.exists())
            records.append({
                "view": view_id,
                "slot": slot_id,
                "status": "existing" if exists else "pending",
                "src": str(src) if src else "",
                "prompt": str(slot.get("prompt") or ""),
            })
            pending += 0 if exists else 1
            continue
        if not out:
            out = deck_dir / "assets" / f"{view_id}-{slot_id}.png"
        out.parent.mkdir(parents=True, exist_ok=True)

        crop = as_box(slot.get("crop_box") or slot.get("source_crop"))
        fit = str(slot.get("fit") or "cover")
        if fit not in {"cover", "contain", "fill", "scale-down"}:
            fit = "cover"
        try:
            source_image = Image.open(source)
            crop_box = pixel_crop_box(crop, source_image.size)
            cropped = source_image.convert("RGBA").crop(crop_box)
            background = (5, 11, 18, 0 if truthy(slot.get("transparent")) else 255)
            fitted = fit_image(cropped, infer_output_size(slot, slot_box, cropped.size), fit, background)
            if truthy(slot.get("transparent")):
                fitted = apply_transparency(fitted, slot)
            save_format = "PNG" if out.suffix.lower() in {"", ".png"} or truthy(slot.get("transparent")) else None
            if not out.suffix:
                out = out.with_suffix(".png")
            fitted.save(out, format=save_format)
            prepared += 1
            records.append({
                "view": view_id,
                "slot": slot_id,
                "status": "prepared",
                "source": str(source),
                "out": str(out),
                "crop_box": {"left": crop_box[0], "top": crop_box[1], "right": crop_box[2], "bottom": crop_box[3]},
                "size": {"w": fitted.width, "h": fitted.height},
                "transparent": truthy(slot.get("transparent")),
                "fit": fit,
            })
        except Exception as exc:  # pragma: no cover - report runtime asset failures.
            errors.append(f"{view_id}:{slot_id}: {exc}")
            records.append({"view": view_id, "slot": slot_id, "status": "error", "error": str(exc)})

    report = {
        "ok": not errors,
        "deck": str(deck_dir),
        "graph": str(graph_path),
        "prepared": prepared,
        "pending": pending,
        "errors": errors,
        "slots": records,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path = report_path.with_suffix(".md")
    lines = [
        "# Visual Slots Report",
        "",
        f"- deck: `{deck_dir}`",
        f"- prepared: {prepared}",
        f"- pending: {pending}",
        f"- errors: {len(errors)}",
        "",
    ]
    for record in records:
        lines.append(f"- `{record['view']}/{record['slot']}`: {record['status']}")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck", type=Path, help="Deck directory containing relationship-graph.json")
    parser.add_argument("--graph", type=Path, help="Graph JSON path. Defaults to deck/relationship-graph.json")
    parser.add_argument("--report", type=Path, help="Report path. Defaults to deck/asset-prompts/visual-slots-report.json")
    args = parser.parse_args()

    deck_dir = args.deck.resolve()
    graph_path = (args.graph or (deck_dir / "relationship-graph.json")).resolve()
    report_path = (args.report or (deck_dir / "asset-prompts" / "visual-slots-report.json")).resolve()
    report = process(deck_dir, graph_path, report_path)
    if report["ok"]:
        print(f"visual-slots-ok prepared={report['prepared']} pending={report['pending']} report={report_path}")
        return 0
    print(f"visual-slots-failed errors={len(report['errors'])} report={report_path}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
