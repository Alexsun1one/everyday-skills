#!/usr/bin/env python3
"""Create a PNG contact sheet from slide screenshots."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("screenshots", type=Path)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--thumb-width", type=int, default=560)
    parser.add_argument("--columns", type=int, default=2)
    args = parser.parse_args()

    files = sorted(
        path for path in args.screenshots.glob("*.png")
        if not path.name.startswith("index") and "contact" not in path.name.lower()
    )
    if not files:
        raise SystemExit(f"no screenshots found in {args.screenshots}")

    first = Image.open(files[0])
    ratio = first.height / first.width
    thumb_w = args.thumb_width
    thumb_h = int(round(thumb_w * ratio))
    cols = max(1, args.columns)
    rows = math.ceil(len(files) / cols)
    pad = 28
    label_h = 30
    out = args.out or (args.screenshots / "contact-sheet.png")
    sheet = Image.new("RGB", (cols * thumb_w + (cols + 1) * pad, rows * (thumb_h + label_h) + (rows + 1) * pad), "#05070d")
    draw = ImageDraw.Draw(sheet)

    for index, path in enumerate(files):
        img = Image.open(path).convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        col = index % cols
        row = index // cols
        x = pad + col * (thumb_w + pad)
        y = pad + row * (thumb_h + label_h + pad)
        draw.text((x, y), path.stem, fill="#f2c96d")
        sheet.paste(img, (x, y + label_h))

    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    print(f"contact-sheet-written {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
