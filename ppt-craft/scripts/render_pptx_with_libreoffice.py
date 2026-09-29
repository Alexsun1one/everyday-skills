#!/usr/bin/env python3
"""Render a PPTX through LibreOffice into PDF and optional PNG pages."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


DEFAULT_SOFFICE_CANDIDATES = [
    "soffice",
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    "/opt/homebrew/bin/soffice",
    "/usr/local/bin/soffice",
]


def resolve_executable(value: str | None, candidates: list[str]) -> str | None:
    if value:
        path = Path(value).expanduser()
        if path.exists():
            return str(path)
        found = shutil.which(value)
        return found or value
    for candidate in candidates:
        found = shutil.which(candidate)
        if found:
            return found
        path = Path(candidate)
        if path.exists():
            return str(path)
    return None


def run_command(cmd: list[str], cwd: Path | None = None) -> dict[str, Any]:
    proc = subprocess.run(cmd, cwd=str(cwd) if cwd else None, capture_output=True, text=True, check=False)
    return {
        "cmd": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }


def parse_pdfinfo(text: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for line in text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        normalized = key.strip().lower().replace(" ", "_")
        result[normalized] = value.strip()
    if "pages" in result:
        try:
            result["pages"] = int(result["pages"])
        except ValueError:
            pass
    return result


def render(pptx: Path, out_dir: Path, soffice_arg: str | None, dpi: int, png: bool, keep_profile: bool) -> dict[str, Any]:
    pptx = pptx.expanduser().resolve()
    out_dir = out_dir.expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    if not pptx.exists():
        raise SystemExit(f"PPTX not found: {pptx}")

    soffice = resolve_executable(soffice_arg, DEFAULT_SOFFICE_CANDIDATES)
    if not soffice:
        raise SystemExit("LibreOffice soffice executable not found")

    profile_tmp = tempfile.TemporaryDirectory(prefix="ppt-craft-lo-profile-")
    profile_dir = Path(profile_tmp.name)
    profile_uri = profile_dir.resolve().as_uri()
    pdf_path = out_dir / f"{pptx.stem}.pdf"
    if pdf_path.exists():
        pdf_path.unlink()

    lo_cmd = [
        soffice,
        "--headless",
        "--invisible",
        "--nologo",
        "--nodefault",
        "--nofirststartwizard",
        f"-env:UserInstallation={profile_uri}",
        "--convert-to",
        "pdf",
        "--outdir",
        str(out_dir),
        str(pptx),
    ]
    lo = run_command(lo_cmd)

    if lo["returncode"] != 0:
        if not keep_profile:
            profile_tmp.cleanup()
        return {
            "ok": False,
            "pptx": str(pptx),
            "out_dir": str(out_dir),
            "soffice": soffice,
            "libreoffice": lo,
            "error": "soffice conversion failed",
        }

    if not pdf_path.exists():
        pdfs = sorted(out_dir.glob("*.pdf"), key=lambda item: item.stat().st_mtime, reverse=True)
        if pdfs:
            pdf_path = pdfs[0]
    if not pdf_path.exists():
        if not keep_profile:
            profile_tmp.cleanup()
        return {
            "ok": False,
            "pptx": str(pptx),
            "out_dir": str(out_dir),
            "soffice": soffice,
            "libreoffice": lo,
            "error": "LibreOffice did not produce a PDF",
        }

    pdfinfo_cmd: dict[str, Any] | None = None
    pdfinfo = resolve_executable("pdfinfo", ["pdfinfo"])
    pdf_metadata: dict[str, Any] = {}
    if pdfinfo:
        pdfinfo_cmd = run_command([pdfinfo, str(pdf_path)])
        if pdfinfo_cmd["returncode"] == 0:
            pdf_metadata = parse_pdfinfo(pdfinfo_cmd["stdout"])

    png_cmd: dict[str, Any] | None = None
    png_files: list[str] = []
    if png:
        pdftoppm = resolve_executable("pdftoppm", ["pdftoppm"])
        if pdftoppm:
            prefix = out_dir / f"{pptx.stem}-lo"
            for old in out_dir.glob(f"{pptx.stem}-lo-*.png"):
                old.unlink()
            png_cmd = run_command([pdftoppm, "-png", "-r", str(dpi), str(pdf_path), str(prefix)])
            if png_cmd["returncode"] != 0:
                if not keep_profile:
                    profile_tmp.cleanup()
                return {
                    "ok": False,
                    "pptx": str(pptx),
                    "out_dir": str(out_dir),
                    "soffice": soffice,
                    "libreoffice": lo,
                    "pdf": str(pdf_path),
                    "pdfinfo": pdfinfo_cmd,
                    "pdftoppm": png_cmd,
                    "error": "pdftoppm conversion failed",
                }
            png_files = [str(path) for path in sorted(out_dir.glob(f"{pptx.stem}-lo-*.png"))]
        else:
            png_cmd = {"returncode": 127, "stdout": "", "stderr": "pdftoppm not found; PNG pages skipped"}

    report = {
        "ok": True,
        "pptx": str(pptx),
        "out_dir": str(out_dir),
        "soffice": soffice,
        "libreoffice": lo,
        "pdf": str(pdf_path),
        "pdf_metadata": pdf_metadata,
        "pdfinfo": pdfinfo_cmd,
        "png_pages": png_files,
        "png_count": len(png_files),
        "pdftoppm": png_cmd,
        "profile_dir": str(profile_dir) if keep_profile else None,
    }
    if not keep_profile:
        profile_tmp.cleanup()
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pptx", type=Path, help="PPTX file to render")
    parser.add_argument("--out-dir", type=Path, required=True, help="Output directory for PDF/PNG/report")
    parser.add_argument("--soffice", help="Optional soffice executable path")
    parser.add_argument("--dpi", type=int, default=144, help="PNG render DPI when pdftoppm is available")
    parser.add_argument("--no-png", action="store_true", help="Only render PDF; skip PNG page extraction")
    parser.add_argument("--keep-profile", action="store_true", help="Keep temporary LibreOffice user profile for debugging")
    parser.add_argument("--report", type=Path, help="Optional report JSON path")
    args = parser.parse_args()

    report = render(args.pptx, args.out_dir, args.soffice, args.dpi, not args.no_png, args.keep_profile)
    report_path = args.report or (args.out_dir / "libreoffice-render-report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if report.get("ok"):
        print(
            "libreoffice-render-ok "
            f"pdf={report.get('pdf')} png_pages={report.get('png_count', 0)} report={report_path.resolve()}"
        )
        return 0
    print(f"libreoffice-render-failed report={report_path.resolve()}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
