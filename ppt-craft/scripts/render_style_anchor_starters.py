#!/usr/bin/env python3
"""Render HTML starter preview decks for PPT Craft style anchors."""

from __future__ import annotations

import argparse
import html
import json
import math
import shutil
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_ANCHORS = SKILL_DIR / "assets" / "style-anchor-library.json"
DEFAULT_STARTERS = SKILL_DIR / "assets" / "style-anchor-starters.json"
ROLE_ORDER = ("cover", "proof", "system", "closing")
VARIANT_BY_ANCHOR = {
    "dark-technical-investor": "control-room",
    "studio-product-keynote": "center-product",
    "swiss-consulting-brief": "executive-grid",
    "data-desk-board-review": "data-desk",
    "editorial-research-atlas": "editorial-spread",
    "calm-clinical-trust": "clinical-protocol",
    "premium-minimal-luxury": "luxury-object",
    "paper-learning-workshop": "worksheet",
    "bold-founder-manifesto": "poster",
    "product-demo-workbench": "workbench",
    "civic-policy-brief": "map-brief",
    "creative-brand-campaign": "moodboard",
    "spatial-experience-showcase": "route-map",
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def slug(value: str) -> str:
    clean = "".join(ch if ch.isalnum() or ch in ("-", "_") else "-" for ch in value.strip().lower())
    return "-".join(part for part in clean.split("-") if part) or "starter"


def clean_hex(value: str | None, fallback: str) -> str:
    raw = str(value or fallback).strip().lstrip("#")
    if len(raw) == 3 and all(ch in "0123456789abcdefABCDEF" for ch in raw):
        raw = "".join(ch * 2 for ch in raw)
    if len(raw) == 6 and all(ch in "0123456789abcdefABCDEF" for ch in raw):
        return f"#{raw.upper()}"
    return fallback


def rgb(hex_color: str) -> tuple[int, int, int]:
    value = clean_hex(hex_color, "#000000").lstrip("#")
    return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)


def mix(a: str, b: str, amount: float) -> str:
    ar, ag, ab = rgb(a)
    br, bg, bb = rgb(b)
    amount = max(0.0, min(1.0, amount))
    return "#" + "".join(
        f"{round(left * (1 - amount) + right * amount):02X}"
        for left, right in ((ar, br), (ag, bg), (ab, bb))
    )


def luminance(hex_color: str) -> float:
    def channel(value: int) -> float:
        v = value / 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4

    r, g, b = rgb(hex_color)
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def readable_on(background: str) -> str:
    return "#F8FAFC" if luminance(background) < 0.42 else "#111827"


def anchor_maps(anchor_path: Path, starter_path: Path) -> tuple[dict[str, dict[str, Any]], dict[str, list[dict[str, Any]]], dict[str, Any]]:
    anchors_data = read_json(anchor_path)
    starters_data = read_json(starter_path)
    anchors = {
        str(anchor.get("id")): anchor
        for anchor in anchors_data.get("anchors", [])
        if isinstance(anchor, dict) and anchor.get("id")
    }
    starters = {
        str(item.get("anchor_id")): item.get("starters", [])
        for item in starters_data.get("anchors", [])
        if isinstance(item, dict) and item.get("anchor_id")
    }
    return anchors, starters, starters_data.get("stage", {"width": 1280, "height": 720})


def css_vars(anchor: dict[str, Any]) -> dict[str, str]:
    palette = anchor.get("palette", {}) if isinstance(anchor.get("palette"), dict) else {}
    bg = clean_hex(palette.get("background"), "#F8FAFC")
    surface = clean_hex(palette.get("surface"), mix(bg, "#FFFFFF", 0.18 if luminance(bg) < 0.42 else 0.72))
    primary = clean_hex(palette.get("primary"), readable_on(bg))
    accent = clean_hex(palette.get("accent") or palette.get("signal") or palette.get("warm"), "#2563EB")
    muted = clean_hex(palette.get("muted"), mix(primary, bg, 0.5))
    danger = clean_hex(palette.get("danger") or palette.get("warning"), "#EF4444")
    positive = clean_hex(palette.get("positive") or palette.get("success") or palette.get("green"), "#22C55E")
    line = mix(primary, bg, 0.72)
    soft = mix(accent, bg, 0.76)
    on_surface = readable_on(surface)
    return {
        "bg": bg,
        "surface": surface,
        "primary": primary,
        "text": clean_hex(palette.get("text"), primary),
        "accent": accent,
        "muted": muted,
        "danger": danger,
        "positive": positive,
        "line": line,
        "soft": soft,
        "on_surface": on_surface,
    }


def tag_list(items: list[Any]) -> str:
    return "".join(f"<span>{html.escape(str(item))}</span>" for item in items[:4])


def mini_table(starter: dict[str, Any], label: str = "Evidence") -> str:
    families = [str(item) for item in starter.get("object_families", [])][:3] or ["signal", "proof", "decision"]
    rows = "".join(
        f"<tr><td>{html.escape(item.title())}</td><td>{html.escape(text)}</td><td>{html.escape(outcome)}</td></tr>"
        for item, text, outcome in zip(
            (families + families)[:3],
            ("Primary object", "Readable proof zone", "Decision implication"),
            ("visible", "traceable", "clear"),
        )
    )
    return f"""
    <table class="mini-table">
      <thead><tr><th>{html.escape(label)}</th><th>Rule</th><th>State</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
    """


def metric_stack() -> str:
    return """
    <div class="metric-stack">
      <article><b>01</b><span>Dominant signal</span></article>
      <article><b>3x</b><span>Focused proof</span></article>
      <article><b>7d</b><span>Decision window</span></article>
    </div>
    """


def loop_nodes(labels: list[str] | None = None) -> str:
    labels = labels or ["Input", "Action", "Proof", "Next"]
    nodes = "".join(f"<article><b>{i}</b><span>{html.escape(label)}</span></article>" for i, label in enumerate(labels[:5], 1))
    return f'<section class="flow-line">{nodes}</section>'


def browser_mock() -> str:
    return """
    <div class="browser-mock">
      <header><i></i><i></i><i></i></header>
      <aside></aside>
      <main>
        <div class="screen-row wide"></div>
        <div class="screen-row"></div>
        <div class="screen-grid"><i></i><i></i><i></i><i></i></div>
      </main>
    </div>
    """


def route_map(label: str) -> str:
    return f"""
    <div class="route-map">
      <svg viewBox="0 0 620 360" aria-hidden="true">
        <path d="M42 270 C120 72 202 320 312 160 S506 80 574 246" fill="none" stroke="currentColor" stroke-width="10" stroke-linecap="round"/>
        <path d="M66 94 L250 82 L302 222 L514 210" fill="none" stroke="currentColor" stroke-width="2" opacity=".35"/>
        <circle cx="42" cy="270" r="18"/><circle cx="208" cy="206" r="18"/><circle cx="366" cy="124" r="18"/><circle cx="574" cy="246" r="18"/>
      </svg>
      <p>{html.escape(label)}</p>
    </div>
    """


def collage(label: str) -> str:
    return f"""
    <div class="collage">
      <i class="c1"></i><i class="c2"></i><i class="c3"></i><i class="c4"></i><i class="c5"></i>
      <strong>{html.escape(label)}</strong>
    </div>
    """


def proof_kit(variant: str, starter: dict[str, Any]) -> str:
    families = [str(item).title() for item in starter.get("object_families", [])][:4] or ["Signal", "Proof", "Implication"]
    labels = (families + ["Signal", "Proof", "Decision", "Risk"])[:4]
    if variant == "center-product":
        return f"""
        <section class="artifact proof-kit product-proof">
          <div class="metric-orbit"><i>01</i><i>3x</i><i>72%</i></div>
          <p>{html.escape(labels[0])} becomes visible around the product.</p>
        </section>
        """
    if variant == "executive-grid":
        return f"""
        <section class="artifact proof-kit memo-proof">
          <header>Decision memo</header>
          <div class="memo-row"><b>{html.escape(labels[0])}</b><span></span></div>
          <div class="memo-row"><b>{html.escape(labels[1])}</b><span></span></div>
          <footer></footer>
        </section>
        """
    if variant == "data-desk":
        return f"""
        <section class="artifact proof-kit dashboard-proof">
          <div class="kpi-row"><b>01</b><b>3x</b><b>7d</b></div>
          <svg viewBox="0 0 320 150"><polyline points="10,122 62,88 118,108 180,52 240,76 306,24" fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="round"/></svg>
        </section>
        """
    if variant == "editorial-spread":
        return f"""
        <section class="artifact proof-kit clipping-proof">
          <article><b>{html.escape(labels[0])}</b><span></span></article>
          <article><b>{html.escape(labels[1])}</b><span></span></article>
          <em>source trail</em>
        </section>
        """
    if variant == "clinical-protocol":
        return f"""
        <section class="artifact proof-kit protocol-proof">
          <label><i></i>{html.escape(labels[0])}</label>
          <label><i></i>{html.escape(labels[1])}</label>
          <label><i></i>{html.escape(labels[2])}</label>
        </section>
        """
    if variant == "luxury-object":
        return f"""
        <section class="artifact proof-kit provenance-proof">
          <div class="seal"></div>
          <div class="swatch-row"><i></i><i></i><i></i></div>
          <p>{html.escape(labels[0])} / {html.escape(labels[1])}</p>
        </section>
        """
    if variant == "worksheet":
        return f"""
        <section class="artifact proof-kit worksheet-proof">
          <article><b>check</b><span></span></article>
          <article><b>compare</b><span></span></article>
          <article><b>repeat</b><span></span></article>
        </section>
        """
    if variant == "poster":
        return f"""
        <section class="artifact proof-kit stamp-proof">
          <b>FACT</b>
          <p>{html.escape(str(starter.get("visual", ""))[:90])}</p>
        </section>
        """
    if variant == "workbench":
        return f"""
        <section class="artifact proof-kit workbench-proof">
          <div class="annotation a">1</div><div class="annotation b">2</div>
          <div class="mini-browser"><i></i><i></i><i></i></div>
        </section>
        """
    if variant in {"map-brief", "route-map"}:
        return f"""
        <section class="artifact proof-kit route-proof">
          <div class="route-dots"><i></i><i></i><i></i><i></i></div>
          <p>{html.escape(labels[0])} -> {html.escape(labels[1])} -> {html.escape(labels[2])}</p>
        </section>
        """
    if variant == "moodboard":
        return f"""
        <section class="artifact proof-kit territory-proof">
          <i></i><i></i><i></i><i></i>
          <p>{html.escape(labels[0])} territory</p>
        </section>
        """
    return f"""
    <section class="artifact proof-kit console-proof">
      <pre>detect -> interpret -> decide</pre>
      <div class="console-bars"><i></i><i></i><i></i></div>
    </section>
    """


