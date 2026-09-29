#!/usr/bin/env python3
"""Run visual QA checks for PPT Craft HTML decks and screenshots."""

from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PIL import Image, ImageFilter, ImageStat


SCRIPT_DIR = Path(__file__).resolve().parent
SCREENSHOT_SCRIPT = SCRIPT_DIR / "screenshot_deck.mjs"
DOM_SCRIPT = SCRIPT_DIR / "visual_dom_metrics.mjs"


@dataclass
class Finding:
    severity: str
    check: str
    slide: str
    message: str
    details: dict[str, Any]


TEXT_ZONE_KEYS = ("claim", "support", "evidence", "loop", "caption", "callout", "text")
BOX_KEYS = ("x", "y", "w", "h")


def slide_pngs(path: Path) -> list[Path]:
    return sorted(
        item
        for item in path.glob("*.png")
        if not item.name.startswith("index")
        and "contact" not in item.name.lower()
        and "visual-qa" not in item.name.lower()
    )


def resolve_screenshot_dir(target: Path, requested: Path | None) -> Path:
    if requested:
        return requested
    if target.is_dir() and slide_pngs(target):
        return target
    qa = target / "qa"
    if qa.exists():
        return qa
    return qa


def run_command(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def ensure_screenshots(target: Path, screenshots: Path, auto: bool) -> None:
    if slide_pngs(screenshots):
        return
    if not auto:
        raise SystemExit(f"no slide screenshots found in {screenshots}; run screenshot_deck.mjs first or pass --auto-screenshot")
    if not (target / "slides").exists():
        raise SystemExit(f"cannot auto-screenshot; no slides folder found in {target}")
    run_command(["node", str(SCREENSHOT_SCRIPT), str(target), "--out", str(screenshots)])


def image_feature(path: Path, size: tuple[int, int] = (16, 9)) -> dict[str, Any]:
    img = Image.open(path).convert("L")
    small = img.resize(size, Image.Resampling.LANCZOS)
    values = [value / 255.0 for value in small.tobytes()]
    mean = sum(values) / len(values)
    centered = [value - mean for value in values]

    edges = img.filter(ImageFilter.FIND_EDGES)
    edge_small = edges.resize(size, Image.Resampling.LANCZOS)
    edge_values = [value / 255.0 for value in edge_small.tobytes()]
    edge_mean = sum(edge_values) / len(edge_values)
    edge_centered = [value - edge_mean for value in edge_values]

    occupancy = []
    width, height = img.size
    block_w = width / size[0]
    block_h = height / size[1]
    edge_pixels = edges.load()
    for row in range(size[1]):
        for col in range(size[0]):
            left = int(round(col * block_w))
            top = int(round(row * block_h))
            right = int(round((col + 1) * block_w))
            bottom = int(round((row + 1) * block_h))
            count = 0
            total = max(1, (right - left) * (bottom - top))
            for y in range(top, bottom):
                for x in range(left, right):
                    if edge_pixels[x, y] > 30:
                        count += 1
            occupancy.append(1.0 if count / total > 0.018 else 0.0)

    return {
        "luminance": centered,
        "edges": edge_centered,
        "occupancy": occupancy,
        "edge_mean": edge_mean,
        "size": img.size,
    }


def cosine(left: list[float], right: list[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right))
    norm_left = math.sqrt(sum(value * value for value in left))
    norm_right = math.sqrt(sum(value * value for value in right))
    if norm_left == 0 or norm_right == 0:
        return 0.0
    return dot / (norm_left * norm_right)


def occupancy_similarity(left: list[float], right: list[float]) -> float:
    matches = sum(1 for a, b in zip(left, right) if a == b)
    return matches / max(1, len(left))


def similarity_score(left: dict[str, Any], right: dict[str, Any]) -> float:
    lum = (cosine(left["luminance"], right["luminance"]) + 1) / 2
    edge = (cosine(left["edges"], right["edges"]) + 1) / 2
    occ = occupancy_similarity(left["occupancy"], right["occupancy"])
    return 0.42 * lum + 0.38 * edge + 0.20 * occ


def edge_pressure(path: Path, margin: int = 18) -> dict[str, Any]:
    img = Image.open(path).convert("L")
    edges = img.filter(ImageFilter.FIND_EDGES)
    width, height = edges.size
    border_boxes = {
        "top": (0, 0, width, margin),
        "bottom": (0, height - margin, width, height),
        "left": (0, 0, margin, height),
        "right": (width - margin, 0, width, height),
    }
    inner = edges.crop((margin, margin, width - margin, height - margin))
    inner_mean = ImageStat.Stat(inner).mean[0] / 255.0
    result: dict[str, Any] = {"inner_edge_mean": round(inner_mean, 4), "edges": {}}
    for name, box in border_boxes.items():
        cropped = edges.crop(box)
        mean = ImageStat.Stat(cropped).mean[0] / 255.0
        result["edges"][name] = round(mean, 4)
    result["max_border_edge_mean"] = max(result["edges"].values())
    return result


def analyze_similarity(files: list[Path], warn_threshold: float, error_threshold: float) -> tuple[list[Finding], list[dict[str, Any]]]:
    features = {path: image_feature(path) for path in files}
    pairs: list[dict[str, Any]] = []
    findings: list[Finding] = []
    for index, left in enumerate(files):
        for right in files[index + 1 :]:
            score = similarity_score(features[left], features[right])
            item = {
                "left": left.name,
                "right": right.name,
                "score": round(score, 4),
            }
            pairs.append(item)
            severity = "error" if score >= error_threshold else "warning" if score >= warn_threshold else ""
            if severity:
                findings.append(
                    Finding(
                        severity=severity,
                        check="similarity",
                        slide=f"{left.name} <> {right.name}",
                        message=f"Slides are visually similar ({score:.3f}).",
                        details=item,
                    )
                )
    pairs.sort(key=lambda item: item["score"], reverse=True)
    return findings, pairs[:20]


def analyze_edge_pressure(files: list[Path], threshold: float) -> tuple[list[Finding], dict[str, Any]]:
    findings: list[Finding] = []
    metrics: dict[str, Any] = {}
    for path in files:
        data = edge_pressure(path)
        metrics[path.name] = data
        noisy_edges = [name for name, value in data["edges"].items() if value >= threshold]
        if noisy_edges:
            findings.append(
                Finding(
                    severity="warning",
                    check="edge-pressure",
                    slide=path.name,
                    message=f"High-detail pixels touch slide edge: {', '.join(noisy_edges)}.",
                    details={"edges": data["edges"], "threshold": threshold},
                )
            )
    return findings, metrics


def load_dom_report(deck: Path, report_path: Path, auto: bool) -> dict[str, Any] | None:
    if report_path.exists():
        return json.loads(report_path.read_text(encoding="utf-8"))
    if not auto or not (deck / "slides").exists():
        return None
    run_command(["node", str(DOM_SCRIPT), str(deck), "--out", str(report_path)])
    return json.loads(report_path.read_text(encoding="utf-8"))


def read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def box_from(value: Any) -> dict[str, float] | None:
    if not isinstance(value, dict):
        return None
    raw = value.get("box") if isinstance(value.get("box"), dict) else value
    if not isinstance(raw, dict) or not all(key in raw for key in BOX_KEYS):
        return None
    try:
        return {key: float(raw[key]) for key in BOX_KEYS}
    except (TypeError, ValueError):
        return None


def stage_from(data: dict[str, Any] | None) -> dict[str, float] | None:
    if not isinstance(data, dict):
        return None
    stage = data.get("stage")
    if not isinstance(stage, dict):
        return None
    try:
        return {"width": float(stage["width"]), "height": float(stage["height"])}
    except (KeyError, TypeError, ValueError):
        return None


def slide_number(value: str) -> int | None:
    match = re.search(r"(\d+)", value)
    if not match:
        return None
    try:
        return int(match.group(1))
    except ValueError:
        return None


def slide_keys(value: str) -> set[str]:
    raw = str(value or "")
    stem = Path(raw).stem
    keys = {raw, stem}
    number = slide_number(stem)
    if number is not None:
        keys.add(f"{number:02d}")
        keys.add(str(number))
    return {key for key in keys if key}


def add_zone(
    zones: list[dict[str, Any]],
    *,
    slide_id: str,
    slide_index: int,
    name: str,
    box: dict[str, float] | None,
    stage: dict[str, float] | None,
    source: str,
) -> None:
    if not box or not stage:
        return
    key = (
        name,
        round(box["x"], 2),
        round(box["y"], 2),
        round(box["w"], 2),
        round(box["h"], 2),
        source,
    )
    for existing in zones:
        existing_key = (
            existing["name"],
            round(existing["box"]["x"], 2),
            round(existing["box"]["y"], 2),
            round(existing["box"]["w"], 2),
            round(existing["box"]["h"], 2),
            existing["source"],
        )
        if existing_key == key:
            return
    zones.append(
        {
            "slide_id": slide_id,
            "slide_index": slide_index,
            "name": name,
            "box": box,
            "stage": stage,
            "source": source,
        }
    )


def collect_blueprint_text_zones(deck: Path) -> dict[str, Any]:
    if not deck.is_dir():
        return {"available": False, "source_files": [], "slides": [], "zones_by_index": {}, "zones_by_key": {}}

    source_files: list[str] = []
    zones_by_index: dict[int, list[dict[str, Any]]] = {}
    zones_by_key: dict[str, list[dict[str, Any]]] = {}
    slide_summaries: list[dict[str, Any]] = []

    def register(slide: dict[str, Any], slide_index: int, zones: list[dict[str, Any]]) -> None:
        slide_id = str(slide.get("id") or f"{slide_index + 1:02d}")
        zones_by_index.setdefault(slide_index, []).extend(zones)
        for key in slide_keys(slide_id):
            zones_by_key.setdefault(key, []).extend(zones)
        slide_summaries.append({"id": slide_id, "index": slide_index, "zones": len(zones)})

    blueprint_path = deck / "layout-blueprint.json"
    blueprint = read_json(blueprint_path)
    if blueprint:
        source_files.append(str(blueprint_path))
        stage = stage_from(blueprint)
        for index, slide in enumerate(blueprint.get("slides", [])):
            if not isinstance(slide, dict):
                continue
            slide_id = str(slide.get("id") or f"{index + 1:02d}")
            zones: list[dict[str, Any]] = []
            for name in TEXT_ZONE_KEYS:
                add_zone(
                    zones,
                    slide_id=slide_id,
                    slide_index=index,
                    name=name,
                    box=box_from(slide.get(name)),
                    stage=stage,
                    source="layout-blueprint",
                )
            for item in slide.get("text_safe_zones", []) if isinstance(slide.get("text_safe_zones"), list) else []:
                if not isinstance(item, dict):
                    continue
                add_zone(
                    zones,
                    slide_id=slide_id,
                    slide_index=index,
                    name=str(item.get("name") or "text-safe"),
                    box=box_from(item),
                    stage=stage,
                    source="layout-blueprint",
                )
            register(slide, index, zones)

    asset_prompt_path = deck / "asset-prompts" / "asset-prompts.json"
    asset_prompts = read_json(asset_prompt_path)
    if asset_prompts:
        source_files.append(str(asset_prompt_path))
        stage = stage_from(asset_prompts)
        for index, slide in enumerate(asset_prompts.get("slides", [])):
            if not isinstance(slide, dict):
                continue
            slide_id = str(slide.get("id") or f"{index + 1:02d}")
            zones: list[dict[str, Any]] = []
            for item in slide.get("text_safe_zones", []) if isinstance(slide.get("text_safe_zones"), list) else []:
                if not isinstance(item, dict):
                    continue
                add_zone(
                    zones,
                    slide_id=slide_id,
                    slide_index=index,
                    name=str(item.get("name") or "text-safe"),
                    box=box_from(item),
                    stage=stage,
                    source="asset-prompts",
                )
            register(slide, index, zones)

    available = bool(source_files)
    return {
        "available": available,
        "source_files": source_files,
        "slides": slide_summaries,
        "zones_by_index": zones_by_index,
        "zones_by_key": zones_by_key,
    }


def zones_for_slide(zone_data: dict[str, Any], slide_name: str, slide_index: int) -> list[dict[str, Any]]:
    for key in slide_keys(slide_name):
        zones = zone_data["zones_by_key"].get(key)
        if zones:
            return zones
    number = slide_number(slide_name)
    if number is not None:
        zones = zone_data["zones_by_index"].get(number - 1)
        if zones:
            return zones
    return zone_data["zones_by_index"].get(slide_index, [])


def scale_box(box: dict[str, float], source_stage: dict[str, float], dom_stage: dict[str, Any]) -> dict[str, float]:
    dom_w = float(dom_stage.get("w") or source_stage["width"])
    dom_h = float(dom_stage.get("h") or source_stage["height"])
    sx = dom_w / source_stage["width"] if source_stage["width"] else 1.0
    sy = dom_h / source_stage["height"] if source_stage["height"] else 1.0
    return {"x": box["x"] * sx, "y": box["y"] * sy, "w": box["w"] * sx, "h": box["h"] * sy}


def rect_inside(rect: dict[str, Any], box: dict[str, float], tolerance: float) -> bool:
    x = float(rect.get("x", 0))
    y = float(rect.get("y", 0))
    w = float(rect.get("w", 0))
    h = float(rect.get("h", 0))
    return (
        x >= box["x"] - tolerance
        and y >= box["y"] - tolerance
        and x + w <= box["x"] + box["w"] + tolerance
        and y + h <= box["y"] + box["h"] + tolerance
    )


def overlap_ratio(rect: dict[str, Any], box: dict[str, float]) -> float:
    x = float(rect.get("x", 0))
    y = float(rect.get("y", 0))
    w = float(rect.get("w", 0))
    h = float(rect.get("h", 0))
    if w <= 0 or h <= 0:
        return 0.0
    left = max(x, box["x"])
    top = max(y, box["y"])
    right = min(x + w, box["x"] + box["w"])
    bottom = min(y + h, box["y"] + box["h"])
    if right <= left or bottom <= top:
        return 0.0
    return ((right - left) * (bottom - top)) / (w * h)


def blueprint_text_zone_findings(
    report: dict[str, Any] | None,
    deck: Path,
    *,
    require_zones: bool,
    tolerance: float,
    min_font_size: float,
) -> tuple[list[Finding], dict[str, Any]]:
    findings: list[Finding] = []
    zone_data = collect_blueprint_text_zones(deck)
    summary: dict[str, Any] = {
        "enabled": report is not None,
        "available": zone_data["available"],
        "source_files": zone_data["source_files"],
        "slides_with_zones": sum(1 for slide in zone_data["slides"] if slide["zones"] > 0),
        "checked_text_boxes": 0,
        "violations": 0,
        "tolerance": tolerance,
        "min_font_size": min_font_size,
    }
    if not report:
        return findings, summary
    if not zone_data["available"]:
        if require_zones:
            findings.append(
                Finding(
                    severity="error",
                    check="blueprint-text-zones",
                    slide="deck",
                    message="No layout-blueprint.json or asset-prompts/asset-prompts.json was found for text-safe-zone QA.",
                    details={"deck": str(deck)},
                )
            )
            summary["violations"] = 1
        return findings, summary

    for index, slide in enumerate(report.get("slides", [])):
        slide_name = str(slide.get("file") or f"{index + 1:02d}")
        zones = zones_for_slide(zone_data, slide_name, index)
        if not zones:
            if require_zones:
                findings.append(
                    Finding(
                        severity="error",
                        check="blueprint-text-zones",
                        slide=slide_name,
                        message="Slide has no text-safe zones in blueprint or asset prompts.",
                        details={"slide_index": index},
                    )
                )
            continue

        scaled_zones = [
            {
                **zone,
                "scaled_box": scale_box(zone["box"], zone["stage"], slide.get("stage") or zone["stage"]),
            }
            for zone in zones
        ]
        for item in slide.get("text_boxes", []):
            try:
                font_size = float(item.get("fontSize") or 0)
            except (TypeError, ValueError):
                font_size = 0.0
            if font_size < min_font_size:
                continue
            text = str(item.get("text") or "").strip()
            if not text:
                continue
            if item.get("graphNode") or item.get("graphLabel") or item.get("visualQaZone") == "graph":
                continue
            summary["checked_text_boxes"] += 1
            rect = item.get("rect") or {}
            if any(rect_inside(rect, zone["scaled_box"], tolerance) for zone in scaled_zones):
                continue
            best_zone = max(
                scaled_zones,
                key=lambda zone: overlap_ratio(rect, zone["scaled_box"]),
                default=None,
            )
            best_overlap = overlap_ratio(rect, best_zone["scaled_box"]) if best_zone else 0.0
            findings.append(
                Finding(
                    severity="error",
                    check="blueprint-text-zones",
                    slide=slide_name,
                    message=f"Text is outside its declared text-safe zones: {text[:80]}",
                    details={
                        "element": item.get("element"),
                        "text": text[:160],
                        "rect": rect,
                        "fontSize": font_size,
                        "best_zone": None
                        if best_zone is None
                        else {
                            "name": best_zone["name"],
                            "source": best_zone["source"],
                            "box": best_zone["scaled_box"],
                            "overlap_ratio": round(best_overlap, 3),
                        },
                        "zones": [
                            {
                                "name": zone["name"],
                                "source": zone["source"],
                                "box": zone["scaled_box"],
                            }
                            for zone in scaled_zones
                        ],
                    },
                )
            )
            summary["violations"] += 1

    return findings, summary


def dom_findings(report: dict[str, Any] | None, contrast_error: float, contrast_warning: float) -> list[Finding]:
    findings: list[Finding] = []
    if not report:
        return findings
    for slide in report.get("slides", []):
        slide_name = str(slide.get("file") or "")
        for item in slide.get("overflows", []):
            findings.append(
                Finding(
                    severity="error",
                    check="overflow",
                    slide=slide_name,
                    message=f"Element overflows the slide stage: {item.get('element', item.get('type', 'document'))}.",
                    details=item,
                )
            )
        for item in slide.get("clipped_text", []):
            findings.append(
                Finding(
                    severity="error",
                    check="text-overflow",
                    slide=slide_name,
                    message=f"Text is clipped or scrolls inside its box: {item.get('text', '')}",
                    details=item,
                )
            )
        for item in slide.get("low_contrast_text", []):
            ratio = float(item.get("ratio", 0))
            if ratio < contrast_error:
                severity = "error"
            elif ratio < contrast_warning:
                severity = "warning"
            else:
                continue
            findings.append(
                Finding(
                    severity=severity,
                    check="contrast",
                    slide=slide_name,
                    message=f"Text contrast is low ({ratio:.2f}): {item.get('text', '')}",
                    details=item,
                )
            )
    return findings


def finding_dict(finding: Finding) -> dict[str, Any]:
    return {
        "severity": finding.severity,
        "check": finding.check,
        "slide": finding.slide,
        "message": finding.message,
        "details": finding.details,
    }


def write_markdown(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# Visual QA Report",
        "",
        f"- deck: `{report['deck']}`",
        f"- screenshots: `{report['screenshots']}`",
        f"- slides: {report['summary']['slides']}",
        f"- errors: {report['summary']['errors']}",
        f"- warnings: {report['summary']['warnings']}",
        f"- fail_on: `{report['thresholds']['fail_on']}`",
        "",
        "## Findings",
        "",
    ]
    findings = report["findings"]
    if not findings:
        lines.append("No visual QA findings.")
    else:
        for item in findings[:80]:
            lines.append(f"- **{item['severity']}** `{item['check']}` `{item['slide']}` - {item['message']}")
    lines.extend(["", "## Most Similar Pairs", ""])
    for item in report["similarity"]["top_pairs"][:12]:
        lines.append(f"- `{item['left']}` <> `{item['right']}`: {item['score']}")
    blueprint = report["summary"]["checks"].get("blueprint_text_zones", {})
    if blueprint.get("enabled"):
        lines.extend(
            [
                "",
                "## Blueprint Text-Safe Zones",
                "",
                f"- available: {blueprint.get('available')}",
                f"- slides_with_zones: {blueprint.get('slides_with_zones')}",
                f"- checked_text_boxes: {blueprint.get('checked_text_boxes')}",
                f"- violations: {blueprint.get('violations')}",
            ]
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="Deck folder or screenshot folder")
    parser.add_argument("--screenshots", type=Path, default=None)
    parser.add_argument("--out", type=Path, default=None, help="JSON report path")
    parser.add_argument("--markdown", type=Path, default=None, help="Markdown report path")
    parser.add_argument("--auto-screenshot", action="store_true", help="Run screenshot_deck.mjs when screenshots are missing")
    parser.add_argument("--skip-dom", action="store_true", help="Skip Playwright DOM overflow/contrast metrics")
    parser.add_argument("--skip-blueprint-zones", action="store_true", help="Skip text-safe-zone checks from layout-blueprint/asset-prompts")
    parser.add_argument("--require-blueprint-zones", action="store_true", help="Fail when blueprint/asset prompt text-safe zones are missing")
    parser.add_argument("--fail-on", choices=("error", "warning", "none"), default="warning")
    parser.add_argument("--similarity-warning", type=float, default=0.965)
    parser.add_argument("--similarity-error", type=float, default=0.985)
    parser.add_argument("--edge-warning", type=float, default=0.065)
    parser.add_argument("--contrast-error", type=float, default=2.0)
    parser.add_argument("--contrast-warning", type=float, default=3.0)
    parser.add_argument("--safe-zone-tolerance", type=float, default=8.0)
    parser.add_argument("--text-zone-min-font-size", type=float, default=10.0)
    args = parser.parse_args()

    target = args.target.resolve()
    screenshot_dir = resolve_screenshot_dir(target, args.screenshots).resolve()
    ensure_screenshots(target, screenshot_dir, args.auto_screenshot)
    files = slide_pngs(screenshot_dir)
    if not files:
        raise SystemExit(f"no slide screenshots found in {screenshot_dir}")

    dom_report_path = screenshot_dir / "visual-dom-report.json"
    dom_report = None if args.skip_dom else load_dom_report(target, dom_report_path, auto=target.is_dir() and (target / "slides").exists())

    findings: list[Finding] = []
    similarity_findings, top_pairs = analyze_similarity(files, args.similarity_warning, args.similarity_error)
    edge_findings, edge_metrics = analyze_edge_pressure(files, args.edge_warning)
    findings.extend(similarity_findings)
    findings.extend(edge_findings)
    findings.extend(dom_findings(dom_report, args.contrast_error, args.contrast_warning))
    blueprint_findings: list[Finding] = []
    blueprint_summary: dict[str, Any] = {"enabled": False}
    if not args.skip_blueprint_zones:
        blueprint_findings, blueprint_summary = blueprint_text_zone_findings(
            dom_report,
            target,
            require_zones=args.require_blueprint_zones,
            tolerance=args.safe_zone_tolerance,
            min_font_size=args.text_zone_min_font_size,
        )
        findings.extend(blueprint_findings)

    findings.sort(key=lambda item: (0 if item.severity == "error" else 1, item.check, item.slide))
    errors = sum(1 for item in findings if item.severity == "error")
    warnings = sum(1 for item in findings if item.severity == "warning")
    out_path = args.out or (screenshot_dir / "visual-qa-report.json")
    markdown_path = args.markdown or (screenshot_dir / "visual-qa-report.md")
    report = {
        "generated_by": "ppt-craft/scripts/visual_qa_deck.py",
        "deck": str(target),
        "screenshots": str(screenshot_dir),
        "summary": {
            "slides": len(files),
            "errors": errors,
            "warnings": warnings,
            "checks": {
                "similarity": len(similarity_findings),
                "edge_pressure": len(edge_findings),
                "dom": 0 if dom_report is None else dom_report.get("summary", {}),
                "blueprint_text_zones": blueprint_summary,
            },
        },
        "thresholds": {
            "similarity_warning": args.similarity_warning,
            "similarity_error": args.similarity_error,
            "edge_warning": args.edge_warning,
            "contrast_error": args.contrast_error,
            "contrast_warning": args.contrast_warning,
            "safe_zone_tolerance": args.safe_zone_tolerance,
            "text_zone_min_font_size": args.text_zone_min_font_size,
            "fail_on": args.fail_on,
        },
        "findings": [finding_dict(item) for item in findings],
        "similarity": {"top_pairs": top_pairs},
        "edge_pressure": edge_metrics,
        "dom_report": str(dom_report_path) if dom_report is not None else None,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(markdown_path, report)

    print(f"visual-qa-report-written {out_path}")
    print(f"visual-qa-markdown-written {markdown_path}")
    print(f"visual-qa-summary slides={len(files)} errors={errors} warnings={warnings}")

    if args.fail_on == "error" and errors:
        return 1
    if args.fail_on == "warning" and (errors or warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
