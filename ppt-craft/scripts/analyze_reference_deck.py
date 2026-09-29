#!/usr/bin/env python3
"""Quick forensics for PPTX/PDF reference decks."""

from __future__ import annotations

import argparse
import collections
import json
import os
import re
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "c": "http://schemas.openxmlformats.org/drawingml/2006/chart",
}


def _slide_number(name: str) -> int:
    match = re.search(r"slide(\d+)\.xml$", name)
    return int(match.group(1)) if match else 0


def analyze_pptx(path: Path) -> dict:
    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        slides = sorted(
            [n for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n)],
            key=_slide_number,
        )
        media = [n for n in names if n.startswith("ppt/media/")]
        charts = [n for n in names if re.match(r"ppt/charts/chart\d+\.xml$", n)]
        masters = [n for n in names if n.startswith("ppt/slideMasters/") and n.endswith(".xml")]
        layouts = [n for n in names if n.startswith("ppt/slideLayouts/") and n.endswith(".xml")]

        size = {}
        if "ppt/presentation.xml" in names:
            pres = ET.fromstring(zf.read("ppt/presentation.xml"))
            sldsz = pres.find("p:sldSz", NS)
            if sldsz is not None:
                size = dict(sldsz.attrib)

        fonts: collections.Counter[str] = collections.Counter()
        font_sizes: collections.Counter[int] = collections.Counter()
        colors: collections.Counter[str] = collections.Counter()
        slide_rows = []

        for idx, name in enumerate(slides, 1):
            root = ET.fromstring(zf.read(name))
            texts = [(t.text or "").strip() for t in root.findall(".//a:t", NS)]
            texts = [t for t in texts if t]
            joined = " ".join(texts)

            for latin in root.findall(".//a:latin", NS):
                typeface = latin.attrib.get("typeface")
                if typeface:
                    fonts[typeface] += 1
            for rpr in root.findall(".//a:rPr", NS):
                sz = rpr.attrib.get("sz")
                if sz and sz.isdigit():
                    font_sizes[int(sz) // 100] += 1
            for srgb in root.findall(".//a:srgbClr", NS):
                val = srgb.attrib.get("val")
                if val:
                    colors[val.upper()] += 1

            slide_rows.append(
                {
                    "slide": idx,
                    "chars": len(joined),
                    "text_runs": len(texts),
                    "shapes": len(root.findall(".//p:sp", NS)),
                    "pictures": len(root.findall(".//p:pic", NS)),
                    "graphics": len(root.findall(".//p:graphicFrame", NS)),
                    "tables": len(root.findall(".//a:tbl", NS)),
                    "charts": len(root.findall(".//c:chart", NS)),
                    "title_guess": joined[:160],
                }
            )

        return {
            "path": str(path),
            "slides": len(slides),
            "masters": len(masters),
            "layouts": len(layouts),
            "chart_count": len(charts),
            "slide_size_emu": size,
            "media_count": len(media),
            "media_extensions": collections.Counter(os.path.splitext(m)[1].lower() or "[none]" for m in media).most_common(),
            "top_fonts": fonts.most_common(12),
            "top_font_sizes_pt": font_sizes.most_common(12),
            "top_colors": colors.most_common(16),
            "slide_density": slide_rows,
        }


def analyze_pdf(path: Path) -> dict:
    result = {"path": str(path)}
    try:
        proc = subprocess.run(["pdfinfo", str(path)], check=False, capture_output=True, text=True)
        if proc.returncode == 0:
            for line in proc.stdout.splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    if key.strip() in {"Pages", "Page size", "File size", "PDF version", "Producer"}:
                        result[key.strip().lower().replace(" ", "_")] = value.strip()
    except FileNotFoundError:
        result["pdfinfo"] = "missing"

    try:
        proc = subprocess.run(["pdftotext", "-f", "1", "-l", "5", "-layout", str(path), "-"], check=False, capture_output=True, text=True)
        if proc.returncode == 0:
            lines = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
            result["first_pages_text_sample"] = lines[:40]
    except FileNotFoundError:
        result["pdftotext"] = "missing"

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pptx", type=Path)
    parser.add_argument("--pdf", type=Path)
    args = parser.parse_args()

    if not args.pptx and not args.pdf:
        parser.error("provide --pptx and/or --pdf")

    report = {}
    if args.pptx:
        report["pptx"] = analyze_pptx(args.pptx)
    if args.pdf:
        report["pdf"] = analyze_pdf(args.pdf)

    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