def system_kit(variant: str, starter: dict[str, Any]) -> str:
    if variant in {"map-brief", "route-map"}:
        return f'<section class="artifact system-kit route-system">{route_map(str(starter.get("visual", ""))[:72])}</section>'
    if variant == "workbench":
        return """
        <section class="artifact system-kit workbench-system">
          <div class="pipeline-card"></div><div class="pipeline-card"></div><div class="pipeline-card"></div>
          <div class="cursor-path"></div>
        </section>
        """
    if variant == "poster":
        return """
        <section class="artifact system-kit manifesto-system">
          <b>OLD</b><b>BREAK</b><b>NEW</b><b>MOVE</b>
        </section>
        """
    if variant == "editorial-spread":
        return """
        <section class="artifact system-kit spread-system">
          <i></i><i></i><i></i><i></i>
        </section>
        """
    if variant == "clinical-protocol":
        return """
        <section class="artifact system-kit care-system">
          <label>screen</label><label>guide</label><label>monitor</label><label>escalate</label>
        </section>
        """
    if variant == "luxury-object":
        return """
        <section class="artifact system-kit ritual-system">
          <i></i><i></i><i></i>
        </section>
        """
    if variant == "worksheet":
        return """
        <section class="artifact system-kit worksheet-system">
          <div></div><div></div><div></div><div></div>
        </section>
        """
    if variant == "moodboard":
        return """
        <section class="artifact system-kit campaign-system">
          <i></i><i></i><i></i><i></i><i></i>
        </section>
        """
    if variant == "center-product":
        return """
        <section class="artifact system-kit product-system">
          <i></i><i></i><i></i><i></i>
        </section>
        """
    return f'<section class="artifact system-kit step-system">{loop_nodes(["Sense", "Frame", "Prove", "Commit"])}</section>'


def closing_kit(variant: str, starter: dict[str, Any]) -> str:
    qa = tag_list(starter.get("qa", []))
    direction = html.escape(str(starter.get("asset_direction", ""))[:130])
    if variant == "poster":
        return f'<section class="artifact close-kit poster-close"><b>ASK</b><p>{direction}</p><div class="tag-row">{qa}</div></section>'
    if variant == "luxury-object":
        return f'<section class="artifact close-kit quiet-close"><div class="seal"></div><p>{direction}</p><div class="tag-row">{qa}</div></section>'
    if variant in {"map-brief", "route-map"}:
        return f'<section class="artifact close-kit route-close"><div class="route-dots"><i></i><i></i><i></i></div><p>{direction}</p><div class="tag-row">{qa}</div></section>'
    return f'<section class="artifact close-kit standard-close"><blockquote>{direction}</blockquote><div class="tag-row">{qa}</div></section>'


def bespoke_visual(variant: str, role: str, starter: dict[str, Any]) -> str:
    visual = str(starter.get("visual") or starter.get("asset_direction") or "")
    families = tag_list(starter.get("object_families", []))
    if variant == "poster":
        huge = "NOW" if role == "cover" else ("FACT" if role == "proof" else ("SHIFT" if role == "system" else "GO"))
        return f'<section class="poster-slab"><b>{huge}</b><p>{html.escape(visual[:90])}</p></section><div class="tag-row">{families}</div>'
    if variant == "editorial-spread":
        return f'<section class="mag-spread"><figure></figure><aside><b>finding</b><p>{html.escape(visual[:110])}</p></aside><footer></footer></section>'
    if variant == "moodboard":
        return collage(visual[:90]) + f'<div class="tag-row">{families}</div>'
    if variant in {"map-brief", "route-map"}:
        return route_map(visual[:96]) + f'<div class="tag-row">{families}</div>'
    if variant == "workbench":
        return browser_mock() + f'<div class="pin p1">1</div><div class="pin p2">2</div><div class="tag-row">{families}</div>'
    if variant == "luxury-object":
        return f'<section class="object-stage"><div class="plinth"></div><div class="artifact"></div><div class="swatch"></div><p>{html.escape(visual[:86])}</p></section>'
    if variant == "worksheet":
        return f'<section class="workbook"><i class="tab"></i><i class="page a"></i><i class="page b"></i><i class="note"></i><p>{html.escape(visual[:80])}</p></section>'
    if variant == "clinical-protocol":
        return f'<section class="protocol"><i></i><i></i><i></i><b>safe</b></section><div class="tag-row">{families}</div>'
    if variant == "executive-grid":
        return f'<section class="issue-tree"><i></i><i></i><i></i><i></i><i></i></section><div class="tag-row">{families}</div>'
    if variant == "data-desk":
        return f'<section class="chart-desk"><svg viewBox="0 0 420 220"><polyline points="20,166 80,122 142,146 208,82 282,104 372,48" fill="none" stroke="currentColor" stroke-width="8" stroke-linecap="round"/><line x1="20" y1="180" x2="390" y2="180" stroke="currentColor" opacity=".25"/><line x1="20" y1="40" x2="20" y2="184" stroke="currentColor" opacity=".25"/></svg></section>{metric_stack()}'
    if variant == "center-product":
        return f'<section class="product-stage"><div class="device"></div><div class="halo-card"></div><p>{html.escape(visual[:80])}</p></section>'
    return f'<section class="technical-grid"><i></i><i></i><i></i><svg viewBox="0 0 420 260"><path d="M40 190 L120 90 L222 132 L340 62" fill="none" stroke="currentColor" stroke-width="6"/><circle cx="40" cy="190" r="16"/><circle cx="120" cy="90" r="16"/><circle cx="222" cy="132" r="16"/><circle cx="340" cy="62" r="16"/></svg></section><div class="tag-row">{families}</div>'


def bespoke_role_artifact(variant: str, role: str, starter: dict[str, Any]) -> str:
    if role == "proof":
        return proof_kit(variant, starter)
    if role == "system":
        return system_kit(variant, starter)
    if role == "closing":
        return closing_kit(variant, starter)
    return ""


