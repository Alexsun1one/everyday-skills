#!/usr/bin/env python3
"""Select local PPT Craft style anchors."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / "assets" / "style-anchor-library.json"


def tokens(value: str) -> list[str]:
    return [t for t in re.split(r"[^a-z0-9\u4e00-\u9fff]+", value.lower()) if t]


def load_library(path: Path = LIBRARY) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def anchor_text(anchor: dict) -> str:
    parts = [
        anchor.get("id", ""),
        anchor.get("name", ""),
        anchor.get("visual_thesis", ""),
        anchor.get("typography", ""),
        anchor.get("layout_grammar", ""),
        anchor.get("motion", ""),
        " ".join(anchor.get("deck_types", [])),
        " ".join(anchor.get("industries", [])),
        " ".join(anchor.get("style_tags", [])),
        " ".join(anchor.get("slide_archetypes", [])),
    ]
    return " ".join(parts).lower()


def score_anchor(anchor: dict, query_tokens: list[str], filters: dict[str, str]) -> tuple[int, list[str]]:
    haystack = anchor_text(anchor)
    score = 0
    reasons: list[str] = []

    for token in query_tokens:
        if token in haystack:
            score += 2
            reasons.append(token)

    for key, field in (
        ("deck_type", "deck_types"),
        ("industry", "industries"),
        ("style", "style_tags"),
    ):
        value = filters.get(key)
        if not value:
            continue
        value_tokens = tokens(value)
        field_text = " ".join(anchor.get(field, [])).lower()
        matched = [t for t in value_tokens if t in field_text or t in haystack]
        if matched:
            score += 5
            reasons.extend(matched)

    if anchor.get("route") == "html-first":
        score += 1

    return score, sorted(set(reasons))


def select(library: dict, query: str, deck_type: str, industry: str, style: str, limit: int) -> list[dict]:
    query_tokens = tokens(" ".join(v for v in [query, deck_type, industry, style] if v))
    filters = {"deck_type": deck_type, "industry": industry, "style": style}
    ranked = []
    for anchor in library.get("anchors", []):
        score, reasons = score_anchor(anchor, query_tokens, filters)
        ranked.append((score, reasons, anchor))
    ranked.sort(key=lambda item: (item[0], item[2].get("name", "")), reverse=True)
    return [
        {
            "score": score,
            "matched": reasons,
            "anchor": anchor,
        }
        for score, reasons, anchor in ranked[:limit]
    ]


def render_markdown(results: list[dict], library: dict) -> str:
    lines = [
        f"default_route: {library.get('default_route', 'html-first')}",
        "",
    ]
    for i, item in enumerate(results, 1):
        anchor = item["anchor"]
        palette = anchor.get("palette", {})
        lines.extend(
            [
                f"## {i}. {anchor['name']} (`{anchor['id']}`)",
                f"- score: {item['score']} ({', '.join(item['matched']) or 'default fit'})",
                f"- route: {anchor.get('route', 'html-first')}",
                f"- best for: {', '.join(anchor.get('deck_types', []))}",
                f"- style tags: {', '.join(anchor.get('style_tags', []))}",
                f"- visual thesis: {anchor.get('visual_thesis', '')}",
                f"- palette: {', '.join(f'{k}={v}' for k, v in palette.items())}",
                f"- typography: {anchor.get('typography', '')}",
                f"- layout grammar: {anchor.get('layout_grammar', '')}",
                f"- slide archetypes: {', '.join(anchor.get('slide_archetypes', []))}",
                f"- starter preview: `python3 scripts/render_style_anchor_starters.py --anchor {anchor['id']} --out /tmp/ppt-craft-{anchor['id']}-starter`",
                f"- HTML-first notes: {anchor.get('html_first_notes', '')}",
                f"- avoid: {', '.join(anchor.get('avoid', []))}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", default="", help="Free-form deck intent/style query")
    parser.add_argument("--deck-type", default="", help="pitch/report/keynote/training/etc.")
    parser.add_argument("--industry", default="", help="ai/healthcare/finance/etc.")
    parser.add_argument("--style", default="", help="dark/premium/editorial/calm/etc.")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--library", type=Path, default=LIBRARY)
    args = parser.parse_args()

    library = load_library(args.library)
    results = select(library, args.query, args.deck_type, args.industry, args.style, args.limit)

    if args.format == "json":
        json.dump({"default_route": library.get("default_route"), "results": results}, sys.stdout, ensure_ascii=False, indent=2)
        print()
    else:
        print(render_markdown(results, library), end="")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
