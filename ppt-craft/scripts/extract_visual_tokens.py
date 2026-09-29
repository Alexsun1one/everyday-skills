#!/usr/bin/env python3
"""Extract objective visual tokens from oracle/reference slide images."""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageFilter, ImageStat


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def luminance(rgb: tuple[int, int, int]) -> float:
    def channel(value: int) -> float:
        v = value / 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4

    return 0.2126 * channel(rgb[0]) + 0.7152 * channel(rgb[1]) + 0.0722 * channel(rgb[2])


def saturation(rgb: tuple[int, int, int]) -> float:
    values = [value / 255.0 for value in rgb]
    high = max(values)
    low = min(values)
    if high == 0:
        return 0.0
    return (high - low) / high


def role_guess(rgb: tuple[int, int, int]) -> str:
    lum = luminance(rgb)
    sat = saturation(rgb)
    if sat > 0.42 and lum > 0.16:
        return "accent"
    if lum < 0.18:
        return "surface-dark"
    if lum > 0.78:
        return "surface-light"
    if sat < 0.16:
        return "neutral-mid"
    return "support"


def image_metrics(path: Path) -> dict[str, Any]:
    img = Image.open(path).convert("RGB")
    gray = img.convert("L")
    edges = gray.filter(ImageFilter.FIND_EDGES)
    edge_stat = ImageStat.Stat(edges).mean[0] / 255.0
    mean_lum = ImageStat.Stat(gray).mean[0] / 255.0
    width, height = img.size
    return {
        "path": str(path),
        "width": width,
        "height": height,
        "aspect_ratio": round(width / height, 4) if height else 0,
        "mean_luminance": round(mean_lum, 4),
        "edge_density": round(edge_stat, 4),
    }


def thumbnail(path: Path, max_side: int = 360) -> Image.Image:
    img = Image.open(path).convert("RGB")
    img.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    return img.copy()


def extract_palette(paths: list[Path], color_count: int) -> list[dict[str, Any]]:
    thumbs = [thumbnail(path) for path in paths]
    if not thumbs:
        return []
    width = sum(img.width for img in thumbs)
    height = max(img.height for img in thumbs)
    combined = Image.new("RGB", (width, height), (255, 255, 255))
    cursor = 0
    for img in thumbs:
        combined.paste(img, (cursor, 0))
        cursor += img.width

    quantized = combined.quantize(colors=color_count, method=Image.Quantize.MEDIANCUT)
    palette = quantized.getpalette() or []
    counts = quantized.getcolors(maxcolors=color_count * 4096) or []
    total = sum(count for count, _ in counts) or 1
    colors: list[dict[str, Any]] = []
    for count, index in sorted(counts, reverse=True):
        offset = index * 3
        rgb = tuple(int(value) for value in palette[offset : offset + 3])
        if len(rgb) != 3:
            continue
        colors.append(
            {
                "hex": rgb_to_hex(rgb),
                "share": round(count / total, 4),
                "role_guess": role_guess(rgb),
                "luminance": round(luminance(rgb), 4),
                "saturation": round(saturation(rgb), 4),
            }
        )
    return colors


def quantize_channel(value: int, step: int = 16) -> int:
    return max(0, min(255, int(round(value / step) * step)))


def focused_palette(paths: list[Path], *, predicate: Any, limit: int, role: str) -> list[dict[str, Any]]:
    counter: Counter[tuple[int, int, int]] = Counter()
    total_pixels = 0
    selected_pixels = 0
    for path in paths:
        img = thumbnail(path, max_side=520)
        if hasattr(img, "get_flattened_data"):
            pixels = list(img.get_flattened_data())
        else:
            pixels = list(img.getdata())
        total_pixels += len(pixels)
        for rgb in pixels:
            if predicate(rgb):
                bucket = tuple(quantize_channel(int(value)) for value in rgb)
                counter[bucket] += 1
                selected_pixels += 1
    if not counter or not total_pixels:
        return []
    colors: list[dict[str, Any]] = []
    for rgb, count in counter.most_common(limit * 4):
        lum = luminance(rgb)
        sat = saturation(rgb)
        if role == "accent" and sat < 0.25:
            continue
        colors.append(
            {
                "hex": rgb_to_hex(rgb),
                "share": round(count / total_pixels, 4),
                "role_guess": role,
                "luminance": round(lum, 4),
                "saturation": round(sat, 4),
            }
        )
        if len(colors) >= limit:
            break
    return colors