def bespoke_slide_html(anchor: dict[str, Any], starter: dict[str, Any], index: int, total: int, stage: dict[str, Any]) -> str:
    role = str(starter.get("role", "starter"))
    anchor_id = str(anchor.get("id") or "")
    variant = VARIANT_BY_ANCHOR.get(anchor_id, "control-room")
    colors = css_vars(anchor)
    anchor_name = str(anchor.get("name") or anchor_id)
    headline = str(starter.get("headline") or anchor_name)
    support = str(starter.get("support") or anchor.get("visual_thesis", ""))
    visual = bespoke_visual(variant, role, starter)
    role_artifact = bespoke_role_artifact(variant, role, starter)
    thesis = str(anchor.get("visual_thesis") or "")
    grammar = str(anchor.get("layout_grammar") or "")
    muted_bg = mix(colors["bg"], "#FFFFFF", 0.12 if luminance(colors["bg"]) < 0.45 else 0.62)
    title_size = "72px" if variant == "poster" else ("52px" if role == "cover" else "42px")

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(anchor_name)} - {html.escape(role)}</title>
  <style>
    * {{ box-sizing: border-box; }}
    html, body {{ margin: 0; width: {stage['width']}px; height: {stage['height']}px; overflow: hidden; background: {colors['bg']}; color: {colors['text']}; font-family: "PingFang SC", "Microsoft YaHei", "Inter", "Aptos", Arial, sans-serif; }}
    .slide {{ position: relative; width: {stage['width']}px; height: {stage['height']}px; overflow: hidden; --bg:{colors['bg']}; --surface:{colors['surface']}; --muted-bg:{muted_bg}; --text:{colors['text']}; --primary:{colors['primary']}; --accent:{colors['accent']}; --muted:{colors['muted']}; --line:{colors['line']}; --soft:{colors['soft']}; --on-surface:{colors['on_surface']}; background: var(--bg); }}
    .chrome {{ position:absolute; left:44px; right:44px; top:28px; display:flex; justify-content:space-between; color:var(--muted); font-size:12px; font-weight:800; letter-spacing:0; }}
    .chrome b {{ color:var(--accent); }}
    .claim {{ position:absolute; z-index:2; background: color-mix(in srgb, var(--surface) 88%, transparent); color:var(--on-surface); border:1px solid color-mix(in srgb, var(--line) 80%, transparent); box-shadow:0 24px 70px rgba(0,0,0,.18); }}
    .claim .kicker {{ margin:0 0 18px; color:var(--accent); font-size:13px; font-weight:850; text-transform:uppercase; }}
    .claim h1 {{ margin:0; color:var(--on-surface); font-size:{title_size}; line-height:.98; font-weight:900; letter-spacing:0; }}
    .claim p {{ margin:22px 0 0; color:var(--muted); font-size:18px; line-height:1.36; font-weight:680; }}
    .visual {{ position:absolute; z-index:1; color:var(--accent); }}
    .caption {{ position:absolute; color:var(--muted); font-size:12px; line-height:1.35; font-weight:700; }}
    .tag-row {{ display:flex; flex-wrap:wrap; gap:8px; }}
    .tag-row span {{ display:inline-flex; min-height:27px; align-items:center; padding:0 10px; border-radius:999px; border:1px solid color-mix(in srgb, var(--line) 78%, transparent); color:var(--text); background:color-mix(in srgb, var(--surface) 72%, transparent); font-size:11px; font-weight:830; }}
    .artifact {{ position:absolute; z-index:3; }}
    .mini-table {{ width:360px; border-collapse:collapse; background:var(--surface); color:var(--on-surface); font-size:13px; box-shadow:0 18px 44px rgba(0,0,0,.18); }}
    .mini-table th,.mini-table td {{ padding:10px 12px; border:1px solid var(--line); text-align:left; }}
    .mini-table th {{ background:color-mix(in srgb, var(--primary) 88%, var(--bg)); color:{readable_on(colors['primary'])}; }}
    .metric-stack {{ display:grid; gap:10px; }}
    .metric-stack article {{ width:120px; min-height:76px; padding:12px; border-radius:10px; background:var(--accent); color:{readable_on(colors['accent'])}; box-shadow:0 14px 34px rgba(0,0,0,.18); }}
    .metric-stack b {{ display:block; font-size:28px; line-height:.9; }}
    .metric-stack span {{ display:block; margin-top:8px; font-size:11px; line-height:1.2; font-weight:760; }}
    .flow-line {{ display:flex; align-items:center; gap:18px; }}
    .flow-line article {{ width:112px; height:108px; border-radius:14px; background:var(--surface); color:var(--on-surface); border:1px solid var(--line); box-shadow:0 16px 38px rgba(0,0,0,.14); display:grid; place-items:center; text-align:center; padding:12px; }}
    .flow-line b {{ width:30px; height:30px; border-radius:50%; display:grid; place-items:center; background:var(--accent); color:{readable_on(colors['accent'])}; }}
    .flow-line span {{ font-size:12px; font-weight:820; }}
    .artifact-proof {{ right:76px; bottom:76px; display:flex; gap:18px; align-items:end; }}
    .artifact-system {{ left:110px; bottom:88px; }}
    .artifact-close {{ right:76px; top:158px; width:350px; min-height:230px; padding:26px; border-radius:16px; background:var(--surface); color:var(--on-surface); border:1px solid var(--line); box-shadow:0 20px 60px rgba(0,0,0,.18); }}
    .artifact-close blockquote {{ margin:0 0 24px; font-size:20px; line-height:1.34; font-weight:760; }}
    .proof-kit,.system-kit,.close-kit {{ position:absolute; z-index:4; color:var(--on-surface); background:color-mix(in srgb, var(--surface) 94%, transparent); border:1px solid var(--line); box-shadow:0 22px 64px rgba(0,0,0,.18); }}
    .proof-kit {{ right:78px; bottom:82px; width:430px; min-height:210px; padding:22px; border-radius:14px; }}
    .system-kit {{ left:74px; bottom:96px; width:500px; min-height:132px; padding:18px; border-radius:14px; }}
    .close-kit {{ right:82px; top:132px; width:350px; min-height:230px; padding:26px; border-radius:16px; }}
    .proof-kit p,.close-kit p {{ margin:0; color:var(--muted); font-size:14px; line-height:1.34; font-weight:760; }}
    .metric-orbit {{ position:relative; height:112px; }}
    .metric-orbit i {{ position:absolute; width:76px; height:76px; border-radius:50%; display:grid; place-items:center; background:var(--accent); color:{readable_on(colors['accent'])}; font-style:normal; font-size:20px; font-weight:900; }}
    .metric-orbit i:nth-child(1) {{ left:0; top:12px; }} .metric-orbit i:nth-child(2) {{ left:96px; top:0; }} .metric-orbit i:nth-child(3) {{ left:210px; top:18px; width:92px; height:92px; }}
    .memo-proof header {{ margin-bottom:18px; color:var(--accent); font-size:13px; font-weight:900; text-transform:uppercase; }}
    .memo-row {{ display:grid; grid-template-columns:120px 1fr; gap:16px; align-items:center; padding:12px 0; border-top:1px solid var(--line); }}
    .memo-row b {{ color:var(--text); font-size:14px; }} .memo-row span,.memo-proof footer {{ display:block; height:12px; border-radius:8px; background:var(--line); opacity:.62; }}
    .dashboard-proof .kpi-row {{ display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin-bottom:18px; }}
    .dashboard-proof .kpi-row b {{ height:58px; display:grid; place-items:center; border-radius:10px; background:var(--accent); color:{readable_on(colors['accent'])}; font-size:24px; }}
    .dashboard-proof svg {{ width:100%; height:96px; color:var(--accent); }}
    .clipping-proof {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; transform:rotate(-1deg); }}
    .clipping-proof article {{ min-height:126px; padding:16px; background:var(--muted-bg); border:1px solid var(--line); box-shadow:0 12px 24px rgba(0,0,0,.10); }}
    .clipping-proof b {{ display:block; color:var(--accent); font-size:14px; }} .clipping-proof span {{ display:block; margin-top:28px; height:36px; background:var(--line); opacity:.5; }}
    .clipping-proof em {{ grid-column:1 / 3; color:var(--muted); font-size:12px; font-style:normal; }}
    .protocol-proof label,.care-system label {{ display:flex; align-items:center; gap:12px; min-height:44px; font-size:14px; font-weight:820; border-bottom:1px solid var(--line); }}
    .protocol-proof i {{ width:20px; height:20px; border-radius:50%; background:var(--accent); display:inline-block; }}
    .seal {{ width:82px; height:82px; border-radius:50%; border:2px solid var(--accent); background:color-mix(in srgb, var(--accent) 13%, transparent); }}
    .swatch-row {{ display:flex; gap:10px; margin:22px 0 16px; }} .swatch-row i {{ width:62px; height:46px; background:var(--accent); opacity:.75; }}
    .worksheet-proof {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; transform:rotate(-1deg); }}
    .worksheet-proof article {{ min-height:150px; padding:14px; background:var(--muted-bg); border:1px solid var(--line); }}
    .worksheet-proof b {{ color:var(--accent); }} .worksheet-proof span {{ display:block; margin-top:28px; height:54px; border:1px dashed var(--line); }}
    .stamp-proof {{ background:var(--accent); color:{readable_on(colors['accent'])}; border-radius:0; }}
    .stamp-proof b {{ display:block; font-size:74px; line-height:.82; }} .stamp-proof p {{ margin-top:18px; color:inherit; opacity:.9; }}
    .workbench-proof .annotation {{ position:absolute; z-index:2; width:42px; height:42px; border-radius:50%; display:grid; place-items:center; background:var(--accent); color:{readable_on(colors['accent'])}; font-weight:900; }}
    .workbench-proof .annotation.a {{ left:54px; top:44px; }} .workbench-proof .annotation.b {{ right:60px; bottom:48px; }}
    .mini-browser {{ position:absolute; left:86px; top:64px; right:54px; bottom:42px; display:grid; gap:10px; }}
    .mini-browser i {{ display:block; border-radius:8px; background:var(--muted-bg); border:1px solid var(--line); }}
    .route-dots {{ display:flex; align-items:center; justify-content:space-between; margin:28px 0; }}
    .route-dots i {{ width:38px; height:38px; border-radius:50%; background:var(--accent); box-shadow:0 0 0 8px color-mix(in srgb, var(--accent) 18%, transparent); }}
    .territory-proof {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; background:color-mix(in srgb, var(--surface) 84%, var(--soft)); }}
    .territory-proof i {{ min-height:68px; background:color-mix(in srgb, var(--accent) 26%, var(--surface)); border:1px solid var(--line); }}
    .territory-proof p {{ grid-column:1 / 3; }}
    .console-proof pre {{ margin:0 0 18px; color:var(--accent); font-size:18px; font-weight:900; font-family:"JetBrains Mono","SFMono-Regular",monospace; }}
    .console-bars {{ display:grid; gap:12px; }} .console-bars i {{ height:28px; background:var(--muted-bg); border:1px solid var(--line); }}
    .route-system {{ padding:0; height:224px; width:520px; overflow:hidden; }}
    .route-system .route-map {{ border:0; border-radius:14px; }}
    .workbench-system {{ display:flex; align-items:center; justify-content:space-between; }}
    .pipeline-card {{ width:126px; height:92px; border-radius:10px; background:var(--muted-bg); border:1px solid var(--line); }}
    .cursor-path {{ position:absolute; left:72px; right:72px; top:64px; height:4px; background:var(--accent); }}
    .manifesto-system {{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; background:transparent; border:0; box-shadow:none; }}
    .manifesto-system b {{ display:grid; place-items:center; min-height:110px; background:var(--surface); border:1px solid var(--line); color:var(--accent); font-size:22px; }}
    .spread-system {{ display:grid; grid-template-columns:1.2fr .7fr 1fr .6fr; gap:12px; transform:rotate(-1deg); }}
    .spread-system i,.worksheet-system div,.campaign-system i,.product-system i,.ritual-system i {{ display:block; min-height:96px; background:var(--muted-bg); border:1px solid var(--line); }}
    .care-system {{ display:grid; grid-template-columns:repeat(4,1fr); gap:10px; background:transparent; border:0; box-shadow:none; }}
    .care-system label {{ justify-content:center; border:1px solid var(--line); background:var(--surface); border-radius:12px; }}
    .ritual-system {{ display:flex; justify-content:center; gap:18px; background:transparent; border:0; box-shadow:none; }}
    .ritual-system i {{ width:108px; min-height:108px; border-radius:50%; }}
    .worksheet-system,.campaign-system,.product-system {{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; background:transparent; border:0; box-shadow:none; }}
    .campaign-system {{ grid-template-columns:repeat(5,1fr); }}
    .product-system i {{ border-radius:18px; }}
    .step-system {{ background:transparent; border:0; box-shadow:none; padding:0; }}
    .standard-close blockquote {{ margin:0 0 24px; font-size:20px; line-height:1.34; font-weight:760; }}
    .poster-close {{ background:var(--surface); border-radius:0; }}
    .poster-close b {{ display:block; color:var(--accent); font-size:68px; line-height:.8; margin-bottom:22px; }}
    .quiet-close {{ background:transparent; box-shadow:none; border-color:color-mix(in srgb, var(--line) 42%, transparent); }}
    .quiet-close .seal {{ margin-bottom:24px; }}
    .route-close .route-dots {{ margin:0 0 22px; }}
    .anchor-line {{ position:absolute; left:44px; right:44px; bottom:26px; display:flex; justify-content:space-between; gap:28px; color:var(--muted); opacity:.54; font-size:10px; line-height:1.25; font-weight:780; }}
    .anchor-line span {{ max-width:46%; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
    .technical-grid,.chart-desk,.product-stage,.issue-tree,.mag-spread,.protocol,.object-stage,.workbook,.poster-slab,.browser-mock,.route-map,.collage {{ position:absolute; inset:0; overflow:hidden; }}
    .technical-grid {{ border:1px solid var(--line); background:linear-gradient(90deg, transparent 39px, color-mix(in srgb, var(--line) 24%, transparent) 40px),linear-gradient(transparent 39px, color-mix(in srgb, var(--line) 18%, transparent) 40px); background-size:40px 40px; border-radius:18px; }}
    .technical-grid i {{ position:absolute; border:1px solid var(--line); background:color-mix(in srgb, var(--surface) 42%, transparent); }}
    .technical-grid i:nth-child(1) {{ left:40px; top:50px; width:180px; height:110px; }}
    .technical-grid i:nth-child(2) {{ right:46px; top:88px; width:140px; height:170px; }}
    .technical-grid i:nth-child(3) {{ left:72px; bottom:52px; width:260px; height:90px; }}
    .technical-grid svg {{ position:absolute; left:62px; right:40px; bottom:58px; width:360px; height:220px; }}
    .technical-grid circle {{ fill:var(--bg); stroke:var(--accent); stroke-width:5; }}
    .product-stage {{ border-radius:28px; background:radial-gradient(circle at 50% 38%, color-mix(in srgb, var(--accent) 28%, transparent), transparent 36%); }}
    .device {{ position:absolute; left:50%; top:50%; width:330px; height:210px; transform:translate(-50%,-44%); border-radius:24px; background:var(--surface); border:1px solid var(--line); box-shadow:0 40px 100px rgba(0,0,0,.26); }}
    .device::before {{ content:""; position:absolute; left:28px; top:28px; right:28px; height:34px; border-radius:8px; background:var(--muted-bg); }}
    .device::after {{ content:""; position:absolute; left:28px; right:28px; bottom:30px; height:88px; border-radius:12px; background:color-mix(in srgb, var(--accent) 18%, var(--muted-bg)); }}
    .halo-card {{ position:absolute; right:86px; bottom:70px; width:138px; height:88px; border-radius:14px; background:color-mix(in srgb, var(--accent) 24%, var(--surface)); border:1px solid var(--line); }}
    .product-stage p,.object-stage p,.workbook p,.route-map p {{ position:absolute; left:38px; right:38px; bottom:30px; color:var(--muted); font-size:15px; line-height:1.28; font-weight:760; }}
    .issue-tree {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:16px; padding:46px; }}
    .issue-tree i {{ display:block; border-radius:8px; background:var(--surface); border:1px solid var(--line); box-shadow:0 12px 30px rgba(0,0,0,.10); }}
    .issue-tree i:first-child {{ grid-column:1 / 4; height:70px; }}
    .chart-desk svg {{ position:absolute; left:42px; top:42px; width:420px; height:220px; }}
    .chart-desk {{ border-radius:18px; background:color-mix(in srgb, var(--surface) 42%, transparent); border:1px solid var(--line); }}
    .mag-spread figure {{ position:absolute; left:32px; top:38px; width:318px; height:318px; margin:0; background:color-mix(in srgb, var(--accent) 24%, var(--surface)); }}
    .mag-spread aside {{ position:absolute; right:32px; top:58px; width:180px; color:var(--on-surface); background:var(--surface); border:1px solid var(--line); padding:22px; box-shadow:0 16px 44px rgba(0,0,0,.14); }}
    .mag-spread aside b {{ color:var(--accent); font-size:28px; }}
    .mag-spread footer {{ position:absolute; left:32px; right:32px; bottom:34px; height:18px; background:linear-gradient(90deg,var(--accent) 0 30%,var(--line) 30% 100%); }}
    .protocol i {{ position:absolute; left:72px; width:320px; height:74px; border-radius:14px; background:var(--surface); border:1px solid var(--line); box-shadow:0 12px 30px rgba(0,0,0,.10); }}
    .protocol i:nth-child(1) {{ top:74px; }} .protocol i:nth-child(2) {{ top:176px; }} .protocol i:nth-child(3) {{ top:278px; }}
    .protocol b {{ position:absolute; right:76px; top:168px; width:96px; height:96px; border-radius:50%; display:grid; place-items:center; background:var(--accent); color:{readable_on(colors['accent'])}; }}
    .object-stage .plinth {{ position:absolute; left:70px; right:70px; bottom:88px; height:54px; background:var(--surface); border:1px solid var(--line); }}
    .artifact {{ position:absolute; }}
    .object-stage .artifact,.object-stage .artifact-avoid {{ display:none; }}
    .object-stage .artifact + * {{ display:none; }}
    .object-stage .plinth + .artifact {{ display:block; }}
    .object-stage .artifact {{ left:160px; top:86px; width:152px; height:152px; transform:rotate(45deg); background:color-mix(in srgb, var(--accent) 24%, transparent); border:2px solid var(--accent); }}
    .object-stage .swatch {{ position:absolute; right:100px; bottom:160px; width:118px; height:88px; background:var(--accent); opacity:.65; }}
    .workbook .page,.workbook .note,.workbook .tab {{ position:absolute; background:var(--surface); border:1px solid var(--line); box-shadow:0 14px 36px rgba(0,0,0,.12); }}
    .workbook .tab {{ left:58px; top:44px; width:138px; height:38px; border-radius:10px 10px 0 0; background:var(--accent); }}
    .workbook .page.a {{ left:58px; top:82px; width:238px; height:280px; border-radius:12px; transform:rotate(-2deg); }}
    .workbook .page.b {{ right:72px; top:90px; width:190px; height:220px; border-radius:12px; transform:rotate(3deg); }}
    .workbook .note {{ left:270px; bottom:60px; width:180px; height:92px; border-radius:8px; background:color-mix(in srgb, var(--accent) 18%, var(--surface)); }}
    .poster-slab {{ background:var(--surface); color:var(--on-surface); display:grid; align-content:center; padding:38px; border:1px solid var(--line); }}
    .poster-slab b {{ font-size:86px; line-height:.82; letter-spacing:0; color:var(--accent); }}
    .poster-slab p {{ margin:22px 0 0; font-size:18px; line-height:1.22; font-weight:780; }}
    .browser-mock {{ border-radius:18px; background:var(--surface); color:var(--on-surface); border:1px solid var(--line); box-shadow:0 30px 80px rgba(0,0,0,.18); }}
    .browser-mock header {{ position:absolute; left:0; right:0; top:0; height:48px; background:color-mix(in srgb, var(--primary) 86%, var(--bg)); }}
    .browser-mock aside {{ position:absolute; left:0; top:48px; bottom:0; width:118px; background:color-mix(in srgb, var(--line) 32%, transparent); }}
    .browser-mock main {{ position:absolute; left:150px; top:82px; right:36px; bottom:36px; }}
    .screen-row,.screen-grid i {{ display:block; border-radius:10px; background:color-mix(in srgb, var(--accent) 14%, var(--muted-bg)); border:1px solid var(--line); }}
    .screen-row {{ height:64px; margin-bottom:20px; }} .screen-row.wide {{ width:88%; }}
    .screen-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:18px; }} .screen-grid i {{ height:104px; }}
    .pin {{ position:absolute; z-index:4; width:34px; height:34px; border-radius:50%; background:var(--accent); color:{readable_on(colors['accent'])}; display:grid; place-items:center; font-weight:900; }} .p1 {{ left:610px; top:160px; }} .p2 {{ right:92px; top:320px; }}
    .route-map {{ border-radius:20px; background:color-mix(in srgb, var(--surface) 42%, transparent); border:1px solid var(--line); }}
    .route-map svg {{ position:absolute; left:22px; top:44px; width:560px; height:310px; }} .route-map circle {{ fill:var(--surface); stroke:var(--accent); stroke-width:6; }}
    .collage i {{ position:absolute; background:color-mix(in srgb, var(--accent) 20%, var(--surface)); border:1px solid var(--line); box-shadow:0 14px 34px rgba(0,0,0,.12); }}
    .collage .c1 {{ left:36px; top:44px; width:210px; height:160px; }} .collage .c2 {{ left:276px; top:38px; width:250px; height:108px; }} .collage .c3 {{ left:300px; top:182px; width:160px; height:180px; }} .collage .c4 {{ right:44px; bottom:50px; width:184px; height:150px; }} .collage .c5 {{ left:54px; bottom:70px; width:180px; height:90px; }}
    .collage strong {{ position:absolute; left:44px; right:44px; bottom:28px; color:var(--text); font-size:18px; line-height:1.18; }}
    .slide.variant-control-room .claim {{ left:58px; top:82px; width:470px; padding:28px; border-radius:8px; }}
    .slide.variant-control-room .visual {{ left:586px; top:72px; width:560px; height:430px; }}
    .slide.variant-center-product .claim {{ left:230px; top:68px; width:820px; padding:30px; border-radius:18px; text-align:center; }}
    .slide.variant-center-product .claim h1 {{ max-width:760px; margin:auto; }}
    .slide.variant-center-product .visual {{ left:220px; top:316px; width:840px; height:270px; }}
    .slide.variant-executive-grid .claim {{ left:70px; top:74px; width:560px; padding:30px; border-radius:4px; }}
    .slide.variant-executive-grid .visual {{ left:700px; top:82px; width:450px; height:344px; }}
    .slide.variant-data-desk .claim {{ left:58px; top:76px; width:500px; padding:28px; border-radius:6px; }}
    .slide.variant-data-desk .visual {{ left:620px; top:76px; width:560px; height:370px; }}
    .slide.variant-editorial-spread .claim {{ left:706px; top:88px; width:440px; padding:30px; border-radius:2px; }}
    .slide.variant-editorial-spread .visual {{ left:70px; top:86px; width:570px; height:430px; }}
    .slide.variant-clinical-protocol .claim {{ left:82px; top:88px; width:520px; padding:28px; border-radius:18px; }}
    .slide.variant-clinical-protocol .visual {{ left:660px; top:86px; width:500px; height:386px; }}
    .slide.variant-luxury-object .claim {{ left:90px; top:110px; width:440px; padding:0; background:transparent; border:0; box-shadow:none; }}
    .slide.variant-luxury-object .claim h1 {{ font-family:Georgia,serif; font-weight:650; }}
    .slide.variant-luxury-object .visual {{ left:670px; top:76px; width:430px; height:440px; }}
    .slide.variant-worksheet .claim {{ left:84px; top:78px; width:500px; padding:28px; border-radius:10px; transform:rotate(-1deg); }}
    .slide.variant-worksheet .visual {{ left:650px; top:76px; width:520px; height:430px; }}
    .slide.variant-poster .claim {{ left:58px; top:70px; width:760px; padding:38px; border-radius:0; }}
    .slide.variant-poster .visual {{ left:860px; top:86px; width:300px; height:430px; }}
    .slide.variant-poster .claim .kicker {{ display:inline-block; padding:5px 9px; color:#111111; background:var(--accent); }}
    .slide.variant-poster .claim p {{ color:#272727; }}
    .slide.variant-poster .tag-row span {{ color:#111111; background:var(--accent); border-color:#111111; }}
    .slide.variant-poster .poster-slab {{ background:var(--accent); color:#111111; border-color:#111111; }}
    .slide.variant-poster .poster-slab b,.slide.variant-poster .poster-slab p {{ color:#111111; }}
    .slide.variant-poster .manifesto-system b {{ color:#111111; background:var(--accent); border-color:#111111; }}
    .slide.variant-poster .poster-close {{ background:var(--accent); color:#111111; border-color:#111111; }}
    .slide.variant-poster .poster-close b,.slide.variant-poster .poster-close p {{ color:#111111; }}
    .slide.variant-workbench .claim {{ left:58px; top:84px; width:420px; padding:28px; border-radius:14px; }}
    .slide.variant-workbench .visual {{ left:520px; top:70px; width:660px; height:470px; }}
    .slide.variant-map-brief .claim {{ left:76px; top:90px; width:480px; padding:28px; border-radius:12px; }}
    .slide.variant-map-brief .visual {{ left:610px; top:78px; width:560px; height:430px; }}
    .slide.variant-moodboard .claim {{ left:70px; top:80px; width:460px; padding:28px; border-radius:12px; }}
    .slide.variant-moodboard .visual {{ left:590px; top:64px; width:585px; height:480px; }}
    .slide.variant-route-map .claim {{ left:70px; top:76px; width:460px; padding:28px; border-radius:10px; }}
    .slide.variant-route-map .visual {{ left:580px; top:70px; width:600px; height:470px; }}
    .role-cover .claim {{ min-height:0; }}
    .role-cover .anchor-line {{ opacity:.28; }}
    .role-proof .claim {{ width:420px; min-height:0; }}
    .role-proof .visual {{ opacity:.42; transform:scale(.92); transform-origin:center; }}
    .role-proof .artifact-proof {{ right:70px; bottom:92px; }}
    .role-system .claim {{ width:390px; min-height:0; }}
    .role-system .visual {{ opacity:.56; transform:scale(.92); transform-origin:center; }}
    .role-system .artifact-system {{ left:74px; bottom:106px; }}
    .role-closing .claim {{ min-height:0; }}
    .role-closing .visual {{ opacity:.42; transform:scale(.94); transform-origin:center; }}
    .role-closing .artifact-close {{ right:86px; top:122px; }}
  </style>
</head>
<body>
  <main class="slide variant-{html.escape(variant)} role-{html.escape(role)}" aria-label="{html.escape(anchor_name)} {html.escape(role)} starter">
    <div class="chrome"><b>{html.escape(anchor_name)}</b><span>{index:02d}/{total:02d} · {html.escape(role)} · {html.escape(str(starter.get("archetype") or ""))}</span></div>
    <section class="claim">
      <p class="kicker">{html.escape(anchor_id)}</p>
      <h1>{html.escape(headline)}</h1>
      <p>{html.escape(support)}</p>
    </section>
    <section class="visual">{visual}</section>
    {role_artifact}
    <div class="anchor-line" data-visual-qa-ignore="true"><span>{html.escape(thesis)}</span><span>{html.escape(grammar)}</span></div>
  </main>
</body>
</html>
"""


def proof_rows(starter: dict[str, Any]) -> str:
    families = [str(item) for item in starter.get("object_families", [])][:3]
    if len(families) < 3:
        families += ["signal", "evidence", "decision"][len(families):]
    return "".join(
        f"<tr><td>{html.escape(family.title())}</td><td>{html.escape(text)}</td><td>{html.escape(outcome)}</td></tr>"
        for family, text, outcome in zip(
            families,
            ("Use one dominant object", "Reserve the proof region", "State the implication"),
            ("Readable", "Traceable", "Decidable"),
        )
    )


def role_visual(role: str, starter: dict[str, Any], variant: str) -> str:
    families = tag_list(starter.get("object_families", []))
    if role == "cover":
        if variant == "poster":
            return f"""
            <div class="poster-field">
              <div class="poster-word">NOW</div>
              <div class="poster-stamp">{html.escape(str(starter.get("visual", ""))[:48])}</div>
            </div>
            <div class="tag-row visual-tags">{families}</div>
            """
        if variant == "editorial-spread":
            return f"""
            <div class="magazine-spread">
              <div class="image-crop"></div>
              <div class="caption-lines"><i></i><i></i><i></i></div>
              <div class="pullquote">finding</div>
            </div>
            <div class="tag-row visual-tags">{families}</div>
            """
        if variant == "moodboard":
            return f"""
            <div class="moodboard-grid">
              <i></i><i></i><i></i><i></i><i></i>
              <b>{html.escape(str(starter.get("visual", ""))[:34])}</b>
            </div>
            <div class="tag-row visual-tags">{families}</div>
            """
        if variant in {"map-brief", "route-map"}:
            return f"""
            <div class="route-stage">
              <svg viewBox="0 0 500 300" aria-hidden="true">
                <path d="M40 220 C120 100, 180 250, 260 120 S410 86, 460 190" fill="none" stroke="currentColor" stroke-width="10" stroke-linecap="round"/>
                <circle cx="40" cy="220" r="18"/><circle cx="205" cy="170" r="18"/><circle cx="350" cy="105" r="18"/><circle cx="460" cy="190" r="18"/>
              </svg>
              <div class="route-label">{html.escape(str(starter.get("visual", ""))[:62])}</div>
            </div>
            <div class="tag-row visual-tags">{families}</div>
            """
        if variant == "workbench":
            return f"""
            <div class="ui-window">
              <div class="ui-top"></div>
              <div class="ui-side"></div>
              <div class="ui-panel a"></div>
              <div class="ui-panel b"></div>
              <div class="ui-panel c"></div>
            </div>
            <div class="tag-row visual-tags">{families}</div>
            """
        if variant == "luxury-object":
            return f"""
            <div class="luxury-stage">
              <div class="plinth"></div>
              <div class="object-gem"></div>
              <div class="material-swatch"></div>
            </div>
            <div class="tag-row visual-tags">{families}</div>
            """
        if variant == "worksheet":
            return f"""
            <div class="worksheet-stage">
              <div class="tab"></div><div class="paper a"></div><div class="paper b"></div><div class="paper c"></div>
            </div>
            <div class="tag-row visual-tags">{families}</div>
            """
        if variant == "clinical-protocol":
            return f"""
            <div class="protocol-stack">
              <div class="care-card"></div><div class="care-card"></div><div class="care-card"></div>
              <div class="safety-badge">safe</div>
            </div>
            <div class="tag-row visual-tags">{families}</div>
            """
        return f"""
        <div class="hero-object">
          <div class="orb"></div>
          <div class="object-card one"></div>
          <div class="object-card two"></div>
          <div class="object-card three"></div>
          <div class="object-label">{html.escape(str(starter.get("visual", "")))}</div>
        </div>
        <div class="tag-row visual-tags">{families}</div>
        """
    if role == "proof":
        return f"""
        <table class="proof-table">
          <thead><tr><th>Object</th><th>Rule</th><th>Result</th></tr></thead>
          <tbody>{proof_rows(starter)}</tbody>
        </table>
        <aside class="signal-card"><b>Signal</b><strong>1</strong><span>dominant proof</span></aside>
        """
    if role == "system":
        nodes = ["Input", "Action", "Proof", "Next"]
        node_html = "".join(f'<div class="node"><b>{index}</b><span>{label}</span></div>' for index, label in enumerate(nodes, 1))
        return f"""
        <div class="loop">
          <div class="loop-line"></div>
          {node_html}
        </div>
        <div class="tag-row visual-tags">{families}</div>
        """
    return f"""
    <div class="closing-card">
      <p>{html.escape(str(starter.get("asset_direction", "")))}</p>
      <div class="tag-row">{families}</div>
    </div>
    <div class="final-mark"></div>
    """


def slide_html(anchor: dict[str, Any], starter: dict[str, Any], index: int, total: int, stage: dict[str, Any]) -> str:
    role = str(starter.get("role", "starter"))
    anchor_id = str(anchor.get("id") or "")
    variant = VARIANT_BY_ANCHOR.get(anchor_id, "control-room")
    colors = css_vars(anchor)
    anchor_name = str(anchor.get("name") or anchor.get("id"))
    headline = str(starter.get("headline") or anchor_name)
    support = str(starter.get("support") or anchor.get("visual_thesis", ""))
    visual = role_visual(role, starter, variant)
    qa = tag_list(starter.get("qa", []))
    archetype = str(starter.get("archetype") or "")
    visual_thesis = str(anchor.get("visual_thesis") or "")
    typography = str(anchor.get("typography") or "")
    motion = str(anchor.get("motion") or "")
    bg_overlay = "radial-gradient(circle at 74% 28%, var(--soft), transparent 30%), linear-gradient(135deg, var(--bg), var(--bg2))"
    if luminance(colors["bg"]) > 0.7:
        bg_overlay = "radial-gradient(circle at 76% 24%, var(--soft), transparent 28%), linear-gradient(135deg, var(--bg), var(--surface))"

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(anchor_name)} - {html.escape(role)}</title>
  <style>
    * {{ box-sizing: border-box; }}
    html, body {{ margin: 0; width: {stage['width']}px; height: {stage['height']}px; overflow: hidden; background: {colors['bg']}; color: {colors['text']}; font-family: "PingFang SC", "Microsoft YaHei", "Inter", "Aptos", Arial, sans-serif; }}
    .slide {{ position: relative; width: {stage['width']}px; height: {stage['height']}px; overflow: hidden; --bg: {colors['bg']}; --bg2: {mix(colors['bg'], '#000000', 0.14)}; --surface: {colors['surface']}; --primary: {colors['primary']}; --text: {colors['text']}; --accent: {colors['accent']}; --muted: {colors['muted']}; --danger: {colors['danger']}; --positive: {colors['positive']}; --line: {colors['line']}; --soft: {colors['soft']}; --on-surface: {colors['on_surface']}; background: {bg_overlay}; }}
    .chrome {{ position: absolute; left: 42px; top: 28px; right: 42px; display: flex; justify-content: space-between; align-items: center; color: var(--muted); font-size: 13px; font-weight: 780; letter-spacing: 0; }}
    .chrome span:first-child {{ color: var(--accent); }}
    .claim {{ position: absolute; left: 72px; top: 96px; width: 548px; min-height: 264px; padding: 30px 32px; background: color-mix(in srgb, var(--surface) 88%, transparent); border: 1px solid color-mix(in srgb, var(--line) 72%, transparent); border-radius: 10px; box-shadow: 0 24px 72px rgba(0,0,0,.20); }}
    .kicker {{ margin: 0 0 18px; color: var(--accent); font-size: 15px; line-height: 1.1; font-weight: 840; }}
    h1 {{ margin: 0; color: var(--text); font-size: 48px; line-height: 1.04; font-weight: 880; letter-spacing: 0; max-width: 486px; }}
    .support {{ margin: 24px 0 0; color: var(--muted); font-size: 20px; line-height: 1.38; font-weight: 640; }}
    .visual {{ position: absolute; left: 680px; top: 96px; width: 500px; height: 420px; }}
    .hero-object {{ position: absolute; inset: 0; border: 1px solid color-mix(in srgb, var(--line) 70%, transparent); border-radius: 18px; background: color-mix(in srgb, var(--surface) 52%, transparent); box-shadow: inset 0 0 0 1px rgba(255,255,255,.05), 0 28px 80px rgba(0,0,0,.24); }}
    .orb {{ position: absolute; right: 70px; top: 58px; width: 178px; height: 178px; border-radius: 999px; border: 2px solid var(--accent); background: color-mix(in srgb, var(--accent) 24%, transparent); }}
    .object-card {{ position: absolute; border-radius: 8px; background: var(--surface); border: 1px solid var(--line); box-shadow: 0 16px 34px rgba(0,0,0,.16); }}
    .object-card.one {{ left: 54px; top: 86px; width: 170px; height: 110px; }}
    .object-card.two {{ left: 124px; top: 226px; width: 220px; height: 82px; }}
    .object-card.three {{ right: 56px; bottom: 48px; width: 130px; height: 96px; background: color-mix(in srgb, var(--accent) 24%, var(--surface)); }}
    .object-label {{ position: absolute; left: 34px; right: 34px; bottom: 28px; color: var(--muted); font-size: 15px; line-height: 1.28; font-weight: 720; }}
    .tag-row {{ display: flex; flex-wrap: wrap; gap: 10px; }}
    .tag-row span {{ display: inline-flex; align-items: center; min-height: 30px; padding: 0 12px; border-radius: 999px; color: var(--text); background: color-mix(in srgb, var(--surface) 76%, transparent); border: 1px solid color-mix(in srgb, var(--line) 78%, transparent); font-size: 12px; font-weight: 820; }}
    .visual-tags {{ position: absolute; left: 0; right: 0; bottom: -58px; }}
    .proof-table {{ position: absolute; left: 0; top: 46px; width: 340px; border-collapse: collapse; color: var(--on-surface); font-size: 14px; line-height: 1.25; background: var(--surface); box-shadow: 0 20px 54px rgba(0,0,0,.20); }}
    .proof-table th, .proof-table td {{ border: 1px solid var(--line); padding: 13px 14px; text-align: left; }}
    .proof-table th {{ background: color-mix(in srgb, var(--primary) 86%, var(--bg)); color: {readable_on(colors['primary'])}; font-weight: 860; }}
    .proof-table td:first-child {{ color: var(--accent); font-weight: 860; }}
    .signal-card {{ position: absolute; right: 0; top: 86px; width: 142px; height: 198px; padding: 18px; border-radius: 14px; background: var(--accent); color: {readable_on(colors['accent'])}; box-shadow: 0 24px 70px rgba(0,0,0,.24); }}
    .signal-card b {{ display: block; font-size: 13px; text-transform: uppercase; }}
    .signal-card strong {{ display: block; margin-top: 22px; font-size: 80px; line-height: .8; }}
    .signal-card span {{ display: block; margin-top: 18px; font-size: 14px; line-height: 1.2; font-weight: 760; }}
    .loop {{ position: absolute; inset: 36px 0 0; height: 300px; }}
    .loop-line {{ position: absolute; left: 42px; right: 42px; top: 148px; height: 4px; background: var(--accent); border-radius: 4px; }}
    .node {{ position: absolute; top: 88px; width: 98px; height: 122px; border-radius: 14px; background: var(--surface); border: 1px solid var(--line); box-shadow: 0 18px 44px rgba(0,0,0,.18); display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; color: var(--on-surface); }}
    .node:nth-child(2) {{ left: 22px; }}
    .node:nth-child(3) {{ left: 148px; }}
    .node:nth-child(4) {{ left: 274px; }}
    .node:nth-child(5) {{ left: 400px; }}
    .node b {{ width: 34px; height: 34px; border-radius: 999px; background: var(--accent); color: {readable_on(colors['accent'])}; display: grid; place-items: center; font-size: 15px; }}
    .node span {{ font-size: 14px; font-weight: 820; }}
    .closing-card {{ position: absolute; left: 40px; top: 62px; width: 398px; min-height: 230px; padding: 30px; border-radius: 18px; background: var(--surface); color: var(--on-surface); border: 1px solid var(--line); box-shadow: 0 24px 72px rgba(0,0,0,.20); }}
    .closing-card p {{ margin: 0 0 30px; font-size: 20px; line-height: 1.36; font-weight: 760; }}
    .final-mark {{ position: absolute; right: 66px; bottom: 54px; width: 168px; height: 168px; border-radius: 28px; border: 3px solid var(--accent); transform: rotate(-8deg); background: color-mix(in srgb, var(--accent) 16%, transparent); }}
    .bottom {{ position: absolute; left: 72px; right: 72px; bottom: 46px; display: grid; grid-template-columns: 1.2fr 1fr 1fr; gap: 18px; align-items: end; }}
    .note {{ min-height: 74px; padding: 14px 16px; border-radius: 10px; background: color-mix(in srgb, var(--surface) 72%, transparent); border: 1px solid color-mix(in srgb, var(--line) 70%, transparent); color: var(--muted); font-size: 13px; line-height: 1.32; font-weight: 680; overflow: hidden; }}
    .note b {{ display: block; margin-bottom: 6px; color: var(--accent); font-size: 11px; text-transform: uppercase; letter-spacing: .04em; }}
    .qa {{ grid-column: span 2; }}
    .variant-center-product .claim {{ left: 230px; top: 74px; width: 820px; min-height: 208px; text-align: center; }}
    .variant-center-product .claim h1 {{ max-width: 760px; margin: 0 auto; }}
    .variant-center-product .visual {{ left: 230px; top: 326px; width: 820px; height: 260px; }}
    .variant-center-product .bottom {{ left: 150px; right: 150px; bottom: 30px; }}
    .variant-executive-grid .claim {{ left: 72px; top: 74px; width: 600px; min-height: 210px; }}
    .variant-executive-grid .visual {{ left: 720px; top: 94px; width: 450px; height: 320px; }}
    .variant-executive-grid .bottom {{ bottom: 42px; }}
    .variant-data-desk .claim {{ left: 64px; top: 72px; width: 520px; min-height: 250px; }}
    .variant-data-desk .visual {{ left: 628px; top: 72px; width: 560px; height: 420px; }}
    .variant-data-desk .bottom {{ left: 64px; right: 64px; bottom: 38px; grid-template-columns: 1fr 1fr 1.2fr; }}
    .variant-editorial-spread .claim {{ left: 690px; top: 88px; width: 460px; min-height: 312px; }}
    .variant-editorial-spread .visual {{ left: 72px; top: 88px; width: 540px; height: 420px; }}
    .variant-editorial-spread .bottom {{ left: 72px; right: 72px; bottom: 42px; }}
    .variant-clinical-protocol .claim {{ left: 82px; top: 88px; width: 520px; min-height: 240px; }}
    .variant-clinical-protocol .visual {{ left: 660px; top: 86px; width: 500px; height: 360px; }}
    .variant-luxury-object .claim {{ left: 92px; top: 104px; width: 460px; min-height: 260px; background: transparent; box-shadow: none; border-color: color-mix(in srgb, var(--line) 38%, transparent); }}
    .variant-luxury-object .visual {{ left: 670px; top: 76px; width: 420px; height: 430px; }}
    .variant-luxury-object .bottom {{ left: 92px; right: 92px; bottom: 52px; }}
    .variant-worksheet .claim {{ left: 88px; top: 78px; width: 500px; min-height: 250px; transform: rotate(-1deg); }}
    .variant-worksheet .visual {{ left: 662px; top: 82px; width: 500px; height: 390px; }}
    .variant-poster .claim {{ left: 72px; top: 74px; width: 760px; min-height: 316px; border-radius: 2px; }}
    .variant-poster .claim h1 {{ font-size: 58px; line-height: .96; max-width: 690px; }}
    .variant-poster .visual {{ left: 870px; top: 88px; width: 280px; height: 420px; }}
    .variant-poster .bottom {{ left: 72px; right: 72px; bottom: 34px; grid-template-columns: .9fr .9fr 1.4fr; }}
    .variant-workbench .claim {{ left: 68px; top: 82px; width: 430px; min-height: 240px; }}
    .variant-workbench .visual {{ left: 535px; top: 74px; width: 645px; height: 450px; }}
    .variant-map-brief .claim {{ left: 78px; top: 92px; width: 490px; min-height: 250px; }}
    .variant-map-brief .visual {{ left: 620px; top: 80px; width: 540px; height: 430px; }}
    .variant-moodboard .claim {{ left: 74px; top: 82px; width: 470px; min-height: 252px; }}
    .variant-moodboard .visual {{ left: 596px; top: 70px; width: 570px; height: 470px; }}
    .variant-route-map .claim {{ left: 74px; top: 78px; width: 470px; min-height: 270px; }}
    .variant-route-map .visual {{ left: 590px; top: 74px; width: 590px; height: 452px; }}
    .poster-field {{ position:absolute; inset:0; display:grid; place-items:center; border:1px solid var(--line); background:color-mix(in srgb, var(--accent) 18%, transparent); color:var(--accent); }}
    .poster-word {{ font-size:82px; font-weight:950; line-height:.85; letter-spacing:0; }}
    .poster-stamp {{ position:absolute; left:24px; right:24px; bottom:24px; color:var(--text); font-size:15px; line-height:1.22; font-weight:830; }}
    .magazine-spread, .moodboard-grid, .route-stage, .ui-window, .luxury-stage, .worksheet-stage, .protocol-stack {{ position:absolute; inset:0; border-radius:18px; border:1px solid var(--line); background:color-mix(in srgb, var(--surface) 70%, transparent); box-shadow:0 28px 80px rgba(0,0,0,.18); overflow:hidden; }}
    .image-crop {{ position:absolute; left:32px; top:34px; width:300px; height:280px; background:color-mix(in srgb, var(--accent) 28%, var(--surface)); }}
    .caption-lines {{ position:absolute; right:34px; top:44px; width:132px; display:grid; gap:14px; }}
    .caption-lines i {{ height:10px; background:var(--line); }}
    .pullquote {{ position:absolute; right:34px; bottom:44px; color:var(--accent); font-size:34px; font-weight:900; }}
    .moodboard-grid i {{ position:absolute; background:color-mix(in srgb, var(--accent) 20%, var(--surface)); border:1px solid var(--line); }}
    .moodboard-grid i:nth-child(1) {{ left:28px; top:34px; width:190px; height:150px; }}
    .moodboard-grid i:nth-child(2) {{ left:250px; top:30px; width:270px; height:94px; }}
    .moodboard-grid i:nth-child(3) {{ left:248px; top:154px; width:138px; height:150px; }}
    .moodboard-grid i:nth-child(4) {{ right:34px; bottom:34px; width:178px; height:150px; }}
    .moodboard-grid i:nth-child(5) {{ left:40px; bottom:46px; width:168px; height:98px; }}
    .moodboard-grid b {{ position:absolute; left:38px; right:38px; bottom:28px; color:var(--text); font-size:18px; line-height:1.18; }}
    .route-stage svg {{ position:absolute; left:22px; top:58px; width:456px; height:280px; color:var(--accent); }}
    .route-stage circle {{ fill:var(--surface); stroke:var(--accent); stroke-width:6; }}
    .route-label {{ position:absolute; left:36px; right:36px; bottom:30px; color:var(--text); font-size:16px; line-height:1.26; font-weight:780; }}
    .ui-top {{ position:absolute; left:0; right:0; top:0; height:48px; background:color-mix(in srgb, var(--primary) 86%, var(--bg)); }}
    .ui-side {{ position:absolute; left:0; top:48px; bottom:0; width:112px; background:color-mix(in srgb, var(--line) 32%, transparent); }}
    .ui-panel {{ position:absolute; background:var(--surface); border:1px solid var(--line); border-radius:10px; }}
    .ui-panel.a {{ left:144px; top:82px; width:360px; height:126px; }}
    .ui-panel.b {{ left:144px; top:238px; width:220px; height:150px; }}
    .ui-panel.c {{ right:36px; top:238px; width:200px; height:150px; background:color-mix(in srgb, var(--accent) 22%, var(--surface)); }}
    .plinth {{ position:absolute; left:72px; right:72px; bottom:76px; height:52px; background:var(--surface); border:1px solid var(--line); }}
    .object-gem {{ position:absolute; left:144px; top:74px; width:150px; height:150px; transform:rotate(45deg); background:color-mix(in srgb, var(--accent) 26%, transparent); border:2px solid var(--accent); }}
    .material-swatch {{ position:absolute; right:82px; bottom:154px; width:118px; height:86px; background:var(--accent); opacity:.72; }}
    .worksheet-stage .paper {{ position:absolute; background:var(--surface); border:1px solid var(--line); border-radius:10px; box-shadow:0 16px 34px rgba(0,0,0,.12); }}
    .worksheet-stage .tab {{ position:absolute; left:44px; top:30px; width:130px; height:38px; background:var(--accent); border-radius:10px 10px 0 0; }}
    .worksheet-stage .paper.a {{ left:44px; top:78px; width:230px; height:270px; transform:rotate(-2deg); }}
    .worksheet-stage .paper.b {{ right:62px; top:86px; width:180px; height:190px; transform:rotate(3deg); }}
    .worksheet-stage .paper.c {{ left:250px; bottom:46px; width:180px; height:100px; }}
    .protocol-stack .care-card {{ position:absolute; left:78px; width:332px; height:72px; border-radius:12px; background:var(--surface); border:1px solid var(--line); }}
    .protocol-stack .care-card:nth-child(1) {{ top:74px; }}
    .protocol-stack .care-card:nth-child(2) {{ top:174px; }}
    .protocol-stack .care-card:nth-child(3) {{ top:274px; }}
    .safety-badge {{ position:absolute; right:62px; top:156px; width:92px; height:92px; border-radius:999px; display:grid; place-items:center; background:var(--accent); color:{readable_on(colors['accent'])}; font-weight:880; }}
  </style>
</head>
<body>
  <main class="slide variant-{html.escape(variant)} role-{html.escape(role)}" aria-label="{html.escape(anchor_name)} {html.escape(role)} starter">
    <div class="chrome"><span>{index:02d}/{total:02d} {html.escape(anchor_name)}</span><span>{html.escape(role.upper())} / {html.escape(archetype)}</span></div>
    <section class="claim">
      <p class="kicker">{html.escape(anchor.get("id", ""))}</p>
      <h1>{html.escape(headline)}</h1>
      <p class="support">{html.escape(support)}</p>
    </section>
    <section class="visual">{visual}</section>
    <section class="bottom">
      <div class="note"><b>Visual thesis</b>{html.escape(visual_thesis)}</div>
      <div class="note"><b>Typography / motion</b>{html.escape(typography)} · {html.escape(motion)}</div>
      <div class="note qa"><b>QA</b><div class="tag-row">{qa}</div></div>
    </section>
  </main>
</body>
</html>
"""


def index_html(title: str, manifest: list[tuple[str, str]], stage: dict[str, Any]) -> str:
    manifest_js = ",\n      ".join(
        f'{{ file: "slides/{html.escape(file)}", label: "{html.escape(label)}" }}'
        for file, label in manifest
    )
    cards = "".join(
        f'<article class="card"><iframe src="slides/{html.escape(file)}" title="{html.escape(label)}"></iframe><div>{html.escape(label)}</div></article>'
        for file, label in manifest
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    * {{ box-sizing: border-box; }}
    html, body {{ margin: 0; min-height: 100%; background: #05070d; color: #e5edf8; font-family: "PingFang SC", "Microsoft YaHei", Arial, sans-serif; }}
    .wrap {{ padding: 28px; }}
    h1 {{ margin: 0 0 8px; font-size: 28px; line-height: 1.1; }}
    p {{ margin: 0 0 24px; color: #94a3b8; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 20px; }}
    .card {{ overflow: hidden; border: 1px solid rgba(148,163,184,.28); border-radius: 10px; background: #0b1120; }}
    iframe {{ display: block; width: 100%; aspect-ratio: {stage['width']} / {stage['height']}; border: 0; background: #111827; }}
    .card div {{ padding: 10px 12px; color: #f2c96d; font-size: 13px; font-weight: 800; }}
  </style>
  <script>
    window.DECK_TITLE = {json.dumps(title, ensure_ascii=False)};
    window.DECK_MANIFEST = [
      {manifest_js}
    ];
  </script>
</head>
<body>
  <main class="wrap">
    <h1>{html.escape(title)}</h1>
    <p>Starter previews for cover, proof, system, and closing slides. These are design seeds, not final copy.</p>
    <section class="grid">{cards}</section>
  </main>
</body>
</html>
"""


def selected_anchor_ids(raw: str, anchors: dict[str, dict[str, Any]]) -> list[str]:
    if raw == "all":
        return list(anchors)
    wanted = [part.strip() for part in raw.split(",") if part.strip()]
    missing = [anchor_id for anchor_id in wanted if anchor_id not in anchors]
    if missing:
        raise SystemExit(f"unknown anchor id(s): {', '.join(missing)}")
    return wanted


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--anchor", default="all", help="Anchor id, comma-separated ids, or all")
    parser.add_argument("--out", type=Path, default=Path("style-anchor-starter-previews"))
    parser.add_argument("--anchors", type=Path, default=DEFAULT_ANCHORS)
    parser.add_argument("--starters", type=Path, default=DEFAULT_STARTERS)
    args = parser.parse_args()

    anchors, starters, stage = anchor_maps(args.anchors, args.starters)
    chosen = selected_anchor_ids(args.anchor, anchors)
    out_dir = args.out.resolve()
    if out_dir.exists():
        shutil.rmtree(out_dir)
    (out_dir / "slides").mkdir(parents=True, exist_ok=True)

    manifest: list[tuple[str, str]] = []
    total = sum(len(starters.get(anchor_id, [])) for anchor_id in chosen)
    index = 0
    used: list[dict[str, Any]] = []
    for anchor_id in chosen:
        anchor = anchors[anchor_id]
        starter_list = sorted(starters.get(anchor_id, []), key=lambda item: ROLE_ORDER.index(item.get("role")) if item.get("role") in ROLE_ORDER else 99)
        for starter in starter_list:
            index += 1
            role = str(starter.get("role") or "starter")
            file = f"{index:02d}-{slug(anchor_id)}-{slug(role)}.html"
            label = f"{anchor_id} / {role}"
            (out_dir / "slides" / file).write_text(bespoke_slide_html(anchor, starter, index, total, stage), encoding="utf-8")
            manifest.append((file, label))
            used.append({"anchor_id": anchor_id, "role": role, "file": f"slides/{file}", "archetype": starter.get("archetype")})

    title = "PPT Craft Style Anchor Starter Library" if args.anchor == "all" else f"PPT Craft Starter: {args.anchor}"
    (out_dir / "index.html").write_text(index_html(title, manifest, stage), encoding="utf-8")
    (out_dir / "style-anchor-starters-used.json").write_text(
        json.dumps({"anchor": args.anchor, "slide_count": len(manifest), "slides": used}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"style-anchor-starters-written {out_dir}")
    print(f"style-anchor-starter-slides {len(manifest)}")
    print(f"style-anchor-starter-anchors {len(chosen)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
