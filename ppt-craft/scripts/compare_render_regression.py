#!/usr/bin/env python3
"""Compare browser HTML screenshots against LibreOffice-rendered PPTX pages."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageStat

SCRIPT_DIR = Path(__file__).resolve().parent

THRESHOLD_KEYS = (
    "mean_warning",
    "mean_error",
    "changed_warning",
    "changed_error",
    "edge_warning",
    "edge_error",
)

DEFAULT_THRESHOLDS = {
    "mean_warning": 0.08,
    "mean_error": 0.16,
    "changed_warning": 0.32,
    "changed_error": 0.58,
    "edge_warning": 0.12,
    "edge_error": 0.22,
}


def natural_key(path: Path) -> list[Any]:
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", path.stem)]


def is_slide_png(path: Path) -> bool:
    name = path.name.lower()
    if path.suffix.lower() != ".png":
        return False
    blocked = ("index", "contact", "diff", "compare", "heat", "report")
    return not any(token in name for token in blocked)


def collect_pngs(folder: Path) -> list[Path]:
    if not folder.exists():
        raise SystemExit(f"folder does not exist: {folder}")
    return sorted((path for path in folder.glob("*.png") if is_slide_png(path)), key=natural_key)


def collect_lo_pngs(folder: Path) -> list[Path]:
    report_path = folder / "libreoffice-render-report.json"
    if report_path.exists():
        try:
            report = json.loads(report_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            report = {}
        png_pages = report.get("png_pages")
        if isinstance(png_pages, list) and png_pages:
            files = [Path(str(path)).expanduser() for path in png_pages]
            files = [path if path.is_absolute() else folder / path for path in files]
            existing = [path for path in files if path.exists()]
            if len(existing) == len(files):
                return existing
    return collect_pngs(folder)


def choose_lo_dir(deck: Path) -> Path:
    candidates = [
        deck / "qa" / "libreoffice-render-script",
        deck / "qa" / "libreoffice-render",
        deck / "qa" / "libreoffice-render-pages",
    ]
    for candidate in candidates:
        if candidate.exists() and collect_lo_pngs(candidate):
            return candidate
    raise SystemExit("could not find LibreOffice PNG pages; pass --lo-dir")


def load_threshold_config(path: Path) -> dict[str, Any]:
    config: dict[str, Any] = {
        "version": 1,
        "default_profile": "default",
        "profiles": {"default": dict(DEFAULT_THRESHOLDS)},
        "aliases": {},
    }
    if path.exists():
        try:
            loaded = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"invalid threshold profile JSON: {path}: {exc}") from exc
        if isinstance(loaded, dict):
            config.update(loaded)
    profiles = config.setdefault("profiles", {})
    if "default" not in profiles:
        profiles["default"] = dict(DEFAULT_THRESHOLDS)
    for name, profile in list(profiles.items()):
        if not isinstance(profile, dict):
            raise SystemExit(f"threshold profile is not an object: {name}")
        merged = dict(DEFAULT_THRESHOLDS)
        merged.update({key: float(profile[key]) for key in THRESHOLD_KEYS if key in profile})
        profiles[name] = merged
    config.setdefault("aliases", {})
    return config


def normalize_profile(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_") or "default"


def infer_deck_type(deck: Path) -> str:
    brief_path = deck / "deck-brief.json"
    if not brief_path.exists():
        return "default"
    try:
        brief = json.loads(brief_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return "default"
    parts: list[str] = []
    for key in ("audience", "deck_job", "route", "density", "language", "style_direction"):
        value = brief.get(key)
        if isinstance(value, str):
            parts.append(value)
    for key in ("style_anchors", "must_keep", "user_decisions", "assumptions", "risks"):
        value = brief.get(key)
        if isinstance(value, list):
            parts.append(json.dumps(value, ensure_ascii=False))
    text = " ".join(parts).lower()
    if any(token in text for token in ("investor", "pitch", "fundraising", "pre-a", "seed", "融资", "路演", "投资人")):
        return "investor"
    if any(token in text for token in ("consulting", "strategy", "mckinsey", "bain", "bcg", "战略", "咨询")):
        return "consulting"
    if any(token in text for token in ("product keynote", "keynote", "launch", "demo", "产品发布", "发布会", "演示")):
        return "product"
    if any(token in text for token in ("report", "research", "policy", "board", "clinical", "报告", "研究", "汇报")):
        return "report"
    if any(token in text for token in ("training", "course", "lesson", "workshop", "课件", "培训", "课程")):
        return "training"
    if any(token in text for token in ("raster", "image deck", "social", "card", "图片", "卡片", "海报")):
        return "raster"
    return "default"


def resolve_threshold_profile(deck: Path, requested: str, config: dict[str, Any]) -> tuple[str, str, dict[str, float]]:
    inferred = infer_deck_type(deck) if requested == "auto" else requested
    normalized = normalize_profile(inferred)
    aliases = {normalize_profile(str(key)): normalize_profile(str(value)) for key, value in config.get("aliases", {}).items()}
    profile_name = aliases.get(normalized, normalized)
    profiles = config.get("profiles", {})
    if profile_name not in profiles:
        profile_name = str(config.get("default_profile") or "default")
    if profile_name not in profiles:
        profile_name = "default"
    thresholds = dict(profiles[profile_name])
    return inferred, profile_name, thresholds


def mean_from_hist(hist: list[int]) -> float:
    total = sum(hist)
    if not total:
        return 0.0
    return sum(index * count for index, count in enumerate(hist)) / (255.0 * total)


def quantile_from_hist(hist: list[int], q: float) -> float:
    total = sum(hist)
    if not total:
        return 0.0
    threshold = total * q
    seen = 0
    for index, count in enumerate(hist):
        seen += count
        if seen >= threshold:
            return index / 255.0
    return 1.0


def changed_ratio(hist: list[int], threshold: int) -> float:
    total = sum(hist)
    if not total:
        return 0.0
    return sum(hist[threshold:]) / total


def edge_image(image: Image.Image) -> Image.Image:
    return image.convert("L").filter(ImageFilter.FIND_EDGES)


def compare_pair(html_path: Path, lo_path: Path, *, width: int, out_dir: Path, index: int) -> dict[str, Any]:
    html = Image.open(html_path).convert("RGB")
    lo = Image.open(lo_path).convert("RGB")
    target_w = width
    target_h = int(round(width * 9 / 16))
    size = (target_w, target_h)
    html_fit = html.resize(size, Image.Resampling.LANCZOS)
    lo_fit = lo.resize(size, Image.Resampling.LANCZOS)

    diff = ImageChops.difference(html_fit, lo_fit)
    diff_gray = diff.convert("L")
    diff_hist = diff_gray.histogram()
    mean_delta = mean_from_hist(diff_hist)
    p95_delta = quantile_from_hist(diff_hist, 0.95)
    changed = changed_ratio(diff_hist, 26)

    html_edge = edge_image(html_fit)
    lo_edge = edge_image(lo_fit)
    edge_diff = ImageChops.difference(html_edge, lo_edge)
    edge_delta = mean_from_hist(edge_diff.histogram())

    html_luma = html_fit.convert("L")
    lo_luma = lo_fit.convert("L")
    luma_delta = mean_from_hist(ImageChops.difference(html_luma, lo_luma).histogram())

    heat = diff_gray.point(lambda value: min(255, value * 4)).convert("RGB")
    heat_pixels = heat.load()
    for y in range(heat.height):
        for x in range(heat.width):
            value = heat_pixels[x, y][0]
            heat_pixels[x, y] = (value, max(0, value // 4), max(0, 120 - value // 3))

    label_h = 26
    pad = 18
    compare = Image.new("RGB", (target_w * 3 + pad * 4, target_h + label_h + pad * 2), "#05070d")
    draw = ImageDraw.Draw(compare)
    labels = [
        f"HTML: {html_path.stem}",
        f"LibreOffice: {lo_path.stem}",
        f"Diff heat mean={mean_delta:.3f}",
    ]
    images = [html_fit, lo_fit, heat]
    for col, (label, image) in enumerate(zip(labels, images, strict=True)):
        x = pad + col * (target_w + pad)
        draw.text((x, pad), label, fill="#f2c96d")
        compare.paste(image, (x, pad + label_h))

    out_dir.mkdir(parents=True, exist_ok=True)
    compare_path = out_dir / f"render-diff-{index:02d}.png"
    heat_path = out_dir / f"render-heat-{index:02d}.png"
    compare.save(compare_path)
    heat.save(heat_path)

    return {
        "index": index,
        "html": str(html_path),
        "libreoffice": str(lo_path),
        "compare": str(compare_path),
        "heat": str(heat_path),
        "html_size": {"w": html.width, "h": html.height},
        "libreoffice_size": {"w": lo.width, "h": lo.height},
        "mean_delta": round(mean_delta, 5),
        "p95_delta": round(p95_delta, 5),
        "changed_ratio": round(changed, 5),
        "edge_delta": round(edge_delta, 5),
        "luma_delta": round(luma_delta, 5),
    }


def make_contact_sheet(files: list[Path], out: Path, thumb_width: int = 560) -> None:
    if not files:
        return
    first = Image.open(files[0])
    ratio = first.height / first.width
    thumb_w = thumb_width
    thumb_h = int(round(thumb_w * ratio))
    cols = 1
    rows = len(files)
    pad = 24
    label_h = 26
    sheet = Image.new("RGB", (thumb_w + pad * 2, rows * (thumb_h + label_h) + (rows + 1) * pad), "#05070d")
    draw = ImageDraw.Draw(sheet)
    for row, path in enumerate(files):
        img = Image.open(path).convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        x = pad
        y = pad + row * (thumb_h + label_h + pad)
        draw.text((x, y), path.stem, fill="#f2c96d")
        sheet.paste(img, (x, y + label_h))
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)


def write_markdown(report: dict[str, Any], path: Path) -> None:
    lines = [
        "# Render Regression Diff",
        "",
        f"- ok: `{str(report['ok']).lower()}`",
        f"- deck type: `{report.get('deck_type', 'default')}`",
        f"- threshold profile: `{report.get('threshold_profile', 'default')}`",
        f"- html pages: {report['html_count']}",
        f"- LibreOffice pages: {report['lo_count']}",
        f"- errors: {len(report['errors'])}",
        f"- warnings: {len(report['warnings'])}",
        f"- contact sheet: `{report.get('contact_sheet', '')}`",
        "",
        "| page | mean | p95 | changed | edge | status |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for page in report["pages"]:
        status = "ok"
        if page.get("errors"):
            status = "error"
        elif page.get("warnings"):
            status = "warning"
        lines.append(
            f"| {page['index']} | {page['mean_delta']:.3f} | {page['p95_delta']:.3f} | "
            f"{page['changed_ratio']:.3f} | {page['edge_delta']:.3f} | {status} |"
        )
    if report["errors"] or report["warnings"]:
        lines.extend(["", "## Findings", ""])
        for item in report["errors"]:
            lines.append(f"- **error** {item}")
        for item in report["warnings"]:
            lines.append(f"- **warning** {item}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck", type=Path)
    parser.add_argument("--html-dir", type=Path, help="Browser screenshot directory. Defaults to deck/qa")
    parser.add_argument("--lo-dir", type=Path, help="LibreOffice PNG directory. Defaults to deck/qa/libreoffice-render*")
    parser.add_argument("--out-dir", type=Path, help="Directory for visual diff images. Defaults to deck/qa/render-diff")
    parser.add_argument("--report", type=Path, help="JSON report path")
    parser.add_argument("--markdown", type=Path, help="Markdown report path")
    parser.add_argument("--width", type=int, default=960)
    parser.add_argument("--deck-type", default="auto", help="Threshold profile or auto. Built-ins: default, investor, consulting, product, report, training, raster")
    parser.add_argument("--threshold-profile", dest="deck_type", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
    parser.add_argument("--thresholds", type=Path, default=SCRIPT_DIR.parent / "assets" / "render-diff-thresholds.json", help="Render diff threshold profile JSON")
    parser.add_argument("--mean-warning", type=float)
    parser.add_argument("--mean-error", type=float)
    parser.add_argument("--changed-warning", type=float)
    parser.add_argument("--changed-error", type=float)
    parser.add_argument("--edge-warning", type=float)
    parser.add_argument("--edge-error", type=float)
    parser.add_argument("--fail-on", choices=("error", "warning", "none"), default="warning")
    args = parser.parse_args()

    deck = args.deck.resolve()
    html_dir = (args.html_dir or (deck / "qa")).resolve()
    lo_dir = (args.lo_dir or choose_lo_dir(deck)).resolve()
    out_dir = (args.out_dir or (deck / "qa" / "render-diff")).resolve()
    report_path = (args.report or (out_dir / "render-diff-report.json")).resolve()
    markdown_path = (args.markdown or report_path.with_suffix(".md")).resolve()
    threshold_config_path = args.thresholds.resolve()
    threshold_config = load_threshold_config(threshold_config_path)
    inferred_deck_type, threshold_profile, thresholds = resolve_threshold_profile(deck, args.deck_type, threshold_config)
    for key in THRESHOLD_KEYS:
        override = getattr(args, key)
        if override is not None:
            thresholds[key] = float(override)

    html_files = collect_pngs(html_dir)
    lo_files = collect_lo_pngs(lo_dir)
    errors: list[str] = []
    warnings: list[str] = []
    if len(html_files) != len(lo_files):
        errors.append(f"page count mismatch: html={len(html_files)} libreoffice={len(lo_files)}")

    pages: list[dict[str, Any]] = []
    for index, (html_path, lo_path) in enumerate(zip(html_files, lo_files), start=1):
        page = compare_pair(html_path, lo_path, width=args.width, out_dir=out_dir, index=index)
        page_errors: list[str] = []
        page_warnings: list[str] = []
        if page["mean_delta"] >= thresholds["mean_error"]:
            page_errors.append(f"mean_delta {page['mean_delta']:.3f} >= {thresholds['mean_error']:.3f}")
        elif page["mean_delta"] >= thresholds["mean_warning"]:
            page_warnings.append(f"mean_delta {page['mean_delta']:.3f} >= {thresholds['mean_warning']:.3f}")
        if page["changed_ratio"] >= thresholds["changed_error"]:
            page_errors.append(f"changed_ratio {page['changed_ratio']:.3f} >= {thresholds['changed_error']:.3f}")
        elif page["changed_ratio"] >= thresholds["changed_warning"]:
            page_warnings.append(f"changed_ratio {page['changed_ratio']:.3f} >= {thresholds['changed_warning']:.3f}")
        if page["edge_delta"] >= thresholds["edge_error"]:
            page_errors.append(f"edge_delta {page['edge_delta']:.3f} >= {thresholds['edge_error']:.3f}")
        elif page["edge_delta"] >= thresholds["edge_warning"]:
            page_warnings.append(f"edge_delta {page['edge_delta']:.3f} >= {thresholds['edge_warning']:.3f}")
        page["errors"] = page_errors
        page["warnings"] = page_warnings
        errors.extend(f"page {index}: {item}" for item in page_errors)
        warnings.extend(f"page {index}: {item}" for item in page_warnings)
        pages.append(page)

    compare_files = [Path(page["compare"]) for page in pages]
    contact_sheet = out_dir / "render-diff-contact-sheet.png"
    make_contact_sheet(compare_files, contact_sheet)

    ok = not errors and (args.fail_on != "warning" or not warnings)
    report = {
        "ok": ok,
        "deck": str(deck),
        "html_dir": str(html_dir),
        "lo_dir": str(lo_dir),
        "out_dir": str(out_dir),
        "deck_type_requested": args.deck_type,
        "deck_type": inferred_deck_type,
        "threshold_profile": threshold_profile,
        "threshold_source": str(threshold_config_path),
        "html_count": len(html_files),
        "lo_count": len(lo_files),
        "errors": errors,
        "warnings": warnings,
        "fail_on": args.fail_on,
        "thresholds": thresholds,
        "contact_sheet": str(contact_sheet),
        "pages": pages,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(report, markdown_path)
    print(f"render-diff-report-written {report_path}")
    print(f"render-diff-contact-sheet {contact_sheet}")
    print(f"render-diff-summary pages={len(pages)} errors={len(errors)} warnings={len(warnings)}")
    if args.fail_on == "none":
        return 0
    if errors:
        return 1
    if args.fail_on == "warning" and warnings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
