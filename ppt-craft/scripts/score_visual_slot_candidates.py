#!/usr/bin/env python3
"""Create and score multi-candidate visual assets for planned visual slots."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

from PIL import Image, ImageFilter

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from process_visual_slots import (  # noqa: E402
    apply_transparency,
    as_box,
    fit_image,
    infer_output_size,
    iter_visual_slots,
    read_json,
    resolve_path,
    truthy,
)


IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def slug(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip()).strip("-")
    return cleaned or "slot"


def percentile(hist: list[int], q: float) -> float:
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


def mean_hist(hist: list[int]) -> float:
    total = sum(hist)
    if not total:
        return 0.0
    return sum(index * count for index, count in enumerate(hist)) / (255.0 * total)


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def band_score(value: float, low: float, high: float, soft: float) -> float:
    if low <= value <= high:
        return 1.0
    if value < low:
        return clamp01(1.0 - (low - value) / max(0.0001, soft))
    return clamp01(1.0 - (value - high) / max(0.0001, soft))


def slot_dir(base: Path, view_id: str, slot_id: str) -> Path:
    return base / slug(view_id) / slug(slot_id)


def output_path(deck_dir: Path, view_id: str, slot: dict[str, Any]) -> Path:
    value = str(slot.get("out") or slot.get("asset_out") or slot.get("src") or "").strip()
    path = resolve_path(deck_dir, value or None)
    if path:
        return path
    return deck_dir / "assets" / f"{slug(view_id)}-{slug(str(slot.get('id') or 'slot'))}.png"


def prompt_text(view_id: str, slot: dict[str, Any], candidate_index: int, total: int) -> str:
    slot_id = str(slot.get("id") or "slot")
    box = slot.get("box") or {}
    transparent = truthy(slot.get("transparent"))
    prompt = str(slot.get("prompt") or "").strip()
    role = str(slot.get("role") or "visual cue").strip()
    ratio = "16:9"
    size = slot.get("output_size") or slot.get("asset_size")
    if isinstance(size, dict) and size.get("w") and size.get("h"):
        ratio = f"{int(size['w'])}:{int(size['h'])}"
    variant_axes = [
        "cleaner silhouette, fewer micro details, stronger negative space",
        "richer internal geometry, still no labels, clear center of gravity",
        "more premium technical depth, quieter border, stronger focal cue",
        "minimal icon-like version with high readability at small size",
    ]
    variant = variant_axes[(candidate_index - 1) % len(variant_axes)]
    lines = [
        f"# Candidate {candidate_index}/{total} for `{view_id}/{slot_id}`",
        "",
        "Generate one local slide asset, not a full slide.",
        "",
        f"- role: {role}",
        f"- target aspect: {ratio}",
        f"- slide slot box pt: x={box.get('x')} y={box.get('y')} w={box.get('w')} h={box.get('h')}",
        f"- transparent PNG preferred: {'yes' if transparent else 'no'}",
        f"- variation axis: {variant}",
        "- no text, no pseudo text, no UI labels, no logos, no watermark",
        "- keep the border quiet so editable PPT text and graph lines can sit nearby",
        "- strong focal shape, readable at small size, no full-slide composition",
        "",
        "Base prompt:",
        prompt or f"{role}, no text, local metaphor asset for a premium technical presentation",
        "",
        "Negative prompt:",
        "busy background, fake labels, typography, random small text, cropped important subject, full-slide poster, low contrast haze",
    ]
    return "\n".join(lines) + "\n"


def write_prompt_pack(deck_dir: Path, graph: dict[str, Any], candidates_dir: Path, count: int) -> dict[str, Any]:
    slots: list[dict[str, Any]] = []
    for view_id, slot in iter_visual_slots(graph):
        slot_id = str(slot.get("id") or f"{view_id}-slot")
        directory = slot_dir(candidates_dir, view_id, slot_id)
        directory.mkdir(parents=True, exist_ok=True)
        prompts = []
        for index in range(1, count + 1):
            prompt_path = directory / f"prompt-{index:02d}.md"
            prompt_path.write_text(prompt_text(view_id, slot, index, count), encoding="utf-8")
            prompts.append(str(prompt_path))
        readme = [
            f"# Visual Slot Candidates: {view_id}/{slot_id}",
            "",
            "Use built-in ImageGen or local image work to create candidate PNGs from the prompt files in this folder.",
            "Name outputs `candidate-01.png`, `candidate-02.png`, etc. For Codex built-in ImageGen orchestration, generate the queue with:",
            "",
            "```bash",
            "python3 scripts/score_visual_slot_candidates.py deck --write-imagegen-queue --plan-only",
            "```",
            "",
            "After candidate images exist, run:",
            "",
            "```bash",
            "python3 scripts/score_visual_slot_candidates.py deck --select",
            "```",
            "",
        ]
        (directory / "README.md").write_text("\n".join(readme), encoding="utf-8")
        slots.append({
            "view": view_id,
            "slot": slot_id,
            "directory": str(directory),
            "prompts": prompts,
        })
    manifest = {
        "deck": str(deck_dir),
        "candidates_dir": str(candidates_dir),
        "candidates_per_slot": count,
        "slots": slots,
    }
    (candidates_dir / "visual-slot-candidates-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def queue_item_prompt(base_prompt: str, candidate_path: Path) -> str:
    return (
        base_prompt
        + "\n"
        + "Built-in ImageGen execution note:\n"
        + "- Use the ChatGPT/Codex built-in ImageGen tool, not an OpenAI API key or external generator.\n"
        + f"- Store the generated PNG at: {candidate_path}\n"
        + "- Preserve transparency when requested; if the tool returns a non-transparent image, keep a clean subject on a quiet dark field.\n"
    )


def write_imagegen_queue(
    deck_dir: Path,
    graph: dict[str, Any],
    candidates_dir: Path,
    count: int,
    queue_path: Path,
) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    for view_id, slot in iter_visual_slots(graph):
        slot_id = str(slot.get("id") or f"{view_id}-slot")
        directory = slot_dir(candidates_dir, view_id, slot_id)
        directory.mkdir(parents=True, exist_ok=True)
        for index in range(1, count + 1):
            prompt_path = directory / f"prompt-{index:02d}.md"
            candidate_path = directory / f"candidate-{index:02d}.png"
            base_prompt = prompt_path.read_text(encoding="utf-8") if prompt_path.exists() else prompt_text(view_id, slot, index, count)
            if not prompt_path.exists():
                prompt_path.write_text(base_prompt, encoding="utf-8")
            items.append(
                {
                    "tool": "builtin_imagegen",
                    "status": "pending",
                    "view": view_id,
                    "slot": slot_id,
                    "candidate_index": index,
                    "prompt_path": str(prompt_path),
                    "candidate_path": str(candidate_path),
                    "slot_output_path": str(output_path(deck_dir, view_id, slot)),
                    "transparent": truthy(slot.get("transparent")),
                    "prompt": queue_item_prompt(base_prompt, candidate_path),
                }
            )

    queue = {
        "version": 1,
        "kind": "ppt-craft-builtin-imagegen-queue",
        "deck": str(deck_dir),
        "candidates_dir": str(candidates_dir),
        "candidates_per_slot": count,
        "items": items,
        "after_generation": [
            "python3 scripts/score_visual_slot_candidates.py deck --select",
            "python3 scripts/render_relationship_graph.py deck",
        ],
    }
    md_path = queue_path.with_suffix(".md")
    queue["markdown"] = str(md_path)
    queue_path.parent.mkdir(parents=True, exist_ok=True)
    queue_path.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Built-in ImageGen Queue",
        "",
        "This queue is for an agent that can call the built-in ImageGen tool. Do not use `OPENAI_API_KEY`, external APIs, or a fake generator for this step.",
        "",
        "For each item:",
        "",
        "1. Call built-in ImageGen with the item prompt.",
        "2. Store the returned PNG at `candidate_path`.",
        "3. Keep important text out of the image; the deck will place editable text, labels, connectors, and charts separately.",
        "",
        "After all required candidates exist, run:",
        "",
        "```bash",
        "python3 scripts/score_visual_slot_candidates.py deck --select",
        "```",
        "",
        "| item | target | prompt |",
        "| --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f"| `{item['view']}/{item['slot']}#{item['candidate_index']:02d}` | "
            f"`{item['candidate_path']}` | `{item['prompt_path']}` |"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return queue


def candidate_files(directory: Path) -> list[Path]:
    if not directory.exists():
        return []
    files = []
    for path in directory.iterdir():
        if path.is_file() and path.suffix.lower() in IMAGE_EXTS and not path.name.startswith("selected"):
            files.append(path)
    return sorted(files)


def seed_current(deck_dir: Path, candidates_dir: Path, graph: dict[str, Any], overwrite: bool) -> int:
    copied = 0
    for view_id, slot in iter_visual_slots(graph):
        slot_id = str(slot.get("id") or f"{view_id}-slot")
        src = resolve_path(deck_dir, str(slot.get("src") or "").strip() or None)
        if not src or not src.exists():
            continue
        directory = slot_dir(candidates_dir, view_id, slot_id)
        directory.mkdir(parents=True, exist_ok=True)
        target = directory / "candidate-01.png"
        if target.exists() and not overwrite:
            continue
        shutil.copy2(src, target)
        copied += 1
    return copied


def border_crop(alpha: Image.Image, width_fraction: float = 0.05) -> Image.Image:
    w, h = alpha.size
    border = max(1, int(min(w, h) * width_fraction))
    mask = Image.new("L", (w, h), 0)
    strips = [
        (0, 0, w, border),
        (0, h - border, w, h),
        (0, 0, border, h),
        (w - border, 0, w, h),
    ]
    for box in strips:
        mask.paste(alpha.crop(box), box)
    return mask


def score_image(path: Path, slot: dict[str, Any]) -> dict[str, Any]:
    image = Image.open(path).convert("RGBA")
    target_size = infer_output_size(slot, as_box(slot.get("box")), image.size)
    target_aspect = target_size[0] / target_size[1]
    aspect = image.width / max(1, image.height)
    aspect_score = clamp01(1.0 - abs(aspect - target_aspect) / max(target_aspect, 0.0001))
    resolution_score = min(1.0, min(image.width / target_size[0], image.height / target_size[1]))

    alpha = image.getchannel("A")
    alpha_hist = alpha.histogram()
    total = image.width * image.height
    alpha_zero = alpha_hist[0] / total
    visible = sum(alpha_hist[24:]) / total
    partial_alpha = sum(alpha_hist[1:255]) / total
    border_visible = sum(border_crop(alpha).histogram()[24:]) / total

    alpha_mask = alpha.point(lambda value: 255 if value > 24 else 0)
    rgb = Image.new("RGB", image.size, "#050b12")
    rgb.paste(image.convert("RGB"), mask=alpha)
    luma = rgb.convert("L")
    luma_hist = luma.histogram(mask=alpha_mask) if visible > 0 else luma.histogram()
    contrast = percentile(luma_hist, 0.92) - percentile(luma_hist, 0.08)
    edge = luma.resize((min(320, image.width), max(1, int(min(320, image.width) * image.height / image.width))), Image.Resampling.LANCZOS).filter(ImageFilter.FIND_EDGES)
    edge_density = mean_hist(edge.histogram())

    if truthy(slot.get("transparent")):
        occupancy_score = band_score(visible, 0.035, 0.28, 0.12)
        border_score = 1.0 - clamp01(border_visible / 0.12)
        alpha_score = band_score(alpha_zero, 0.55, 0.97, 0.2)
    else:
        occupancy_score = band_score(visible, 0.55, 1.0, 0.25)
        border_score = 1.0 - clamp01(border_visible / 0.55)
        alpha_score = 1.0
    contrast_score = band_score(contrast, 0.12, 0.72, 0.16)
    edge_score = band_score(edge_density, 0.015, 0.18, 0.10)

    score = 100 * (
        0.16 * resolution_score
        + 0.14 * aspect_score
        + 0.18 * occupancy_score
        + 0.16 * contrast_score
        + 0.16 * border_score
        + 0.10 * edge_score
        + 0.10 * alpha_score
    )

    warnings: list[str] = []
    if resolution_score < 0.85:
        warnings.append("candidate is below target output size")
    if aspect_score < 0.82:
        warnings.append("candidate aspect ratio is far from slot output ratio")
    if occupancy_score < 0.6:
        warnings.append("candidate subject occupancy is weak or too crowded")
    if border_score < 0.6:
        warnings.append("candidate border is too busy for a local slot")
    if contrast_score < 0.55:
        warnings.append("candidate contrast is weak")

    return {
        "path": str(path),
        "score": round(score, 2),
        "size": {"w": image.width, "h": image.height},
        "target_size": {"w": target_size[0], "h": target_size[1]},
        "metrics": {
            "resolution_score": round(resolution_score, 4),
            "aspect_score": round(aspect_score, 4),
            "visible_ratio": round(visible, 4),
            "alpha_zero_ratio": round(alpha_zero, 4),
            "partial_alpha_ratio": round(partial_alpha, 4),
            "border_visible_ratio": round(border_visible, 4),
            "contrast": round(contrast, 4),
            "edge_density": round(edge_density, 4),
            "occupancy_score": round(occupancy_score, 4),
            "border_score": round(border_score, 4),
            "contrast_score": round(contrast_score, 4),
            "edge_score": round(edge_score, 4),
            "alpha_score": round(alpha_score, 4),
        },
        "warnings": warnings,
    }


def normalize_and_save(candidate: Path, slot: dict[str, Any], out: Path) -> None:
    image = Image.open(candidate).convert("RGBA")
    size = infer_output_size(slot, as_box(slot.get("box")), image.size)
    fit = str(slot.get("fit") or "cover")
    if fit not in {"cover", "contain", "fill", "scale-down"}:
        fit = "cover"
    background = (5, 11, 18, 0 if truthy(slot.get("transparent")) else 255)
    output = fit_image(image, size, fit, background)
    if truthy(slot.get("transparent")):
        output = apply_transparency(output, slot)
    out.parent.mkdir(parents=True, exist_ok=True)
    output.save(out if out.suffix else out.with_suffix(".png"))


def write_markdown(report: dict[str, Any], path: Path) -> None:
    lines = [
        "# Visual Slot Candidate Scores",
        "",
        f"- ok: `{str(report['ok']).lower()}`",
        f"- slots: {len(report['slots'])}",
        f"- errors: {len(report['errors'])}",
        f"- warnings: {len(report['warnings'])}",
        "",
        "| slot | candidates | best score | selected |",
        "| --- | ---: | ---: | --- |",
    ]
    for slot in report["slots"]:
        best = slot.get("best") or {}
        lines.append(
            f"| `{slot['view']}/{slot['slot']}` | {len(slot.get('candidates', []))} | "
            f"{best.get('score', 0):.2f} | `{slot.get('selected_out', '')}` |"
        )
    if report["errors"] or report["warnings"]:
        lines.extend(["", "## Findings", ""])
        for item in report["errors"]:
            lines.append(f"- **error** {item}")
        for item in report["warnings"]:
            lines.append(f"- **warning** {item}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def score_slots(
    deck_dir: Path,
    graph: dict[str, Any],
    candidates_dir: Path,
    *,
    select: bool,
    min_score: float,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    slots: list[dict[str, Any]] = []
    for view_id, slot in iter_visual_slots(graph):
        slot_id = str(slot.get("id") or f"{view_id}-slot")
        directory = slot_dir(candidates_dir, view_id, slot_id)
        files = candidate_files(directory)
        slot_record: dict[str, Any] = {
            "view": view_id,
            "slot": slot_id,
            "directory": str(directory),
            "candidates": [],
        }
        if not files:
            errors.append(f"{view_id}/{slot_id}: no candidate images found in {directory}")
            slots.append(slot_record)
            continue
        scored = sorted((score_image(path, slot) for path in files), key=lambda item: item["score"], reverse=True)
        slot_record["candidates"] = scored
        best = scored[0]
        slot_record["best"] = best
        if best["score"] < min_score:
            errors.append(f"{view_id}/{slot_id}: best score {best['score']:.2f} < {min_score:.2f}")
        for warning in best.get("warnings", []):
            warnings.append(f"{view_id}/{slot_id}: {warning}")
        if select and best["score"] >= min_score:
            out = output_path(deck_dir, view_id, slot)
            normalize_and_save(Path(best["path"]), slot, out)
            slot_record["selected_out"] = str(out)
        slots.append(slot_record)
    return {
        "ok": not errors,
        "deck": str(deck_dir),
        "candidates_dir": str(candidates_dir),
        "selected": select,
        "min_score": min_score,
        "errors": errors,
        "warnings": warnings,
        "slots": slots,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck", type=Path)
    parser.add_argument("--graph", type=Path, help="Graph JSON path. Defaults to deck/relationship-graph.json")
    parser.add_argument("--candidates-dir", type=Path, help="Candidate image root. Defaults to deck/asset-prompts/visual-slot-candidates")
    parser.add_argument("--report", type=Path, help="JSON report path")
    parser.add_argument("--markdown", type=Path, help="Markdown report path")
    parser.add_argument("--write-prompts", action="store_true", help="Write prompt files for each slot/candidate")
    parser.add_argument("--write-imagegen-queue", "--builtin-imagegen-queue", action="store_true", help="Write a built-in ImageGen execution queue for Codex/agent orchestration")
    parser.add_argument("--imagegen-queue", type=Path, help="Built-in ImageGen queue JSON path. Defaults to deck/asset-prompts/builtin-imagegen-queue.json")
    parser.add_argument("--plan-only", action="store_true", help="Write prompt/queue artifacts and exit before candidate scoring")
    parser.add_argument("--candidates-per-slot", type=int, default=4)
    parser.add_argument("--seed-current", action="store_true", help="Copy each current slot src into candidate-01.png for smoke testing")
    parser.add_argument("--overwrite-seed", action="store_true")
    parser.add_argument("--select", action="store_true", help="Copy the best candidate to the slot output path")
    parser.add_argument("--min-score", type=float, default=55.0)
    parser.add_argument("--fail-on", choices=("error", "warning", "none"), default="warning")
    args = parser.parse_args()

    deck_dir = args.deck.resolve()
    graph_path = (args.graph or (deck_dir / "relationship-graph.json")).resolve()
    candidates_dir = (args.candidates_dir or (deck_dir / "asset-prompts" / "visual-slot-candidates")).resolve()
    report_path = (args.report or (deck_dir / "asset-prompts" / "visual-slot-candidate-scores.json")).resolve()
    markdown_path = (args.markdown or report_path.with_suffix(".md")).resolve()
    imagegen_queue_path = (args.imagegen_queue or (deck_dir / "asset-prompts" / "builtin-imagegen-queue.json")).resolve()
    graph = read_json(graph_path)

    manifest = None
    imagegen_queue = None
    if args.write_prompts or args.write_imagegen_queue:
        manifest = write_prompt_pack(deck_dir, graph, candidates_dir, max(1, args.candidates_per_slot))
        print(f"visual-slot-prompts-written {candidates_dir}")
    if args.write_imagegen_queue:
        imagegen_queue = write_imagegen_queue(deck_dir, graph, candidates_dir, max(1, args.candidates_per_slot), imagegen_queue_path)
        print(f"visual-slot-imagegen-queue-written {imagegen_queue_path}")
    if args.seed_current:
        copied = seed_current(deck_dir, candidates_dir, graph, args.overwrite_seed)
        print(f"visual-slot-candidates-seeded copied={copied}")

    if args.plan_only:
        report = {
            "ok": True,
            "deck": str(deck_dir),
            "candidates_dir": str(candidates_dir),
            "selected": False,
            "plan_only": True,
            "min_score": args.min_score,
            "errors": [],
            "warnings": [],
            "slots": [],
        }
    else:
        report = score_slots(deck_dir, graph, candidates_dir, select=args.select, min_score=args.min_score)
    if manifest:
        report["prompt_manifest"] = manifest
    if imagegen_queue:
        report["imagegen_queue"] = imagegen_queue
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(report, markdown_path)
    print(f"visual-slot-candidate-report-written {report_path}")
    print(f"visual-slot-candidate-summary slots={len(report['slots'])} errors={len(report['errors'])} warnings={len(report['warnings'])}")
    if args.fail_on == "none":
        return 0
    if report["errors"]:
        return 1
    if args.fail_on == "warning" and report["warnings"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