def merged_palette(paths: list[Path], color_count: int) -> list[dict[str, Any]]:
    base = extract_palette(paths, color_count)
    accent = focused_palette(
        paths,
        predicate=lambda rgb: saturation(rgb) > 0.35 and luminance(rgb) > 0.06,
        limit=6,
        role="accent",
    )
    light = focused_palette(
        paths,
        predicate=lambda rgb: luminance(rgb) > 0.62 and saturation(rgb) < 0.45,
        limit=3,
        role="surface-light",
    )
    merged: list[dict[str, Any]] = []
    seen: set[str] = set()
    for color in base + accent + light:
        hex_value = str(color["hex"])
        if hex_value in seen:
            continue
        seen.add(hex_value)
        merged.append(color)
    merged.sort(key=lambda item: (0 if item["role_guess"] == "accent" else 1, -float(item["share"])))
    return merged


def tonal_bands(palette: list[dict[str, Any]]) -> dict[str, list[str]]:
    bands = {"dark": [], "mid": [], "light": [], "accent": []}
    for color in palette:
        hex_value = str(color["hex"])
        lum = float(color.get("luminance") or 0)
        sat = float(color.get("saturation") or 0)
        if color.get("role_guess") == "accent" or (sat > 0.42 and 0.16 < lum < 0.9):
            bands["accent"].append(hex_value)
            continue
        if lum < 0.24:
            bands["dark"].append(hex_value)
        elif lum > 0.74:
            bands["light"].append(hex_value)
        else:
            bands["mid"].append(hex_value)
    return {name: values[:5] for name, values in bands.items()}


def build_tokens(paths: list[Path], args: argparse.Namespace) -> dict[str, Any]:
    palette = merged_palette(paths, args.colors)
    return {
        "version": 1,
        "deck_id": args.deck_id or "",
        "source_images": [image_metrics(path) for path in paths],
        "palette": palette,
        "tonal_bands": tonal_bands(palette),
        "type_system": {
            "title": "Fill from oracle inspection: display face/weight, size band, line-height, title placement.",
            "body": "Fill from oracle inspection: readable body face/weight, size band, line length.",
            "caption": "Fill from oracle inspection: caption and source-note treatment.",
            "numeric": "Fill from oracle inspection: metric/table/chart number style.",
        },
        "layout_grammar": {
            "stage": "16:9 fixed stage; convert oracle composition into layout-blueprint coordinates before rendering.",
            "regions": [
                "Declare title/support/evidence/loop/text-safe zones before final styling.",
                "Keep generated imagery away from text zones unless it creates quiet plates or scrims.",
                "Use varied archetypes across the deck; do not repeat simple left/right or top/bottom splits.",
            ],
            "rhythm": "Alternate cover, proof, system, detail, and closing archetypes while preserving one visual thesis.",
            "negative_space": "Negative space is a reserved design object, not leftover blankness.",
        },
        "text_backplates": [
            "Use plates, strips, scrims, tickets, chips, or plaques whenever text crosses imagery or texture.",
            "Backplates must be part of the blueprint, not last-minute patches.",
        ],
        "object_grammar": [
            "Use native charts/tables/connectors for editable proof slides when route allows.",
            "Use chips, badges, evidence plates, callout leaders, and route loops to avoid flat card walls.",
        ],
        "image_policy": {
            "oracle_usage": "Use generated oracle plates as style targets. Rebuild final slides with editable HTML/PPTX layers unless raster route is chosen.",
            "text_policy": "For editable/hybrid decks, important final language must be external editable text even if the oracle image used baked text for exploration.",
        },
        "qa_rules": [
            "visual_qa_deck.py must pass with warning-blocking behavior.",
            "For serious decks, visual_qa_deck.py --require-blueprint-zones must pass.",
            "No meaningful text may sit outside declared text-safe zones.",
            "No important text may sit directly on busy image texture without a plate, strip, scrim, ticket, or quiet field.",
            "Similarity warnings require archetype/object-grammar repair or an explicit delivery waiver.",
        ],
        "forbidden_drift": [
            "Generic purple SaaS gradient",
            "Repeated card wall",
            "Raw text over busy image",
            "Fake tiny image text",
            "Only left/right or top/bottom layouts",
        ],
        "notes": args.notes or "",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("images", type=Path, nargs="+", help="Oracle/reference slide images")
    parser.add_argument("--out", type=Path, required=True, help="Output visual-tokens.json")
    parser.add_argument("--deck-id", default="")
    parser.add_argument("--notes", default="")
    parser.add_argument("--colors", type=int, default=12)
    args = parser.parse_args()

    images = [path.resolve() for path in args.images]
    missing = [path for path in images if not path.exists()]
    if missing:
        raise SystemExit(f"missing image(s): {', '.join(str(path) for path in missing)}")
    if args.colors < 4 or args.colors > 32:
        raise SystemExit("--colors must be between 4 and 32")

    tokens = build_tokens(images, args)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(tokens, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"visual-tokens-written {args.out}")
    print(
        "visual-token-summary "
        f"images={len(images)} colors={len(tokens['palette'])} "
        f"mean_luminance={round(sum(item['mean_luminance'] for item in tokens['source_images']) / len(images), 4)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
